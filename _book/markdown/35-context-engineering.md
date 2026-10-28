# Context Engineering

Chapter 34 showed that the wall a loop runs into depends entirely on the tokens each step
adds: the same window stops a terse loop at step 638 and a fat-stepped one at step 13, and
which of those you have is a measurement rather than a guess. It left the question that
follows unasked — where those tokens come from. This chapter breaks one run's context down by
source, and then works through the four things you can do about the answer: load later,
summarise and prove what survived, write notes outside the window, and give a step a window of
its own.

*The problem.* My agent works for three steps and then starts forgetting, repeating itself and
going in circles.

*The question.* What is actually in the context by the time a run is twenty steps old, and
which of the things I could do about it is worth doing?

## Where the Context Actually Goes

**Context engineering** is deciding what occupies the context at each step of a run. It is a
different job from writing a prompt, which Chapter 18 owns, because a prompt is written once
and a run's context is rebuilt twenty times — and almost none of what is in it the twentieth
time was written by you.

Here is one run measured. A support agent works a single refund over twenty steps.

```python
"""Where a 20-step run's context actually came from.

Chapter 34 showed that what fills a loop's context is tokens per
step, and that the window wall moves from step 638 to step 13 when
that number moves. It did not ask where those tokens come from.
This is the same context, broken down by source.

The run is a support agent working one refund. The token counts are
plausible rather than measured; the per-tool definition cost is
chapter 23's figure, 200 characters a schema, which is about 50
tokens.
"""
INSTRUCTION = 1_200
PER_TOOL = 50

# step, tool, target, tokens the model spent deciding, tokens back
STEPS = [
    (1,  "search_orders",     "A-4471",                90,   420),
    (2,  "get_order",         "A-4471",                70, 1_150),
    (3,  "read_doc",          "refunds.pdf",           60, 8_400),
    (4,  "get_customer",      "c-3392",                80,   760),
    (5,  "search_kb",         "late delivery refund", 110, 2_300),
    (6,  "read_doc",          "shipping-sla.pdf",      60, 5_600),
    (7,  "get_tracking",      "A-4471",                70,   980),
    (8,  "get_carrier_events","A-4471",                90, 1_840),
    (9,  "search_orders",     "c-3392",                80, 1_260),
    (10, "get_order",         "A-4102",                70, 1_150),
    (11, "search_kb",         "repeat late delivery", 120, 2_050),
    (12, "read_doc",          "goodwill-credits.pdf",  60, 4_600),
    (13, "get_balance",       "c-3392",                70,   340),
    (14, "check_eligibility", "A-4471",               150,   520),
    (15, "search_kb",         "partial refund wording",110, 1_700),
    (16, "get_order_items",   "A-4471",                70,   890),
    (17, "read_doc",          "refunds.pdf",           60, 8_400),
    (18, "compute_refund",    "A-4471",               180,   260),
    (19, "draft_reply",       "c-3392",               420,    95),
    (20, "submit_refund",     "A-4471",               130,   140),
]

TOOLS = sorted({tool for _, tool, _, _, _ in STEPS})
TOOL_DEFS = PER_TOOL * len(TOOLS)
DECISIONS = sum(d for _, _, _, d, _ in STEPS)
RESULTS = sum(r for _, _, _, _, r in STEPS)
TOTAL = INSTRUCTION + TOOL_DEFS + DECISIONS + RESULTS


def table():
    rows = [("instruction", INSTRUCTION),
            (f"tool definitions ({len(TOOLS)})", TOOL_DEFS),
            ("the model's own decisions", DECISIONS),
            ("tool results", RESULTS)]
    print("  Where the context stood at the end of step 20.\n")
    print("  source                      tokens    share")
    for name, n in rows:
        print(f"  {name:<26}{n:>7,}{n / TOTAL * 100:>8.1f}%")
    print(f"  {'-' * 26}{'-' * 7}{'-' * 8}")
    print(f"  {'final context':<26}{TOTAL:>7,}{100.0:>8.1f}%")


def biggest(n=4):
    top = sorted(STEPS, key=lambda s: -s[4])[:n]
    print(f"\n  The {n} largest results, out of {len(STEPS)} steps.\n")
    print("   step  tool       target                tokens")
    for step, tool, target, _, r in top:
        print(f"   {step:>4}  {tool:<10} {target:<21}{r:>6,}")
    share = sum(s[4] for s in top)
    print(f"   {'':4}  {'':10} {'':21}{'-' * 6}")
    print(f"   {'':4}  {'':10} {'':21}{share:>6,}")
    rest = RESULTS - share
    print(f"\n  {share:,} of {RESULTS:,} result tokens — "
          f"{share / RESULTS * 100:.1f}% — from")
    print(f"  {n} of {len(STEPS)} steps. The other {len(STEPS) - n} "
          f"together are {rest:,}.")


def reread():
    seen = {}
    for step, tool, target, _, r in STEPS:
        if tool != "read_doc":
            continue
        if target in seen:
            first = seen[target]
            print(f"\n  {target} was read at step {first} and again at")
            print(f"  step {step}. The second read added {r:,} tokens, "
                  f"{r / TOTAL * 100:.1f}% of")
            print("  the final context, and the first copy was still")
            print("  there. Nothing in the loop noticed.")
        else:
            seen[target] = step


def menu():
    need = -(-RESULTS // PER_TOOL)
    print(f"\n  Tool definitions are {TOOL_DEFS:,} tokens for "
          f"{len(TOOLS)} tools.")
    print(f"  For them to reach the {RESULTS:,} the results take, the")
    print(f"  registry would need {need:,} tools. Trimming the menu is")
    print("  chapter 23's selection problem. It is not a context")
    print("  problem at any registry a person would write.")


if __name__ == "__main__":
    table()
    biggest()
    reread()
    menu()
```

```text
  Where the context stood at the end of step 20.

  source                      tokens    share
  instruction                 1,200     2.6%
  tool definitions (13)         650     1.4%
  the model's own decisions   2,150     4.6%
  tool results               42,855    91.5%
  -----------------------------------------
  final context              46,855   100.0%

  The 4 largest results, out of 20 steps.

   step  tool       target                tokens
      3  read_doc   refunds.pdf           8,400
     17  read_doc   refunds.pdf           8,400
      6  read_doc   shipping-sla.pdf      5,600
     12  read_doc   goodwill-credits.pdf  4,600
                                         ------
                                         27,000

  27,000 of 42,855 result tokens — 63.0% — from
  4 of 20 steps. The other 16 together are 15,855.

  refunds.pdf was read at step 3 and again at
  step 17. The second read added 8,400 tokens, 17.9% of
  the final context, and the first copy was still
  there. Nothing in the loop noticed.

  Tool definitions are 650 tokens for 13 tools.
  For them to reach the 42,855 the results take, the
  registry would need 858 tools. Trimming the menu is
  chapter 23's selection problem. It is not a context
  problem at any registry a person would write.
```

**Four numbers out of that, and the first one is the chapter.**

**Tool results are 91.5 per cent of the context.** The instruction is 2.6 and the tool
definitions are 1.4. Chapter 18's ordering already said that what reaches the model matters
more than how the instruction is worded; this is the same finding from the other side, and
sharper, because in a loop the material arriving is not something you wrote directly. It is
whatever the last nineteen steps happened to fetch, in whatever shape the tool returned it —
and Chapter 36 is where you get a say in that shape.

**The distribution is not flat.** Four of twenty steps carry 63 per cent of the result tokens,
two of them the same document.
So the lever is not "make every step terser" — it is three or four particular steps, and you
cannot know which without looking. Two of those four are the same document, so the first fix
below removes one of them, and what is left is three steps carrying 54 per cent of what
remains. The two findings are not independent: fixing either changes the other's figure.

**One document was read twice**, and the second read cost 8,400 tokens, 17.9 per cent of the
final context, while the first copy was still sitting there. Nothing in the loop noticed,
because nothing in a loop remembers what it has already opened unless your code does.

**And the tool menu is not where the problem is.** Thirteen tools are 650 tokens. For the
definitions to rival the results you would need 858 tools. Chapter 23 gave two reasons to keep
a registry small — the tokens on every call, and the harder choice the model makes from a
longer menu. This measurement says which of the two to argue from: the second one.

> **Note:** The token counts here are plausible and not measured, like every worked example in
> this book, and the per-tool figure is Chapter 23's. What is worth carrying is the *shape* —
> results dominating, a few steps dominating those — and the shape is not universal. A run that
> makes two calls and sends a long instruction has the opposite profile. Chapter 33's trace is
> where checking which one you have starts, because it records a request's tokens in and out
> and its tool calls. It does not hold this breakdown: getting that means recording the token
> count of each tool result as well, which is one field added to the list Chapter 33 settles.

## Instructions and the Tool Menu

Two of the levers people reach for first are now measured, so this section is short.

**On a run shaped like this one, the instruction's length is not a context problem.** At 2.6
per cent it cannot be. Write it for clarity and stop counting its words — and take the
measurement first, because the Note above says what the other shape looks like.

**What does matter about it is its level of detail**, and the detail that pays is not a
description of the task. Here is the same instruction at two levels.

```text
  an instruction that describes the task

    You are a support agent. Help the customer with their
    refund question. Be accurate and polite. Use the tools
    available to you.

  the same instruction at the level of detail that pays

    You are a support agent handling one refund question.
    If a tool returns no rows, say so in your answer and
    do not make the same call again. If a document does
    not answer the question, do not open a second one on
    the same point. Stop and hand over when a refund
    would exceed 250, or once you have proposed an amount.
```

The first is 22 words and the second 63, and the second says three things the first leaves to
the model's judgement at step 14: what a dead end looks like, what not to repeat, and when to
stop. Those are the decisions a step cannot work out for itself from the task description. The
third of them is Chapter 4's stopping condition, and Chapter 4 says a loop needs all three of
its stopping reasons: the model saying it is done, a step limit, and your code refusing. The
first of those is the one the instruction can speak to, and the other two are in your code —
so the instruction's job there is to *agree* with the code rather than to contradict it. A loop
whose instruction says "keep trying" and whose code stops at ten steps will spend its last step
arguing.

**And the cost of the longer one is not a context cost.** Nearly three times the words, on a
part of the context that was 2.6 per cent of it. That is the measurement above earning its keep: it
tells you which of your instincts about the instruction to ignore.

**The tool menu is a selection problem, not a context one.** Trim it because thirteen plausible
tools make a harder choice than five, which is Chapter 23's point and Chapter 36's subject. Do
not trim it to save context; the arithmetic above says there is no context there to save.

## Just in Time, Not Up Front

Chapter 28 asked how much relevant text a single request can afford, and answered it with a
budget. A loop raises a question a single request cannot: a document opened at step 3 is in the
context for every step after it, so *when* you load decides how long you carry it.

**Just-in-time retrieval** is opening a document at the step that needs it, rather than loading
the library before the run starts. The question this section settles is which of the two costs
less, and the answer is not the one usually given.

The library below is the twelve documents the refund task might have needed.

```python
"""Loading the library up front against opening a document when the
step needs it.

Chapter 28 asked how much relevant text one request can afford. This
is the other question, and it only exists in a loop: a document
opened at step 3 is in the context for every step after it, so WHEN
you load decides how long you carry it.

The library is the twelve documents the refund task in fill.py might
have needed. Three of them it actually opened.
"""
from fill import (INSTRUCTION, TOOL_DEFS, DECISIONS, STEPS)

LIBRARY = [
    ("refunds.pdf",             8_400),
    ("shipping-sla.pdf",        5_600),
    ("goodwill-credits.pdf",    4_600),
    ("returns-process.pdf",     6_200),
    ("warranty-terms.pdf",      7_100),
    ("fraud-rules.pdf",         5_900),
    ("chargeback-guide.pdf",    9_300),
    ("carrier-contracts.pdf",  11_500),
    ("tax-by-region.pdf",       4_800),
    ("gift-cards.pdf",          3_700),
    ("subscription-billing.pdf",8_900),
    ("escalation-matrix.pdf",   2_600),
]
CAT_PER_DOC = 20     # one line a document, so a step can choose
SEARCH_PER_OPEN = 300  # the candidate list that leads to one open

READS = [(t, r) for _, tool, t, _, r in STEPS if tool == "read_doc"]
OPENED = {t for t, _ in READS}
LIB_TOTAL = sum(n for _, n in LIBRARY)
CATALOGUE = CAT_PER_DOC * len(LIBRARY)
DOC_TOKENS_JIT = sum(r for _, r in READS)
OTHER_RESULTS = sum(r for _, tool, _, _, r in STEPS if tool != "read_doc")
FIXED = INSTRUCTION + TOOL_DEFS + DECISIONS + OTHER_RESULTS


def library():
    print(f"  {len(LIBRARY)} documents the task might need, "
          f"{len(OPENED)} it opened.\n")
    print("  document                  tokens  opened?")
    for name, n in LIBRARY:
        mark = "yes" if name in OPENED else "-"
        print(f"  {name:<24}{n:>8,}  {mark}")
    print(f"  {'-' * 24}{'-' * 8}")
    print(f"  {'the whole library':<24}{LIB_TOTAL:>8,}")
    never = LIB_TOTAL - sum(n for name, n in LIBRARY if name in OPENED)
    print(f"\n  Never opened: {never:,} tokens, "
          f"{never / LIB_TOTAL * 100:.1f}% of the library.")


def both():
    rows = [
        ("instruction",          INSTRUCTION,  INSTRUCTION),
        ("tool definitions",     TOOL_DEFS,    TOOL_DEFS),
        ("catalogue of the library", 0,       CATALOGUE),
        ("documents",            LIB_TOTAL,    DOC_TOKENS_JIT),
        ("searches that found them", 0, SEARCH_PER_OPEN * len(READS)),
        ("decisions",            DECISIONS,    DECISIONS),
        ("other tool results",   OTHER_RESULTS, OTHER_RESULTS),
    ]
    up = sum(a for _, a, _ in rows)
    jit = sum(b for _, _, b in rows)
    print("\n  What the context holds at step 20, both ways.\n")
    print("                            up front  just in time")
    for name, a, b in rows:
        fa = f"{a:,}" if a else "-"
        print(f"  {name:<24}{fa:>10}{b:>14,}")
    print(f"  {'-' * 24}{'-' * 10}{'-' * 14}")
    print(f"  {'':24}{up:>10,}{jit:>14,}")
    print(f"\n  {up / jit:.2f} times as much, and the difference is")
    print("  documents no step asked for.")
    return up, jit


def reread(jit):
    first, extra = {}, 0
    for t, r in READS:
        if t in first:
            extra += r
        else:
            first[t] = r
    print(f"\n  One thing up front buys: it cannot re-read. "
          f"refunds.pdf")
    print(f"  was opened twice, so just-in-time paid {extra:,} tokens")
    print(f"  for it a second time. Without that it would be "
          f"{jit - extra:,},")
    print("  and up front still costs more than twice as much.")


def crossover(up):
    print("\n  How much of the library a task would have to touch")
    print("  before loading it up front is the cheaper arrangement,")
    print("  taking the documents in the order listed and opening")
    print("  each one ONCE - the favourable case for just in time,")
    print("  which is why the row for 3 documents is lower than the")
    print("  48,295 above:\n")
    print("   docs   just in time   up front")
    running = 0
    answer = None
    for k, (_, n) in enumerate(LIBRARY, 1):
        running += n
        jit = FIXED + CATALOGUE + SEARCH_PER_OPEN * k + running
        if k in (1, 3, 6, 9, 11, 12):
            print(f"   {k:>4}   {jit:>12,}   {up:>8,}")
        if answer is None and jit >= up:
            answer = k
    print(f"\n  Up front wins at {answer} of {len(LIBRARY)} documents and")
    print("  not before. That is the finding: just in time is not a")
    print("  tuning choice, it is the arrangement unless a task")
    print("  genuinely reads nearly everything.")


if __name__ == "__main__":
    library()
    up, jit = both()
    reread(jit)
    crossover(up)
```

```text
  12 documents the task might need, 3 it opened.

  document                  tokens  opened?
  refunds.pdf                8,400  yes
  shipping-sla.pdf           5,600  yes
  goodwill-credits.pdf       4,600  yes
  returns-process.pdf        6,200  -
  warranty-terms.pdf         7,100  -
  fraud-rules.pdf            5,900  -
  chargeback-guide.pdf       9,300  -
  carrier-contracts.pdf     11,500  -
  tax-by-region.pdf          4,800  -
  gift-cards.pdf             3,700  -
  subscription-billing.pdf   8,900  -
  escalation-matrix.pdf      2,600  -
  --------------------------------
  the whole library         78,600

  Never opened: 60,000 tokens, 76.3% of the library.

  What the context holds at step 20, both ways.

                            up front  just in time
  instruction                  1,200         1,200
  tool definitions               650           650
  catalogue of the library         -           240
  documents                   78,600        27,000
  searches that found them         -         1,200
  decisions                    2,150         2,150
  other tool results          15,855        15,855
  ------------------------------------------------
                              98,455        48,295

  2.04 times as much, and the difference is
  documents no step asked for.

  One thing up front buys: it cannot re-read. refunds.pdf
  was opened twice, so just-in-time paid 8,400 tokens
  for it a second time. Without that it would be 39,895,
  and up front still costs more than twice as much.

  How much of the library a task would have to touch
  before loading it up front is the cheaper arrangement,
  taking the documents in the order listed and opening
  each one ONCE - the favourable case for just in time,
  which is why the row for 3 documents is lower than the
  48,295 above:

   docs   just in time   up front
      1         28,795     98,455
      3         39,595     98,455
      6         59,695     98,455
      9         86,195     98,455
     11         99,395     98,455
     12        102,295     98,455

  Up front wins at 11 of 12 documents and
  not before. That is the finding: just in time is not a
  tuning choice, it is the arrangement unless a task
  genuinely reads nearly everything.
```

**Three quarters of the library was never opened.** 60,000 tokens of it, which under the
up-front arrangement are carried from step 1 to step 20 and read by nobody.

**And the crossover is not where people put it.** Loading up front only becomes the cheaper
arrangement when a task reads eleven of the twelve documents. That is worth saying plainly,
because "it depends on your workload" is the usual answer and it is too weak: on these numbers
just in time wins at every workload except reading nearly the whole library, so it is the
arrangement rather than the tuning choice.

**The one thing up front buys is that it cannot re-read.** The document already in the context
is free to consult again, so the 8,400-token second read of `refunds.pdf` does not happen.
Just in time pays for that mistake and up front cannot make it — and it still costs more than
twice as much here, so the fix is not to load everything. The fix is to keep a record of the
documents [**already in the context**]{.noindex} — not of everything ever opened, because compaction takes
the copy away and a stale memo would then suppress a re-read the run needs. Four lines of code,
and the largest single saving on the table.

> **Tip:** The part people leave out is the catalogue. Just in time needs each step to know
> what exists without opening it, which means one line a document — a name and a sentence —
> carried for the whole run. Here that is 240 tokens for twelve documents, and without it a
> step cannot choose and will either guess or open everything. The catalogue is the price of
> the arrangement, and it is small. It is not one of Chapter 29's indexes: nothing is searched
> and nothing is approximated, it is a list of names.

## Compaction, and How to Prove What Survived

Chapter 18 gave four things to do when a history will not fit, said that summarising loses
things silently, and sent one thing here: if you summarise, you need a way to find out what was
lost. This is that mechanism.

**Compaction** is replacing the record of a run with a shorter one that keeps the facts later
steps need. It is the summarise strategy from Chapter 18 applied to a loop rather than to a
conversation, and the difference matters: a conversation's turns were written by a person who
can notice that something has gone missing, and a loop's record is read, while the run is still
going, only by a model that cannot. Somebody reads it afterwards, from Chapter 33's trace,
which is too late to stop the run going round in circles.

So the mechanism is a list. Before the summary is written, you name the facts the rest of the
task depends on — a **must-keep list** — and afterwards you check the summary against it.

```python
"""Compacting the record of the run in fill.py, and proving what
survived.

Chapter 18 said a summary is lossy and the loss is silent, and sent
the mechanism that proves what survived here. This is that
mechanism: name the facts the rest of the task depends on BEFORE
summarising, then check the summary against the list.
"""
from fill import STEPS, TOTAL

RECORD = [
    "order A-4471 found, placed 2026-09-14",
    "A-4471: 3 items, 128.40, promised 2026-09-17,"
    " delivered 2026-09-23",
    "refunds: full refund if late by more than 3 days;"
    " manager approval above 250",
    "c-3392, Pro plan since 2026-03-02",
    "late delivery is a service failure, not a product fault",
    "SLA: late counts from the promised date, not dispatch",
    "tracking: delivered 2026-09-23 09:12",
    "carrier held the parcel 09-18 to 09-22, address check",
    "c-3392 has 4 previous orders",
    "A-4102 was also late, by 2 days, no refund claimed",
    "a second late delivery within 90 days allows a"
    " goodwill credit",
    "goodwill credit: up to 20, one per 90 days, NOT"
    " stackable with a refund",
    "account balance: no credit on the account",
    "eligible: late by 6 days",
    "partial refund wording template found",
    "shipping was 8.40 of the 128.40",
    "refunds: full refund if late by more than 3 days;"
    " manager approval above 250",
    "refund 128.40, within the 250 limit, no manager needed",
    "reply drafted",
    "submitted, ref R-9981",
]

# Written down BEFORE the summary. Each is a fact a later step would
# get wrong without it, and the probe is the string that has to
# survive. Two of the eight are things that are NOT so.
MUST_KEEP = [
    ("late by 6 days",                      "6 days"),
    ("late counts from the promised date",  "promised"),
    ("manager approval only above 250",     "250"),
    ("goodwill credit not stackable",       "stackable"),
    ("no credit on the account",            "no credit"),
    ("A-4102 was late and unclaimed",       "A-4102"),
    ("the carrier held it for an address check", "address check"),
    ("the amount is 128.40",                "128.40"),
]

# Declared here, not derived: which of the eight are about
# something that is NOT so. The split below is then a count.
NEGATIVE = {"goodwill credit not stackable",
            "no credit on the account"}

NAIVE = (
    "Order A-4471 for 128.40 was promised 2026-09-17 and delivered"
    " 2026-09-23, so it is late by 6 days measured from the promised"
    " date. The refund policy allows a full refund and needs manager"
    " approval only above 250. Order A-4102 was also late. The"
    " carrier held the parcel for an address check. Refund submitted"
    " as R-9981."
)

CAREFUL = NAIVE[:-1] + (
    " A goodwill credit is not stackable with a refund, and the"
    " account carries no credit, so neither was offered."
)


def survives(summary):
    return [(fact, probe, probe.lower() in summary.lower())
            for fact, probe in MUST_KEEP]


def report(name, summary):
    rows = survives(summary)
    kept = sum(1 for _, _, ok in rows if ok)
    print(f"\n  {name}: {len(summary.split())} words, "
          f"{kept} of {len(rows)} facts kept")
    for fact, _, ok in rows:
        if not ok:
            print(f"    MISSING  {fact}")
    return kept


def split(summary):
    """Cross-tabulate what was lost against what is a negative."""
    tab = {(n, k): 0 for n in (True, False) for k in (True, False)}
    for fact, _, ok in survives(summary):
        tab[(fact in NEGATIVE, ok)] += 1
    print("\n  The naive summary's losses, against whether the fact")
    print("  is about something that is NOT so.\n")
    print("                      kept   dropped")
    for neg, label in ((True, "about a negative"),
                       (False, "about a positive")):
        print(f"    {label:<18}{tab[(neg, True)]:>6}"
              f"{tab[(neg, False)]:>10}")
    print(f"\n  A clean split, on {len(NEGATIVE)} cases out of "
          f"{len(MUST_KEEP)}. That is a")
    print("  demonstration and not a measurement: both summaries")
    print("  were written by hand, and two is the whole sample.")


def trigger(window=128_000):
    largest = max(r for _, _, _, _, r in STEPS)
    print(f"\n  When to compact. The window is {window:,} tokens and")
    print(f"  the largest single result in this run was "
          f"{largest:,}, so")
    print("  compaction has to leave at least that much room.\n")
    print("  trigger at   room left   fits it?")
    for pct in (80, 90, 95, 98):
        room = window - int(window * pct / 100)
        print(f"  {pct:>9}%   {room:>9,}   "
              f"{'yes' if room >= largest else 'NO'}")
    last = max(p for p in range(1, 100)
               if window - int(window * p / 100) >= largest)
    print(f"\n  So 95% is not a cautious setting, it is a broken one")
    print(f"  on this run. The highest whole per cent that works is")
    print(f"  {last}%, and it is set by the largest result you might")
    print("  still take, not by a round number.")


if __name__ == "__main__":
    print(f"  The context to be compacted is {TOTAL:,} tokens.")
    print(f"  The {len(RECORD)}-line record below is already one line a")
    print("  step, so that it fits on a page; the summary is what")
    print("  replaces the whole context, not what replaces the")
    print("  record.\n")
    print(f"  {len(MUST_KEEP)} facts were named before summarising.")
    a = report("naive summary", NAIVE)
    b = report("careful summary", CAREFUL)
    print(f"\n  {b - a} more facts kept, for "
          f"{len(CAREFUL.split()) - len(NAIVE.split())} more words.")
    chars = len(CAREFUL)
    print(f"  The careful summary is {chars} characters, about "
          f"{chars // 4} tokens")
    print(f"  by chapter 10's rule, against {TOTAL:,}: a factor of "
          f"{TOTAL / (chars // 4):.0f}.")
    print("\n  Both missing facts are things that are NOT so, and a")
    print("  kept one is what stops a later step trying the same")
    print("  thing again.")
    print("\n  The check is a probe for a string, not a reader. It")
    print("  cannot tell whether the summary says the fact")
    print("  CORRECTLY - the same limit chapter 28 found in a")
    print("  mechanical citation check. It is necessary, not")
    print("  sufficient.")
    split(NAIVE)
    trigger()
```

```text
  The context to be compacted is 46,855 tokens.
  The 20-line record below is already one line a
  step, so that it fits on a page; the summary is what
  replaces the whole context, not what replaces the
  record.

  8 facts were named before summarising.

  naive summary: 54 words, 6 of 8 facts kept
    MISSING  goodwill credit not stackable
    MISSING  no credit on the account

  careful summary: 73 words, 8 of 8 facts kept

  2 more facts kept, for 19 more words.
  The careful summary is 426 characters, about 106 tokens
  by chapter 10's rule, against 46,855: a factor of 442.

  Both missing facts are things that are NOT so, and a
  kept one is what stops a later step trying the same
  thing again.

  The check is a probe for a string, not a reader. It
  cannot tell whether the summary says the fact
  CORRECTLY - the same limit chapter 28 found in a
  mechanical citation check. It is necessary, not
  sufficient.

  The naive summary's losses, against whether the fact
  is about something that is NOT so.

                      kept   dropped
    about a negative       0         2
    about a positive       6         0

  A clean split, on 2 cases out of 8. That is a
  demonstration and not a measurement: both summaries
  were written by hand, and two is the whole sample.

  When to compact. The window is 128,000 tokens and
  the largest single result in this run was 8,400, so
  compaction has to leave at least that much room.

  trigger at   room left   fits it?
         80%      25,600   yes
         90%      12,800   yes
         95%       6,400   NO
         98%       2,560   NO

  So 95% is not a cautious setting, it is a broken one
  on this run. The highest whole per cent that works is
  93%, and it is set by the largest result you might
  still take, not by a round number.
```

**The careful summary keeps eight facts of eight for nineteen more words.** That is the whole
trade, and it is a cheap one. The naive summary is not shorter in any way that matters; it is
simply missing two things.

**Both missing facts are things that are not so**, and there is an argument for expecting that
rather than reading it as an accident: a summary records what was established, and "no credit
on the account" establishes nothing to record.

**But the argument is weaker than it looks, and the list above is where that shows.** Three of
the facts that survived are not events either — a policy threshold, an amount, and a rule about
which date counts. If non-events live at three for three and negatives die at two for two, then
having no event to narrate is not what separated them; something nearer to *being about a path
not taken* is doing the work. On Chapter 6's ladder this sits at [**demonstration**]{.noindex} — it worked,
on an example chosen by the person showing you — and no higher: one pair of summaries, two
dropped facts, both written by hand. It is not a derivation either, which is the one kind of
evidence Chapter 6 puts above the ladder, because no arithmetic settles what a summariser keeps.

**It is still worth acting on, because of the price.** Putting the negative results in the
must-keep list first costs one line. And a negative result that is *kept* is what stops a later
step trying the same thing again, so losing one is how a run starts going in circles —
which is this chapter's opening problem arriving on schedule.

**The check is a probe for a string, not a reader.** It cannot tell you whether the summary
states the fact correctly, only that the words are there — the same limit Chapter 28 found in a
mechanical citation check, and the same verdict: necessary, not sufficient. What it does
reliably is catch an omission, and omission is the failure that is otherwise silent.

**And what to summarise is already on the first table.** Tool results are 91.5 per cent of this
context and a few steps carry most of those, so most of compaction's work is in the
document reads. The decisions are 2,150 tokens across twenty steps, and the last few steps are
what the next step is about — both cheap enough to keep word for word. So compaction replaces
the big reads with the facts they yielded and leaves the decisions and the recent steps alone.
That is a smaller cut than the factor above and a safer one, because nothing that was never
bulky gets rewritten by a model.

> **Warning:** The must-keep list has to be written before the summary, and the reason is not
> process hygiene. A list written afterwards is written *from* the summary, so what it holds is
> what the summary kept — and the check then passes on a summary that dropped something. That is
> not a weak test, it is a test of the wrong thing, and it will look like a passing gate.

**When to compact is arithmetic, and 95 per cent is the wrong answer.** Compaction has to
leave room for whatever the next step brings back. On a 128,000-token window a trigger at 95
per cent leaves 6,400 tokens, and the largest single result in this run was 8,400 — so the step
after the trigger overflows anyway. The order is what makes that bite: the result arrives before
you can compact it away, so the room the trigger leaves has to be able to hold it. The highest whole per cent that works here is 93, and the
number that sets it is the largest result you might still take, not a round figure that sounds
cautious.

> **Note:** Two things set that figure and you choose only one of them. The window is a
> model's property, from Chapter 16, so the same registry on a larger window gets a higher
> trigger. On a fixed window it is your registry that decides: add one tool that can return a
> 30,000-token document and the trigger drops to 76 per cent. That makes it the kind of number
> to compute in code from the largest result your tools can return, rather than to write down
> once in a configuration file.

## Structured Notes, and Memory That Outlives the Window

Compaction keeps a run's record inside one window. The other arrangement is to put facts
*outside* the window: the agent writes a **structured note** — a key and a value in a file or a
table — and reads it back on a later step or a later run.

This is the one piece of context engineering that is not about tokens, and it has a failure the
others do not. A note is model output. It has every property Chapter 16 gave model output, and
reading it back puts it in the context as a tool result in Chapter 18's message list — Chapter
23 is exact about this, and a result is a `tool` message written by your code. Which is to say
it arrives looking like something your code vouched for, and a model wrote it.

So a note carries two more fields: where it came from and when it was written. Together those
are its **provenance**.

```python
"""Notes an agent wrote and reads back on a later run.

A note is model output. It has every property chapter 16 gave model
output, and reading it back puts it in the context as something the
agent has no way to doubt. So a note carries where it came from and
when it was written, and this is what those two fields buy.

Six notes about one customer. Two are wrong.
"""
from datetime import date

TODAY = date(2026, 10, 29)

# key, what the note asserts, when it was written, where it came from
NOTES = [
    ("plan",              "Pro",   date(2026, 3, 2),  "read"),
    ("manager_threshold", "250",   date(2026, 1, 15), "read"),
    ("late_deliveries",   "0",     date(2026, 9, 23), "inferred"),
    ("channel",           "email", date(2026, 5, 11), "told"),
    ("goodwill_cap",      "20",    date(2026, 2, 20), "read"),
    ("carrier",           "Hallmark",
                                   date(2026, 4, 8),  "read"),
]

# what is so now, and the date it became so
TRUTH = {
    "plan":              ("Basic",    date(2026, 6, 1)),
    "manager_threshold": ("250",      date(2026, 1, 10)),
    "late_deliveries":   ("2",        date(2026, 9, 14)),
    "channel":           ("email",    date(2026, 5, 11)),
    "goodwill_cap":      ("20",       date(2026, 2, 20)),
    "carrier":           ("Hallmark", date(2026, 4, 8)),
}

# what the source field tells you WITHOUT the truth column
MEANS = {
    "read":     ("was true of a document on that date",
                 "re-read the document"),
    "inferred": ("was never checked against anything",
                 "verify it before acting"),
    "told":     ("is as good as whoever said it",
                 "confirm it with them"),
}


def verdict(key, asserts, written):
    truth, since = TRUTH[key]
    if asserts == truth:
        return "correct"
    return "stale" if since > written else "wrong"


def notes_as_written():
    print("  The six notes as the agent reads them back.\n")
    for key, asserts, _, _ in NOTES:
        print(f"    {key} = {asserts}")
    print("\n  Nothing there distinguishes the two wrong notes from")
    print("  the four right ones, and the agent will act on all six.")


def with_provenance():
    print("\n  The same notes with the two fields, checked against")
    print("  what is so now.\n")
    print("  note                 says      source    age  verdict")
    for key, asserts, written, source in NOTES:
        age = (TODAY - written).days
        v = verdict(key, asserts, written)
        print(f"  {key:<20} {asserts:<9} {source:<8} {age:>4}  {v}")
    bad = [k for k, a, w, _ in NOTES if verdict(k, a, w) != "correct"]
    print(f"\n  {len(bad)} of {len(NOTES)} are not correct: ", end="")
    print(", ".join(f"{k} ({verdict(k, a, w)})"
                    for k, a, w, _ in NOTES if k in bad))


def what_source_buys():
    print("\n  What the source field says on its own, before anyone")
    print("  checks anything.\n")
    for source in ("read", "inferred", "told"):
        mine = [k for k, _, _, s in NOTES if s == source]
        says, do = MEANS[source]
        print(f"  {source} ({len(mine)}): it {says}")
        print(f"      so: {do}")
    print("\n  It does not say which note is wrong. The stale one is")
    print("  caught by a date - the plan note was written before the")
    print("  plan changed. The wrong one is not: late_deliveries was")
    print("  INFERRED from one order and was false the day it was")
    print("  written, so only going back to the source catches it.")
    print("  That is what the field is for: it gives you an order to")
    print("  check in, and a way to check each kind.")


if __name__ == "__main__":
    notes_as_written()
    with_provenance()
    what_source_buys()
```

```text
  The six notes as the agent reads them back.

    plan = Pro
    manager_threshold = 250
    late_deliveries = 0
    channel = email
    goodwill_cap = 20
    carrier = Hallmark

  Nothing there distinguishes the two wrong notes from
  the four right ones, and the agent will act on all six.

  The same notes with the two fields, checked against
  what is so now.

  note                 says      source    age  verdict
  plan                 Pro       read      241  stale
  manager_threshold    250       read      287  correct
  late_deliveries      0         inferred   36  wrong
  channel              email     told      171  correct
  goodwill_cap         20        read      251  correct
  carrier              Hallmark  read      204  correct

  2 of 6 are not correct: plan (stale), late_deliveries (wrong)

  What the source field says on its own, before anyone
  checks anything.

  read (4): it was true of a document on that date
      so: re-read the document
  inferred (1): it was never checked against anything
      so: verify it before acting
  told (1): it is as good as whoever said it
      so: confirm it with them

  It does not say which note is wrong. The stale one is
  caught by a date - the plan note was written before the
  plan changed. The wrong one is not: late_deliveries was
  INFERRED from one order and was false the day it was
  written, so only going back to the source catches it.
  That is what the field is for: it gives you an order to
  check in, and a way to check each kind.
```

**Two of the six notes are wrong, and they fail in different ways.** The plan note was true
when it was written and the plan changed afterwards — it is *stale*, and a date catches it. The
late-delivery note was false the day it was written, because it was inferred from a single
order — it is simply *wrong*, and no date will ever catch it. Only going back to the source
will.

**That is the answer to why an agent's own memory is untrusted input.** Not because a model is
unreliable in some general way, but because a note is a claim with no evidence attached, written
by the same process that produced everything else in the context, and read back as though
somebody had checked it. The two fields do not make it true. They tell you which notes can
expire and which were never verified, which is an order to check in and a method for each kind.
Chapter 36 generalises this to anything a tool hands back, and Chapter 51 to the rule underneath
it — that a model cannot reliably tell an instruction from data.

> **Warning:** An inferred note is the dangerous one, and it is the one that is cheapest to
> write. "The customer has never had a late delivery" is one line; it is a generalisation from
> whatever happened to be in the context at the time; and a later run reads it as a fact about
> the customer. If you keep notes at all, keep the source field, and treat `inferred` as a
> question rather than an answer.

## A Sub-Agent Is a Second Window

The last arrangement gives a step a window of its own. A **sub-agent** is a nested run with its
own context and its own stopping condition, which returns only its answer to the run that
started it.

What that buys is visible in the numbers above. The three documents the refund task opened were
18,600 tokens, and what the parent run actually needed from them was three facts: that lateness
counts from the promised date, that the manager threshold is 250, and that a goodwill credit
caps at 20 and is not stackable with a refund. All three are facts from the must-keep list
above, and written as that list writes them — *late counts from the promised date*, *manager approval only
above 250*, *goodwill credit not stackable* — they are 96 characters, so about twenty-four
tokens by Chapter 10's rule. A sub-agent that opens the documents and returns those three facts
keeps 18,600 tokens in its own context and puts two dozen in the parent's.

What it costs is three things, and the third is the one that is easy to miss.

It pays for its own instruction and tool definitions, which the parent already paid for once.
It cannot be consulted afterwards, because its context is gone when it returns — so a question
the parent thinks of at step 18 means opening the documents again. And the parent cannot see
what the sub-agent saw, so a wrong summary from it is a wrong fact in the parent with nothing
left to check it against. That is Chapter 4's compounding error at the hand-off, and it is
worse here than inside a loop, because inside a loop the earlier result is still in the context
and a later step can contradict it.

> **Note:** A sub-agent is a context decision and not an organisational one. It is worth it when
> a sub-task reads a great deal and returns a little, which is the shape of searching,
> summarising a long document, or checking a list. It is not worth it when the parent will need
> the detail later, and it is not a way to divide a problem among specialists — that is Chapter
> 37, which is also where the arithmetic on running several of them lives.

## What To Actually Do

1. **Measure before you tune.** Break one real run's context down by source. Chapter 33's trace
   is where the numbers start, and it takes one more field — the token count of each tool
   result — before it can give you the breakdown.
2. **Remember what you have opened.** A record of the documents [**already in the context**]{.noindex} —
   not of everything ever opened, because compaction removes the copy and a stale memo would
   then suppress a re-read the run needs. The cheapest saving available.
3. **Retrieve just in time, and carry a catalogue.** Up front only pays when a task reads
   nearly everything, and the catalogue is what makes choosing possible.
4. **Write the must-keep list before you compact**, and put the negative results in it first,
   because that is where a summary is most likely to be thin and one line is what it costs.
5. [**Compute the compaction trigger**]{.noindex} from the largest result your tools can
   return, and
   recompute it when you add a tool.
6. **Give every note a source and a date**, and treat `inferred` as something to verify rather
   than something to use.
7. **Use a sub-agent where a sub-task reads a lot and returns a little**, and not where the
   parent will want the detail back.

> **Warning:** None of this reaches Chapter 4's compounding error. Every item above changes
> what the context holds, and a twenty-step run whose context is half the size is still a
> twenty-step run with twenty chances to be wrong. Two items do touch correctness, and it is
> worth being exact about which: a verified note is a false fact not acted on, and a kept negative result stops a later step taking an action
> that cannot work, which is not only a saving. What none of it does is improve the model's
> judgement on a step it was always going to take.

## Lab: Measure a Context and Set a Trigger

Pen, paper and a calculator, then the four programs. Thirty minutes, and there is a key for
every step.

**Step 1.** From the first table, you are allowed one change to this run. Which do you make?

*Expected result:* keep a record of the documents already in the context. Step 17 re-reads
`refunds.pdf` for
8,400 tokens, 17.9 per cent of the final context, and the copy from step 3 is still there. No
other single change on the table is worth as much, and this one loses nothing.

**Step 2.** Compute what the run would hold with that fix.

*Expected result:* `\(46{,}855 - 8{,}400 = 38{,}455\)`{=latex}, a cut of 17.9 per cent. Note
which column it comes out of: the tool results, which is the only column big enough for a
change to show up in.

**Step 3.** A different system's largest single tool result is 20,000 tokens, on the same
128,000-token window. Where do you set the compaction trigger?

*Expected result:* the room left at `\(p\)`{=latex} per cent is
`\(128{,}000 - 1{,}280p\)`{=latex}, and that has to be at least 20,000, so
`\(p \le 84.375\)`{=latex} — [**84 per cent**]{.noindex}. Not 90, and not 95. The tool
decides the
trigger.

**Step 4.** Your task is to book travel, and the record so far holds: the dates are flexible by
one day, the traveller has no visa for one of the destinations, the cheapest flight found so far
is 410, the preferred airline has no seats, and the budget is 600. Write the must-keep list.

*Expected result:* all five, and the two to be sure of are the negatives — *no visa* and *no
seats on the preferred airline*. Those are what stop a later step proposing a route the traveller
cannot fly and an airline that cannot carry them. A summary of "what has been found" will keep
the 410 and the 600 and drop both.

**Step 5.** A note reads `open_tickets = 0`, written 40 days ago, source `inferred`. What do you
do with it, and what is the worse problem?

*Expected result:* verify it, because `inferred` means it was never checked against anything —
the age is beside the point, since a note that was false when written does not become true or
false with time. The worse problem is that it is a negative: a later step that reads it has no
reason to look for tickets, so the note suppresses the check that would have corrected
it.

**Step 6.** A task reads ten of the twelve documents. Up front or just in time?

*Expected result:* still just in time. Ten documents are 67,100 tokens, so the just-in-time
total is `\(19{,}855 + 240 + 3{,}000 + 67{,}100 = 90{,}195\)`{=latex} against 98,455 up front —
cheaper by 8,260. The crossover is at eleven. This is the step that shows "it depends on your
workload" to be the wrong answer.

**Step 7.** Someone proposes a sub-agent for each of the twelve documents, to cut the parent's
context. What do you say?

*Expected result:* it does not cut the total, it moves it — and twelve sub-agents pay twelve
instructions and twelve sets of tool definitions, so the total goes up. A sub-agent earns its
place when a sub-task reads a great deal and returns a little; one document and one fact is a
tool call, not a sub-agent. Chapter 37 is where running several of them is costed.

## Summary, Key Terms, and Review Questions

### Summary

**Context engineering** is deciding what occupies the context at each step of a run, and the
first thing to do is measure. On the twenty-step run worked here, tool results are 91.5 per cent
of the final context, the instruction is 2.6 and the tool definitions 1.4 — so the instruction's
length is not a context problem and the tool menu is a selection problem rather than a context
one. Four of twenty steps carry 63 per cent of the result tokens — two of them the same
document — and one document read twice
cost 17.9 per cent of the whole context while the first copy was still there, which makes
remembering what you have opened the cheapest saving available. **Just-in-time retrieval** beats
loading the library up front until a task reads eleven of twelve documents, and it needs a
catalogue — one line a document — to make choosing possible. **Compaction** replaces a run's record
with a shorter one, and the way to prove nothing important was dropped is a **must-keep list**
written *before* the summary and checked against it afterwards; a list written after is written
from the summary and tests nothing. The facts to put in that list first are the negative
results — and that claim is a demonstration on Chapter 6's ladder and no higher, because both
summaries were written by hand and two dropped facts are the whole sample. What is not in doubt
is why it matters: a kept negative result is what stops a step repeating itself, and putting
them first costs one line. The
compaction trigger is set by the largest single result your tools can return — 93 per cent, not
95, on a 128,000-token window with an 8,400-token result. A **structured note** puts a fact
outside the window and is untrusted input because it is model output read back as established;
its **provenance** — where it came from and when it was written — separates a note that went
stale from one that was never true, and only the first is caught by a date. A **sub-agent** gives
a sub-task its own window, which is worth it when it reads a great deal and returns a little, and
costs a repeated instruction, a context you cannot consult again, and a hand-off nothing checks.

### Key Terms

| Term | Meaning |
|---|---|
| **Context engineering** | Deciding what occupies the context at each step of a run. Distinct from writing a prompt (Chapter 18), because a prompt is written once and a run's context is rebuilt every step, mostly out of material you did not write |
| **Just-in-time retrieval** | Opening a document when a step needs it rather than loading the library before the run starts. Needs a catalogue of what exists — one line a document, not one of Chapter 29's indexes; beats loading up front unless a task reads nearly all of it |
| **Compaction** | Replacing the record of a run with a shorter one that keeps the facts later steps need. Chapter 18's summarise strategy applied to a loop, where nothing reading the record *while the run is still going* can notice an omission |
| **Must-keep list** | The facts the rest of the task depends on, named before the summary is written and checked against it after. Written afterwards it is written from the summary and tests nothing |
| **Structured note** | A fact the agent writes outside the context window as a key and a value, and reads back later. Model output, so it is untrusted input however plainly it is phrased |
| **Provenance** | A note's two extra fields: where it came from — read, inferred or told — and when it was written. They do not make a note true; they say which notes expire and which were never checked |
| **Sub-agent** | A nested run with its own context and stopping condition, returning only its answer. Keeps what it read out of the parent's context, and cannot be consulted once it has returned |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Where a loop's context goes | Tool results — 91.5% of the worked run, against 2.6% instruction and 1.4% tool definitions |
| The compaction trigger | Room left must be at least the largest single result: `\(\text{window} - p \times \text{window}/100 \ge \text{largest}\)`{=latex} |
| Worked: trigger | 128,000-token window, 8,400-token largest result, so 93% — not 95% |
| Up front against just in time | Up front only wins at 11 of 12 documents |
| First into the must-keep list | The negative results — the cheapest line in it |
| A note's two fields | Where it came from, and when it was written |

### Review Questions

1. You are told an agent's context is full and the instruction should be shortened. What do you measure, and what do you expect to find?
2. What is the one change to a loop that saves the most context for the least work, and why does nothing else substitute for it?
3. When does loading documents up front beat opening them on demand?
4. What is compaction, and how do you prove nothing important was dropped?
5. Why treat an agent's own memory as untrusted input, and what do the two extra fields on a note actually buy?
6. When is a sub-agent worth it, and what does it cost?

### Review Answers

1. Break one real run's context down by source — instruction, tool definitions, the model's own
decisions, tool results. Chapter 33's trace gives you a request's tokens in and out and its
tool calls, and one more field — the token count of each tool result — turns that into this
breakdown. On a loop,
expect the tool results to dominate: 91.5 per cent on the run worked here, against 2.6 for the
instruction. So shortening the instruction cannot help, and the places to look are the few steps
that fetched the most. Four of twenty steps carried 63 per cent of the result tokens, and two
of those four are the same document, so the first fix leaves three steps at 54 per cent of what
is left. The
exception to expect is a run that makes very few calls and sends a long instruction, which has
the opposite profile — which is why the answer is to measure rather than to assume either shape.
2. Keep a record of the documents already in the context. In the worked run `refunds.pdf` was read at step 3 and
again at step 17, and the second read cost 8,400 tokens — 17.9 per cent of the final context —
while the first copy was still in it. Nothing in a loop notices this, because nothing in a loop
remembers what it has opened unless your code does. It substitutes for nothing else because it
trades nothing away while the copy is still there, and every other lever in this chapter does
trade something — a catalogue to carry, a fact a summary dropped, a note nobody verified, a
context that cannot be consulted again. The record has to be of what is *in the context*, not
of everything ever opened, because compaction removes the copy.
3. When the task reads nearly the whole library. On the twelve documents worked here, up front
only becomes cheaper at eleven of them, so just in time is the arrangement rather than a tuning
choice. The one thing up front buys is that it cannot re-read, since a document already in the
context is free to consult again — but that is an argument for remembering what you have opened,
not for loading everything, because up front still cost more than twice as much here.
4. Compaction is replacing the record of a run with a shorter one that keeps the facts later
steps need. You prove nothing important was dropped with a must-keep list: name the facts the
rest of the task depends on *before* the summary is written, then check the summary against each
one. Written afterwards the list comes out of the summary and the check passes vacuously. The
check is a string probe, so it catches omission and cannot tell you the summary states a fact
correctly — necessary, not sufficient, the same verdict Chapter 28 reached about mechanical
citation checks. And trigger it from the largest single result your tools can return: on a
128,000-token window with an 8,400-token result, 93 per cent and not 95, because 95 leaves 6,400
and the next step overflows.
5. Because a note is model output, with every property Chapter 16 gave it, and reading it back
puts it in the context as a tool result, which Chapter 23 is exact about — something your code
appears to have vouched for and will now be treated
as established, with no evidence attached. The two fields do not make it true. They tell you
which notes can expire and which were never checked: a note read from a document on a date can
go stale, and a date catches that; a note inferred from whatever was in the context was false the
day it was written, and no date will ever catch it. So they buy an order to check in and a method
for each kind.
6. When a sub-task reads a great deal and returns a little — searching, summarising a long
document, checking a list. In the worked run the three documents were 18,600 tokens and the
parent needed three facts of about two dozen tokens from them. It costs its own instruction and tool
definitions, paid again; a context that is gone when it returns, so a question thought of later
means opening the documents again; and a hand-off the parent cannot check, which is Chapter 4's
compounding error with nothing left to contradict it. Chapter 37 is where running several of them
is costed.

> **You understand this when** you can say what share of your own agent's context is tool
> results, and name the one step that put the most of it there.
