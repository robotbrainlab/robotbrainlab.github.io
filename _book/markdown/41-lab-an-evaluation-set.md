# Lab: An Evaluation Set, and Two Prompts Compared Properly

Chapter 20 built the statistics and ran them on invented marks. Chapter 40 called a model and
measured what it cost. This lab puts the two together on real replies: thirty labelled cases from
the corpus, two prompts that differ in one sentence, and an interval on the difference between
them.

It also sets a trap, on purpose, and the trap is the chapter. **The verdict reverses depending on
how you grade**, and the tightest interval in the chapter is the one most likely to be misread.

*The problem.* I have two prompts and a feeling. I want a number with an interval around it.

*The question.* What does it take to compare two prompts in a way you could defend — and what does
the number you end up with actually measure?

> **Note:** As in chapter 40, the `text` blocks are one real run, and reading them as a promise is
> the mistake this chapter is about. **What held across three runs on different days is every
> verdict and the sign of every difference**; the task is extraction at temperature 0, and the
> model agreed with itself on all three trials of almost every case. The `mentioned` and
> `norm+notation` rows came out identical on every run, which matters because the +0.967 this
> chapter ends on is one of them. **What moved is one case at the margin.** The group of replies
> that carry a unit the prompt forbade was four cases in the run printed here and three in each
> later one — a different case each time — which is enough to move `strict` from 0.700 to 0.733;
> and on one of the three runs `contains` and `normalised` moved by about a case too. So expect
> your own figures to differ from these in the last case or two, and treat step 5 as the step that
> matters: the failures you read are yours, not mine. The two figures of a different kind again are
> the mean reply lengths in step 4, which carry whatever the model felt like saying; they are
> quoted as "about", and the shape rather than the digits is the point.

## Step 1: Thirty Cases the Corpus Can Actually Support

Make a folder, put the corpus in it, and set the key:

```text
  mkdir -p ~/sandbox/ch41 && cd ~/sandbox/ch41
  python3 -m venv .venv && source .venv/bin/activate
  cp -r <where you unpacked the book's labs>/corpus .
  export OPENAI_API_KEY="sk-..."
```

Every program below takes the corpus from `./corpus`, or from `CORPUS` if you put it elsewhere.
Nothing is installed; the standard library is enough again.

> **Note:** What this lab costs before you run it. Step 4 makes [**180 calls**]{.noindex} — thirty cases, two
> prompts, three trials — each sending one corpus document of a few hundred tokens and getting
> back a few. It is dominated by input tokens and comes to a little over a cent on a small model,
> but it is the first lab in the book whose cost is not negligible by inspection, and the figure to
> watch is the product: cases times prompts times trials. Forty minutes, most of it reading.

A case is an input plus whatever marks the answer right or wrong — chapter 20's definition, and
this lab needs thirty of them. The task is extraction: a question, a corpus document that answers
it, and the exact value a correct answer contains. What grades it is an **exact-match
grader** — string equality after a normalisation you declare — and [**no judge is needed**]{.noindex}, because
a figure can be compared by a program, which is chapter 31's rule for sorting a check into code or
judgement.

```python
"""Build the thirty cases, and refuse to write one the corpus does not support.

Each case is a question, the document that answers it, and the exact
string a correct answer contains. The assertion at the bottom is the
point: an expected answer that does not appear in its own document is
a case about nothing, and this is the cheapest moment to find out.
"""
import os
import pathlib
import sys

# The corpus the book ships, unpacked beside this file as `corpus/`.
# ask.py uses the same variable and the same default. A hardcoded
# path here would be a fact about one machine.
CORPUS = pathlib.Path(os.environ.get("CORPUS", "corpus")) / "docs"

#  question, document, expected exact answer
CASES = [
 ("How many days do I have to return a standard item?", "returns-standard", "30"),
 ("How many days do I have to return a clearance item?", "returns-clearance", "14"),
 ("Within how many days of the goods arriving is a refund issued?", "refunds-policy", "14"),
 ("What is the goodwill cap per order, in pounds?", "refunds-policy", "20"),
 ("What is the standard delivery charge on an order under 40 pounds?", "delivery-fees", "3.99"),
 ("What is the named-day delivery charge?", "delivery-fees", "5.99"),
 ("What is the next-day delivery charge?", "delivery-fees", "7.99"),
 ("What is the flat charge for a two-person delivery?", "delivery-fees", "19.99"),
 ("What is the surcharge for the Scottish Highlands and islands?", "delivery-exceptions", "9.50"),
 ("What is the surcharge for Northern Ireland?", "delivery-exceptions", "6.50"),
 ("What is the surcharge for the Isle of Man and the Channel Islands?", "delivery-exceptions", "11.00"),
 ("What is the surcharge for the Isles of Scilly?", "delivery-exceptions", "14.00"),
 ("How many years does the warranty run for?", "warranty-full", "two"),
 ("How many days is a repair itself covered for?", "warranty-full", "ninety"),
 ("For how many days are consumable parts covered?", "warranty-full", "ninety"),
 ("How many hours do I have to report cosmetic damage on delivery?", "damaged-on-arrival", "48"),
 ("How many days is a return postage label valid for?", "return-postage-labels", "21"),
 ("How many working days can a bank transfer refund take?", "refund-to-a-closed-card", "10"),
 ("How much does Harbour Plus cost per year, in pounds?", "plan-harbour-plus", "29"),
 ("How many years of warranty does Harbour Plus give?", "plan-harbour-plus", "three"),
 ("What is the capacity of the HL-2208 kettle, in litres?", "product-kettle-hl-2208", "1.7"),
 ("What is the power of the HL-2208 kettle, in watts?", "product-kettle-hl-2208", "3000"),
 ("What is the product code for a replacement kettle filter?", "product-kettle-hl-2208", "HL-2208-F"),
 ("How wide are the slots on the HL-2209 toaster, in millimetres?", "product-toaster-hl-2209", "34"),
 ("What is the maximum bulb wattage for the HL-3310 lamp?", "product-lamp-hl-3310", "60"),
 ("What is the maximum load of the HL-5512 chair, in kilograms?", "product-chair-hl-5512", "120"),
 ("What is the seat height of the HL-5512 chair, in centimetres?", "product-chair-hl-5512", "46"),
 ("Below how many units does an item show as low stock?", "stock-codes-and-statuses", "ten"),
 ("For how many years are order records kept?", "data-and-privacy", "seven"),
 ("Within how many working days does stage two of a complaint get a reply?", "complaints-process", "ten"),
]

if __name__ == "__main__":
    bad = []
    for q, doc, want in CASES:
        text = (CORPUS / f"{doc}.md").read_text()
        if want.lower() not in text.lower():
            bad.append((q[:46], doc, want))
    print(f"  {len(CASES)} cases, {len(set(d for _, d, _ in CASES))} documents")
    if bad:
        print(f"\n  {len(bad)} expected answers are NOT in their document:")
        for q, d, w in bad:
            print(f"    {w!r:<12} not in {d}  ({q})")
        sys.exit(1)
    print("  every expected answer appears in its own document")

    with open("cases.tsv", "w") as f:
        f.write("case_id\tquestion\tdoc_id\tanswer\n")
        for i, (q, d, a) in enumerate(CASES, 1):
            f.write(f"c{i:02d}\t{q}\t{d}\t{a}\n")
    print(f"  wrote cases.tsv")
```

```text
  30 cases, 17 documents
  every expected answer appears in its own document
  wrote cases.tsv
```

**The assertion at the bottom is the step.** An expected answer that does not appear in the
document it is drawn from is a case about nothing, and the moment to find that out is before you
have spent a hundred and eighty calls on it. It cost nothing to write and it is the only thing
standing between a labelled set and a set of labels somebody remembers being true.

It passes here with nothing refused, which is what it should do on a set built by copying answers
out of their documents. It is worth having anyway: the moment somebody edits a document — and
chapter 54's subject is that documents change under you — this is what turns a silently wrong key
into a failed run. **And it does not catch everything.** Step 5 finds two defects in this same key
that an assertion about presence cannot see, because both expected answers are present and still
wrong.

Seventeen of the corpus's forty documents carry a question. That is deliberate: the other
twenty-three are there as distractors for later labs, and a case set that drew on all forty would
have no room for them.

> **Tip:** Write the answers as the document writes them. Every one of these is copied out of its
> document rather than typed from memory, which is why the assertion passes — and step 5 is about
> the one way that discipline still leaves a defect behind.

## Step 2: The Client, and Two Prompts That Differ in One Sentence

Chapter 40 built the client: key from the environment, model pinned to a dated snapshot, one
timeout, no retry. Nothing here is new except the two instructions.

```python
"""The client, and the two prompts being compared.

Chapter 40 built this shape: key from the environment, model pinned to
a dated snapshot, one timeout, no retry. Nothing here is new except
the two instructions at the bottom, which differ in exactly one thing.
"""

import json
import os
import pathlib
import urllib.request

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 120
# The corpus the book ships, unpacked beside this file as `corpus/`.
# Set CORPUS to point somewhere else. build_cases.py uses the same
# variable and the same default; two defaults for one variable is a
# way to have a lab that works only for whoever wrote it.
CORPUS = pathlib.Path(os.environ.get("CORPUS", "corpus")) / "docs"

# The only difference between the two prompts is B's last sentence.
PROMPT_A = ("Answer the question using only the document below.\n\n"
            "Document:\n{doc}\n\nQuestion: {q}")
PROMPT_B = ("Answer the question using only the document below.\n"
            "Reply with the value only: no sentence, no explanation, and no "
            "units unless the question asks for them.\n\n"
            "Document:\n{doc}\n\nQuestion: {q}")


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def ask(template, question, doc_id, max_tokens=60):
    doc = (CORPUS / f"{doc_id}.md").read_text()
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user",
                      "content": template.format(doc=doc, q=question)}],
        "max_tokens": max_tokens, "temperature": 0,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"].strip()


def cases(path="cases.tsv"):
    rows = pathlib.Path(path).read_text().strip().split("\n")[1:]
    return [tuple(r.split("\t")) for r in rows]


if __name__ == "__main__":
    cs = cases()
    print(f"  {len(cs)} cases, model {MODEL}")
    cid, q, doc, want = cs[8]
    print(f"\n  {cid}: {q[:52]}")
    print(f"  expected: {want!r}\n")
    for name, tmpl in (("A", PROMPT_A), ("B", PROMPT_B)):
        r = ask(tmpl, q, doc)
        print(f"  prompt {name} -> {r[:44]!r}" + (" ..." if len(r) > 44 else ""))
```

```text
  30 cases, model gpt-4o-mini-2024-07-18

  c09: What is the surcharge for the Scottish Highlands and
  expected: '9.50'

  prompt A -> 'The surcharge for the Scottish Highlands and' ...
  prompt B -> '9.50 pounds'
```

**Read the two replies.** Both contain 9.50. Neither *is* 9.50. Prompt A wraps it in a sentence
with markdown emphasis; prompt B gives the value and a unit. That is the visible effect of the
extra sentence, and already enough to make the comparison depend on something that is not the
prompts. Step 5 finds two more things it changed — and notice already that B has given a unit,
which is the one thing the extra sentence told it not to do.

The two prompts differ in exactly one sentence, which is chapter 18's rule and the reason any of
what follows can be attributed to anything.

## Step 3: Three Graders, and They Disagree About One Reply

Before running anything over thirty cases, decide what counts as right. Three obvious graders,
and they do not agree.

```python
"""Three graders, and the same reply graded three ways.

The chapter's point lives here. "Which prompt is better" is not a
question about the prompts alone: it is a question about the prompts
and the grader together, and two of these three cannot answer it.
"""

import re

UNITS = ("pounds", "pound", "days", "day", "hours", "hour", "years", "year",
         "litres", "litre", "watts", "watt", "millimetres", "mm",
         "centimetres", "cm", "kilograms", "kg", "units", "working days")


def strict(reply, answer):
    """The reply IS the answer. Nothing else."""
    return reply == answer


def contains(reply, answer):
    """The answer appears somewhere in the reply."""
    return answer.lower() in reply.lower()


def normalised(reply, answer):
    """The reply is the answer once formatting and a trailing unit go."""
    return _norm(reply) == _norm(answer)


def _norm(s):
    s = s.lower().strip()
    s = s.replace("*", "").replace("`", "")       # markdown emphasis
    s = re.sub(r"^(the answer is|it is|answer:)\s*", "", s)
    s = s.strip(" .,:;!?\"'")
    for u in sorted(UNITS, key=len, reverse=True):  # longest first
        if s.endswith(" " + u):
            s = s[: -len(u) - 1].strip()
    return s.strip(" .,")


GRADERS = (("strict", strict), ("contains", contains),
           ("normalised", normalised))

if __name__ == "__main__":
    SAMPLES = [
        ("The surcharge for the Highlands is **9.50 pounds**.", "9.50"),
        ("9.50 pounds", "9.50"),
        ("9.50", "9.50"),
        ("The answer is 30 days.", "30"),
        ("It is covered for ninety days.", "ninety"),
        ("6.50", "9.50"),
    ]
    print("  One reply, three graders.\n")
    print(f"  {'reply':<34} {'want':<7} strict cont norm")
    for reply, want in SAMPLES:
        r = [("y" if f(reply, want) else "-") for _, f in GRADERS]
        short = reply if len(reply) <= 32 else reply[:29] + "..."
        print(f"  {short:<34} {want:<7} {r[0]:^6} {r[1]:^4} "
              f"{r[2]:^4}".rstrip())

    print("\n  Read the last row first: all three agree when the answer")
    print("  is wrong, which is the only thing they agree on.\n")
    print("  `strict` fails a correct answer for having a word")
    print("  round it. `contains` passes anything that mentions the")
    print("  number, including a sentence that gets the point")
    print("  backwards. `normalised` strips emphasis, a leading")
    print("  'the answer is' and one trailing unit, and no more -")
    print("  which is why row 5 fails it and row 4 passes. A")
    print("  hand-written normaliser is not consistent until")
    print("  somebody makes it so.\n")
    print("  None of the three is right in general. Which one is")
    print("  right depends on what reads the answer: a program")
    print("  parsing it wants something near `strict`, a person")
    print("  reading it is closer to `contains`, and a measurement")
    print("  of whether the model KNEW wants something looser than")
    print("  any of these three, which step 6 has to add. Three")
    print("  different questions, and a score with no grader")
    print("  beside it does not say which one was asked.")
```

```text
  One reply, three graders.

  reply                              want    strict cont norm
  The surcharge for the Highlan...   9.50      -     y    -
  9.50 pounds                        9.50      -     y    y
  9.50                               9.50      y     y    y
  The answer is 30 days.             30        -     y    y
  It is covered for ninety days.     ninety    -     y    -
  6.50                               9.50      -     -    -

  Read the last row first: all three agree when the answer
  is wrong, which is the only thing they agree on.

  `strict` fails a correct answer for having a word
  round it. `contains` passes anything that mentions the
  number, including a sentence that gets the point
  backwards. `normalised` strips emphasis, a leading
  'the answer is' and one trailing unit, and no more -
  which is why row 5 fails it and row 4 passes. A
  hand-written normaliser is not consistent until
  somebody makes it so.

  None of the three is right in general. Which one is
  right depends on what reads the answer: a program
  parsing it wants something near `strict`, a person
  reading it is closer to `contains`, and a measurement
  of whether the model KNEW wants something looser than
  any of these three, which step 6 has to add. Three
  different questions, and a score with no grader
  beside it does not say which one was asked.
```

**The last row is the only agreement.** All three reject a wrong answer. On a *correct* answer
they split, and the split is not a matter of strictness — it is three different questions wearing
one name.

`strict` asks whether the reply is the answer and nothing else. `contains` asks whether the right
value is in there somewhere, which a sentence satisfies and so does a sentence that draws the
opposite conclusion. `normalised` strips markdown emphasis, a leading *the answer is*, and one
trailing unit, and is otherwise `strict`. The rule it applies is an **answer normalisation**: the
statement of which two strings count as the same answer.

**And `normalised` is visibly inconsistent, which is worth leaving in.** It passes *The answer is
30 days.* and fails *It is covered for ninety days.* — because it strips a leading phrase from a
list it happens to contain and a trailing unit from another, and *covered for* is on neither list.
A hand-written normaliser is a pile of special cases until somebody makes it a rule, and a
measurement resting on one inherits every gap.

> **Warning:** None of the three is right in general, and choosing one is not a technicality to
> get past. A program that parses the answer wants something near `strict`. A person reading it is
> closer to `contains`. A measurement of whether the model *knew* the answer wants something
> looser than all three, which step 6 has to add. Those are different systems asking different
> questions, and a score without the grader beside it does not say which was asked.

## Step 4: Run It

Thirty cases, two prompts, three trials each. Chapter 20's rule on trials applies and is why this
program writes every trial to a file rather than averaging as it goes: **the averaging happens
within a case**, so one case stays one row, and doing it in the open means you can check that it
was done.

```python
"""Run both prompts over all thirty cases, three times each, and save it.

Chapter 20's rule: trials are averaged WITHIN a case, so one case
stays one row. This writes every trial to a file so the averaging
happens where you can see it, and so the expensive part runs once.
"""

import pathlib

from ask import PROMPT_A, PROMPT_B, ask, cases

TRIALS = 3
OUT = pathlib.Path("results.tsv")


if __name__ == "__main__":
    cs = cases()
    prompts = (("A", PROMPT_A), ("B", PROMPT_B))
    total = len(cs) * len(prompts) * TRIALS
    print(f"  {len(cs)} cases x {len(prompts)} prompts x {TRIALS} trials"
          f" = {total} calls\n")

    lengths = {"A": [], "B": []}
    with OUT.open("w") as f:
        f.write("case_id\tprompt\ttrial\tanswer\treply\n")
        done = 0
        for cid, q, doc, want in cs:
            for name, template in prompts:
                for t in range(1, TRIALS + 1):
                    reply = ask(template, q, doc).replace("\t", " ")
                    reply = reply.replace("\n", " \\n ")
                    f.write(f"{cid}\t{name}\t{t}\t{want}\t{reply}\n")
                    lengths[name].append(len(reply))
                    done += 1
            f.flush()
            if int(cid[1:]) % 10 == 0:
                print(f"  {done:>3}/{total} calls", flush=True)

    print(f"\n  wrote {OUT}, {done} rows\n")
    for name in ("A", "B"):
        L = lengths[name]
        print(f"  prompt {name}: mean {sum(L)/len(L):>5.1f} characters,"
              f" from {min(L):>2} to {max(L):>3}")
    print("\n  That is the only thing this program measures, and")
    print("  it is the whole of what the instruction changed so")
    print("  far. Nothing here says whether either prompt got")
    print("  the answer right.")
```

```text
  30 cases x 2 prompts x 3 trials = 180 calls

   60/180 calls
  120/180 calls
  180/180 calls

  wrote results.tsv, 180 rows

  prompt A: mean  54.9 characters, from 32 to  92
  prompt B: mean   4.2 characters, from  1 to  12

  That is the only thing this program measures, and
  it is the whole of what the instruction changed so
  far. Nothing here says whether either prompt got
  the answer right.
```

**One hundred and eighty calls, and the only thing measured so far is length.** Prompt A's replies
average about fifty-five characters; prompt B's average about four. A factor of thirteen, from one
sentence.

That is worth pausing on, because it is the entire observable effect of the instruction at this
point. Nothing in that output says either prompt got an answer right. It would be easy to look at
a reduction of more than tenfold in output and feel that something had improved — and chapter 1
already told you that the reply is the dearer half of the exchange, so something *has* — but
whether the answers are still correct is a separate question that no amount of looking at lengths
will settle.

## Step 5: Read the Failures Before You Believe the Score

This is the step people skip, and skipping it is how a confident number with a tight interval
gets reported about nothing.

```python
"""Read the failures before believing the score. All of them.

Chapter 30's method applied to a measurement. The trap this program
exists to avoid is reading the failures of ONE grader: each of the
three sees a different set, and the cheapest one to look at is the
one that sees least.
"""

import pathlib

from grade import contains, normalised, strict

RESULTS = "results.tsv"
CASES = "cases.tsv"


def rows():
    text = pathlib.Path(RESULTS).read_text().strip().split("\n")[1:]
    return [tuple(l.split("\t")) for l in text]


def questions():
    text = pathlib.Path(CASES).read_text().strip().split("\n")[1:]
    return {l.split("\t")[0]: l.split("\t")[1] for l in text}


if __name__ == "__main__":
    rs, qs = rows(), questions()
    first = [r for r in rs if r[2] == "1"]

    print("  How many of prompt B's thirty cases each grader")
    print("  marks wrong, on the first trial:\n")
    for name, g in (("strict", strict), ("normalised", normalised),
                    ("contains", contains)):
        n = sum(1 for cid, p, t, w, r in first
                if p == "B" and not g(r, w))
        print(f"    {name:<12} {n:>2} of 30")
    print("\n  Three different sets, and the loosest sees fewest. So")
    print("  read the union, not the convenient one.\n")

    union = [(cid, w, r) for cid, p, t, w, r in first
             if p == "B" and not strict(r, w)]
    print(f"  Prompt B, every case `strict` rejects ({len(union)}):\n")
    for cid, want, reply in union:
        tag = ("notation" if not contains(reply, want)
               else "unit" if normalised(reply, want) else "qualifier")
        print(f"    {cid}  key {want!r:9} got {reply!r:14} {tag}")

    g1 = [u for u in union if not contains(u[2], u[1])]
    g2 = [u for u in union if normalised(u[2], u[1])]
    g3 = [u for u in union
          if contains(u[2], u[1]) and not normalised(u[2], u[1])]

    worded = [1 for cid, p, t, w, r in first
              if p == "B" and w.isalpha()]
    in_words = [1] * (len(worded) - len(g1))

    def cases(rows):
        """The count and its noun from the same expression.

        Printing len(rows) and then writing 'four' in the sentence
        under it is how this program contradicted itself on the
        first run where a group changed size.
        """
        return f"{len(rows)} case" + ("" if len(rows) == 1 else "s")

    # The three labels are the three KINDS of defect, not a count.
    # A group that is empty on your run leaves its number out.
    present = [g for g in (g1, g3, g2) if g]
    print(f"\n  {len(present)} groups, each a different defect.\n")

    if g1:
        print(f"  1. {cases(g1)}, keyed in words, answered in digits.")
        print("     The model is right. The KEY is wrong, because")
        print("     it allows one notation and the document uses the")
        print("     other. It is not that a terse reply always")
        print(f"     gives digits: {cases(in_words)} came back in")
        print("     words.\n")

    if g3:
        print(f"  2. {cases(g3)}, keyed {g3[0][1]!r}, "
              f"answered {g3[0][2]!r}.")
        print("     The document says 'takes up to 10 working days'.")
        print("     The model quoted the document and the key did")
        print("     not. A second kind of key defect: a dropped")
        print("     qualifier.\n")

    if g2:
        print(f"  3. {cases(g2)}, answered with a unit the prompt")
        print("     forbade. Prompt B says 'no units unless the")
        print("     question asks for them' and none of these")
        print(f"     questions does. So it was disobeyed on {len(g2)}")
        print("     of 30 - and `normalised` strips a trailing unit,")
        print("     so the headline score never shows it. The grader")
        print("     written to be fair to prompt A quietly forgave")
        print("     prompt B's only real failure.\n")

    print("  None of them was found by noticing repeatability.")
    print("  All of them were found by reading the replies, which")
    print("  is chapter 30's method and the only one that works")
    print("  here.")
```

```text
  How many of prompt B's thirty cases each grader
  marks wrong, on the first trial:

    strict        9 of 30
    normalised    5 of 30
    contains      4 of 30

  Three different sets, and the loosest sees fewest. So
  read the union, not the convenient one.

  Prompt B, every case `strict` rejects (9):

    c09  key '9.50'    got '9.50 pounds'  unit
    c10  key '6.50'    got '6.50 pounds'  unit
    c11  key '11.00'   got '11.00 pounds' unit
    c12  key '14.00'   got '14.00 pounds' unit
    c13  key 'two'     got '2'            notation
    c14  key 'ninety'  got '90'           notation
    c15  key 'ninety'  got '90'           notation
    c18  key '10'      got 'up to 10'     qualifier
    c20  key 'three'   got '3'            notation

  3 groups, each a different defect.

  1. 4 cases, keyed in words, answered in digits.
     The model is right. The KEY is wrong, because
     it allows one notation and the document uses the
     other. It is not that a terse reply always
     gives digits: 3 cases came back in
     words.

  2. 1 case, keyed '10', answered 'up to 10'.
     The document says 'takes up to 10 working days'.
     The model quoted the document and the key did
     not. A second kind of key defect: a dropped
     qualifier.

  3. 4 cases, answered with a unit the prompt
     forbade. Prompt B says 'no units unless the
     question asks for them' and none of these
     questions does. So it was disobeyed on 4
     of 30 - and `normalised` strips a trailing unit,
     so the headline score never shows it. The grader
     written to be fair to prompt A quietly forgave
     prompt B's only real failure.

  None of them was found by noticing repeatability.
  All of them were found by reading the replies, which
  is chapter 30's method and the only one that works
  here.
```

**Nine cases, three defects, and only one of them is about notation.**

**Four are the key's notation.** The model answered `2`, `90`, `3` where the key says `two`,
`ninety`, `three`. It is right every time; the key allows one notation and the document uses the
other. Note what the program is careful *not* to claim: three other word-keyed cases came back in
words, so "a terse reply gives digits" is a tendency of four cases in seven and not a mechanism.

**One is the key dropping a qualifier.** Case 18 asks how many working days a bank transfer can
take, the key says `10`, and the document says *the transfer takes up to 10 working days*. The
model answered `up to 10`. **It quoted the document and the key did not.** That is a second kind of
key defect and an assertion about presence cannot find it, because `10` is in the document — it is
just not the whole of what the document says.

**And four are the prompt being disobeyed, which is the finding worth the chapter.** Prompt B says
*no units unless the question asks for them*. None of the four surcharge questions asks. The model
returned `9.50 pounds`, `6.50 pounds`, `11.00 pounds`, `14.00 pounds`. So the instruction the whole
comparison is about was [**ignored on four of thirty cases**]{.noindex} — and the headline score never shows
it, because `normalised` strips a trailing unit. **The grader written to be fair to prompt A
quietly forgave prompt B's only real failure.**

That last one is the reason step 5 reads the *union* and not one grader's list. Each of the three
graders sees a different set, the loosest sees fewest, and the cheapest one to look at is the one
that hides most. Had this chapter read `contains`'s four and stopped — which is what its first
draft did — it would have found the notation defect, missed the other two, and concluded that the
format instruction worked.

> **Warning:** The temptation here is to notice that the notation cases fail on all three trials
> and make a rule of it. **Do not.** Chapter 20 is explicit that in a real evaluation set *most
> cases are reliably right or reliably wrong, and only a few are genuinely uncertain* — so failing
> every trial is the ordinary condition of a failing case, not a signal that the case is broken.
> Chapter 33 has the name for one that stays failing: a [**standing failure**]{.noindex}, which is a real
> failure somebody has to work. What found all three defects here was reading the replies, which
> is chapter 30's method. Repeatability found nothing; it was a property of these defects and not
> a diagnostic for them.

**A score with an interval round it would have reported all nine as prompt B being worse and told
you nothing about any of it.** The interval would have been narrow, because the effects are
perfectly consistent. Narrow is not the same as right.

> **Tip:** The cheapest version of this step is the one above: print every reply a strict grader
> rejects *for the prompt you are testing*, with the key beside it, and read them. Nine rows here,
> all of them prompt B's — `strict` rejects all thirty of prompt A's, which is the score and not a
> list worth reading. Chapter 30 owns the
> method and calls it error analysis; this is the smallest useful instance of it, run on a
> measurement rather than on a product.

## Step 6: The Interval, and the Verdict You Can Defend

Now the repair the last step earned, and then chapter 20's three lines.

```python
"""The paired bootstrap, and the verdict.

Chapter 20 owns all of this: average the trials WITHIN a case so one
case stays one row, put the interval on the DIFFERENCE rather than on
the two scores, and resample cases rather than results. Three lines
of it are the method and the rest is reading the output honestly.
"""

import pathlib
import random

from grade import GRADERS, _norm

# The repair step 5 earned. The documents write these in words and
# the model answered four of them in digits, so the key scored four
# correct answers wrong. This is the rule, declared rather than
# buried in a regex.
WORDS = {"one": "1", "two": "2", "three": "3", "four": "4",
         "five": "5", "six": "6", "seven": "7", "eight": "8",
         "nine": "9", "ten": "10", "fourteen": "14", "twenty": "20",
         "thirty": "30", "forty": "40", "fifty": "50", "ninety": "90"}


def same(a, b):
    return a == b or WORDS.get(a) == b or WORDS.get(b) == a


DIGITS = {v: k for k, v in WORDS.items()}


def mentioned(reply, answer):
    """Is the right value in the reply at all, in either notation?

    Symmetric on purpose. The first version mapped a word key to
    digits and not the other way. 22 of the 30 keys here are
    digits, and five of those have a word form in WORDS at all
    - 30, 14, 14, 20 and 10 - so a correct word-form reply to
    any of those five was marked wrong, by the grader being
    called the one that asks whether the model knew.
    """
    r = reply.lower()
    a = answer.lower()
    forms = {a}
    if a in WORDS:
        forms.add(WORDS[a])
    if a in DIGITS:
        forms.add(DIGITS[a])
    return any(f in r for f in forms)


def either_notation(reply, answer):
    """`normalised`, with words and digits counted as the same.
    This is the one that asks whether a program could READ it."""
    return same(_norm(reply), _norm(answer))

TRIALS_PER_CASE = 3
RESAMPLES = 10_000
SEED = 41


def per_case(grader):
    """One mark per case per prompt: the mean over that case's trials."""
    tally = {}
    rows = pathlib.Path("results.tsv").read_text().strip().split("\n")[1:]
    for line in rows:
        cid, p, t, want, reply = line.split("\t")
        tally.setdefault((cid, p), []).append(1.0 if grader(reply, want) else 0.0)
    cases = sorted({cid for cid, _ in tally})
    return [(sum(tally[(c, "A")]) / len(tally[(c, "A")]),
             sum(tally[(c, "B")]) / len(tally[(c, "B")])) for c in cases]


def interval(pairs, n=RESAMPLES):
    rng = random.Random(SEED)
    k = len(pairs)
    diffs = []
    for _ in range(n):
        s = [pairs[rng.randrange(k)] for _ in range(k)]
        diffs.append(sum(b - a for a, b in s) / k)
    diffs.sort()
    return diffs[int(0.025 * n)], diffs[int(0.975 * n)]


if __name__ == "__main__":
    print(f"  {TRIALS_PER_CASE} trials averaged within each case, so one")
    print("  case is one row. Then the interval on the DIFFERENCE.\n")
    print("    grader           A      B    B-A   95% interval  wins")
    rows = list(GRADERS) + [("mentioned", mentioned),
                            ("norm+notation", either_notation)]
    for name, g in rows:
        pairs = per_case(g)
        a = sum(x for x, _ in pairs) / len(pairs)
        b = sum(y for _, y in pairs) / len(pairs)
        lo, hi = interval(pairs)
        if lo > 0:
            v = "B"
        elif hi < 0:
            v = "A"
        else:
            v = "neither"
        print(f"    {name:<13} {a:.3f}  {b:.3f} {b-a:+.3f} "
              f"{lo:+.3f} to {hi:+.3f}  {v}")

    pairs = per_case(either_notation)
    agree = sum(1 for x, y in pairs if x == y)
    aonly = sum(1 for x, y in pairs if x > y)
    bonly = sum(1 for x, y in pairs if y > x)
    print(f"\n  On the grader this chapter defends, {len(pairs)} cases:")
    verb = "comes" if agree == 1 else "come"
    print(f"    {agree} {verb} out the same under both prompts")
    print(f"    {aonly} favour A, {bonly} favour B")
    print(f"\n  The comparison rests on those {aonly + bonly} cases and not")
    print(f"  on the {agree} that agree - chapter 20's last line.\n")
    print("  Now the `mentioned` row. Both prompts score 1.000,")
    print("  and read that carefully: it is a CEILING with no")
    print("  discriminating cases, and its interval contains zero,")
    print("  so by chapter 20's rule it says `cannot tell` rather")
    print("  than proving the two equal. What it does establish -")
    print("  as far as a substring test can, since one accepts a")
    print("  value that is in the reply for another reason - is")
    print("  that the right value is somewhere in every reply.\n")
    print("  So the +0.967 below it measures format, and this set")
    print("  cannot separate the two prompts on accuracy at all.")
    print("  B is the prompt to use when a program reads the")
    print("  answer. Whether B is better at the TASK is a question")
    print("  these thirty cases were too easy to ask.\n")
    print("  And the tightest interval here is the most likely to")
    print("  be misread, which is not a coincidence: a mechanical")
    print("  effect is perfectly consistent, so the width collapses")
    print("  while saying nothing about what was measured.")
```

```text
  3 trials averaged within each case, so one
  case is one row. Then the interval on the DIFFERENCE.

    grader           A      B    B-A   95% interval  wins
    strict        0.000  0.700 +0.700 +0.533 to +0.867  B
    contains      1.000  0.867 -0.133 -0.267 to -0.033  A
    normalised    0.000  0.833 +0.833 +0.700 to +0.967  B
    mentioned     1.000  1.000 +0.000 +0.000 to +0.000  neither
    norm+notation 0.000  0.967 +0.967 +0.900 to +1.000  B

  On the grader this chapter defends, 30 cases:
    1 comes out the same under both prompts
    0 favour A, 29 favour B

  The comparison rests on those 29 cases and not
  on the 1 that agree - chapter 20's last line.

  Now the `mentioned` row. Both prompts score 1.000,
  and read that carefully: it is a CEILING with no
  discriminating cases, and its interval contains zero,
  so by chapter 20's rule it says `cannot tell` rather
  than proving the two equal. What it does establish -
  as far as a substring test can, since one accepts a
  value that is in the reply for another reason - is
  that the right value is somewhere in every reply.

  So the +0.967 below it measures format, and this set
  cannot separate the two prompts on accuracy at all.
  B is the prompt to use when a program reads the
  answer. Whether B is better at the TASK is a question
  these thirty cases were too easy to ask.

  And the tightest interval here is the most likely to
  be misread, which is not a coincidence: a mechanical
  effect is perfectly consistent, so the width collapses
  while saying nothing about what was measured.
```

**Five graders, and two axes.** They differ in two independent ways, and a grader named by one of
them alone is not identified. The first axis is what counts as a match: `strict`, `normalised` and
`norm+notation` want the reply to *be* the answer, while `contains` and `mentioned` accept the
value anywhere inside it. The second is which notation the key is allowed to be in: `strict`,
`normalised` and `contains` take the key as written, while `norm+notation` and `mentioned` accept
either `two` or `2`. So *the grader that wants the value anywhere* names two graders whose verdicts
are opposite, and so does *the grader that accepts either notation*. From here each one is called
by its name.

**Read the `wins` column down.** Five graders over the same one hundred and eighty trials, and one
of them says prompt A is better, with an interval that clears zero. If you had written `contains`
and stopped, you would have a defensible-looking result pointing the wrong way.

**Then read the `mentioned` row, because that is the verdict.** Asking only whether the right
value is present anywhere in either notation, **both prompts score 1.000.** Every reply on
every case contains the right value in one notation or the other — and read that as the ceiling it
is, not as proof. Its interval contains zero, so chapter 20's rule makes it *cannot tell*; and what
it establishes goes only as far as a substring test can, which is not far: `mentioned` would accept
`ten` inside `often`. Step 5 read prompt B's nine rejected replies one at a time. It never looked at
prompt A's, so what stands behind prompt A's 1.000 is a grader and not a reading.

**So the +0.967 on the row below is not accuracy. It is format.** Prompt B is not better at the
task. Prompt B is better at being graded — which is a genuine reason to prefer it when a program
has to read the answer, and a completely different claim from the one a +0.900 to +1.000 interval
looks like it is making.

That is the answer to the interview question, and it is not "I ran a bootstrap". It is: here is the
set, here is the grader and why that one, here is what I read before believing it, and here is
what the number measures — which in this case is parseability and not capability.

> **Warning:** The tightest interval in this chapter is the most misleading one, and that is not a
> coincidence. An effect that is purely mechanical — a format instruction either applies or it
> does not — is perfectly consistent across cases and trials, so the interval collapses. **Width
> measures how reliably you have found something, never whether it is the thing you wanted.**

## What To Actually Do

1. **Write the cases down with the answers copied out of the source**, and assert that each answer
   appears in the document it came from.
2. **Choose the grader before you run anything**, say which question you are asking, and write the
   choice down beside the score for ever after. This chapter adds two graders *after* the run,
   which is the move chapter 20 warns about for the case set — change it mid-comparison and you
   have stopped measuring. What makes it legitimate here is that both repairs are justified by the
   documents and not by which prompt lost: the key was wrong about a notation and about a
   qualifier, and would have been wrong whichever prompt that favoured.
3. **Change one sentence between the two prompts**, so the difference can be attributed.
4. **Run every case more than once** and average the trials *within* the case, so one case stays
   one row.
5. **Read every failure a strict grader rejects for the prompt you are testing**, and not one
   grader's list. Nine for prompt B here, and they were three different defects: four the key's
   notation, one the key dropping a qualifier the document has, and four the prompt's own
   instruction being ignored.
6. **Expect a failing case to fail every time.** Chapter 20 says most cases are reliably right or
   reliably wrong, so repeatability is not a signal of anything; what diagnoses a failure is
   reading it.
7. **Put the interval on the difference, paired**, and resample cases rather than results.
8. **Say how many cases actually disagree.** Here it is 29 of 30 on the final grader, which is
   unusually many and worth saying because it is usually unusually few.
9. **Ask what the number measures** before reporting it. A format instruction can produce a huge,
   tight, entirely genuine interval around a change in parseability.
10. **Report the grader, the case count, the trial count and the interval together.** Any one of
    them alone is a number somebody can misread, and they will.

## Summary, Key Terms, and Review Questions

### Summary

Thirty extraction cases from the corpus — a question, the document that answers it, and the exact
value — graded by an exact-match grader, so no judge is needed, which is chapter 31's rule for
sorting a check into code or judgement. The cases are built by a program that **asserts every
expected answer appears in its own document**, because a case whose answer is not in its source is
a case about nothing. Two prompts differing in one sentence: B adds *reply with the value only*.
That one sentence takes the mean reply from about 55 characters to about 4, more than tenfold, and at
that point nothing has been measured about correctness at all. **Three graders disagree about the
same correct reply**: `strict` wants the reply to be the answer, `contains` wants the value present
anywhere, `normalised` strips emphasis, a leading *the answer is* and one trailing unit —
and visibly inconsistently, passing *The answer is 30 days.* while failing *It is covered for
ninety days.* **Reading the failures is the step that matters, and it has to be the union and not one
grader's list** — the three graders reject 9, 5 and 4 of prompt B's thirty cases, and the loosest
sees fewest. Read all nine and they are **three different defects**. Four are the key's notation:
the model answers `2`, `90`, `3` where the key says `two`, `ninety`, `three`, and it is right every
time — though three other word-keyed cases came back in words, so a terse reply giving digits is a
tendency of four in seven and not a mechanism. One is the key dropping a qualifier: it says `10`
where the document says *up to 10 working days*, and the model quoted the document. **And four are
the prompt being ignored** — B says *no units unless the question asks*, none of the four surcharge
questions asks, and the model returned `9.50 pounds` anyway. The headline never shows that, because
`normalised` strips a trailing unit: **the grader written to be fair to prompt A forgave prompt B's
only real failure.** None of the three was found by noticing repeatability, and chapter 20 says why
that could not have worked — most cases in a real set are reliably right or reliably wrong, so
failing every trial is the ordinary condition of a failing case rather than a signal. Chapter 33's
name for one that stays failing is a **standing failure**. With a notation rule added, chapter 20's
paired bootstrap over 10,000 resamples gives five verdicts from the same 180 trials, and **one
grader, `contains`, says prompt A is better with an interval clearing zero.** On `mentioned` — the
right value present in either notation — both prompts score 1.000, and that is a **ceiling with no
discriminating cases**, so by chapter 20's own rule it is *cannot tell* rather than proof of
anything; what it does establish, as far as a substring test can, is that the right value is
somewhere in every reply. **So the +0.967 is a measurement of format and this set cannot separate the two
prompts on accuracy at all.** The comparison rests on the 29 cases that disagree and not on the one
that agrees. And the general lesson: the tightest
interval in the chapter is the most misleading, because a mechanical effect is perfectly consistent
and so collapses the width — **width measures how reliably you found something, never whether it is
the thing you wanted.**

### Key Terms

| Term | Meaning |
|---|---|
| **Exact-match grader** | A grader whose verdict is string equality after a declared normalisation. Needs no judge, which is what makes it reachable first. Chapter 30 calls exact match *useless* and is right about its own case, grading free prose against a reference — and this chapter's step 6 shows why, with prompt A scoring 0.000 on thirty replies that a substring grader accepts in full. It works here only because the answer is one figure, and the declared normalisation is the whole of it |
| **Answer normalisation** | The rule saying which two strings count as the same answer: what case, punctuation, emphasis, units and notation are ignored. Not chapter 12's normalisation, which is about a model's internals. Write it down, because a score is a measurement of it as much as of the model |

### Worth Memorising

| Item | Value or formula |
|---|---|
| What a score needs beside it | The grader, the case count, the trial count and the interval. Any one alone can be misread |
| Where the trials go | Averaged *within* a case, so one case stays one row (chapter 20) |
| What to do before reading a score | Read the failures, and every grader's set rather than one grader's. Five of the nine here were the key and not the model |
| A case that fails every trial | The ordinary condition of a failing case (chapter 20), and not a signal about anything. What separates a wrong answer from a wrong key is reading the reply (chapter 30) |
| What a narrow interval means | That the effect is consistent. Not that it is the effect you wanted |
| The order of the question | Did the model know? Then: could a program read it? Those are different graders and different claims |

### Review Questions

1. How did you compare two prompts in a way you could defend?
2. You have a score of 0.967 with an interval of +0.900 to +1.000. What is wrong with reporting
that as an accuracy improvement?
3. Your strictest grader rejects nine of thirty replies and your loosest rejects four. Which set
do you read, and why?
4. Why does this lab need no judge, and what would make one necessary?
5. Your grader marks a reply wrong that a person would mark right. Name three ways that can happen
and say which one is your fault.

### Review Answers

1. A fixed set of thirty cases with the answers copied out of the source documents, and a program
that asserts each answer actually appears in the document it came from — so the set cannot be a
set of labels somebody remembers. Both prompts differ in exactly one sentence, so any difference
can be attributed (chapter 18). Three trials per case, **averaged within the case** so one case
stays one row (chapter 20). A grader chosen and written down before the run, with the choice
justified: a program parsing the answer wants near-exact equality, a person reading it wants the
value present anywhere, and a measurement of whether the model *knew* wants something looser than any of them. Then
a paired bootstrap on the **difference**, resampling cases rather than results. And the two things
that make it defensible rather than merely computed: **I read the failures of every grader before
looking at the score**, which turned up five cases where the key was wrong and not the prompt, and
four where prompt B broke its own instruction; and I said what the number measures, which here is
format rather than accuracy, because `mentioned` — which asks only whether the value is present
anywhere in either notation — separates the two prompts not at all.
2. Because a tight interval says the effect is consistent, not that it is the effect you named.
Here the thing being measured is whether a format instruction applied — and a format instruction
either applies or it does not, so it is perfectly consistent across cases and trials and the
interval collapses. The same 180 trials, graded by `mentioned` — the value present anywhere in
either notation — give both prompts 1.000, a ceiling with nothing to discriminate between, so by
chapter 20's rule it says *cannot tell* rather than that the two are equal. So the 0.967 is parseability. It is real, it is worth having if a program has to read the answer, and calling it
accuracy is false. **Width measures how reliably you found something, never whether it is the thing
you wanted.**
3. The union, which here means the strict grader's nine. Each grader rejects a different set, the
loosest rejects fewest, and the loosest is the one it is comfortable to read — so reading it is how
you find the smallest number of defects your data holds rather than all of them. In this chapter
the four hold one defect and the nine hold three: four cases where the key allowed only the
notation the document did not use, one where the key dropped the document's qualifier, and four
where the prompt's own formatting instruction was broken. The last group is the one no *score*
would have shown you, because the grader chosen for the headline strips exactly what it produced.
It is visible only in the list of replies a strict grader rejects.
4. Because the answer is a figure, and a figure can be compared by a program — which is chapter
31's test for sorting a check into code or judgement: code can decide where the comparison is
between two things both literally present. What would make a judge necessary is an answer whose
correctness is a question about meaning: a summary, an explanation, a rewrite, or anything where
two different strings are both right. Note that this lab is already *most* of the way to needing
one — the normaliser is a pile of special cases, and every special case added to it is a judgement
being made in code rather than by a judge.
5. **The reply is right but formatted differently** — a sentence round the value, markdown
emphasis, a unit the key omits. **The reply is right in another notation** — digits where the key
has words, which is this chapter's own defect. **The key is wrong** — the expected answer is not
what the document says. The first two are the grader's fault and therefore yours; the third is the
set's fault and therefore also yours. Which is the point: every one of the three is something you
built, and none of them is the model being bad at the task. That is why the failures get read
before the score does.

> **You understand this when** somebody shows you a tight interval on a prompt comparison and your
> first question is what the grader counted as a right answer.
