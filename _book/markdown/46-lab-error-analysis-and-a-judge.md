# Lab: Error Analysis, and a Judge You Can Trust

Chapter 45 built a pipeline and measured its stages. This chapter takes the thing the pipeline
produces — answers — and turns them into something you can run on every change. Chapter 30 gave
the method: read real outputs, write a note on each failure, group the notes into named failure
modes, and let the modes choose what you measure. Chapter 31 gave the measuring: a pass-or-fail
check per mode, code wherever code can decide, and a judge that has to be validated before it is
believed. Chapter 33 gave the set you keep. This chapter runs all three on eighty real answers
and reports what they cost.

*The problem.* I have forty real outputs and no idea how to turn them into something I can
measure.

*The question.* What does chapter 30's afternoon actually buy on a system that mostly works —
and what does it not buy that you would have assumed it did?

**Three results, so that the chapter's shape is visible before the work.** The forty answers of
the problem statement hold eight failures, not forty, which is the first thing the arithmetic
says and the whole reason this lab reads eighty. The six failure modes that come out of the
seventeen failures are a list of *names* and not an *order*, and the mode the first forty call
largest is third on the eighty. And the judge, built for the largest mode no code check reaches,
comes out worse than doing nothing — twice, under two instructions — which is a finding about
the judge and not about the mode.

**What this lab does not do.** It teaches no new measure, and it adds nothing to the book's
vocabulary of evaluation: chapter 30 owns the method and the words *error analysis* and *failure
mode*, chapter 31 owns judges, baselines, self-agreement and the flip count, chapter 33 owns the
regression set, criteria drift and the trace, and chapter 20 owns every interval here. **It does
name six failure modes, and they are this application's rather than the book's** — they come out
of its own notes in step 4, as chapter 30's method says they must. Two of the six are chapter 30's
name for name, two are new, and two are one of chapter 30's split in half — a split chapter 30
does not make, and the reason its own citation checks dent that mode instead of closing it. Step 4
says which is which and why. It measures no retrieval: there is no recall and no nDCG in
it, because the system is chapter 45's and is not changed to improve it. It computes no
groundedness figure — that is chapter 32's claim-level check, named here and not built, and step
5 is where that matters: one of the six modes needs exactly that check and gets none, which is
the clearest thing the non-scope costs. It does not reduce cost or latency (chapter 49), does not
attack anything (chapter 50), and has no agent in it (chapters 34 to 38). And it re-derives nothing of chapter 20's:
its resampling is applied in two of the programs and each says in its docstring that the method
is 20's. **Neither application is a paired comparison** — both resample one sample — and the one
place this chapter compares two versions, step 7, uses a list of cases and no interval at all.

**What you need.** Chapter 45's folder, exactly as that chapter left it. Copy it, so that this
chapter's files cannot overwrite that chapter's results:

```text
  cp -r ~/sandbox/ch45 ~/sandbox/ch46 && cd ~/sandbox/ch46
```

That brings `corpus/`, `parse.py`, `index.py`, `search.py`, `key.py`, `answer.py` and the two
vector caches with it. Nothing in them is edited. Set `OPENAI_API_KEY` in your environment.
Seven new programs, in this order, each importing only from the ones before it:

| Save as | What it does | Imports |
|---|---|---|
| `questions.py` | eighty questions, and which documents answer each | nothing |
| `run.py` | runs chapter 45's pipeline over one batch, and traces it | `answer`, `search`, `questions` |
| `notes.py` | my verdict on every answer, and one note per failure | `questions`, `answer` |
| `modes.py` | the grouping, the counts, and what the counts carry | `notes` |
| `checks.py` | a check per mode, and the code ones run over all eighty | `search`, `modes`, `notes`, `questions`, `run` |
| `judge.py` | two judges for one mode, in chapter 31's order | `answer`, `modes`, `notes`, `run` |
| `regress.py` | the set, one change to the system, three repeats | `answer`, `checks`, `modes`, `notes`, `run` |

> **Note:** What this lab costs before you run it, because it is the dearest in Part III and the
> arithmetic is worth seeing. Eighty answers is eighty chat calls and eighty query embeddings.
> The two judges are 480 calls — eighty cases, two judges, three showings each. The regression
> run is 480 more — eighty cases, two versions, three repeats. Just over a thousand calls, each
> one sending a few hundred tokens of passage and getting back a few dozen, which comes to a few
> pence on a small model. **The figure to watch is the product**, exactly as in chapter 41:
> cases times versions times repeats, multiplied again by however many judges you are comparing.
> Two hours, and more than half of it is reading rather than running.

> **Note:** The `text` blocks are one real run on 30 October 2026, and chapter 45's warning
> applies unchanged: your figures will differ in the last case or two. **What is stable is the
> structure of every finding here** — the failure rate near a fifth, the six modes, the tie at
> the top of the table, the judge far below its baseline, and the regression set's two blind
> spots. **What moves is which individual case lands where.** My own labels are the one thing in
> this chapter that is not reproducible at all: they are my reading, the chapter prints the rule
> I applied, and a second reader did disagree with me on one of the eighty, and the chapter says which.

## Step 1: Forty Answers, and the Questions That Produced Them

Chapter 30's method starts with real outputs. The pipeline from chapter 45 is the thing that
produces them, so the only thing missing is questions — and writing them is where the first
decision of the chapter sits.

```python
"""Eighty questions in two batches, and which documents hold each answer.

The questions were written against the corpus, so what every answer
SHOULD rest on is known before anything runs. `holds` is that: the
document ids carrying the answer, and an empty tuple where the corpus
does not answer the question at all. It is provenance and not an
answer string - chapter 41's exact-match key does not work here,
because these answers are prose and two different sentences can both
be right.

FIRST is forty questions spread across the corpus, written before any
output existed. SECOND is forty more, written AFTER reading the first
forty's answers, and aimed at the kinds of question that failed:
questions two documents answer between them, questions about two
near-duplicate policies, and questions asking what to do rather than
what a figure is. That aim is a bias and it is declared here, because
chapter 30 is explicit that a set selected by where the failures were
gives that selection's mode shares and not the application's.

A few questions the corpus cannot answer at all, and they are in the
set on purpose: an application that invents a figure does it when
there is no figure to find. The program prints which they are rather
than this docstring naming a count that an edit would falsify.
"""

#  question, the documents that hold the answer
FIRST = [
 ("How long do I have to return a standard item?",
  ("returns-standard", "how-to-start-a-return")),
 ("How long do I have to return a clearance item?",
  ("returns-clearance", "how-to-start-a-return")),
 ("How long do I have to return something I bought?",
  ("returns-standard", "returns-clearance", "how-to-start-a-return")),
 ("How long does a refund take?",
  ("refunds-policy", "where-is-my-refund", "refunds-faq")),
 ("Is a refund 14 days or 30 days?",
  ("refunds-policy", "where-is-my-refund", "refunds-faq")),
 ("What does standard delivery cost on a 20 pound order?",
  ("delivery-fees",)),
 ("What does standard delivery cost on a 20 pound order to an IV postcode?",
  ("delivery-fees", "delivery-exceptions")),
 ("What is the delivery surcharge for Northern Ireland?",
  ("delivery-exceptions",)),
 ("Can I have next-day delivery to the Isle of Man?",
  ("delivery-exceptions",)),
 ("How much is two-person delivery to the Isles of Scilly?",
  ("delivery-exceptions",)),
 ("Which postcodes carry the 14.00 pound surcharge?",
  ("delivery-exceptions",)),
 ("What is HL-2208?",
  ("product-kettle-hl-2208",)),
 ("How much does the HL-2208 kettle cost?",
  ()),
 ("What does the K mean at the end of HL-2208-K?",
  ("sku-conventions",)),
 ("What is the code for a replacement kettle filter, and what does it cost?",
  ("product-kettle-hl-2208",)),
 ("How wide are the slots on the toaster?",
  ("product-toaster-hl-2209",)),
 ("Is the kettle dishwasher safe?",
  ("product-kettle-hl-2208",)),
 ("What is the maximum bulb wattage for the floor lamp?",
  ("product-lamp-hl-3310",)),
 ("Does one dining chair need two-person delivery?",
  ("product-chair-hl-5512",)),
 ("What does Harbour Plus include?",
  ("plan-harbour-plus", "plan-comparison")),
 ("Does Harbour Plus include next-day delivery?",
  ("plan-harbour-plus", "plan-comparison")),
 ("Does Harbour Plus cover the Highlands surcharge?",
  ("plan-harbour-plus",)),
 ("How long is the warranty?",
  ("warranty-summary", "warranty-full")),
 ("You replace my item under warranty after eighteen months. "
  "How long is the replacement covered for?",
  ("warranty-full",)),
 ("How long is a repair itself covered for?",
  ("warranty-full",)),
 ("Is the kettle's limescale filter covered by the warranty?",
  ("warranty-full", "product-kettle-hl-2208")),
 ("Is the toaster's crumb tray a consumable part?",
  ("product-toaster-hl-2209",)),
 ("I use the kettle in a cafe. Is it covered?",
  ("warranty-full",)),
 ("My order arrived damaged. What do I do?",
  ("damaged-on-arrival",)),
 ("How long do I have to report cosmetic damage on delivery?",
  ("damaged-on-arrival", "warranty-full")),
 ("An item is missing from my parcel. How long do I have to tell you?",
  ("missing-item-in-a-parcel",)),
 ("You sent the wrong item. Do I pay the return postage?",
  ("wrong-item-sent",)),
 ("I am returning a gift. Can the money go to my own card?",
  ("gift-returns",)),
 ("My card is closed. Where does my refund go?",
  ("refund-to-a-closed-card", "refunds-policy")),
 ("How long does a bank transfer refund take?",
  ("refund-to-a-closed-card", "refunds-policy")),
 ("Can I cancel an order after it has been dispatched?",
  ("cancellations",)),
 ("How long is a return postage label valid for?",
  ("return-postage-labels",)),
 ("What is your VAT number?",
  ()),
 ("Do you deliver to Australia?",
  ("international-delivery",)),
 ("On what date did the 2026 surcharge schedule take effect?",
  ()),
]

SECOND = [
 ("Are the return rules the same for clearance items as for standard ones?",
  ("returns-standard", "returns-clearance")),
 ("Do I pay the postage to return a clearance item?",
  ("returns-clearance", "return-postage-labels")),
 ("Do I pay the postage to return a standard item?",
  ("returns-standard", "how-to-start-a-return")),
 ("What do I do to start a return?",
  ("how-to-start-a-return",)),
 ("Can I return something I have already assembled?",
  ("returns-standard", "returns-clearance")),
 ("Does opening the box count as using it?",
  ("returns-standard", "returns-clearance")),
 ("Will I get the delivery charge back if I return one item out of three?",
  ("refunds-policy", "refunds-faq")),
 ("When do the 14 days for my refund start?",
  ("refunds-policy", "where-is-my-refund")),
 ("My refund has not arrived after three weeks. What should I check?",
  ("where-is-my-refund",)),
 ("Is a goodwill payment a refund?",
  ("refunds-faq", "refunds-policy")),
 ("What is the most you will pay as goodwill?",
  ("refunds-policy",)),
 ("How long does delivery take to the Scottish Highlands?",
  ("delivery-exceptions", "delivery-time-estimates")),
 ("How long does standard delivery take?",
  ("delivery-fees", "delivery-time-estimates")),
 ("I ordered on Saturday. When will it be dispatched?",
  ("weekend-and-holiday-delivery", "delivery-time-estimates")),
 ("What is the cut-off time for next-day delivery?",
  ("delivery-fees", "opening-hours")),
 ("Is next-day delivery free with Harbour Plus?",
  ("plan-harbour-plus", "plan-comparison")),
 ("How many small orders a year make Harbour Plus worth buying?",
  ("plan-comparison",)),
 ("Can I use a matched price and Harbour Plus free delivery together?",
  ("price-matching", "plan-harbour-plus")),
 ("You lowered the price a week after I bought. Do I get the difference?",
  ("price-matching",)),
 ("Do you match a marketplace seller's price?",
  ("price-matching",)),
 ("Who delivers a next-day parcel?",
  ("shipping-partners",)),
 ("Who delivers a pallet?",
  ("shipping-partners",)),
 ("Can I choose which carrier delivers my parcel?",
  ("shipping-partners",)),
 ("Can you change the delivery address on my order?",
  ("changing-a-delivery-address",)),
 ("Does changing the delivery address change what I pay?",
  ("changing-a-delivery-address",)),
 ("What does Picking mean on my order?",
  ("how-to-track-an-order",)),
 ("My tracking has not moved for a day. What can you do about it?",
  ("how-to-track-an-order",)),
 ("What does Low stock mean?",
  ("stock-codes-and-statuses",)),
 ("What does Available to order mean, and how long does it take?",
  ("stock-codes-and-statuses",)),
 ("How long do you keep my order records?",
  ("data-and-privacy",)),
 ("Can you delete everything you hold about me?",
  ("data-and-privacy",)),
 ("Do you store my card number?",
  ("data-and-privacy", "updating-payment-details")),
 ("Why can I not edit the card saved on my account?",
  ("updating-payment-details",)),
 ("How long does a stage-two complaint take to answer?",
  ("complaints-process",)),
 ("Who replies to a stage-one complaint?",
  ("complaints-process",)),
 ("What hours can I telephone you?",
  ("contact-us", "opening-hours")),
 ("Can I return an online order to the shop on Harbour Lane?",
  ("opening-hours",)),
 ("How long is a password reset link valid for?",
  ("account-password-reset",)),
 ("I ordered as a guest. How do I track it?",
  ("how-to-track-an-order",)),
 ("What happens under the warranty if you have discontinued the item?",
  ("warranty-full",)),
]

BATCHES = {1: FIRST, 2: SECOND}


def cases(batch):
    """Case ids run c01.. in batch 1 and d01.. in batch 2, so a case
    id is unique across the eighty and says which batch it came from."""
    letter = "c" if batch == 1 else "d"
    return [(f"{letter}{i:02d}", q, h)
            for i, (q, h) in enumerate(BATCHES[batch], 1)]


def all_cases():
    return cases(1) + cases(2)


if __name__ == "__main__":
    import pathlib
    docs = pathlib.Path("corpus/docs")
    known = {p.stem for p in docs.glob("*.md")}
    bad = [(q, d) for _, q, h in all_cases() for d in h if d not in known]
    print(f"  {len(FIRST)} questions in batch 1,"
          f" {len(SECOND)} in batch 2\n")
    if bad:
        print(f"  {len(bad)} named a document that does not exist:")
        for q, d in bad:
            print(f"    {d!r} in {q[:44]!r}")
        raise SystemExit(1)
    print("  every document named exists in corpus/docs")

    for b in (1, 2):
        cs = cases(b)
        none = [c for c in cs if not c[2]]
        multi = [c for c in cs if len(c[2]) > 1]
        cited = {d for _, _, h in cs for d in h}
        print(f"\n  batch {b}")
        print(f"    {len(cs) - len(none)} the corpus answers,"
              f" {len(none)} it does not")
        print(f"    {len(multi)} need more than one document")
        print(f"    {len(cited)} of the {len(known)} documents hold an answer")
        if none:
            print("    the corpus answers none of these:")
            for cid, q, _ in none:
                print(f"      {cid}  {q[:50]}")

    both = {d for _, _, h in cases(1) for d in h} & \
           {d for _, _, h in cases(2) for d in h}
    everything = {d for _, _, h in all_cases() for d in h}
    print(f"\n  across the eighty: {len(everything)} of {len(known)}"
          f" documents hold an answer,")
    print(f"  {len(both)} of them in both batches")
```

```text
  40 questions in batch 1, 40 in batch 2

  every document named exists in corpus/docs

  batch 1
    37 the corpus answers, 3 it does not
    13 need more than one document
    25 of the 40 documents hold an answer
    the corpus answers none of these:
      c13  How much does the HL-2208 kettle cost?
      c38  What is your VAT number?
      c40  On what date did the 2026 surcharge schedule take 

  batch 2
    40 the corpus answers, 0 it does not
    16 need more than one document
    25 of the 40 documents hold an answer

  across the eighty: 38 of 40 documents hold an answer,
  12 of them in both batches
```

**The questions are written against the corpus, which is not the same as being written from the
answers.** Each one names the documents that hold its answer, and three of the first forty name
nothing at all, because the corpus does not answer them. That column is provenance rather than an
answer key: chapter 41's exact-match grader works on a figure and does not work here, since these
answers are prose and two different sentences can both be right.

**What it buys is the one thing an answer key would not.** Chapter 31's table files *the passages
do answer the question* under judgement, because in production nobody has written down what the
documents hold. Here I have, so the three refusals in the set can be checked without a judge —
and step 5 is where that distinction turns into a measurement rather than an observation.

**Thirteen of the forty need more than one document between them**, which is deliberate and is the
one place where the questions lean. Chapter 27's split answer and chapter 28's budget are both
about that case, and chapter 45 ended with two retrieval failures of exactly that shape.

> **Tip:** Write the `holds` column while you write the question, from the document, not
> afterwards from memory. The program checks that every document named exists, which catches a
> typo and nothing else; what it cannot check is whether the document really answers the
> question, and that is why the column is written at the moment you are looking at the document.

Then run the pipeline over them. Nothing in it changes: chapter 45's dense ranking over the same
176 chunks, chapter 45's fill-by-rank-and-stop under the same 2,500-character budget, and chapter
45's closing instruction word for word.

```python
"""Run the chapter 45 pipeline over a batch of questions, and trace it.

Nothing about the system changes here. The retrieval is chapter 45's
dense ranking over the same 176 chunks, the assembly is chapter 45's
fill-by-rank-and-stop under the same 2500-character budget, and the
instruction is the one chapter 45 ended on, word for word. This
program only asks it forty questions instead of eight and writes one
trace per request, with chapter 33's fields.

    python3 run.py 1      writes outputs-1.json
    python3 run.py 2      writes outputs-2.json

It writes each file once and reads it afterwards, because the answers
are the raw material of every step below and re-running them would
change the thing being analysed under you.
"""
import json
import pathlib
import sys
import time
import uuid

import answer
import search
from questions import cases


def path(batch):
    return pathlib.Path(f"outputs-{batch}.json")


def run(batch):
    cache = search.vectors()
    out = []
    for cid, q, holds in cases(batch):
        t0 = time.monotonic()
        order, scores = search.dense(q, cache)
        t1 = time.monotonic()
        kept, unreached, left = answer.build(q, order)
        d = answer.ask(answer.context(q, kept))
        t2 = time.monotonic()
        text = d["choices"][0]["message"]["content"]
        try:
            reply = json.loads(text)
        except json.JSONDecodeError:
            reply = {"answer": text, "citations": []}
        out.append({
            "request_id": uuid.uuid4().hex[:6],
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "case_id": cid,
            "question": q,
            "holds": list(holds),
            "retrieval_query": q,
            "candidates": [[c, round(scores[c], 4)] for c in order[:10]],
            "passages_sent": kept,
            "room_left": left,
            "model": d["model"],
            "prompt_tokens": d["usage"]["prompt_tokens"],
            "output_tokens": d["usage"]["completion_tokens"],
            "finish_reason": d["choices"][0]["finish_reason"],
            "answer": reply.get("answer", ""),
            "citations": reply.get("citations", []),
            "retrieval_ms": round((t1 - t0) * 1000, 1),
            "model_ms": round((t2 - t1) * 1000, 1),
            "total_ms": round((t2 - t0) * 1000, 1),
        })
        print(f"  {cid} {len(out):2d}/{len(cases(batch))}", flush=True)
    path(batch).write_text(json.dumps(out, indent=1))
    return out


def outputs(batch):
    p = path(batch)
    return json.loads(p.read_text()) if p.exists() else run(batch)


if __name__ == "__main__":
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ts = outputs(batch)
    sent = [len(t["passages_sent"]) for t in ts]
    tin = sum(t["prompt_tokens"] for t in ts)
    tout = sum(t["output_tokens"] for t in ts)
    print(f"\n  batch {batch}: {len(ts)} requests,"
          f" model {ts[0]['model']}")
    print(f"  {sum(sent)} passages sent in all,"
          f" {min(sent)} to {max(sent)} a request")
    print(f"  {tin} input tokens, {tout} output\n")

    show = ("c01", "c07", "c13", "c20") if batch == 1 else \
           ("d01", "d07", "d12", "d31")
    print("  Four whole answers, which is where the work starts:\n")
    for cid in show:
        t = next(x for x in ts if x["case_id"] == cid)
        q = t["question"]
        print(f"    {cid}  {q if len(q) <= 52 else q[:49] + '...'}")
        print(answer.wrap(t["answer"], "          ", "          "))
        for c in t["citations"]:
            print(f"          cites {c.get('id')}")
        print(f"          holds: {', '.join(t['holds']) or '(nothing)'}")
        print()
    print("  Reading four is not reading forty, and the next step")
    print("  is the forty. There is no shortcut and no program that")
    print("  does it for you.")
```

```text

  batch 1: 40 requests, model gpt-4o-mini-2024-07-18
  266 passages sent in all, 3 to 11 a request
  24054 input tokens, 2250 output

  Four whole answers, which is where the work starts:

    c01  How long do I have to return a standard item?
          You may return a standard item within 30 days of
          delivery
          cites returns-standard#1
          holds: returns-standard, how-to-start-a-return

    c07  What does standard delivery cost on a 20 pound or...
          Standard delivery is 3.99 pounds on orders under 40
          pounds.
          cites delivery-fees#1
          holds: delivery-fees, delivery-exceptions

    c13  How much does the HL-2208 kettle cost?
          The price of the HL-2208 kettle is not mentioned in
          the passages.
          holds: (nothing)

    c20  What does Harbour Plus include?
          Harbour Plus costs 29 pounds a year and includes:
          cites plan-harbour-plus#1
          holds: plan-harbour-plus, plan-comparison

  Reading four is not reading forty, and the next step
  is the forty. There is no shortcut and no program that
  does it for you.
```

**One trace per request, with chapter 33's fields**, which is what makes the rest of the chapter
possible. Chapter 33's trace section ends on the content decision: drop the four content fields
and five of eight questions survive, and the three that do not are the ones needing the text. The
three it loses are exactly what an error analysis is: *why did it say that*, *is this the same
failure as yesterday's*, and *can this become a regression case*. This lab keeps the content,
which is the choice that makes it a lab and would be a decision with a deletion window attached
in production.

**The four answers printed are chosen and not sampled, and that is the point of printing them.**
One is right, one is a correct refusal of a question the corpus cannot answer, and two are
failures you can see without thinking about them. `c07` is asked about an IV postcode, the
passage with the 9.50 surcharge in it was sent, and the answer gives the base charge alone.
`c20`'s answer ends at a colon: the list it was introducing is not there. Neither needs a metric
and neither would be visible in one. Reading four is not reading forty.
## Step 2: Read All Forty, and Write One Note on Each Failure

This is chapter 30's steps 1 and 2 and there is no program in it. Open the forty answers beside
their questions and the passages each was given, decide pass or fail, and write one line on every
failure in your own words — [**before**]{.noindex} you have any categories, because the categories you start
with are the ones you already believe in.

It takes about fifty minutes. The output is a file with my verdicts in it and nothing else.

```python
"""My verdict on all eighty answers, and one note on each failure.

This is chapter 30's steps 1 and 2 and there is no program in it. I
read every one of the eighty answers beside its question and the
passages it was given, decided pass or fail, and wrote one line on
each failure in my own words before I had any categories. The notes
are untidy for that reason and the untidiness is the discipline: a
category written first is a category I already believed in.

The rule I applied, written down so that somebody else could apply
the same one: a case FAILS if a customer acting on the answer would
be misinformed, or if the answer does not contain what was asked, or
if the citation does not let the customer check it. Some of these
verdicts can be argued the other way; the program lists those, in
both directions, and names no count here that a changed label would
falsify.

FAIL is the verdict. The note is the evidence for it.
"""

NOTES = {
 "c03": "asked generally how long to return something and got only the"
        " standard 30 days; the clearance passage saying 14 was sent",
 "c05": "asked which of two figures is right and got one of them, with"
        " no mention that the other passage says 30",
 "c07": "gave the base delivery charge and ignored the 9.50 surcharge"
        " for IV, which was in the passages",
 "c09": "right answer, but the quote is attached to the PDF and the"
        " sentence is in delivery-exceptions",
 "c20": "the answer ends at a colon; the list it was introducing is"
        " missing",
 "c22": "right answer, cited a passage that says a surcharge exists"
        " rather than one saying the plan excludes it",
 "c24": "asked how long a replacement is covered for and got the rule;"
        " the passage gives six months for exactly eighteen",
 "c29": "asked what to do and was told what not to do; the 48-hour"
        " report was in the passages",
 "d01": "right answer, cited a document that was not even sent, and"
        " the quote is from how-to-start-a-return",
 "d04": "told me a prepaid label is issued, which is the clearance"
        " policy's own section 3 and its section 4 says the opposite",
 "d05": "asked whether an assembled item can go back and got the"
        " condition-on-arrival rule instead",
 "d07": "right answer, the quote belongs to refunds-policy and was"
        " cited to refunds-faq",
 "d08": "said the 14 days start when the goods arrive; the policy says"
        " from when the warehouse books them in, and another passage"
        " says that is two or three days later",
 "d09": "right answer, the quote drops a sentence from the middle of"
        " the passage with no ellipsis",
 "d16": "asked whether next-day is free on the plan and got the"
        " standard 7.99 price",
 "d26": "the citation id is '#3' with no document name at all",
 "d33": "answered why a card cannot be removed; I asked why it cannot"
        " be edited, and both are in the same passage",
}

#  The labels I would argue about with a second reader, and why.
#  Chapter 30's lab makes this point with its own note 13: a partition
#  check cannot tell you the grouping is right, and the protection is
#  a written criterion or a second person. Some are failures I would
#  defend and could lose; at least one is a PASS I could lose, which
#  is the direction that is easy to forget to look for - every verdict
#  rule has a boundary and it cuts both ways. The program sorts them
#  into the two directions and counts each.
ARGUABLE = {
 "d09": "the citation names the right passage and the quote is a fair"
        " abridgement of it. It fails my rule because a quote that is"
        " not in the passage cannot be checked against it, and that"
        " is what a citation is for. A reader who scored this a pass"
        " would have sixteen failures and one fewer mode member",
 "d05": "'may be refused and sent back at your cost' does point the"
        " right way. It fails my rule because the sentence that says"
        " assembled counts as used was never in the passages, so the"
        " answer does not contain what was asked",
 "c04": "I scored this a PASS and a second reader scored it a"
        " FAIL, which makes it the one label the two readings"
        " disagree on. The case against me is strong: c04 and c05"
        " were given the SAME answer with the SAME citation, I"
        " failed c05, and c04's question is the more open of the"
        " two. The reason I hold the pass is that the verdict is of"
        " an answer relative to its question - c05 asks which of"
        " two figures is right, so one figure and no mention of the"
        " other fails the question asked; c04 asks how long a"
        " refund takes, and the governing policy's own figure,"
        " cited to the policy, answers it. Scored a fail it joins"
        " *Answers for one case when two apply* and the top three"
        " become 5, 5 and 5",
 "c33": "I scored this a PASS and would defend it weakly. The asker"
        " is the gift's recipient and asks about their own card; the"
        " answer is phrased about the BUYER's card and says the"
        " refund goes to the recipient as credit. The information is"
        " there and the pronouns are not. A reader who failed it"
        " would have eighteen failures and a seventh mode",
}


#  The second reading, which chapter 30's lab asks for in as many
#  words: "the protection against getting it wrong is a second person
#  reading the same notes, or a written criterion for each mode that
#  a note can be tested against". This chapter has both. A second
#  reader was given the eighty answers, their questions, the passages
#  each was sent, the corpus, and the verdict rule above - and not my
#  labels - and read all eighty.
SECOND_READING_DISAGREES = ["c04"]


def verdicts(cases):
    """fail where there is a note, pass everywhere else."""
    return {cid: ("F" if cid in NOTES else "P") for cid, _, _ in cases}


if __name__ == "__main__":
    import sys

    import answer
    import questions
    # `python3 notes.py 1` after the first forty; no argument once
    # both batches have been read.
    only = int(sys.argv[1]) if len(sys.argv) > 1 else None
    cs = questions.cases(only) if only else questions.all_cases()
    v = verdicts(cs)
    byq = {cid: q for cid, q, _ in cs}
    fails = [c for c in v if v[c] == "F"]
    if not only:
        unknown = [c for c in NOTES if c not in byq]
        assert not unknown, unknown

    for b, letter in ((1, "c"), (2, "d")):
        n = [c for c in fails if c.startswith(letter)]
        total = sum(1 for c in v if c.startswith(letter))
        if total:
            print(f"  batch {b}: {len(n)} failures in {total} answers"
                  f"   {len(n)/total:.0%}")
    print(f"\n  {len(fails)} failures in {len(v)} answers"
          f"   {len(fails)/len(v):.0%}\n")
    print("  Every note, in the order I wrote them:\n")
    for cid in sorted(fails):
        q = byq[cid]
        q = q if len(q) <= 52 else q[:49] + "..."
        print(f"    {cid}  {q}")
        print(answer.wrap(NOTES[cid], "          ", "          ", 62))
    arg = [c for c in ARGUABLE if c in byq]
    asfail = [c for c in arg if c in fails]
    aspass = [c for c in arg if c not in fails]
    agree = len(v) - len([c for c in SECOND_READING_DISAGREES
                          if c in byq])
    print(f"\n  A second reader, given the same {len(v)} answers,"
          f" the")
    print(f"  same passages and the rule above but not my labels,")
    print(f"  agreed on {agree} of {len(v)} and disagreed on"
          f" {len(v) - agree}:")
    for c in SECOND_READING_DISAGREES:
        if c in byq:
            print(f"    {c}  I said {v[c]}, the second reader said"
                  f" {'F' if v[c] == 'P' else 'P'}")
    print()
    plural = "label" if len(arg) == 1 else "labels"
    print(f"  {len(arg)} {plural} I would argue about with a second"
          f" reader:")
    print(f"    {len(asfail)} failures I might lose:"
          f" {', '.join(sorted(asfail)) or '(none)'}")
    noun = "pass" if len(aspass) == 1 else "passes"
    print(f"    {len(aspass)} {noun} I might lose:"
          f" {', '.join(sorted(aspass)) or '(none)'}")
    print("  There is no structure above this line and that is")
    print("  correct: the notes come first and the categories come")
    print("  out of them.")
```

```text
  batch 1: 8 failures in 40 answers   20%

  8 failures in 40 answers   20%

  Every note, in the order I wrote them:

    c03  How long do I have to return something I bought?
          asked generally how long to return something and
          got only the standard 30 days; the clearance
          passage saying 14 was sent
    c05  Is a refund 14 days or 30 days?
          asked which of two figures is right and got one of
          them, with no mention that the other passage says
          30
    c07  What does standard delivery cost on a 20 pound or...
          gave the base delivery charge and ignored the 9.50
          surcharge for IV, which was in the passages
    c09  Can I have next-day delivery to the Isle of Man?
          right answer, but the quote is attached to the PDF
          and the sentence is in delivery-exceptions
    c20  What does Harbour Plus include?
          the answer ends at a colon; the list it was
          introducing is missing
    c22  Does Harbour Plus cover the Highlands surcharge?
          right answer, cited a passage that says a surcharge
          exists rather than one saying the plan excludes it
    c24  You replace my item under warranty after eighteen...
          asked how long a replacement is covered for and got
          the rule; the passage gives six months for exactly
          eighteen
    c29  My order arrived damaged. What do I do?
          asked what to do and was told what not to do; the
          48-hour report was in the passages

  A second reader, given the same 40 answers, the
  same passages and the rule above but not my labels,
  agreed on 39 of 40 and disagreed on 1:
    c04  I said P, the second reader said F

  2 labels I would argue about with a second reader:
    0 failures I might lose: (none)
    2 passes I might lose: c04, c33
  There is no structure above this line and that is
  correct: the notes come first and the categories come
  out of them.
```

**Eight failures in forty answers, and the eight are the chapter's first finding.** The problem
statement says *forty real outputs*, and chapter 30's method asks for about forty *failures* —
"enough that a real pattern repeats and few enough to read in an afternoon". Those are not the
same quantity and the difference is the failure rate. **At this batch's rate of one in five,
forty failures is two hundred answers read** — step 4 recomputes it off all eighty and gets a
hundred and ninety. The afternoon chapter 30 prices the method at is an afternoon per forty
*failures*, and not per forty outputs.

**The rule for what counts as a failure is written down in the program, above the notes.** A case
fails if a customer acting on the answer would be misinformed, or if the answer does not contain
what was asked, or if the citation does not let the customer check it. That statement is the
**verdict rule**: what counts as a failure, fixed before any labelling and kept beside the labels
for ever after. Writing it is what lets a second reader reproduce these labels — chapter 30's lab
asks for exactly this, "a written criterion for each mode that a note can be tested against", and
this is the same thing one level up, at the verdict rather than the mode.

**And it is the rule chapter 33's criteria drift is about.** Criteria drift is this rule moving
while nobody is looking at it. Written down and dated, a flip count against it is a measurement;
unwritten, there is nothing for the second reading to disagree with.

> **Warning:** Two of the eight notes begin *right answer* — `c09` and `c22` — and three more do
> on the second forty. Five of the seventeen failures are answers a customer would act on
> correctly, failing on the citation alone.
> If your verdict rule only asks whether the answer was right, those cases are passes and the
> largest mode in this chapter does not exist. **What you count as a failure decides what modes
> you can find**, and that decision is made before any grouping, which is why it belongs in
> writing beside the labels rather than in your head.

**And one of the seventeen is a defect in the documents as well as in the answer, which is a
thing an error analysis finds and a metric never does.** Case `d04` asks what to do to start a
return and is told, among other correct things, that a prepaid postage label is issued. That is
false for a clearance item — and one of the reasons it is false is that the *document* says it. The clearance returns policy's section 3 promises
a return reference and a prepaid label; its section 4 says return postage on a clearance item is
paid by the customer and [**no label is issued**]{.noindex}. Section 3 is a verbatim copy of the standard
policy's section 3, where both halves are true, and the clause was never adjusted when the two
policies were made near-duplicates of each other. The third document in that territory, the one
about postage labels, sides with section 4.

**And then the part that stops this being an excuse.** The document about postage labels was one
of the nine passages sent, and the sentence it carries is *"Clearance items do not get a label,
because return postage on clearance is paid by the customer."* The answer had what it needed to
resolve the contradiction in front of it and took the other side. So **two things are wrong at
once** — the source contradicts itself, and the answer picked the half that no other passage
supports — and the verdict rule makes it a failure for the second reason as much as the first. Its
mode is *Answers for one case when two apply*, which is the right place for it: the question spans
two policies, two of the passages sent disagree, and the answer stopped at one.

Chapter 32's corpus holds two documents that disagree about a figure on purpose. This is one
document disagreeing with itself by accident, which nothing in `labs/corpus/verify.py` tests for
and nothing in its README declares — and **the only way anybody was going to find it was by
reading eighty answers.** That is worth more than the case it cost: an error analysis audits the
documents as well as the system, and it is the only thing in this chapter that does.

> **Note:** This is also the hazard chapter 33 names in its trace section from the other side — *a
> code check comparing an answer against your documents changes verdict when the documents change,
> silently*. Here the documents did not change; they were inconsistent to begin with, which the
> check cannot see either. **A measurement over your own documents inherits every defect in them**,
> and no amount of care about the measurement reaches a wrong sentence in the source.

**And the written rule is what let somebody else apply it.** Chapter 30's lab says the
protection against getting a label wrong is a second person reading the same material, or a
written criterion a case can be tested against. This chapter has both: a second reader was given
the eighty answers, their questions, the passages each was sent, the corpus and the rule — and
not my labels — and read all eighty. **We agree on 79 and disagree on one.**

The one is `c04`, *how long does a refund take*, which I scored a pass and the second reader
scored a failure. The case against me is strong and the program prints it: `c04` and `c05` were
given the **same answer with the same citation**, I failed `c05`, and `c04`'s question is the
more open of the two. The reason I hold the pass is that a verdict is of an answer *relative to
its question* — `c05` asks which of two figures is right, so one figure and no mention of the
other fails the question asked, while `c04` asks how long a refund takes and the governing
policy's own figure, cited to the policy, answers it. **Step 4 computes what it would cost to be
wrong about that**, and the answer is the chapter's headline result.

> **Note:** Four labels are flagged as arguable and they run in both directions — two failures I
> might lose and two passes I might lose. `c33` is the clearest of the second kind: the asker is
> a gift's recipient asking about their own card, and the answer is phrased about the buyer's.
> The information is there and the pronouns are not. **Every verdict rule has a boundary and it
> cuts both ways**, and a list of arguable cases that all runs one way is a list somebody stopped
> reading halfway.

> **Tip:** Keep the notes untidy. Mine say things like *asked what to do and was told what not to
> do*, which is not a category and is not trying to be. The moment a note is written in the
> vocabulary of a category, it has stopped being evidence about an output and become a vote for a
> grouping you have not made yet.

## Step 3: Eight Failures Will Not Group. Read Forty More.

Try to group eight failures and the problem is immediate: most of the groups have one member. A
group of one is a **singleton mode** — a named kind resting on a single failure, which is a guess
about a kind rather than an established one. It may be the first of a dozen or the only one there
will ever be, and nothing about the eight tells you which; the only way to find out is to read
more output.

So write forty more questions and run the same system over them. The second forty go where the
first forty's failures were — questions two documents answer between them, questions about the
two near-duplicate return policies, and questions asking what to do rather than what a figure is.
**That aim is a bias and it has to be declared**, because chapter 30 is explicit that a set
selected by where the failures were gives that selection's shares rather than the application's.
Both lists are in `questions.py`; `run.py 2` runs the second.

```text

  batch 2: 40 requests, model gpt-4o-mini-2024-07-18
  338 passages sent in all, 5 to 12 a request
  22561 input tokens, 2506 output

  Four whole answers, which is where the work starts:

    d01  Are the return rules the same for clearance items...
          No, the return rules are not the same for clearance
          items as for standard ones.
          cites returns-clearance#3
          cites returns-standard#1
          holds: returns-standard, returns-clearance

    d07  Will I get the delivery charge back if I return o...
          Returning one item from an order of several does
          not refund the delivery charge.
          cites refunds-faq#2
          holds: refunds-policy, refunds-faq

    d12  How long does delivery take to the Scottish Highl...
          5 to 7 working days
          cites delivery-time-estimates#2
          holds: delivery-exceptions, delivery-time-estimates

    d31  Can you delete everything you hold about me?
          Deletion cannot remove the order records we are
          required to keep; everything else goes.
          cites data-and-privacy#4
          holds: data-and-privacy

  Reading four is not reading forty, and the next step
  is the forty. There is no shortcut and no program that
  does it for you.
```

```text
  batch 1: 8 failures in 40 answers   20%
  batch 2: 9 failures in 40 answers   22%

  17 failures in 80 answers   21%

  Every note, in the order I wrote them:

    c03  How long do I have to return something I bought?
          asked generally how long to return something and
          got only the standard 30 days; the clearance
          passage saying 14 was sent
    c05  Is a refund 14 days or 30 days?
          asked which of two figures is right and got one of
          them, with no mention that the other passage says
          30
    c07  What does standard delivery cost on a 20 pound or...
          gave the base delivery charge and ignored the 9.50
          surcharge for IV, which was in the passages
    c09  Can I have next-day delivery to the Isle of Man?
          right answer, but the quote is attached to the PDF
          and the sentence is in delivery-exceptions
    c20  What does Harbour Plus include?
          the answer ends at a colon; the list it was
          introducing is missing
    c22  Does Harbour Plus cover the Highlands surcharge?
          right answer, cited a passage that says a surcharge
          exists rather than one saying the plan excludes it
    c24  You replace my item under warranty after eighteen...
          asked how long a replacement is covered for and got
          the rule; the passage gives six months for exactly
          eighteen
    c29  My order arrived damaged. What do I do?
          asked what to do and was told what not to do; the
          48-hour report was in the passages
    d01  Are the return rules the same for clearance items...
          right answer, cited a document that was not even
          sent, and the quote is from how-to-start-a-return
    d04  What do I do to start a return?
          told me a prepaid label is issued, which is the
          clearance policy's own section 3 and its section 4
          says the opposite
    d05  Can I return something I have already assembled?
          asked whether an assembled item can go back and got
          the condition-on-arrival rule instead
    d07  Will I get the delivery charge back if I return o...
          right answer, the quote belongs to refunds-policy
          and was cited to refunds-faq
    d08  When do the 14 days for my refund start?
          said the 14 days start when the goods arrive; the
          policy says from when the warehouse books them in,
          and another passage says that is two or three days
          later
    d09  My refund has not arrived after three weeks. What...
          right answer, the quote drops a sentence from the
          middle of the passage with no ellipsis
    d16  Is next-day delivery free with Harbour Plus?
          asked whether next-day is free on the plan and got
          the standard 7.99 price
    d26  What does Picking mean on my order?
          the citation id is '#3' with no document name at
          all
    d33  Why can I not edit the card saved on my account?
          answered why a card cannot be removed; I asked why
          it cannot be edited, and both are in the same
          passage

  A second reader, given the same 80 answers, the
  same passages and the rule above but not my labels,
  agreed on 79 of 80 and disagreed on 1:
    c04  I said P, the second reader said F

  4 labels I would argue about with a second reader:
    2 failures I might lose: d05, d09
    2 passes I might lose: c04, c33
  There is no structure above this line and that is
  correct: the notes come first and the categories come
  out of them.
```

**Seventeen failures in eighty answers, and the aim bought one failure.** Eight in the first
forty, nine in the second — a rate of 20 per cent against 22 per cent, which on forty cases each
is well inside the noise. **So the bias I was careful to declare did not show up in the rate.** Writing questions at the
kinds of thing that had failed produced one more failure than spreading them across the corpus
did, and one failure in forty is nothing. The honest reading is that **these two batches cannot
tell you whether the aim worked**: it may have worked a little, or not at all, and nothing here
separates those. What the declaration buys is that the question is open rather than unasked.

**What the second forty did buy is members.** Three of the first forty's five modes rested on a
single answer. Step 4's table has the counts, and the short version is that one of those three
became a group of five, and two of them are still groups of one at eighty.

> **Note:** The second forty is written after reading the first forty's answers, which is the
> move chapter 20 warns about when it is done to a *case set* mid-comparison — change the set and
> you have stopped measuring. What makes it legitimate here is that nothing is being compared
> yet. There is no score in this chapter until step 7, and the set is fixed before it. If you
> have already published a figure on the first forty, adding forty more is a new figure and not
> an improvement to the old one.

> **Warning:** Eighty answers is not a large set and this chapter never pretends it is. What it
> is, is eighty answers somebody actually read, which is more than most applications have. The
> figures below are honest about resting on seventeen failures, and every one of them says so
> with its denominator printed beside it.
## Step 4: Name the Modes, Count Them, and Ask What the Counts Carry

Now chapter 30's step 3. A person groups the notes; the program counts them, checks that the
grouping is a partition, and then asks the question chapter 30's table invites and does not
answer — whether the counts support an order.

```python
"""Grouping the notes into named failure modes, and counting them.

A PERSON did the grouping, after reading every answer. The program
counts, checks the partition, and then asks the question chapter 30's
table invites and does not answer: can the counts be put in an order
at all? Chapter 20's resampling answers it, and the answer is the
reason this chapter does not stop at a table.

Every mode is named after what the answer did, never after the stage
of the pipeline suspected of causing it. Two pairs are close enough
that the naming had to be decided rather than fallen into, and the
comments say what the distinction is.
"""
import random

from notes import ARGUABLE, NOTES

# mode -> the cases a person put in it, after reading all eighty
MODE = {
 # the quote cannot be found where the citation says it is: a
 # different document, no document, or text the passage does not
 # contain. All five are checkable without reading the answer.
 "Citation points somewhere else":
     ["c09", "d01", "d07", "d09", "d26"],
 # the answer is about something adjacent to the question. It is a
 # sentence from the passages and it is not the one asked for.
 "Answers a neighbouring question":
     ["c24", "c29", "d05", "d16", "d33"],
 # the question spans two policies or two documents and the answer
 # takes one of them and stops. Distinct from the mode above: here
 # the sentence given IS one of the right ones.
 "Answers for one case when two apply":
     ["c03", "c05", "c07", "d04"],
 "Not an answer at all":
     ["c20"],
 # the quote is real, in a document that was sent, and does not
 # establish the sentence it is attached to. Distinct from the first
 # mode: nothing mechanical can tell this one from a good citation.
 "Citation does not support the claim":
     ["c22"],
 "Contradicts the passage":
     ["d08"],
}

#  Every label notes.py flags as arguable, written out as the move it
#  would be: (case, the mode it is in now, the mode it would be in).
#  None on the right means scored a pass and so in no mode; None on
#  the left means I scored it a pass, so a failure verdict puts it
#  somewhere. "(its own)" is a mode no other failure here would join,
#  which is what notes.py says about c33.
#
#  The list is the four from notes.ARGUABLE and nothing else. An
#  earlier version of this block held a label that is NOT arguable and
#  left out one that is, and the conclusion reversed when that was
#  corrected - so the assertion below is checked against ARGUABLE
#  rather than trusted.
WHAT_IF = [
 ("d09", "Citation points somewhere else", None),
 ("d05", "Answers a neighbouring question", None),
 ("c04", None, "Answers for one case when two apply"),
 ("c33", None, "(its own)"),
]

RESAMPLES = 10_000
SEED = 46
# The three modes with more than one failure in them, which is the
# split a person would draw by eye. Named here so the program can
# test the split rather than assert it.
LARGE = ["Citation points somewhere else",
         "Answers a neighbouring question",
         "Answers for one case when two apply"]


def counts():
    return sorted(((len(v), k) for k, v in MODE.items()), reverse=True)


def shares(sample):
    where = {c: m for m, cs in MODE.items() for c in cs}
    out = {m: 0 for m in MODE}
    for c in sample:
        out[where[c]] += 1
    return out


def resample(n, rounds=RESAMPLES, seed=SEED):
    """Chapter 20's procedure, resampling FAILURES. Its assumption,
    stated because it is doing all the work here: that these
    seventeen are a sample of the failures, so the shares are the
    shares of whatever they are a sample of.

    Three questions, because the table invites three claims: is the
    first mode bigger than the second; is the third bigger than the
    biggest of the rest; and are the three I call large the three
    largest."""
    r = random.Random(seed)
    pool = [c for cs in MODE.values() for c in cs]
    small = [m for m in MODE if m not in LARGE]
    tie, edge, same = [], [], 0
    for _ in range(rounds):
        s = [pool[r.randrange(len(pool))] for _ in range(n)]
        sh = shares(s)
        tie.append((sh[LARGE[0]] - sh[LARGE[1]]) / n)
        edge.append((sh[LARGE[2]] - max(sh[m] for m in small)) / n)
        top3 = {m for m, _ in sorted(sh.items(),
                                     key=lambda kv: -kv[1])[:3]}
        same += top3 == set(LARGE)
    tie.sort()
    edge.sort()
    lo = int(0.025 * rounds)
    hi = int(0.975 * rounds)
    return (tie[lo], tie[hi]), (edge[lo], edge[hi]), same / rounds


if __name__ == "__main__":
    assigned = sorted(c for v in MODE.values() for c in v)
    print(f"  {len(assigned)} notes assigned to {len(MODE)} modes")
    print(f"  every note used exactly once? "
          f"{assigned == sorted(NOTES)}\n")

    total = len(assigned)
    running = 0
    print("  mode                                   n   share  running")
    for n, name in counts():
        running += n
        print(f"  {name:36s} {n:2d}  {n/total:5.0%}   {running/total:5.0%}")

    a, b = len(MODE[LARGE[0]]), len(MODE[LARGE[1]])
    print(f"\n  Chapter 30 stops at that table and works the largest")
    print(f"  mode. Read the first two rows before doing that: {a}")
    print(f"  and {b}.")
    if a == b:
        print("  They are the same number, so which of them the table")
        print("  prints first is the sort order and nothing else.\n")
    else:
        print(f"  They differ by {abs(a - b)}, which the resampling below")
        print("  is about: a difference is not yet an order.\n")
    print("  So ask what the counts can carry, with chapter 20's")
    print("  resampling over the failures:\n")

    print("    failures  first two       third vs rest   same top 3")
    for n in (total, 40, 100, 300):
        (tlo, thi), (elo, ehi), same = resample(n)
        tag = " <- mine" if n == total else ""
        print(f"    {n:^8d} {tlo:+.3f} to {thi:+.3f}  "
              f"{elo:+.2f} to {ehi:+.2f}  {same:6.2%}{tag}")

    sizes = [total, 40, 100, 300]
    zeroed = [n for n in sizes
              if resample(n)[0][0] <= 0 <= resample(n)[0][1]]
    print(f"\n  The first column contains zero at {len(zeroed)} of the"
          f" {len(sizes)} sizes")
    print(f"  ({', '.join(str(n) for n in zeroed)}), and only gets")
    print("  narrower. Read that as what it is: the resample draws")
    print(f"  from these failures, in which the two modes hold {a}")
    print(f"  and {b}, so what it narrows is a statement about that")
    print("  pair and not about the application. What more")
    print("  failures buys is the SECOND column - and read its")
    print("  low bound rather than its sign. The third mode's gap")
    print("  over the small ones, by size:")
    for n in sizes:
        (_, _), (elo, _), _ = resample(n)
        where = ("below zero" if elo < 0
                 else "at zero" if elo == 0 else "above zero")
        print(f"    {n:5d} failures   low end {elo:+.3f}   {where}")
    print()
    print("  And the last column is the one claim the seventeen")
    print("  come close to supporting: the three modes I call large")
    print(f"  come out as the three largest in"
          f" {resample(total)[2]:.0%} of resamples,")
    print("  which is a statement about a GROUP and still not an")
    print("  order inside it.\n")

    rate = total / 80
    print(f"  What the next size up costs, at {total} failures in")
    print("  every 80 answers:")
    for want in (40, 100):
        print(f"    {want:3d} failures needs about"
              f" {round(want / rate / 10) * 10} answers read")
    print("\n  That is the bill chapter 31 names when it says to")
    print("  label failures rather than cases, arriving one step")
    print("  earlier than expected: it is already due here, before")
    print("  any judge exists.\n")

    print("  One cell of that table does not hold still, and it is")
    print("  worth printing rather than hiding. Chapter 31's lab")
    print("  says a resampled interval should be stable at ten")
    print("  thousand rounds, and that an unstable one means too few")
    print("  rounds or far too few labels. Both halves are testable")
    print("  and the first one settles it.\n")
    seeds = 60
    high = {}
    print(f"    rounds    how the high end falls over {seeds} seeds")
    for rounds in (RESAMPLES, 5 * RESAMPLES, 20 * RESAMPLES):
        vals = {}
        for s in range(1, seeds + 1):
            (_, _), (elo, ehi), _ = resample(total, rounds=rounds, seed=s)
            vals.setdefault(round(ehi, 4), []).append(s)
        high[rounds] = vals
        shown = ", ".join(f"{k:+.3f} on {len(v)}"
                          for k, v in sorted(vals.items()))
        print(f"    {rounds:7d}   {shown}")
    worst = max(high[RESAMPLES], key=lambda k: len(high[RESAMPLES][k]))
    other = [k for k in high[RESAMPLES] if k != worst]
    print(f"\n  The two values are {worst:+.4f} and"
          f" {other[0]:+.4f}, which are")
    print(f"  {round(worst * total)} of {total} and {round(other[0] * total)}"
          f" of {total}: the high end is a DISCRETE")
    print("  quantile, and at ten thousand rounds the 97.5th")
    print("  percentile lands either side of that boundary")
    print("  depending on the seed. More rounds pushes almost every")
    print("  seed onto one side - and read the table rather than")
    print("  the sentence, because at five times the rounds it is")
    print(f"  still {len(high[5 * RESAMPLES].get(other[0], []))}"
          f" seeds of {seeds} and not none.\n")
    print("  So this cell is chapter 31's FIRST reason, too few")
    print("  rounds, and not its second. The reason that matters is")
    print("  that the figure the argument above rests on is the LOW")
    print("  end, and that one is the same on every one of the")
    print(f"  {seeds} seeds at every round count in the table.\n")

    print("  What the first forty on their own would have given,")
    print("  which is the argument for having read the second:\n")
    print("    mode                                 first 40   all 80")
    for _, name in counts():
        one = [c for c in MODE[name] if c.startswith("c")]
        print(f"    {name:36s} {len(one):6d} {len(MODE[name]):8d}")
    firstonly = [m for m in MODE
                 if any(c.startswith("c") for c in MODE[m])]
    singles = [m for m in firstonly
               if len([c for c in MODE[m] if c.startswith("c")]) == 1]
    grew = [m for m in singles if len(MODE[m]) > 1]
    one40 = max(MODE, key=lambda m: len([c for c in MODE[m]
                                         if c.startswith("c")]))
    rank = [k for _, k in counts()].index(one40) + 1
    print(f"\n  And the mode the first forty called largest,")
    print(f"  {one40!r},")
    ordinal = {1: "first", 2: "second", 3: "third", 4: "fourth",
               5: "fifth", 6: "sixth"}[rank]
    print(f"  comes {ordinal} on the eighty. Working the largest mode")
    print("  after forty answers would have been working that one.\n")
    print(f"  {len(firstonly)} modes, not {len(MODE)}, and {len(singles)} of them"
          f" resting on a")
    print(f"  single answer. {len(grew)} of those {len(singles)} became a group once")
    print(f"  the second forty was read and {len(singles) - len(grew)} did not."
          f" A mode with")
    print("  one example in it is a guess about a kind, and the")
    print("  only way to find out is to read more output.\n")

    where = {c: m for m, cs in MODE.items() for c in cs}
    inside = [c for c in ARGUABLE if c in where]
    outside = [c for c in ARGUABLE if c not in where]
    flagged = sorted(c for c, _, _ in WHAT_IF)
    assert flagged == sorted(ARGUABLE), (flagged, sorted(ARGUABLE))
    print("  And the result that table carries - the names and not")
    print(f"  the order - is one judgement call from changing."
          f" All {len(WHAT_IF)}")
    print("  rows below are the labels notes.py flags as arguable,")
    print("  and the assert above is what keeps them that list:\n")
    winners = []
    for cid, src, dst in WHAT_IF:
        counts = {m: len(cs) for m, cs in MODE.items()}
        if src:
            counts[src] -= 1
        if dst and dst in counts:
            counts[dst] += 1
        elif dst:
            counts[dst] = 1
        top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
        shape = ", ".join(str(v) for _, v in top)
        tied = top[0][1] == top[1][1]
        winners.append(None if tied else top[0][0])
        move = ("scored a pass" if dst is None
                else "scored a fail" if src is None
                else "moved one mode over")
        print(f"    {cid} {move}: top three become {shape},")
        if src is None:
            print(f"        into {dst}")
        print(f"        {'still tied at the top' if tied else 'an ORDER'}")
        if not tied:
            print(f"        and it is {top[0][0]!r}")
    ordered = [w for w in winners if w]
    print(f"\n  {len(winners) - len(ordered)} of the {len(winners)} leave a tie"
          f" and {len(ordered)} produce an order.")
    if len(set(ordered)) == len(ordered) > 1:
        print("  And the orders name DIFFERENT modes:")
        for w in ordered:
            print(f"    {w}")
        print("  so not even the direction survives one reading. The")
        print("  table gives six names and nothing about their order,")
        print("  and that is not a caveat on the finding - it is the")
        print("  finding.\n")
    elif len(set(ordered)) == 1:
        print(f"  Both orders name {ordered[0]!r}, so the shape is")
        print("  one reading away from changing while the direction")
        print("  holds - a hypothesis the printed table does not")
        print("  contain.\n")
    else:
        print("  No reading produces an order at all.\n")

    print(f"  {len(inside)} of the {total} I would argue about, and what")
    print("  moving one would do:")
    for cid in sorted(inside):
        m = where[cid]
        print(f"    {cid}  in {m!r}:")
        print(f"        {len(MODE[m])} of {total} now,"
              f" {len(MODE[m]) - 1} if scored a pass")
    for cid in sorted(outside):
        print(f"    {cid}  a PASS I might lose, so it is in no mode")
        print(f"        {total} failures now, {total + 1} if scored a")
        print("        fail, and it would need a mode of its own")
    print("\n  A partition check cannot tell you the grouping is")
    print("  right, only that it is a grouping. The protection is a")
    print("  written rule per mode, or a second reader.")
```

```text
  17 notes assigned to 6 modes
  every note used exactly once? True

  mode                                   n   share  running
  Citation points somewhere else        5    29%     29%
  Answers a neighbouring question       5    29%     59%
  Answers for one case when two apply   4    24%     82%
  Not an answer at all                  1     6%     88%
  Contradicts the passage               1     6%     94%
  Citation does not support the claim   1     6%    100%

  Chapter 30 stops at that table and works the largest
  mode. Read the first two rows before doing that: 5
  and 5.
  They are the same number, so which of them the table
  prints first is the sort order and nothing else.

  So ask what the counts can carry, with chapter 20's
  resampling over the failures:

    failures  first two       third vs rest   same top 3
       17    -0.353 to +0.353  -0.12 to +0.41  82.72% <- mine
       40    -0.250 to +0.250  +0.00 to +0.30  97.08%
      100    -0.150 to +0.150  +0.06 to +0.26  99.95%
      300    -0.087 to +0.087  +0.11 to +0.22  100.00%

  The first column contains zero at 4 of the 4 sizes
  (17, 40, 100, 300), and only gets
  narrower. Read that as what it is: the resample draws
  from these failures, in which the two modes hold 5
  and 5, so what it narrows is a statement about that
  pair and not about the application. What more
  failures buys is the SECOND column - and read its
  low bound rather than its sign. The third mode's gap
  over the small ones, by size:
       17 failures   low end -0.118   below zero
       40 failures   low end +0.000   at zero
      100 failures   low end +0.060   above zero
      300 failures   low end +0.110   above zero

  And the last column is the one claim the seventeen
  come close to supporting: the three modes I call large
  come out as the three largest in 83% of resamples,
  which is a statement about a GROUP and still not an
  order inside it.

  What the next size up costs, at 17 failures in
  every 80 answers:
     40 failures needs about 190 answers read
    100 failures needs about 470 answers read

  That is the bill chapter 31 names when it says to
  label failures rather than cases, arriving one step
  earlier than expected: it is already due here, before
  any judge exists.

  One cell of that table does not hold still, and it is
  worth printing rather than hiding. Chapter 31's lab
  says a resampled interval should be stable at ten
  thousand rounds, and that an unstable one means too few
  rounds or far too few labels. Both halves are testable
  and the first one settles it.

    rounds    how the high end falls over 60 seeds
      10000   +0.353 on 44, +0.412 on 16
      50000   +0.353 on 58, +0.412 on 2
     200000   +0.353 on 60

  The two values are +0.3529 and +0.4118, which are
  6 of 17 and 7 of 17: the high end is a DISCRETE
  quantile, and at ten thousand rounds the 97.5th
  percentile lands either side of that boundary
  depending on the seed. More rounds pushes almost every
  seed onto one side - and read the table rather than
  the sentence, because at five times the rounds it is
  still 2 seeds of 60 and not none.

  So this cell is chapter 31's FIRST reason, too few
  rounds, and not its second. The reason that matters is
  that the figure the argument above rests on is the LOW
  end, and that one is the same on every one of the
  60 seeds at every round count in the table.

  What the first forty on their own would have given,
  which is the argument for having read the second:

    mode                                 first 40   all 80
    Citation points somewhere else            1        5
    Answers a neighbouring question           2        5
    Answers for one case when two apply       3        4
    Not an answer at all                      1        1
    Contradicts the passage                   0        1
    Citation does not support the claim       1        1

  And the mode the first forty called largest,
  'Answers for one case when two apply',
  comes third on the eighty. Working the largest mode
  after forty answers would have been working that one.

  5 modes, not 6, and 3 of them resting on a
  single answer. 1 of those 3 became a group once
  the second forty was read and 2 did not. A mode with
  one example in it is a guess about a kind, and the
  only way to find out is to read more output.

  And the result that table carries - the names and not
  the order - is one judgement call from changing. All 4
  rows below are the labels notes.py flags as arguable,
  and the assert above is what keeps them that list:

    d09 scored a pass: top three become 5, 4, 4,
        an ORDER
        and it is 'Answers a neighbouring question'
    d05 scored a pass: top three become 5, 4, 4,
        an ORDER
        and it is 'Citation points somewhere else'
    c04 scored a fail: top three become 5, 5, 5,
        into Answers for one case when two apply
        still tied at the top
    c33 scored a fail: top three become 5, 5, 4,
        into (its own)
        still tied at the top

  2 of the 4 leave a tie and 2 produce an order.
  And the orders name DIFFERENT modes:
    Answers a neighbouring question
    Citation points somewhere else
  so not even the direction survives one reading. The
  table gives six names and nothing about their order,
  and that is not a caveat on the finding - it is the
  finding.

  2 of the 17 I would argue about, and what
  moving one would do:
    d05  in 'Answers a neighbouring question':
        5 of 17 now, 4 if scored a pass
    d09  in 'Citation points somewhere else':
        5 of 17 now, 4 if scored a pass
    c04  a PASS I might lose, so it is in no mode
        17 failures now, 18 if scored a
        fail, and it would need a mode of its own
    c33  a PASS I might lose, so it is in no mode
        17 failures now, 18 if scored a
        fail, and it would need a mode of its own

  A partition check cannot tell you the grouping is
  right, only that it is a grouping. The protection is a
  written rule per mode, or a second reader.
```

**Six modes, every note in exactly one, and two of the six are pairs that had to be decided
rather than fallen into.** *Citation points somewhere else* and *Citation does not support the
claim* are both about a citation, and they are a different kind of wrong: the first is a quote
that is not where the citation says it is, and the second is a real quote, in a document that
was sent, which does not establish the sentence it is attached to. *Answers a neighbouring
question* and *Answers for one case when two apply* are both about the answer missing the
question, and they differ in the same way: in the first the sentence given is the wrong one, and
in the second it is one of the right ones and the answer stopped there.

Chapter 30 is explicit that two large modes fixed in different places must not be merged to tidy
the list, and both of those pairs are that case. The reason is visible two steps later: of each
pair, one half is a check in code and the other half needs a judgement.

**And it is worth saying which of the six are new and which are chapter 30's under another
name**, because a taxonomy that quietly renames somebody else's is not an error analysis. Two are
chapter 30's, name for name: *Not an answer at all* and *Contradicts the passage*. Two are new:
*Answers for one case when two apply*, which needs a corpus whose questions span two documents,
and *Answers a neighbouring question*, which is near chapter 30's *Answers a different question*
and not it. All five of mine are the right subject and the wrong sentence; two of chapter 30's
four are a different subject altogether — *answered about shipping when asked about returns* — and
the other two are a different conversation, *answered the question asked two turns earlier*. The
distinction is real and it is narrower than it looks, which is why step 5's check for my mode
borrows chapter 31's wording for chapter 30's.

**And the last two are one of chapter 30's modes, split in half.** Its *Citation does not support*
holds eight failures. Three of them — *cited a document that does not exist*, *cited policy.pdf
but the quote is not in it*, *cited the right document, wrong paragraph* — are the kind a
substring test settles. **Chapter 30 measures its three mechanical citation checks at 3 of those 8
and the three are exactly those three.** It explains the figure as well as printing it, in its
own words: the checks are necessary and not sufficient, and the remaining five are of two kinds,
four pointing at something real that does not settle the claim and one carrying no citation at
all.

**What chapter 30 does not do is split the mode, and splitting it is what lets the check close
instead of dent.** A mode that mixes a substring failure with an entailment failure guarantees
that any check for it covers a part; separated, the same family of checks closes one half outright
and leaves the other named and uncovered, which is step 5's result and the clearest thing this
taxonomy does that chapter 30's does not. **And chapter 30's odd one out is a gap in my checks
rather than in its mode**: an answer with no citation at all passes all three of mine, because
each tests the citations the answer has. Step 5 measures it and nothing here exposes it, because
the only three answers carrying no citation are correct refusals.

**Then the table, and the row to read before working the largest mode.** The first two modes hold
five failures each. They are the same number, so which of them the table prints first is the sort
order and nothing else — and chapter 30's *What To Actually Do* ends on [**step 8**]{.noindex}, *then fix the
largest mode*. There is no largest.

**So ask what seventeen failures can carry, with chapter 20's resampling over the failures
themselves.** Three questions, because the table invites three claims, and the three answers are
different:

- **Is the first mode bigger than the second?** At seventeen the gap runs from −0.353 to +0.353,
  so nothing here orders them. Read down the column and the interval narrows to ±0.087 at three
  hundred while staying centred on zero — which is the resample telling you, honestly, that
  **counting more failures drawn from an exactly equal pair narrows the statement that they are
  equal and never turns it into an order.** The Note below says what that does and does not
  establish, because the resample draws from these seventeen.
- **Is the third mode bigger than the three singletons?** Read the low end rather than the sign.
  At seventeen it is −0.118, so no. At forty it is exactly zero — it reaches and does not clear.
  At a hundred it is +0.060 and at three hundred +0.110. **That one is a real gap and it is
  affordable**, and the table of low ends by size is the thing to look at rather than the
  interval's width.
- **Are the three modes I call large the three largest?** In 83 per cent of resamples at
  seventeen, and 97 per cent at forty. That is the one claim the seventeen come close to
  supporting, and it is a statement about a *group* with no order inside it.

**And the cost of the next size up is arithmetic, not judgement.** Seventeen failures came out of
eighty answers, so forty failures is about a hundred and ninety answers read and a hundred is
about four hundred and seventy. **Chapter 31 says to label failures rather than cases and prices
that as the expensive part of validating a judge. The bill arrives one step earlier than that:
it is already due at the taxonomy, before any judge exists.**

**The last block is the one that would have cost a fortnight.** On the first forty alone the
largest mode was *Answers for one case when two apply*, at three. On the eighty it is third, at
four, and the two modes above it were a 1 and a 2 in the first forty. **Working the largest mode
after forty answers would have been working the mode that comes third after eighty** — not
because the first forty were unrepresentative in any way I could have detected, but because three
against two is not a difference.

> **Warning:** This is the chapter's sharpest result and it is easy to take the wrong lesson from
> it. The lesson is [**not**]{.noindex} that error analysis needs hundreds of failures before it
> is worth doing. The six names are established on seventeen, every one of them with a worked
> example, and the names are what the checks get built from — a check does not need to know which
> mode is biggest. The lesson is that [**the names**]{.noindex} and [**the order**]{.noindex} are
> two different findings with two different prices, and chapter 30's table prints them in one
> place without saying so.

> **Note:** Two limits on that arithmetic, and the first one matters more than it looks. **The
> resample draws from these seventeen**, so the top two modes are exactly equal in everything it
> draws and the first column is centred on zero *by construction*. What the column establishes is
> therefore narrow and still worth having: that on seventeen failures these two modes are
> indistinguishable, and that the width of the indistinguishability is ±0.35. It does not
> establish that the two modes are equal in the application — only that nothing here separates
> them. **And the second limit is chapter 20's own assumption**, which the program states: that
> these seventeen are a sample of the failures. They are not a sample of my *inputs*, because the
> second forty were aimed, which is chapter 30's tip exactly. The two batches failed at 20 and 22
> per cent, so the aim did not show up in the rate, and the per-batch mode counts are in the
> table's own first column against its second.

> **Tip:** `every note used exactly once? True` is worth the line it costs. It proves the
> grouping is a partition and it cannot tell you the grouping is right — and the program's own
> what-if block is the demonstration. Each of the four arguable labels changes the top of the
> table on its own: `d09` scored a pass gives 5, 4, 4; `d05` scored a pass gives 5, 4, 4; `c04`
> scored a failure gives 5, 5, 5; `c33` scored a failure gives 5, 5, 4. **Two of the four produce
> an order and the two orders name different modes** — `d09` puts *Answers a neighbouring
> question* on top and `d05` puts *Citation points somewhere else* there. So not even the
> direction survives one reading, and that is the finding rather than a caveat on it.

## Step 5: A Check Per Mode, Sorted by What It Needs

Chapter 30's step 4 is to let the modes choose the metrics. Chapter 31's first section is the
question that comes before building any of them: does this check need a judgement at all? The
answer is in what the check needs in order to decide, and the column is written before anything
is implemented.

```python
"""A check per mode, sorted by what it needs, and the code ones run.

Chapter 31's rule decides who runs each check: code wherever the
comparison is between two things that are both literally present, a
judge only where the verdict needs a decision about what text MEANS.
NEEDS below is that column, written before anything was implemented.

Then the code checks are run over all eighty answers and marked
FAILURE BY FAILURE against my own labels, which is chapter 30's rule:
a check catches failures and a mode is a group of them, so a mode
covered in part is the ordinary case.
"""
import json
import re

import search
from modes import MODE
from notes import NOTES
from questions import all_cases
from run import outputs

#  mode, check, who decides, what it needs to decide.
#
#  The first three are chapter 28's three mechanical citation checks,
#  adapted to what this pipeline's citations actually carry. 28's
#  first two are here unchanged in substance - does the document
#  exist, is the quote in it. 28's third, the offset, is dropped,
#  because chapter 45's instruction asks for an id and a quote and
#  never asks for an offset. One is added that 28 does not have and
#  this pipeline makes possible: whether the cited passage was among
#  the ones SENT, which a trace answers and a document store cannot.
#
#  The `needs` text is the guess made BEFORE implementing, and it is
#  left as it was written. One of them is wrong and the measurement
#  below corrects it: the stub check needs the last character and
#  does not need the length, which is the opposite of the order its
#  own line puts them in.
NEEDS = [
 ("Citation points somewhere else", "the cited id is a passage id",
  "code", "a string against a list of ids"),
 ("Citation points somewhere else", "the cited id was one of the passages sent",
  "code", "a string against the request's own list"),
 ("Citation points somewhere else", "the quote is in the passage cited",
  "code", "a substring test, under a declared normalisation"),
 ("Not an answer at all", "the answer is not a stub",
  "code", "the length, and the last character"),
 ("Contradicts the passage", "every figure in the answer is in a passage",
  "code", "a regular expression and a substring test"),
 ("Refuses when the answer is there", "the answer is not a refusal",
  "code", "a phrase list, once you have read your own refusals"),
 ("Refuses when the answer is there", "the passages do answer the question",
  "judge", "deciding whether a passage answers a question"),
 ("Answers a neighbouring question", "the answer is about what was asked",
  "judge", "deciding what two pieces of text are about"),
 ("Answers for one case when two apply", "the answer covers every case the question spans",
  "judge", "deciding how many cases a question has"),
 ("Citation does not support the claim", "the quote establishes the sentence",
  "judge", "deciding whether one piece of text entails another"),
 ("Contradicts the passage", "the answer does not restate a passage inexactly",
  "judge", "deciding whether two sentences say the same thing"),
]

REFUSALS = ("do not provide", "does not provide", "not mentioned",
            "no information", "cannot find", "not specified")
FIGURE = re.compile(r"\b\d+(?:\.\d+)?\b")


def norm(s):
    """The normalisation, declared. Chapter 45 earned this: a quote
    compared as it stands fails on markdown emphasis and on a line
    break, and both are formatting rather than a different claim."""
    s = s.replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def trim(s):
    """And one more rule, which the measurement below is about: a
    quote cut short and given a full stop of its own."""
    return norm(s).rstrip(" .,;:")


def cited_id_exists(t):
    return all(c.get("id") in search.BY_ID for c in t["citations"])


def cited_id_was_sent(t):
    return all(c.get("id") in t["passages_sent"] for c in t["citations"])


def quote_in_passage(t, rule=trim):
    for c in t["citations"]:
        row = search.BY_ID.get(c.get("id"))
        if row is None or rule(c.get("quote", "")) not in norm(row["text"]):
            return False
    return True


def not_a_stub(t):
    """The rule the measurement below arrives at. The obvious one -
    an answer under some number of characters - is `long_enough`,
    and it is kept so the two can be counted against each other."""
    a = t["answer"].strip()
    return bool(a) and not a.endswith(":")


def long_enough(t):
    a = t["answer"].strip()
    return bool(a) and len(a) > 12


def figures_in_passages(t):
    sent = norm(" ".join(search.BY_ID[c]["text"]
                         for c in t["passages_sent"]))
    return all(f in sent for f in FIGURE.findall(norm(t["answer"])))


def not_a_refusal(t):
    a = t["answer"].lower()
    return not any(p in a for p in REFUSALS)


#  check, the function, the mode it was built for
CODE = [
 ("cited id is a passage id", cited_id_exists,
  "Citation points somewhere else"),
 ("cited id was among the passages sent", cited_id_was_sent,
  "Citation points somewhere else"),
 ("quote is in the passage cited", quote_in_passage,
  "Citation points somewhere else"),
 ("answer does not end at a colon", not_a_stub,
  "Not an answer at all"),
 ("every figure is in a passage", figures_in_passages,
  "Contradicts the passage"),
 ("answer is not a refusal", not_a_refusal,
  "Refuses when the answer is there"),
]


def says(n, singular, plural=None):
    """A count and its verb from the same expression. Entry 64 of
    this project's defect ledger is a print line stating a count
    beside a sentence that assumes it, so the sentence is built
    here instead of typed."""
    plural = plural or singular + "s"
    if n == 0:
        return f"none of them is a {singular}"
    if n == 1:
        return f"1 of them is a {singular}"
    return f"{n} of them are {plural}"


def alarms(fn, ts):
    """The cases a check fires on. A check PASSES a good answer, so
    it fires when it returns False."""
    return [t["case_id"] for t in ts if not fn(t)]


if __name__ == "__main__":
    ts = outputs(1) + outputs(2)
    fails = set(NOTES)
    where = {c: m for m, cs in MODE.items() for c in cs}
    code = [c for c in NEEDS if c[2] == "code"]
    judge = [c for c in NEEDS if c[2] == "judge"]

    print(f"  {len(NEEDS)} checks for {len(MODE)} modes:"
          f" {len(code)} code, {len(judge)} judge\n")
    print("  CODE CAN DECIDE THESE.")
    for _, name, _, needs in code:
        print(f"    {name}")
        print(f"      needs: {needs}")
    print("\n  THESE NEED A JUDGEMENT.")
    for _, name, _, needs in judge:
        print(f"    {name}")
        print(f"      needs: {needs}")

    modes = {c[0] for c in NEEDS}
    split = sorted(m for m in modes
                   if {c[2] for c in NEEDS if c[0] == m} == {"code", "judge"})
    mine = len([m for m in modes if m in MODE])
    has_code = sorted(m for m in modes
                      if "code" in {c[2] for c in NEEDS if c[0] == m})
    print(f"\n  {len(modes)} modes appear in that table: my {mine}, plus")
    mine_in = len(set(MODE.get("Refuses when the answer is there", [])))
    print("  chapter 30's 'Refuses when the answer is there', which")
    print(f"  {mine_in} of my {len(ts)} answers are in.\n")
    print(f"  {len(has_code)} of the {len(modes)} have SOME part code can decide:")
    for m in has_code:
        tag = "  <- and a judge part too" if m in split else ""
        print(f"    {m}{tag}")
    print(f"\n  {len(modes) - len(has_code)} have none, and they are the ones about")
    print("  meaning from end to end:")
    for m in sorted(modes):
        if m not in has_code:
            print(f"    {m}")
    print("\n  The refusal mode's rows are in the table on purpose.")
    print("  Its check is cheap and the mode is one I would expect")
    print("  of a system over documents - which is exactly the")
    print("  reasoning chapter 30 warns against, and the")
    print("  measurement below is what settles it.\n")

    print(f"  Now run the code checks over all {len(ts)} answers."
          f" {len(fails)} are")
    print("  failures by my own reading. `fires` is how many answers")
    print("  the check rejects; `fails` how many of those are")
    print("  failures; `mode` how many are failures of the mode the")
    print("  check was built for.\n")
    print("  check                                fires fails mode")
    union = set()
    for name, fn, mode in CODE:
        a = set(alarms(fn, ts))
        real = a & fails
        inmode = a & set(MODE.get(mode, []))
        union |= real
        print(f"  {name:36s} {len(a):4d} {len(real):5d} {len(inmode):4d}")

    cite = [c for c in CODE if c[2] == "Citation points somewhere else"]
    cu = set()
    for _, fn, _ in cite:
        cu |= set(alarms(fn, ts))
    m = set(MODE["Citation points somewhere else"])
    sets = sorted((set(alarms(fn, ts)) for _, fn, _ in cite), key=len)
    nested = all(a <= b for a, b in zip(sets, sets[1:]))
    print(f"\n  The {len(cite)} citation rows are"
          f" {'nested' if nested else 'NOT nested'}, so take")
    print(f"  their union: {len(cu)} answers rejected,"
          f" {len(cu & fails)} of them failures,")
    print(f"  {len(cu & m)} of the {len(m)} in the mode and {len(m - cu)} missed.")
    if not (m - cu):
        print("  That is a mode closed outright by a check that reads")
        print("  none of the prose.\n")
    else:
        print("  That is a mode dented and not closed.\n")

    print("  Now the two rows that were nearly wrong, because the")
    print("  rule inside a check is where the work is.\n")
    for label, fn in (("answer longer than 12 characters", long_enough),
                      ("answer does not end at a colon", not_a_stub)):
        a = set(alarms(fn, ts))
        print(f"    {label:33s} fires {len(a):2d},"
              f" fails {len(a & fails):2d}")
    short = sorted(set(alarms(long_enough, ts)) - fails)
    byid = {x["case_id"]: x for x in ts}
    print(f"\n  The length rule rejects {len(short)} correct answers,")
    print("  and they are right and short:")
    for cid in short:
        print(f"    {cid}  {byid[cid]['answer'].strip()[:44]!r}")
    stubs = sorted(set(alarms(not_a_stub, ts)))
    noun = "answer" if len(stubs) == 1 else "answers"
    print(f"\n  The {len(stubs)} {noun} the colon rule rejects, by")
    print("  length:")
    for cid in stubs:
        a = byid[cid]["answer"].strip()
        print(f"    {cid}  {len(a):3d} characters, ending {a[-1]!r}")
    longest = max(len(byid[c]['answer'].strip()) for c in short)
    print(f"\n  The longest answer the length rule rejected is"
          f" {longest}")
    print("  characters, so on this set length and stub-ness do not")
    print("  order the same way at all: the last character does the")
    print("  work and the length does none of it.")
    print()

    for label, rule in (("quote as it stands", norm),
                        ("trailing punctuation trimmed", trim)):
        a = set(alarms(lambda t, r=rule: quote_in_passage(t, r), ts))
        print(f"    {label:30s} fires {len(a):2d},"
              f" fails {len(a & fails):2d}, mode {len(a & m):2d}")
    strict = set(alarms(lambda t: quote_in_passage(t, norm), ts))
    extra = sorted(strict - set(alarms(quote_in_passage, ts)))
    exf = [c for c in extra if c in fails]
    print(f"\n  The stricter rule rejects {len(extra)} more:"
          f" {', '.join(extra)}. Each")
    print("  of those matches its passage once trailing punctuation")
    print("  goes - which is what the two rules differ by, so it is")
    print("  true of them by construction. In every case here it is")
    print("  a quote cut short and given a full stop of its own,")
    print("  which is formatting and not a different claim.")
    verb = "is" if len(exf) == 1 else "are"
    print(f"  {len(exf)} of the {len(extra)} {verb} a failure, and for an")
    print(f"  unrelated reason: {', '.join(exf) if exf else '(none)'}."
          f" The other {len(extra) - len(exf)}")
    print("  are correct answers, correctly cited. The normalisation")
    print("  rule is part of the check and not a detail of it.\n")

    figs = set(alarms(figures_in_passages, ts))
    refs = set(alarms(not_a_refusal, ts))
    print("  And the two checks I would have built on a hunch.\n")
    print(f"  'every figure is in a passage' fires on {len(figs)} of"
          f" {len(ts)},")
    print(f"  and {says(len(figs & fails), 'failure')}. The check")
    print("  everybody writes first covers nothing here, which is")
    print("  the measurement and not a prediction.\n")
    holds = {x["case_id"]: x["holds"] for x in ts}
    unanswerable = [c for c in sorted(refs) if not holds[c]]
    print(f"  'answer is not a refusal' fires on {len(refs)}, and")
    print(f"  {says(len(refs & fails), 'failure')}."
          f" {len(unanswerable)} of the {len(refs)} are questions the")
    print("  corpus cannot answer, so those refusals are correct")
    if len(unanswerable) == len(refs) and not (refs & fails):
        print("  and every alarm it raises is a false one - chapter")
        print("  31's point that such a check fires on a correct")
        print("  refusal, measured here:")
    else:
        print("  and the rest are not. Chapter 31's point is that such")
        print("  a check fires on a correct refusal; here it is:")
    for cid in sorted(refs):
        q = next(q for c, q, _ in all_cases() if c == cid)
        tag = "yes" if holds[cid] else " no"
        print(f"    {cid}  answerable: {tag}   {q[:36]}")
    ref_mode = "Refuses when the answer is there"
    print(f"\n  The mode it was built for holds"
          f" {len(MODE.get(ref_mode, []))} of my"
          f" {len(fails)} failures.")
    print("  Building it first would have been a week spent on a")
    print("  mode this application does not have, which is chapter")
    print("  30's argument with my own numbers.\n")

    print(f"  All {len(CODE)} code checks together reject"
          f" {len(set().union(*(set(alarms(f, ts)) for _, f, _ in CODE)))}"
          f" answers and catch")
    print(f"  {len(union)} of the {len(fails)} failures.")
    left = sorted(fails - union)
    print(f"  {len(left)} failures left, in these modes:\n")
    for mode, cs in MODE.items():
        miss = [c for c in cs if c in left]
        if miss:
            tag = "  <- none covered" if len(miss) == len(cs) else ""
            print(f"    {mode:36s} {len(miss)} of {len(cs)}{tag}")
    nocite = [t["case_id"] for t in ts if not t["citations"]]
    blank = {"citations": [], "passages_sent": [], "answer": "no cite"}
    assert all(fn(blank) for _, fn, _ in cite)
    bad = [c for c in nocite if c in fails]
    print(f"\n  And one thing those {len(cite)} checks do NOT reach, which")
    print("  no failure here exposes and chapter 30's application")
    print(f"  had: every one of them PASSES an answer carrying no")
    print("  citation at all, because each tests every citation the")
    print("  answer has and there are none to test. Chapter 30's")
    print("  *Citation does not support* holds exactly such a note -")
    print("  *gave an answer with no citation at all* - and chapter")
    print("  30 counts it apart from the other four for that reason.")
    print(f"  {len(nocite)} answers here carry no citation"
          f" ({', '.join(nocite)}),")
    print(f"  and {len(bad)} of them is a failure, so the gap costs")
    print("  nothing on this set. It would cost everything on one")
    print("  where an answer is expected to cite.\n")
    print("  That is the honest list of what no check of mine")
    print("  reaches. The next step builds a judge for one line of")
    print("  it, and one only.")
```

```text
  11 checks for 6 modes: 6 code, 5 judge

  CODE CAN DECIDE THESE.
    the cited id is a passage id
      needs: a string against a list of ids
    the cited id was one of the passages sent
      needs: a string against the request's own list
    the quote is in the passage cited
      needs: a substring test, under a declared normalisation
    the answer is not a stub
      needs: the length, and the last character
    every figure in the answer is in a passage
      needs: a regular expression and a substring test
    the answer is not a refusal
      needs: a phrase list, once you have read your own refusals

  THESE NEED A JUDGEMENT.
    the passages do answer the question
      needs: deciding whether a passage answers a question
    the answer is about what was asked
      needs: deciding what two pieces of text are about
    the answer covers every case the question spans
      needs: deciding how many cases a question has
    the quote establishes the sentence
      needs: deciding whether one piece of text entails another
    the answer does not restate a passage inexactly
      needs: deciding whether two sentences say the same thing

  7 modes appear in that table: my 6, plus
  chapter 30's 'Refuses when the answer is there', which
  0 of my 80 answers are in.

  4 of the 7 have SOME part code can decide:
    Citation points somewhere else
    Contradicts the passage  <- and a judge part too
    Not an answer at all
    Refuses when the answer is there  <- and a judge part too

  3 have none, and they are the ones about
  meaning from end to end:
    Answers a neighbouring question
    Answers for one case when two apply
    Citation does not support the claim

  The refusal mode's rows are in the table on purpose.
  Its check is cheap and the mode is one I would expect
  of a system over documents - which is exactly the
  reasoning chapter 30 warns against, and the
  measurement below is what settles it.

  Now run the code checks over all 80 answers. 17 are
  failures by my own reading. `fires` is how many answers
  the check rejects; `fails` how many of those are
  failures; `mode` how many are failures of the mode the
  check was built for.

  check                                fires fails mode
  cited id is a passage id                1     1    1
  cited id was among the passages sent    2     2    2
  quote is in the passage cited           5     5    5
  answer does not end at a colon          1     1    1
  every figure is in a passage            0     0    0
  answer is not a refusal                 3     0    0

  The 3 citation rows are nested, so take
  their union: 5 answers rejected, 5 of them failures,
  5 of the 5 in the mode and 0 missed.
  That is a mode closed outright by a check that reads
  none of the prose.

  Now the two rows that were nearly wrong, because the
  rule inside a check is where the work is.

    answer longer than 12 characters  fires  6, fails  0
    answer does not end at a colon    fires  1, fails  1

  The length rule rejects 6 correct answers,
  and they are right and short:
    c06  '3.99 pounds'
    c08  '6.50 pounds'
    c11  'TR21 to TR25'
    c14  'K is black'
    c16  '34 mm wide'
    c18  'max 60 W'

  The 1 answer the colon rule rejects, by
  length:
    c20   49 characters, ending ':'

  The longest answer the length rule rejected is 12
  characters, so on this set length and stub-ness do not
  order the same way at all: the last character does the
  work and the length does none of it.

    quote as it stands             fires  8, fails  6, mode  5
    trailing punctuation trimmed   fires  5, fails  5, mode  5

  The stricter rule rejects 3 more: c07, c28, d32. Each
  of those matches its passage once trailing punctuation
  goes - which is what the two rules differ by, so it is
  true of them by construction. In every case here it is
  a quote cut short and given a full stop of its own,
  which is formatting and not a different claim.
  1 of the 3 is a failure, and for an
  unrelated reason: c07. The other 2
  are correct answers, correctly cited. The normalisation
  rule is part of the check and not a detail of it.

  And the two checks I would have built on a hunch.

  'every figure is in a passage' fires on 0 of 80,
  and none of them is a failure. The check
  everybody writes first covers nothing here, which is
  the measurement and not a prediction.

  'answer is not a refusal' fires on 3, and
  none of them is a failure. 3 of the 3 are questions the
  corpus cannot answer, so those refusals are correct
  and every alarm it raises is a false one - chapter
  31's point that such a check fires on a correct
  refusal, measured here:
    c13  answerable:  no   How much does the HL-2208 kettle cos
    c38  answerable:  no   What is your VAT number?
    c40  answerable:  no   On what date did the 2026 surcharge 

  The mode it was built for holds 0 of my 17 failures.
  Building it first would have been a week spent on a
  mode this application does not have, which is chapter
  30's argument with my own numbers.

  All 6 code checks together reject 9 answers and catch
  6 of the 17 failures.
  11 failures left, in these modes:

    Answers a neighbouring question      5 of 5  <- none covered
    Answers for one case when two apply  4 of 4  <- none covered
    Citation does not support the claim  1 of 1  <- none covered
    Contradicts the passage              1 of 1  <- none covered

  And one thing those 3 checks do NOT reach, which
  no failure here exposes and chapter 30's application
  had: every one of them PASSES an answer carrying no
  citation at all, because each tests every citation the
  answer has and there are none to test. Chapter 30's
  *Citation does not support* holds exactly such a note -
  *gave an answer with no citation at all* - and chapter
  30 counts it apart from the other four for that reason.
  3 answers here carry no citation (c13, c38, c40),
  and 0 of them is a failure, so the gap costs
  nothing on this set. It would cost everything on one
  where an answer is expected to cite.

  That is the honest list of what no check of mine
  reaches. The next step builds a judge for one line of
  it, and one only.
```

**Read the `needs` lines and chapter 31's rule appears on its own.** Every check in the first
list compares two things that are both literally present — a string against a list of ids, a
quote against a passage, the last character of the answer, a digit against a passage. Every check
in the second list needs a decision about what text *means*: entailment, aboutness, how many
cases a question has. There is no substring test for any of those.

**Four of the seven modes in that table have a part code can decide, and two of those four also
have a judge part. Read the comparison with chapter 31 like for like before quoting it**: the
seven includes chapter 30's refusal mode, which none of my eighty answers is in, and chapter 31's
eight were all modes with members. Of my own six, [**three**]{.noindex} have a code part against chapter 31's
seven of eight — and the difference is not noise. Three of my six modes are about meaning from end to
end — *Answers a neighbouring question*, *Answers for one case when two apply* and *Citation does
not support the claim* — and no part of any of them is a comparison between two things that are
both present. Chapter 31's rule still holds exactly as stated: a mode is not a code mode or a
judge mode, and running the cheap part first leaves the judge less to be wrong about. What has
changed is how much of this application's trouble the cheap part reaches.

**The three citation rows are chapter 28's, and they close a mode here where chapter 30 measured
them closing three failures of eight.** Chapter 28's three are: does the document exist, is the
quote in it, is it at the offset claimed. The first two are here in substance. [**The third is
dropped**]{.noindex}, because chapter 45's instruction asks the model for an id and a quote and
never asks for an offset, so there is no *claimed* offset to verify. Chapter 45 does check the
stored one — its index keeps a locator per chunk and its step 6 asks whether that locator still
finds the text the row recorded — which is a different check with a different failure behind
it. **And one is added that chapter 28 does not have**:
whether the cited passage was among the ones *sent*. That check exists only because there is a
trace — a document store cannot answer it, and chapter 33's `passages_sent` field is what makes
it possible.

Taken together the three reject five answers, all five are failures, all five are in the mode,
and none is missed. **A mode closed outright by a check that reads none of the prose is the best
thing in this chapter and it took an afternoon.** Chapter 30 is right that the same family of
checks caught 3 of 8 on its application and right about why — necessary and not sufficient — and
the difference here is not that the checks got better. It is that this taxonomy puts the failures
they *can* catch in one mode and the failure they cannot in another, which is what the split
decided two steps ago was for.

**Then the two rows that were nearly wrong, because the rule inside a check is where the work
is.** The obvious shape of a check for *Not an answer at all* is a length threshold. It rejects
six answers and not one of them is a failure: `c06` is *3.99 pounds*, `c16` is *34 mm wide*,
`c18` is *max 60 W*. They are right and short. **The longest answer the length rule rejects is
twelve characters and the one real stub is forty-nine**, so on this set the two do not order the
same way at all: the last character does the work and the length does none of it. Chapter 30 says
coverage is not the test and chapter 31 measures the property that is — firing only on failures —
and this is that property deciding between two spellings of the same check.

**And the `needs` column still carries the wrong guess, on purpose.** It says the stub check
needs *the length, and the last character*, which is the order I wrote before implementing
anything and is the opposite of what the measurement found. Leaving it is the honest record of a
column written in advance; the program's comment says so, and a column that quietly agreed with
the result afterwards would be no record at all.

**And the quote check's normalisation rule is part of the check and not a detail of it.** Compare
a quote as it stands and the check fires on eight answers, six of them failures. Trim a trailing
full stop and it fires on five, all five failures. The three it stops rejecting — `c07`, `c28`
and `d32` — each cut a quote short and gave it a full stop of its own, which is formatting rather
than a different claim. One of those three is a failure for a completely unrelated reason, and
the other two are correct answers correctly cited.

**Then the two checks I would have built on a hunch, and this is chapter 30's argument with my
own numbers in it.** *Every figure in the answer is in a passage* — the invented-figure check,
the one everybody writes first — fires on [**nothing**]{.noindex}. There is no invented figure in these
eighty answers. *The answer is not a refusal* fires on three, and all three are the questions the
corpus cannot answer, so all three refusals are correct and the detector is pure false alarm. Its
mode has no members in my taxonomy at all. **Building either of those first would have been a
week spent on a mode this application does not have.**

**All six code checks together catch six of the seventeen failures, and the eleven left are the
honest list.** *Answers a neighbouring question* 5 of 5 uncovered, *Answers for one case when two
apply* 4 of 4, and one each in the two singleton modes. That list is what a judge is for, and the
next step builds one for the largest line in it and one only.

**Which leaves a gap the chapter had better name rather than let you find.** Of the three frequent
modes, one is closed in code and one gets the judge step 6 builds. The third — *Answers for one
case when two apply*, four failures, and the mode the first forty called largest — gets a row in
the `needs` table and nothing else: no code, no judge, no measurement. Step 6 is why: one judge
per mode is chapter 31's step 3, the judge it builds takes 480 calls and comes out unusable, and
a second judge built the same way would most likely do the same. **What it would cost is a
number, and the number is in step 6.** The same is true of *Citation does not support the claim*,
whose one check — does the quote establish the sentence — is the claim-level check chapter 32
owns, declared out of scope in the opening and still the thing that mode needs.

> **Note:** The refusal detector's row is in the table deliberately, and so is the invented-figure
> row. Chapter 30's step 9 does the same thing with a made-up metric — "the answer should be under
> 100 words" — and finds it catches nothing. The difference here is that these two are not made
> up: they are the two checks a competent engineer would reach for first on a retrieval system,
> and the measurement is what says they are not this application's checks. **A check you are
> confident about is still a check with a coverage figure.**

> **Warning:** `the answer is not a refusal` is also the clearest case of chapter 30's rule that
> a check reaches outside the mode it was built for, and in the wrong direction. Its three alarms
> are all passes. A refusal detector on its own fires on a correct refusal, which is why chapter
> 30 named its mode *Refuses when the answer is there* and why chapter 31 files the second half —
> whether the passages do answer the question — under judgement. This lab has the `holds` column
> and can decide it in code; nothing in production has that column.
## Step 6: One Judge, Validated in Chapter 31's Order

Eleven of the seventeen failures are out of reach of code, and the largest line in that list is
*Answers a neighbouring question* at five. So: one judge, for that one named mode, returning pass
or fail on that one thing. Not a score, and not one judge for everything — chapter 31's step 3.

Chapter 31's order is the whole of the method here, and the reason is that the first two
measurements need no labels and can end the exercise on their own. Self-agreement first. Then the
flip count under an arbitrary change. Then the do-nothing baseline, which needs labels and no
judge. Then, last, agreement with my labels, split into the two figures that matter.

```python
"""Two judges for one named mode, measured in chapter 31's order.

The mode is 'Answers a neighbouring question' - five of the seventeen
failures, and the largest line in what no code check of mine reaches.
A judge returns pass or fail on that one thing and nothing else. It
never sees my label and it never sees the other modes.

Chapter 31's order is the method, and it is followed because the
first two measurements need no labels and can end the exercise on
their own:

  1  self-agreement: the same case shown twice, and the flips counted
  2  the flip count under an arbitrary change: the answer printed
     before the question instead of after
  3  the do-nothing baseline, from my labels and no judge
  4  then, and only then, agreement with my labels, split into the
     two numbers that matter, with chapter 20's interval on each

B differs from A by one sentence, so the difference can be attributed
to it - chapter 18's rule, and chapter 31 compared two judges the
same way. The sentence was chosen by reading A's own `why` field on
the answers it rejected, which is chapter 30's method applied to the
judge rather than to the application.

It writes verdicts.json once and reads it afterwards. 480 calls.
"""
import json
import pathlib
import random

import answer
from modes import MODE
from notes import NOTES
from run import outputs

MODE_NAME = "Answers a neighbouring question"
OUT = pathlib.Path("verdicts.json")
RESAMPLES = 10_000
SEED = 46

COMMON = (
    "You are checking one named fault in a support answer, and "
    "nothing else.\n\n"
    "The fault: the answer is about something next to the question "
    "rather than about the question. It gives a rule when a figure "
    "was asked for, or says what not to do when asked what to do, "
    "or answers a nearby question instead of the one asked.\n\n"
    "Ignore everything else. Do not judge whether the answer is "
    "true, whether it is complete, or whether its citation is "
    "right."
)

# The one sentence that is the whole difference between them.
EXTRA = (
    "An answer that contains what the question asked for is a pass, "
    "however short it is and however closely it quotes the document."
)

REPLY = ("Reply as JSON: {\"verdict\": \"pass\" or \"fail\", "
         "\"why\": \"one short sentence\"}. "
         "\"fail\" means the fault is present.")

JUDGES = {
    "A": f"{COMMON}\n\n{REPLY}",
    "B": f"{COMMON}\n\n{EXTRA}\n\n{REPLY}",
}


def prompt(instruction, question, text, swapped=False):
    """The arbitrary element is the ORDER of the two pieces. Chapter
    31 varies exactly such a thing and counts the flips, because a
    verdict that depends on it is not a verdict about the answer."""
    if swapped:
        body = f"Answer: {text}\n\nQuestion: {question}"
    else:
        body = f"Question: {question}\n\nAnswer: {text}"
    return f"{instruction}\n\n{body}"


def ask_judge(instruction, question, text, swapped=False):
    d = answer.ask(prompt(instruction, question, text, swapped))
    raw = d["choices"][0]["message"]["content"]
    try:
        got = json.loads(raw)
        v, why = got.get("verdict", ""), got.get("why", "")
    except json.JSONDecodeError:
        v, why = raw, ""
    fail = str(v).strip().lower().startswith("fail")
    return ("F" if fail else "P"), why


def run():
    ts = outputs(1) + outputs(2)
    rows = []
    for i, t in enumerate(ts, 1):
        row = {"case_id": t["case_id"],
               "mine": "F" if t["case_id"] in MODE[MODE_NAME] else "P"}
        for name, instruction in JUDGES.items():
            first, why = ask_judge(instruction, t["question"],
                                   t["answer"])
            second, _ = ask_judge(instruction, t["question"],
                                  t["answer"])
            swap, _ = ask_judge(instruction, t["question"],
                                t["answer"], True)
            row[name] = {"first": first, "second": second,
                         "swapped": swap, "why": why}
        rows.append(row)
        print(f"  {t['case_id']} {i:2d}/{len(ts)}", flush=True)
    OUT.write_text(json.dumps(rows, indent=1))
    return rows


def verdicts():
    return json.loads(OUT.read_text()) if OUT.exists() else run()


def column(rows, name, which):
    return [r[name][which] for r in rows]


def figures(pairs):
    hits = sum(1 for m, j in pairs if m == "F" and j == "F")
    fails = sum(1 for m, j in pairs if m == "F")
    alarms = sum(1 for m, j in pairs if j == "F")
    agree = sum(1 for m, j in pairs if m == j)
    return (agree / len(pairs),
            hits / fails if fails else None,
            hits / alarms if alarms else None)


def interval(pairs, index, rounds=RESAMPLES, seed=SEED):
    """Chapter 20's procedure. The method is 20's; what matters here
    is which denominator each figure rests on."""
    r = random.Random(seed)
    n = len(pairs)
    out = []
    for _ in range(rounds):
        s = [pairs[r.randrange(n)] for _ in range(n)]
        v = figures(s)[index]
        if v is not None:
            out.append(v)
    out.sort()
    return out[len(out) // 40], out[len(out) * 39 // 40]


def ids(cs, width=58, indent="       "):
    return answer.wrap(", ".join(cs), indent, indent, width)


if __name__ == "__main__":
    rows = verdicts()
    mine = [r["mine"] for r in rows]
    byid = {r["case_id"]: r for r in rows}
    n = len(rows)
    nf = mine.count("F")

    print(f"  Two judges, one mode: {MODE_NAME!r}.")
    print(f"  {n} cases, {nf} of which I labelled fail for THIS mode.")
    print(f"  {len(NOTES)} of the {n} are failures of some kind, so"
          f" {len(NOTES) - nf} of")
    print("  them are passes as far as this judge is concerned.\n")
    print(f"  B is A plus one sentence:")
    print(answer.wrap(f'"{EXTRA}"', "    ", "    ", 60))
    print("\n  Why that sentence, before the figures: A's own `why`")
    print("  field on four answers it rejected.\n")
    for cid in ("c14", "c17", "d11", "d20"):
        t = next(x for x in outputs(1) + outputs(2)
                 if x["case_id"] == cid)
        print(f"    {cid}  Q: {t['question'][:48]}")
        print(answer.wrap(f"A: {t['answer']}", "          ",
                          "              ", 62))
        print(answer.wrap(f"why: {byid[cid]['A']['why']}", "          ",
                          "              ", 62))
        print()
    tmpl = [r for r in rows
            if r["mine"] == "P" and r["A"]["first"] == "F"
            and "instead of" in r["A"]["why"].lower()]
    alarmed = [r for r in rows
               if r["mine"] == "P" and r["A"]["first"] == "F"]
    print("  Every one of those `why` lines has the same shape, and")
    print(f"  so do {len(tmpl)} of A's {len(alarmed)} false alarms: 'the answer")
    print("  provides X instead of Y'. Read the X in each one. A")
    print("  colour is what a colour code means; an amount is what")
    print("  'the most you will pay' asks for; 'we do not match' is")
    print("  the answer to 'do you match'. The instruction's own")
    print("  examples of the fault became a template, and the")
    print("  verdict followed the template rather than the answer.")
    print("  The sentence added to B is aimed at exactly that.\n")

    print("  1. SELF-AGREEMENT. The same case shown twice. No")
    print("     labels used, so this runs first.\n")
    print("     judge   same both times     flipped on")
    for name in JUDGES:
        f1 = column(rows, name, "first")
        f2 = column(rows, name, "second")
        same = sum(1 for a, b in zip(f1, f2) if a == b)
        flips = [r["case_id"] for r in rows
                 if r[name]["first"] != r[name]["second"]]
        print(f"       {name}     {same:3d} of {n}  {same/n:4.0%}"
              f"     {', '.join(flips) if flips else '(none)'}")
    worst = min(sum(1 for a, b in zip(column(rows, k, "first"),
                                      column(rows, k, "second"))
                    if a == b) for k in JUDGES)
    print(f"\n     Neither flips on more than {n - worst} of the {n},"
          f" which is")
    print("     the result chapter 31 says to get before labelling")
    print("     anything - and it is not enough on its own, as the")
    print("     next measurement shows.\n")

    print("  2. THE FLIP COUNT under an arbitrary change: the answer")
    print("     printed before the question instead of after. Still")
    print("     no labels.\n")
    print("     judge   fails Q first   fails A first   changed")
    for name in JUDGES:
        f1 = column(rows, name, "first")
        sw = column(rows, name, "swapped")
        ch = [r["case_id"] for r in rows
              if r[name]["first"] != r[name]["swapped"]]
        print(f"       {name}       {f1.count('F'):3d} of {n}"
              f"       {sw.count('F'):3d} of {n}      {len(ch):3d}")
    print("\n     Nothing changed but which of two blocks came")
    print("     first. A judge can be repeatable on the same prompt")
    print("     and still move with the order, because the two")
    print("     measurements are of different things: one asks")
    print("     whether it is consistent, the other whether it is")
    print("     consistent about the ANSWER.\n")

    print("  3. THE BASELINE. What a judge that says pass to")
    print("     everything scores on my labels. No judge needed.\n")
    base = sum(1 for m in mine if m == "P")
    print(f"     agrees with me on        {base:3d} of {n}"
          f"   {base/n:4.0%}")
    print(f"     of the {nf} failures, catches  0           0%\n")
    print("     That is what every figure below has to beat. It is")
    print(f"     high because the mode is rare: {nf} failures in"
          f" {n}")
    print("     answers.\n")

    print("  4. AGREEMENT WITH MY LABELS, split into the two numbers")
    print("     that matter, with chapter 20's interval and the")
    print("     labels each figure rests on.\n")
    for name in JUDGES:
        f1 = column(rows, name, "first")
        pairs = list(zip(mine, f1))
        agree, caught, real = figures(pairs)
        spec = [("agrees with me", agree, n, 0),
                ("of failures, caught", caught, nf, 1),
                ("of its alarms, real", real, f1.count("F"), 2)]
        print(f"     judge {name}")
        print("       figure                value  labels   interval")
        for label, value, labels, idx in spec:
            lo, hi = interval(pairs, idx)
            print(f"       {label:21s} {value:5.0%}  {labels:6d}"
                  f"   {lo:4.0%} to {hi:4.0%}")
        missed = [r["case_id"] for r in rows
                  if r["mine"] == "F" and r[name]["first"] == "P"]
        alarmed = [r["case_id"] for r in rows
                   if r["mine"] == "P" and r[name]["first"] == "F"]
        print(f"       missed {len(missed)}, false alarms"
              f" {len(alarmed)}")
        if missed:
            print(ids(missed))
        print()

    print("     Three readings of that block, cheapest first.\n")

    stats = {}
    for name in JUDGES:
        f1 = column(rows, name, "first")
        pairs = list(zip(mine, f1))
        agree, caught, real = figures(pairs)
        stats[name] = {
            "agree": agree, "caught": caught, "real": real,
            "alarms": f1.count("F"),
            "missed": sum(1 for m, j in pairs if m == "F" and j == "P"),
            "other": len([r["case_id"] for r in rows
                          if r["mine"] == "P"
                          and r[name]["first"] == "F"
                          and r["case_id"] in NOTES]),
        }

    below = [k for k, s in stats.items() if s["agree"] < base / n]
    word = ("Both are" if len(below) == len(stats)
            else f"{len(below)} of {len(stats)} are")
    print(f"     ONE. {word} below the baseline, and one sentence")
    print("     bought a great deal without rescuing either.\n")
    for name, s in stats.items():
        gap = base / n - s["agree"]
        word = "WORSE than" if gap > 0 else "better than"
        print(f"       judge {name}: {s['agree']:.0%} against the"
              f" baseline's {base/n:.0%},")
        print(f"                {abs(gap):.0%} {word} doing nothing")
    a, b = stats["A"]["agree"], stats["B"]["agree"]
    print(f"\n     One sentence moved the figure by {abs(b - a):.0%},"
          f" and it is")
    print("     still not enough. A judge this far below its")
    print("     baseline is")
    print("     a judge whose instructions are wrong. Chapter 31's")
    print("     step 4 is self-agreement and both of these pass it,")
    print("     so the rule that applies is the Tip after its step")
    print("     10: a judge answering a question about print order")
    print("     cannot be rescued by more labelling.\n")

    print("     TWO. The catch rate is not a measurement, and its")
    print("     interval says so by being degenerate.\n")
    for name, s in stats.items():
        f1 = column(rows, name, "first")
        lo, hi = interval(list(zip(mine, f1)), 1)
        print(f"       judge {name}: {s['caught']:.0%}, interval"
              f" {lo:.0%} to {hi:.0%}, {s['missed']} missed")
    if all(s["missed"] == 0 for s in stats.values()):
        print(f"\n     Neither missed one of the {nf}, so every resample")
        print(f"     of those {nf} is {nf} caught failures and the")
        print("     interval collapses onto a point. Chapter 41's")
        print("     name for that is a ceiling with no")
        print("     discriminating cases. A resampled interval")
        print("     reports the spread the resample can produce, so")
        print("     one with nothing to vary reports none - a width")
        print("     of zero here is the absence of evidence and not")
        print(f"     certainty. What it IS is a hypothesis worth")
        print(f"     testing on more than {nf} labels.\n")

    print("     THREE. What they are, read as what they would")
    print("     actually be used for.\n")
    print("       judge  flags  of which real  reading saved")
    for name, s in stats.items():
        print(f"         {name}    {s['alarms']:3d} of {n}"
              f"      {s['real']:4.0%}"
              f"        {1 - s['alarms'] / n:5.0%}")
    bb = stats["B"]
    print("\n     Read judge B's row as a sieve rather than as a")
    print(f"     measurement and it is not useless: flag"
          f" {bb['alarms']} answers")
    print(f"     of {n}, read those, and on this set you would have")
    print(f"     found {nf - bb['missed']} of the {nf} failures of this"
          f" mode having")
    print(f"     read {bb['alarms'] / n:.0%} of the output. That is chapter")
    print("     31's step 9 - decide")
    print("     which error you can afford - and a false alarm you")
    print("     clear by reading one answer is cheap. What you may")
    print("     NOT do is report the agreement figure, because it")
    print("     is worse than reporting nothing.\n")
    for name, s in stats.items():
        print(f"     And {s['other']} of judge {name}'s false alarms are")
        print("     failures of another mode. An alarm on a real")
        print("     failure of another mode is still a false alarm")
        print("     for this judge, because this judge was asked one")
        print("     question.")
    print()
    flips = {name: len([r for r in rows
                        if r[name]["first"] != r[name]["swapped"]])
             for name in JUDGES}
    worst = max(flips.values())
    print("     The measurement that settles it, though, is")
    print("     measurement 2, and it needed no labels at all:")
    print(f"     {flips['A']} and {flips['B']} verdicts of {n} change when the")
    print("     answer is printed before the question. A judge whose")
    print(f"     verdict moves on {worst/n:.0%} of cases with the order")
    print("     of two blocks is not measuring the answer, and no")
    print("     amount of labelling would have told you so.")
```

```text
  Two judges, one mode: 'Answers a neighbouring question'.
  80 cases, 5 of which I labelled fail for THIS mode.
  17 of the 80 are failures of some kind, so 12 of
  them are passes as far as this judge is concerned.

  B is A plus one sentence:
    "An answer that contains what the question asked for is
    a pass, however short it is and however closely it
    quotes the document."

  Why that sentence, before the figures: A's own `why`
  field on four answers it rejected.

    c14  Q: What does the K mean at the end of HL-2208-K?
          A: K is black
          why: The answer provides information about the
              color instead of explaining what the 'K'
              signifies.

    c17  Q: Is the kettle dishwasher safe?
          A: Dishwasher safe: no. Rinse the inside and wipe
              the outside.
          why: The answer provides a rule about cleaning
              instead of directly addressing the question
              about dishwasher safety.

    d11  Q: What is the most you will pay as goodwill?
          A: 20 pounds per order
          why: The answer provides a specific amount instead
              of explaining the concept of goodwill.

    d20  Q: Do you match a marketplace seller's price?
          A: We do not match marketplace sellers
          why: The answer addresses what is not done instead
              of directly answering the question about
              matching prices.

  Every one of those `why` lines has the same shape, and
  so do 37 of A's 45 false alarms: 'the answer
  provides X instead of Y'. Read the X in each one. A
  colour is what a colour code means; an amount is what
  'the most you will pay' asks for; 'we do not match' is
  the answer to 'do you match'. The instruction's own
  examples of the fault became a template, and the
  verdict followed the template rather than the answer.
  The sentence added to B is aimed at exactly that.

  1. SELF-AGREEMENT. The same case shown twice. No
     labels used, so this runs first.

     judge   same both times     flipped on
       A      78 of 80   98%     c27, c32
       B      77 of 80   96%     c34, d21, d35

     Neither flips on more than 3 of the 80, which is
     the result chapter 31 says to get before labelling
     anything - and it is not enough on its own, as the
     next measurement shows.

  2. THE FLIP COUNT under an arbitrary change: the answer
     printed before the question instead of after. Still
     no labels.

     judge   fails Q first   fails A first   changed
       A        50 of 80        79 of 80       29
       B        34 of 80        65 of 80       31

     Nothing changed but which of two blocks came
     first. A judge can be repeatable on the same prompt
     and still move with the order, because the two
     measurements are of different things: one asks
     whether it is consistent, the other whether it is
     consistent about the ANSWER.

  3. THE BASELINE. What a judge that says pass to
     everything scores on my labels. No judge needed.

     agrees with me on         75 of 80    94%
     of the 5 failures, catches  0           0%

     That is what every figure below has to beat. It is
     high because the mode is rare: 5 failures in 80
     answers.

  4. AGREEMENT WITH MY LABELS, split into the two numbers
     that matter, with chapter 20's interval and the
     labels each figure rests on.

     judge A
       figure                value  labels   interval
       agrees with me          44%      80    32% to  54%
       of failures, caught    100%       5   100% to 100%
       of its alarms, real     10%      50     2% to  19%
       missed 0, false alarms 45

     judge B
       figure                value  labels   interval
       agrees with me          64%      80    54% to  74%
       of failures, caught    100%       5   100% to 100%
       of its alarms, real     15%      34     3% to  28%
       missed 0, false alarms 29

     Three readings of that block, cheapest first.

     ONE. Both are below the baseline, and one sentence
     bought a great deal without rescuing either.

       judge A: 44% against the baseline's 94%,
                50% WORSE than doing nothing
       judge B: 64% against the baseline's 94%,
                30% WORSE than doing nothing

     One sentence moved the figure by 20%, and it is
     still not enough. A judge this far below its
     baseline is
     a judge whose instructions are wrong. Chapter 31's
     step 4 is self-agreement and both of these pass it,
     so the rule that applies is the Tip after its step
     10: a judge answering a question about print order
     cannot be rescued by more labelling.

     TWO. The catch rate is not a measurement, and its
     interval says so by being degenerate.

       judge A: 100%, interval 100% to 100%, 0 missed
       judge B: 100%, interval 100% to 100%, 0 missed

     Neither missed one of the 5, so every resample
     of those 5 is 5 caught failures and the
     interval collapses onto a point. Chapter 41's
     name for that is a ceiling with no
     discriminating cases. A resampled interval
     reports the spread the resample can produce, so
     one with nothing to vary reports none - a width
     of zero here is the absence of evidence and not
     certainty. What it IS is a hypothesis worth
     testing on more than 5 labels.

     THREE. What they are, read as what they would
     actually be used for.

       judge  flags  of which real  reading saved
         A     50 of 80       10%          38%
         B     34 of 80       15%          57%

     Read judge B's row as a sieve rather than as a
     measurement and it is not useless: flag 34 answers
     of 80, read those, and on this set you would have
     found 5 of the 5 failures of this mode having
     read 42% of the output. That is chapter
     31's step 9 - decide
     which error you can afford - and a false alarm you
     clear by reading one answer is cheap. What you may
     NOT do is report the agreement figure, because it
     is worse than reporting nothing.

     And 7 of judge A's false alarms are
     failures of another mode. An alarm on a real
     failure of another mode is still a false alarm
     for this judge, because this judge was asked one
     question.
     And 4 of judge B's false alarms are
     failures of another mode. An alarm on a real
     failure of another mode is still a false alarm
     for this judge, because this judge was asked one
     question.

     The measurement that settles it, though, is
     measurement 2, and it needed no labels at all:
     29 and 31 verdicts of 80 change when the
     answer is printed before the question. A judge whose
     verdict moves on 39% of cases with the order
     of two blocks is not measuring the answer, and no
     amount of labelling would have told you so.
```

**The judge is worse than doing nothing, twice, and the reason it is worth four hundred and
eighty calls to find that out is that every step on the way says something different.**

**Start with the `why` field, because reading the judge's own output is chapter 30's method
turned on the judge.** Judge A rejects *K is black* as *the answer provides information about the
colour instead of explaining what the 'K' signifies*. It rejects *20 pounds per order* as *a
specific amount instead of explaining the concept of goodwill*. Thirty-seven of its forty-five
false alarms carry the words *instead of*. **The instruction's own examples of the fault — it
gives a rule when a figure was asked for, it says what not to do when asked what to do — became
a template, and the verdict followed the template rather than the answer.** A judge asked for a
verdict and a reason will give you a reason that fits the verdict, and the reason is where you
can see that happening.

**Self-agreement is high and tells you nothing you can use.** Judge A holds its verdict on 78 of
80 showings, judge B on 77. Chapter 31 says to run this first and it is right: a judge that
changes its mind cannot be validated, only fixed. What this measurement cannot see is a judge
that is consistently wrong, and both of these are.

**The flip count is the measurement that settles it, and it needed no labels either.** Print the
answer before the question instead of after and judge A's verdict changes on 29 of 80 cases and
judge B's on 31. Its rejection rate goes from 50 to 79 of 80 for A, and from 34 to 65 for B.
**Nothing changed but which of two blocks came first.** Chapter 31 makes this point with a
pairwise judge and says in a Note that the same procedure applies to any arbitrary element of a
judge's prompt; this is that Note, measured. A verdict that moves on 36 and 39 per cent of cases
with the print order is not a verdict about the answer, and no amount of labelling would have
revealed it.

**Then the baseline, which is the number the rest of the chapter's figures have to beat.** A
judge that says pass to everything agrees with me on 75 of 80, which is 94 per cent, and finds
nothing. It is high because the mode is rare — five failures in eighty answers — and chapter 31
says exactly this: on a working application the baseline is high precisely because the
application mostly works.

**Judge A scores 44 per cent and judge B 64, so they are 50 and 30 points *below* doing
nothing.** That is a long way outside anything chapter 31's two judges did: against a baseline of
80 per cent its judge A scored 85 and its judge B 82, so both were above it. **And the one
sentence added to B moved the figure by twenty points**, which is the largest single effect in
this chapter and still leaves the judge unusable. **The rung of chapter 31's advice this lands on
is worth getting right.** Its step 4 is self-agreement, and both judges pass that. The rule that
applies here is the Tip after its step 10: a judge that disagrees with itself *or that is
answering a question about print order* cannot be rescued by more labelling. Both of these are
the second kind, and step 5 — vary the arbitrary element and count the flips — is what found
it.

**The catch rate reads 100 per cent for both and is not a measurement.** Neither judge missed one
of the five, so every resample of five caught failures is five caught failures, and the interval
collapses onto a point: 100 per cent to 100 per cent. Chapter 41's name for a figure of that
shape is a ceiling with no discriminating cases, and that is the right name for it — **a
resampled interval reports the spread the resample can produce, and a resample with nothing to
vary produces none.** A width of zero here is the absence of evidence wearing the costume of
certainty, which is the opposite of what a narrow interval usually means. What the figure is, is
a hypothesis about five answers that would need more than five labels to test — step 4's bill
arriving for the third time.

**And read the last block as what the judge would be used for rather than as a score.** Judge B
flags 34 of 80 answers, 15 per cent of them real, and on this set you would have found all five
failures of the mode having read 42 per cent of the output. **As a sieve that is worth having**;
as a reported agreement figure it is worse than reporting nothing. Chapter 31's step 9 is the
decision: a false alarm you clear by reading one answer is cheap, and the same judge gating a
release would teach everybody to ignore it. What you may not do is quote the 64 per cent.

> **Warning:** Seven of judge A's 45 false alarms and four of judge B's 29 are real failures —
> of *other* modes. It is tempting to score those as hits, and it is wrong: this judge was asked
> one question, and an answer it rejects for the wrong reason is an answer it has not judged.
> Chapter 30's rule that a check reaches outside the mode it was built for is a fact about
> coverage, not a licence to re-credit the alarm.

> **Note:** Both judges catching all five is itself a hint about what is wrong with them, and the
> cleanest way to see it is the extreme: a judge that rejects all 80 answers catches every failure
> there is, at a precision of 6 per cent. Rejecting 34 of 80 is not that, and it is a long way
> towards it. **A catch rate is only interesting beside the alarm count**, which is why chapter 31
> insists on reporting two numbers and why neither is deducible from the single agreement
> figure.

> **Tip:** Look at where the 480 calls go. Measurements 1 and 2 use all of them between them —
> the same showing, a second showing, and a reordered showing. Measurements 3 and 4 reuse the
> first showing and cost nothing extra; what they cost is the labelling, which is eighty answers
> read by a person. **So the entire API budget of this step buys the two measurements that need
> no labels**, which is the right way round. Run them on your own judge before you label a single
> case: had I stopped after measurement 2 I would have learnt the one thing that decided it.
## Step 7: A Regression Set That Can See a Regression

Chapter 33 owns the set you keep and assumes a verdict. The verdict here is the one step 5 built,
because step 6's judge does not ship — and it is [**five**]{.noindex} of step 5's six code checks, not six.
`the answer is not a refusal` is left out, and leaving it out is the first thing this step gets
right: step 5 measured it at three alarms and no failures, so every answer it rejects is a
correct refusal. **A check that fires only on correct answers is not a verdict.** Left in, it
would have put a floor under the pass count that nothing in the output would show, and the
program prints how big: **one case, `c40`, unable to pass any of its six runs** — in a step whose
whole argument is that you read the list and not the score. Step 5's figure was three alarms, and
on the re-run it is one, because `c13` stops refusing and `c38` refuses in words the phrase list
does not hold. **A check's own alarm count is not stable either**, which is a second reason not to
build a verdict out of one you have not measured on the data you are about to use it on.

The change is one sentence added to chapter 45's instruction, aimed at the mode the code checks
cover: *give the id of the passage the quote is copied from, and copy the quote exactly, with no
words left out.* To keep the change attributable, the passages are held at exactly what version 1
sent — re-running retrieval under a longer instruction would move the budget fill as well, and
then two things would have changed.

```python
"""The regression set, one change to the system, and repeats.

Chapter 33 owns all of this and assumes a verdict. The verdict here
is the one step 5 built: an answer passes when every code check
passes. That is the whole of what this set can see, and the end of
the program says which modes it is therefore blind to.

The change is one sentence in the instruction, aimed at the mode the
code checks cover. To keep the change attributable, the passages are
held at exactly what version 1 sent - re-running retrieval under a
longer instruction would change the budget fill as well, and then
two things would have moved (chapter 18's rule, and chapter 28 owns
the budget arithmetic).

    python3 regress.py        writes runs.json, 480 calls

Three repeats of each case against each version, because chapter 33
is explicit that one run of a comparison reports the dice.
"""
import json
import pathlib

import answer
import checks
from modes import MODE
from notes import NOTES
from run import outputs

OUT = pathlib.Path("runs.json")
REPEATS = 3

#  What I found on READING the re-run answers, case by case, the way
#  step 2 read the first eighty. This is a label and not a
#  measurement, which is why it is written out here beside the notes
#  it is a continuation of.
REREAD = {
 "c13": "the labelled run refused this correctly, because the corpus"
        " holds no price for the kettle. Both versions of the re-run"
        " answer it instead: version 1 gives the replacement"
        " FILTER's price, version 2 gives what the product code"
        " means. Three repeats each, stable, and every check in the"
        " verdict passes all six times",
}

# Step 5 measured `the answer is not a refusal` at three alarms and no
# failures on this application: every answer it rejects is a correct
# refusal of a question the corpus cannot answer. A check that fires
# only on correct answers is not a verdict, so it is not in this one.
# How many cases it would floor is a question about THIS data and the
# program prints it rather than carrying step 5's three over.
DROPPED = "answer is not a refusal"
VERDICT = [c for c in checks.CODE if c[0] != DROPPED]

# One sentence added to chapter 45's instruction, and nothing else.
ADDED = (" Give the id of the passage the quote is copied from, and "
         "copy the quote exactly, with no words left out."
         )
V1 = answer.INSTRUCTION
V2 = answer.INSTRUCTION.replace(
    "and give that passage's id.",
    "and give that passage's id." + ADDED)
VERSIONS = {"v1": V1, "v2": V2}
assert V2 != V1


def context(instruction, question, kept):
    body = "\n".join(f"[{c}] {checks.search.BY_ID[c]['text']}"
                     for c in kept)
    return f"{instruction}\n\n{body}\n\nQuestion: {question}"


def one(instruction, t):
    d = answer.ask(context(instruction, t["question"],
                           t["passages_sent"]))
    raw = d["choices"][0]["message"]["content"]
    try:
        reply = json.loads(raw)
    except json.JSONDecodeError:
        reply = {"answer": raw, "citations": []}
    return {"case_id": t["case_id"],
            "question": t["question"],
            "passages_sent": t["passages_sent"],
            "answer": reply.get("answer", ""),
            "citations": reply.get("citations", [])}


def run():
    ts = outputs(1) + outputs(2)
    rows = []
    total = len(ts) * len(VERSIONS) * REPEATS
    done = 0
    for t in ts:
        for v, instruction in VERSIONS.items():
            for r in range(1, REPEATS + 1):
                out = one(instruction, t)
                out["version"], out["repeat"] = v, r
                rows.append(out)
                done += 1
        print(f"  {t['case_id']} {done:3d}/{total}", flush=True)
    OUT.write_text(json.dumps(rows, indent=1))
    return rows


def runs():
    return json.loads(OUT.read_text()) if OUT.exists() else run()


def verdict(row):
    """The only verdict this set has: every code check in VERDICT
    passes. Five of step 5's six; see DROPPED above."""
    return "P" if all(fn(row) for _, fn, _ in VERDICT) else "F"


def grid(rows):
    out = {}
    for r in rows:
        out.setdefault((r["case_id"], r["version"]), []).append(verdict(r))
    return out


def self_quoted(row):
    """Citations whose quote is in the ANSWER and not in the passage
    they name. A quote that can be found in the model's own sentence
    and nowhere else is the model citing itself."""
    n = 0
    for c in row["citations"]:
        q = checks.trim(c.get("quote", ""))
        unit = checks.search.BY_ID.get(c.get("id"))
        in_passage = unit is not None and q in checks.norm(unit["text"])
        in_answer = bool(q) and q in checks.norm(row["answer"])
        n += in_answer and not in_passage
    return n


def majority(vs):
    """Chapter 33's rule: a case is not a failure until it fails MORE
    often than it passes, so a tie is a pass."""
    return "F" if vs.count("F") * 2 > len(vs) else "P"


if __name__ == "__main__":
    rows = runs()
    g = grid(rows)
    cases = sorted({c for c, _ in g})
    fails = set(NOTES)
    where = {c: m for m, cs in MODE.items() for c in cs}

    unstable = [c for c in cases
                if any(len(set(g[(c, v)])) > 1 for v in VERSIONS)]
    print(f"  {len(cases)} cases, {len(VERSIONS)} versions,"
          f" {REPEATS} repeats each"
          f" = {len(rows)} calls")
    print(f"  the verdict is {len(VERDICT)} of step 5's"
          f" {len(checks.CODE)} code checks. Left out:")
    print(f"  {DROPPED!r}, which step 5 measured")
    print("  at three alarms and no failures")
    fn = next(f for n_, f, _ in checks.CODE if n_ == DROPPED)
    floored = sorted({r["case_id"] for r in rows if not fn(r)})
    always = [c for c in floored
              if all(not fn(r) for r in rows if r["case_id"] == c)]
    print(f"  on this run it fires on {len(floored)} case(s),"
          f" {len(always)} of them in")
    print(f"  every run: {', '.join(always) if always else '(none)'}."
          f" Left in, that is the")
    print("  floor it would have put under both pass counts\n")
    print(f"  {len(cases) - len(unstable)} cases gave the same verdict"
          f" all {REPEATS} times.")
    print(f"  {len(unstable)} did not:"
          f" {', '.join(unstable) if unstable else '(none)'}\n")

    for v in VERSIONS:
        m = [majority(g[(c, v)]) for c in cases]
        print(f"    {v}  {m.count('P')} of {len(cases)} pass"
              f"   {m.count('P')/len(cases):.0%}")

    broke = [c for c in cases
             if majority(g[(c, "v1")]) == "P"
             and majority(g[(c, "v2")]) == "F"]
    fixed = [c for c in cases
             if majority(g[(c, "v1")]) == "F"
             and majority(g[(c, "v2")]) == "P"]
    print(f"\n  Read it as a list, not a score."
          f" {len(fixed)} fixed, {len(broke)} broken.")
    print(f"    fixed:  {', '.join(fixed) if fixed else '(none)'}")
    print(f"    broken: {', '.join(broke) if broke else '(none)'}\n")

    print("  And now chapter 33's trap, on this data. The set you")
    print("  would have kept after the first reading is the cases")
    print(f"  that failed, which is {len(fails)} of the {len(cases)}. Run only")
    print("  those:\n")
    sub = [c for c in cases if c in fails]
    s_broke = [c for c in sub
               if majority(g[(c, "v1")]) == "P"
               and majority(g[(c, "v2")]) == "F"]
    s_fixed = [c for c in sub
               if majority(g[(c, "v1")]) == "F"
               and majority(g[(c, "v2")]) == "P"]
    print(f"    {len(s_fixed)} fixed, {len(s_broke)} regressions found,"
          f" against {len(broke)} real.")
    outside = [c for c in broke if c not in fails]
    if outside and len(outside) == len(broke):
        head = ("The breakage is" if len(broke) == 1
                else f"All {len(broke)} breakages are")
        print(f"    {head} outside that set: {', '.join(outside)}")
    else:
        print(f"    {len(outside)} of the {len(broke)} outside that set:"
              f" {', '.join(outside) if outside else '(none)'}")
    if outside:
        was = "It passed" if len(outside) == 1 else "Each of them passed"
        print(f"    {was} version 1, which is exactly why a set of")
        print("    past failures does not contain it.\n")

    print("  The breakage is worth opening, because the change")
    print("  caused it and the check caught it.\n")
    for cid in broke:
        for v in VERSIONS:
            r = next(x for x in rows if x["case_id"] == cid
                     and x["version"] == v and x["repeat"] == 1)
            fired = [n for n, fn, _ in VERDICT if not fn(r)]
            print(f"    {cid} {v}  {verdict(r)}  self-quoted citations:"
                  f" {self_quoted(r)}")
            for c in r["citations"]:
                print(f"       cites {c.get('id')}")
                print(answer.wrap(f'"{c.get("quote", "")[:70]}"',
                                  "         ", "         ", 60))
            if fired:
                print(f"       fired: {', '.join(fired)}")
    print()
    for v in VERSIONS:
        rs = [r for r in rows if r["version"] == v]
        cs = sorted({r["case_id"] for r in rs if self_quoted(r)})
        print(f"    {v}: {sum(self_quoted(r) for r in rs)} citations quote"
              f" the ANSWER and not the")
        print(f"        passage they name, over {len(cs)} case(s):"
              f" {', '.join(cs) if cs else '(none)'}")
    counts = {v: sum(self_quoted(r) for r in rows
                     if r["version"] == v) for v in VERSIONS}
    ratio = (counts["v2"] / counts["v1"]) if counts["v1"] else None
    times = f"{ratio:.0f} times as often" if ratio else "where v1 had none"
    print("\n  The sentence added to version 2 asked for the quote to")
    print("  be copied exactly with no words left out. What it")
    print(f"  produced {times} is a citation quoting the")
    print("  model's own sentence rather than the document - which")
    print("  is a quote that looks more exact and is not a quote at")
    print("  all. The check that caught it is the same check the")
    print("  change was written to satisfy.\n")

    print("  Then the cases that would not hold still, which chapter")
    print(f"  33's step 5 is about and which this run has"
          f" {len(unstable)} of.\n")
    print("    case   v1 fails of 3   v2 fails of 3   reported as")
    for c in unstable:
        a = [verdict(r) for r in rows if r["case_id"] == c
             and r["version"] == "v1"]
        b = [verdict(r) for r in rows if r["case_id"] == c
             and r["version"] == "v2"]
        ma, mb = majority(a), majority(b)
        tag = ("a regression" if ma == "P" and mb == "F"
               else "a fix" if ma == "F" and mb == "P"
               else "no change")
        print(f"    {c}        {a.count('F')}               "
              f"{b.count('F')}           {tag}")
    print("\n  Read the rows where the report says no change. The")
    print("  verdict is the majority of three and the tie-break is")
    print("  chapter 33's - a case is not a regression until it")
    print("  fails MORE often than it passes - so a case that moved")
    print("  from failing twice in three to failing three times in")
    print("  three is reported as nothing having happened. The")
    print("  movement is real and the set is silent about it,")
    print("  because a majority verdict throws away the rate.\n")

    print("  Then the part a score hides even when the set is whole.")
    print("  What the verdict can SEE, by mode. The answers here are")
    print("  the eighty I labelled, not a re-run of them, because the")
    print("  question is which of MY failures this verdict fires on:")
    print()
    labelled = outputs(1) + outputs(2)
    seen = {t["case_id"] for t in labelled if verdict(t) == "F"}
    print("    mode                                 failures  seen")
    nseen = 0
    for m, cs in MODE.items():
        k = len(set(cs) & seen)
        nseen += k > 0
        print(f"    {m:36s} {len(cs):6d} {k:6d}")
    blind = sorted(fails - seen)
    print(f"\n  The verdict fires on some failure of {nseen} of the"
          f" {len(MODE)} modes")
    print(f"  and on none of the other {len(MODE) - nseen}."
          f" {len(blind)} of the {len(fails)} failures")
    print("  are invisible to this set, because no check of mine")
    print("  fires on them and the judge did not ship. A regression")
    print("  in any of those modes passes silently, and the set")
    print("  reports green.\n")

    by_id = {t["case_id"]: t for t in labelled}
    first = {c: next(r for r in rows if r["case_id"] == c
                     and r["version"] == "v1" and r["repeat"] == 1)
             for c in cases}
    changed = [c for c in cases
               if first[c]["answer"].strip() != by_id[c]["answer"].strip()]
    moved = sorted(c for c in cases
                   if verdict(by_id[c]) != verdict(first[c]))
    silent = [c for c in changed if c not in moved]
    print("  Before any of that, the thing the table cannot show.")
    print(f"  Run version 1 again and {len(changed)} of the {len(cases)}"
          f" answers come back")
    print(f"  different in their text. The verdict moves on"
          f" {len(moved)} of them")
    print(f"  and not on the other {len(silent)}. Same system, same")
    print("  passages, same instruction, and the set is silent about")
    print("  every one of those changes.\n")
    for cid, note in REREAD.items():
        print(f"  I read {cid} again, and it is the one I would stop")
        print("  a release for:\n")
        print(f"    {cid}  {by_id[cid]['question']}")
        shown = [("labelled", by_id[cid])]
        shown += [(f"{v} r{r}", next(x for x in rows
                                     if x["case_id"] == cid
                                     and x["version"] == v
                                     and x["repeat"] == r))
                  for v in VERSIONS for r in (1,)]
        for tag, r in shown:
            print(f"      {tag:9s} {verdict(r)}")
            print(answer.wrap(r["answer"], "          ", "          ", 58))
        print()
        print(answer.wrap(note, "    ", "    ", 60))
        print()
        print("  So a correct refusal became a wrong answer, and")
        print("  BOTH versions do it - which means the change under")
        print("  test did not cause it and is not excused by it")
        print("  either. The regression set reports nothing: not in")
        print("  the fixed list, not in the broken list, because no")
        print("  check of mine fires on an answer that is simply")
        print("  wrong. This is the same blind spot the mode table")
        print("  names, arriving as an actual regression rather than")
        print("  as a count.\n")

    if moved:
        noun = "case" if len(moved) == 1 else "cases"
        print(f"  And the {len(moved)} {noun} the verdict DID move on,")
        print("  where a re-run looks like a result:\n")
        for c in moved:
            for tag, r in (("labelled", by_id[c]), ("re-run  ", first[c])):
                fired = [n for n, fn, _ in VERDICT if not fn(r)]
                print(f"    {c} {tag} {verdict(r)}  "
                      f"{', '.join(fired) if fired else '(nothing fires)'}")
                print(answer.wrap(r["answer"], "         ", "         ",
                                  58))
                ids = [x.get("id") for x in r["citations"]]
                print(f"         cites {len(ids)}:"
                      f" {', '.join(ids) if ids else '(none)'}")
            print()
        grew = [c for c in moved
                if len(first[c]["citations"]) > len(by_id[c]["citations"])]
        print(f"  {len(grew)} of those {len(moved)} grew a citation between the")
        print("  two runs, and for each of those that is the whole")
        print("  mechanism: another citation appeared, its quote")
        print("  abridges the middle of the passage, and the quote")
        print("  check fires. Nothing about the change under test is")
        print("  involved.\n")
        print("  So a mechanical verdict is a function of an answer,")
        print("  and asking the same system twice gives two answers.")
        print("  The mode table below uses the answers I labelled,")
        print("  because those are the ones the labels belong to.\n")
    print("  That is two blind spots in one set and they are")
    print("  different. Chapter 33's is a blindness to cases that")
    print("  have never failed, and it is fixed by keeping passing")
    print("  cases. This one is a blindness to KINDS, and no amount")
    print("  of cases fixes it: it is fixed by building the check.")
```

```text
  80 cases, 2 versions, 3 repeats each = 480 calls
  the verdict is 5 of step 5's 6 code checks. Left out:
  'answer is not a refusal', which step 5 measured
  at three alarms and no failures
  on this run it fires on 1 case(s), 1 of them in
  every run: c40. Left in, that is the
  floor it would have put under both pass counts

  77 cases gave the same verdict all 3 times.
  3 did not: c07, c20, d26

    v1  73 of 80 pass   91%
    v2  74 of 80 pass   92%

  Read it as a list, not a score. 2 fixed, 1 broken.
    fixed:  c09, d07
    broken: c12

  And now chapter 33's trap, on this data. The set you
  would have kept after the first reading is the cases
  that failed, which is 17 of the 80. Run only
  those:

    2 fixed, 0 regressions found, against 1 real.
    The breakage is outside that set: c12
    It passed version 1, which is exactly why a set of
    past failures does not contain it.

  The breakage is worth opening, because the change
  caused it and the check caught it.

    c12 v1  P  self-quoted citations: 0
       cites product-kettle-hl-2208#0
         "A 1.7 litre jug kettle with a 3000 W element, a
         concealed element and "
    c12 v2  F  self-quoted citations: 1
       cites product-kettle-hl-2208#0
         "HL-2208 is a 1.7 litre jug kettle with a 3000 W
         element, a concealed e"
       fired: quote is in the passage cited

    v1: 2 citations quote the ANSWER and not the
        passage they name, over 1 case(s): d07
    v2: 8 citations quote the ANSWER and not the
        passage they name, over 3 case(s): c07, c12, d26

  The sentence added to version 2 asked for the quote to
  be copied exactly with no words left out. What it
  produced 4 times as often is a citation quoting the
  model's own sentence rather than the document - which
  is a quote that looks more exact and is not a quote at
  all. The check that caught it is the same check the
  change was written to satisfy.

  Then the cases that would not hold still, which chapter
  33's step 5 is about and which this run has 3 of.

    case   v1 fails of 3   v2 fails of 3   reported as
    c07        2               3           no change
    c20        2               3           no change
    d26        3               2           no change

  Read the rows where the report says no change. The
  verdict is the majority of three and the tie-break is
  chapter 33's - a case is not a regression until it
  fails MORE often than it passes - so a case that moved
  from failing twice in three to failing three times in
  three is reported as nothing having happened. The
  movement is real and the set is silent about it,
  because a majority verdict throws away the rate.

  Then the part a score hides even when the set is whole.
  What the verdict can SEE, by mode. The answers here are
  the eighty I labelled, not a re-run of them, because the
  question is which of MY failures this verdict fires on:

    mode                                 failures  seen
    Citation points somewhere else            5      5
    Answers a neighbouring question           5      0
    Answers for one case when two apply       4      0
    Not an answer at all                      1      1
    Citation does not support the claim       1      0
    Contradicts the passage                   1      0

  The verdict fires on some failure of 2 of the 6 modes
  and on none of the other 4. 11 of the 17 failures
  are invisible to this set, because no check of mine
  fires on them and the judge did not ship. A regression
  in any of those modes passes silently, and the set
  reports green.

  Before any of that, the thing the table cannot show.
  Run version 1 again and 8 of the 80 answers come back
  different in their text. The verdict moves on 1 of them
  and not on the other 7. Same system, same
  passages, same instruction, and the set is silent about
  every one of those changes.

  I read c13 again, and it is the one I would stop
  a release for:

    c13  How much does the HL-2208 kettle cost?
      labelled  P
          The price of the HL-2208 kettle is not
          mentioned in the passages.
      v1 r1     P
          The price of the replacement filter is 4.50
          pounds.
      v2 r1     P
          So `HL-2208-K` is a small appliance, product
          2208, in black.

    the labelled run refused this correctly, because the
    corpus holds no price for the kettle. Both versions of
    the re-run answer it instead: version 1 gives the
    replacement FILTER's price, version 2 gives what the
    product code means. Three repeats each, stable, and
    every check in the verdict passes all six times

  So a correct refusal became a wrong answer, and
  BOTH versions do it - which means the change under
  test did not cause it and is not excused by it
  either. The regression set reports nothing: not in
  the fixed list, not in the broken list, because no
  check of mine fires on an answer that is simply
  wrong. This is the same blind spot the mode table
  names, arriving as an actual regression rather than
  as a count.

  And the 1 case the verdict DID move on,
  where a re-run looks like a result:

    c07 labelled P  (nothing fires)
         Standard delivery is 3.99 pounds on orders under
         40 pounds.
         cites 1: delivery-fees#1
    c07 re-run   F  quote is in the passage cited
         Standard delivery is 3.99 pounds on orders under
         40 pounds and free on orders of 40 pounds or
         more.
         cites 2: delivery-fees#1, delivery-exceptions#2

  1 of those 1 grew a citation between the
  two runs, and for each of those that is the whole
  mechanism: another citation appeared, its quote
  abridges the middle of the passage, and the quote
  check fires. Nothing about the change under test is
  involved.

  So a mechanical verdict is a function of an answer,
  and asking the same system twice gives two answers.
  The mode table below uses the answers I labelled,
  because those are the ones the labels belong to.

  That is two blind spots in one set and they are
  different. Chapter 33's is a blindness to cases that
  have never failed, and it is fixed by keeping passing
  cases. This one is a blindness to KINDS, and no amount
  of cases fixes it: it is fixed by building the check.
```

**Start with the figure before the comparison, because it is the one that decides how to read
everything after it.** Run version 1 again — the same system, the same passages, the same
instruction — and **eight of the eighty answers come back with different text**. The verdict
moves on one of the eight and is silent about the other seven. Before any change has been tested,
the set has told you that a tenth of its cases are not the cases you labelled.

**And one of those seven is a regression the set reports as nothing at all.** `c13` asks how much
the kettle costs, which the corpus does not say, and the labelled run refused it correctly — step
5 held it up as one of the three correct refusals that make the refusal detector worthless. Run
version 1 again and all three repeats answer *"The price of the replacement filter is 4.50
pounds"*: the wrong product's price, a figure a customer would act on. Version 2's three repeats
answer *"So `HL-2208-K` is a small appliance, product 2208, in black"*, which is not an answer to
the question at all. **Every check in the verdict passes all six times.** It is not in the fixed
list and not in the broken list, because no check of mine fires on an answer that is merely
wrong.

**Then the comparison itself. As a score it is 73 of 80 against 74. As a list it is two fixes and
a breakage.** Chapter 33's sentence — a score is a net and a regression set is a list — is a
sentence until you have run one, and then it is 2 − 1 = +1.

**The two fixes are the change working exactly as designed.** On `c09` version 1 quoted
*delivery-exceptions*' wording and attributed it to the PDF; version 2 quotes the PDF's own
wording, which says *services* where the policy says *delivery*. On `d07` version 1 quoted
*refunds-policy*'s sentence and credited it to *refunds-faq*; version 2 quotes the sentence
*refunds-faq* actually contains. Two of the five citation failures are gone and the answers are no
worse.

**And the breakage is the chapter's best single result, because the fix caused it and the check
the fix was written to satisfy is what caught it.** On `c12` version 2 cites the kettle document
with the quote *"HL-2208 is a 1.7 litre jug kettle with a 3000 W element…"* — and that sentence is
not in the kettle document. It is the model's own answer. The document says *"A 1.7 litre jug
kettle…"*. Asked to copy the quote exactly, the model copied itself.

**That is measurable rather than anecdotal, which is why the program measures it.** A citation
whose quote can be found in the answer and not in the passage it names is the model citing
itself: version 1 has two such citations across one case, version 2 has eight across three.
**The instruction written to make citations more exact made them four times more often not
citations at all.**

**Then chapter 33's trap, on real data.** The set you would have kept after step 2 is the cases
that failed — seventeen of the eighty. Run only those and it reports two fixes and *zero
regressions*, when there is one. `c12` passed version 1, which is precisely why a set of past
failures does not contain it. Chapter 33 demonstrates this on twenty invented cases; it is the
same arithmetic and it does not care that these eighty are real.

**And then the three cases that would not hold still, which is chapter 33's step 5 happening
rather than being described.** Of eighty cases, seventy-seven gave the same verdict all three
times. The three that did not are reported as *no change*, and every one of them moved: `c07` and
`c20` went from failing twice in three to failing three times in three, and `d26` went the other
way. **A majority verdict throws away the rate**, and chapter 33's tie-break — a case is not a
regression until it fails more often than it passes — is what makes a two-in-three into a
three-in-three look like nothing. The movement is real and the report is silent.

**Last, the blind spot that is not chapter 33's.** The verdict fires on some failure of two of the
six modes and on none of the other four: five of five in *Citation points somewhere else*, one of
one in *Not an answer at all*, and nothing anywhere else. **Eleven of the seventeen failures are
invisible to this set**, which is step 5's count arriving again because it is the same count — the
checks are the same checks and the labelled answers are the same answers. A regression in any of
those four modes passes silently and the set reports green, which `c13` is not a hypothetical
about but an instance of.

**Two blind spots in one set, and they are different things.** Chapter 33's is a blindness to
*cases* that have never failed, and it is fixed by keeping the passing cases you have — which this
set does, all eighty of them. This one is a blindness to *kinds*, and no number of cases fixes it.
It is fixed by building the check, which is step 5, which is why the order of this chapter is the
order it is. And a case outside the eighty is outside the set however the set is built, which is a
third thing again and the reason step 2 never stops being worth doing.

> **Warning:** The temptation at the end of a step like this is to report the one point. Do not.
> The honest report of version 2 is: two citation failures fixed, one new failure of the same mode
> introduced, self-quoted citations up from two to eight, three cases whose failure rate moved
> without the verdict moving, one correct refusal turned into a wrong answer in both versions
> where the set cannot see it, and no information at all about eleven of the seventeen known
> failures. **Every one of
> those sentences is actionable and the point is not.**

> **Note:** Version 2 is probably still the version to ship, and saying so is not a contradiction.
> It fixes two real failures, its breakage is caught by a check that runs on every request, and
> the self-quoting it causes is detectable by the same check. `c13` is the one that would stop me,
> and it is not evidence against version 2: version 1 does the same thing on the same case. What
> you may not do is ship on the strength of 74 against 73 — chapter 20's question of whether a
> one-case difference on eighty cases is real has an obvious answer, and this comparison never
> needed a bootstrap, because the list decided it.

> **Tip:** The cheapest improvement available to this set is not more cases and not a better
> judge. It is **recording the fail count rather than the verdict**: three of eighty cases moved
> and the set could have said so, for the cost of one extra column. Chapter 33's step 5 says a
> case near the threshold crosses it for free; the column is what makes the crossing visible
> instead of silent. The second cheapest is [**recording the answer text**]{.noindex}, which is what turned up
> `c13`: eight answers changed and the verdict could see one of them.
## Summary, Key Terms, and Review Questions

### Summary

Chapter 45's pipeline, eighty questions written against the shipped corpus, and chapters 30, 31
and 33 run end to end on the answers. **The problem statement's forty real outputs hold eight
failures, not forty** — the system fails on about a fifth of what it is asked — so chapter 30's
*about forty failures* is two hundred answers read, and the method's afternoon is an afternoon per
forty *failures*. Eight failures group into five modes with three resting on a single answer,
which is a guess about a kind rather than a kind, so a second forty go in, aimed at the kinds that
had failed. **The aim did not show up in the rate**: eight failures in the first forty at 20 per
cent and nine in the second at 22, and one failure in forty separates nothing, so whether the aim
worked is a question these two batches cannot answer. What it did buy is members.

**The verdict rule is written down before any label, and that is what let somebody else apply
it.** A case fails if a customer acting on the answer would be misinformed, or if the answer does
not contain what was asked, or if the citation does not let the customer check it. **Five of the
seventeen failures are answers a customer would act on correctly**, failing on the citation alone,
so a rule that asked only whether the answer was right would not have the largest mode in the
chapter at all. Chapter 30's lab asks for a second person reading the same material; a second
reader was given the eighty answers, their questions, the passages each was sent, the corpus and
the rule — and not my labels. **We agree on 79 of 80.** The one disagreement is `c04`, which I
pass and the second reader fails, and it is in the chapter because the arithmetic of being wrong
about it is the chapter's headline result.

**Seventeen failures, six named modes, and every note in exactly one of them.** Two pairs had to
be decided rather than fallen into, and both for the reason chapter 30 gives — two modes fixed in
different places must not be merged. *Citation points somewhere else* is a quote that is not where
the citation says it is; *Citation does not support the claim* is a real quote from a sent passage
that does not establish the sentence. *Answers a neighbouring question* is the wrong sentence
given; *Answers for one case when two apply* is a right sentence and a stop. Of each pair, one half
is a check in code and the other needs a judgement, which is what makes the split pay.

**Then the result the chapter exists for: the counts give the names and not the order.** The top
two modes hold five failures each, so which the table prints first is the sort order. Chapter 20's
resampling over the failures answers three different questions. The gap between the top two runs
from −0.353 to +0.353 at seventeen failures and narrows to ±0.087 at three hundred while staying
centred on zero — and **the resample draws from a pair that is exactly equal, so what it narrows
is the statement that they are equal and it never turns into an order.** The third mode's gap over
the singletons has a low end of −0.118 at seventeen, exactly zero at forty, +0.060 at a hundred:
that one is a real gap and it is affordable. And the three modes called large are the three largest
in 83 per cent of resamples at seventeen and 97 at forty. One cell of that table does not hold
still across seeds, and chapter 31's lab names the two reasons an interval does that; **counting
how many of sixty seeds move it, at three round counts, settles which one it is here**. Sixteen of
sixty move at ten thousand rounds, two at fifty thousand, none at two hundred thousand — too few
rounds, not too few labels, and read the table rather than the sentence, because two of sixty is
not none. The low end, which is the figure the argument rests on, is the same on all sixty seeds
at every round count in the table. At seventeen failures in eighty answers,
forty failures is a hundred and ninety answers read and a hundred is four hundred and seventy.
**Chapter 31 prices labelling failures as the expensive part of validating a judge; the bill is
already due at the taxonomy, before any judge exists.**

**And the table's shape is one judgement call from changing, in three directions.** The first forty's
largest mode comes **third** on the eighty — working the largest mode after forty answers would
have been working the wrong one, not because the first forty were unrepresentative but because
three against two is not a difference. Then each of the four arguable labels moves the top on its
own: `d09` scored a pass gives 5, 4, 4; `d05` scored a pass gives 5, 4, 4; `c04` scored a failure
gives 5, 5, 5; `c33` scored a failure gives 5, 5, 4. **Two of the four produce an order and the two
orders name different modes** — `d09` puts *Answers a neighbouring question* first and `d05` puts
*Citation points somewhere else* there. Not even the direction survives one reading.

**A check per mode, sorted by what it needs, and the code ones run.** Eleven checks, six code and
five judge, and chapter 31's rule appears in the `needs` column on its own: every code check
compares two things both literally present, every judge check needs a decision about meaning. Four
of the seven modes in that table have a code part — and read that against chapter 31's seven of
eight like for like before quoting it, because the seven includes chapter 30's refusal mode, which
none of these eighty answers is in. **Of my own six, three have a code part.** **The three citation
rows are chapter 28's**, with the offset check dropped, since this pipeline's instruction asks for
no offset and so makes no claim to verify, and one added that only a trace makes possible — was the
cited passage among the ones *sent*. Together they reject five answers, all five failures, all five
in the mode, none missed: a mode closed by a check that reads no prose.

**And the rule inside a check is where the work is, twice over.** A length threshold for *Not an
answer at all* rejects six correct short answers and no failures, and the longest answer it rejects
is twelve characters against the one real stub's forty-nine, so **length and stub-ness do not order
the same way at all**: the last character does the work and the length does none of it. The quote
check compared as it stands fires on eight answers, six of them failures; with a trailing full stop
trimmed it fires on five and all five are failures. **The two checks built on a hunch cover
nothing**: the invented-figure check fires on none of the eighty, and the refusal detector fires
three times on three correct refusals of questions the corpus cannot answer. Its mode has none of
the seventeen failures in it. All six code checks catch six of the seventeen, and the eleven left
are the honest list — including *Answers for one case when two apply*, four failures and the mode
the first forty called largest, which gets a row in the table and no check at all.

**One judge, for the largest mode code cannot reach, measured in chapter 31's order — and it is
worse than doing nothing, twice.** Self-agreement first, needing no labels: 78 of 80 for judge A and
77 for judge B, which chapter 31 says to establish before labelling and which cannot see a judge
that is consistently wrong. Then the flip count, still needing no labels: print the answer before
the question instead of after and A's verdict changes on 29 of 80 and B's on 31, with the rejection
rate going 50 → 79 and 34 → 65, which is 36 and 39 per cent of the eighty. **A verdict that moves
with the print order on that many is not a verdict about the answer.** Then the baseline, which needs labels and no judge:
pass-to-everything agrees on 75 of 80, which is 94 per cent, high because the mode is rare. **Judge
A scores 44 and judge B 64, so they are 50 and 30 points below doing nothing.** Reading the judge's
own `why` field says what is wrong — 37 of judge A's 45 false alarms carry the words *instead of*,
the shape the instruction's own examples of the fault suggested, so **the examples became a template
and the verdict followed the template**. One sentence aimed at that moved the figure twenty points,
the largest single effect in the chapter, and still left it unusable: the rule that applies is the
Tip after chapter 31's step 10, that a judge answering a question about print order cannot be
rescued by more labelling. The catch rate reads 100 per cent for both with an interval of 100 to
100, which is not a measurement but five failures none of which was missed — chapter 41's ceiling
with no discriminating cases, and **a resampled interval reports the spread the resample can
produce, so one with nothing to vary produces none.** What judge B is, is a sieve: 34 flags of 80,
15 per cent of them real, all five of that mode's failures found having read 42 per cent of the
output. Worth having; not a number to report.

**Last, the regression set, with the checks as its verdict because the judge did not ship — five of
the six, not six.** `the answer is not a refusal` is left out, because step 5 measured it at three
alarms and no failures: a check that fires only on correct answers is not a verdict, and left in it
would have put an invisible floor under the pass count. One sentence added to the instruction,
passages held at what version 1 sent so the change is attributable, three repeats of eighty cases
against each version. **Before any comparison, the figure that decides how to read the rest**: run
version 1 again and eight of the eighty answers come back different in their text, and the verdict
moves on one of the eight. **One of the other seven is a regression the set reports as nothing** —
`c13` asks a price the corpus does not hold, the labelled run refused it correctly, and all three
repeats of each version answer it instead, version 1 with the wrong product's price. Every check in
the verdict passes all six times. **As a score the change is 73 of 80 against 74. As a list it is
two fixes and a breakage** — chapter 33's *a score is a net and a regression set is a list*, arrived
at rather than quoted. The two fixes are the change working. **The breakage is the change backfiring
into the very check it was written to satisfy**: asked to copy the quote exactly, the model cited the
kettle document with a sentence from its own answer, and citations whose quote is in the answer and
not in the passage they name went from two across one case to eight across three. Run only the
seventeen past failures and the set reports two fixes and **zero regressions**, because `c12` passed
version 1 and a set of past failures cannot contain a case that has never failed. Seventy-seven of
eighty cases held their verdict all three times; the three that did not are all reported as *no
change* while every one of them moved between two failures in three and three in three, because **a
majority verdict throws away the rate**. And the verdict fires on some failure of two of the six
modes and on none of the other four: **eleven of the seventeen failures are invisible to the set**,
which is step 5's count arriving again because it is the same count. That is two blind spots and they
are different things — chapter 33's blindness to cases that never failed, fixed by keeping the
passing cases you have, and a blindness to *kinds*, which no number of cases fixes and only building
the check does. A case outside the eighty is outside the set however it is built, which is a third
thing again.

### Key Terms

| Term | Meaning |
|---|---|
| **Verdict rule** | The written statement of what counts as a failure, fixed before any labelling and kept beside the labels. What you count as a failure decides which modes you can find: five of this chapter's seventeen failures are answers a customer would act on correctly, and a rule asking only whether the answer was right would not have them. Written down, a second reader can apply it — here two readings of the same eighty agreed on 79. Chapter 33's criteria drift is this rule moving while nobody counts it |
| **Singleton mode** | A named failure mode resting on one failure. It is a guess about a kind rather than an established kind, and only more output settles which: of the three singletons after forty answers here, one became a group of five and two did not move |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Forty outputs against forty failures | Chapter 30's method wants about 40 *failures*. 17 in 80 answers here, so 40 failures is about 190 answers read and 100 is about 470 |
| What a taxonomy on 17 failures establishes | The names, not the order. The top two modes tied at 5, and the resampled gap between them ran −0.353 to +0.353 and stayed centred on zero at every size |
| When the order arrives | The third mode's gap over the singletons has a low end of −0.118 at 17 failures, 0.000 at 40 and +0.060 at 100. A resample drawn from an exactly equal pair narrows the statement that they are equal and never orders them |
| The singleton test | 3 of the first forty's 5 modes rested on one failure; one of the three became a group of five and two did not |
| How robust a mode table is | Four arguable labels each change the top of this one: 5,4,4 / 5,4,4 / 5,5,5 / 5,5,4. Two produce an order and the two orders name *different* modes, so not even the direction survives one reading |
| Two readings of one set | A second reader applying the same written rule to the same 80 answers agreed on 79. The rule is what makes that possible |
| The code/judge split, measured | 3 of my 6 modes had a code part — 4 of 7 including chapter 30's refusal mode, which has no members here, against chapter 31's 7 of 8. The six code checks caught 6 of 17 failures |
| Where a check's accuracy lives | In its rule. A length threshold rejected 6 correct answers and 0 failures, and the longest it rejected was 12 characters against the one real stub's 49. A quote compared as it stands fired on 8 (6 failures); trimmed of a trailing stop, on 5 (5 failures) |
| The two judge measurements needing no labels | Self-agreement — the same case twice — and the flip count under an arbitrary reordering. Here 78 and 77 of 80, then 29 and 31 of 80 verdicts changed by print order alone |
| A judge below its baseline | Baseline 94 per cent (the mode is rare); judge A 44, judge B 64. One sentence moved it 20 points and it still should not ship. That is an instructions problem, not a labels problem |
| A catch rate on five labels | 100 per cent with an interval of 100 to 100: nothing missed on five failures, so the resample has nothing to vary and reports no spread. A width of zero is the absence of evidence, not certainty |
| A score against a list | 73 of 80 against 74 of 80 is +1 point. The list is 2 fixed and 1 broken |
| What a majority verdict throws away | The rate. Three cases moved between 2-of-3 and 3-of-3 failures and all three were reported as no change |
| What a verdict without the text throws away | 8 of 80 answers came back different on a re-run of the same version; the verdict saw one of them, and one of the seven it missed was a correct refusal turned into a wrong figure |
| The two blind spots of a regression set | Cases that never failed — fixed by keeping the passing cases you have — and modes with no check, which no number of cases fixes. 11 of 17 failures were invisible here |

### Review Questions

1. You have forty real outputs from a working system and no metrics. What does chapter 30's
   method give you, and what does it not?
2. Your error analysis gives six named modes and you are about to work the largest. What do you
   check first?
3. How do you decide whether a check needs a model, and what did that decide here?
4. Your judge agrees with your labels on 64 per cent of cases. What do you do?
5. Your regression set reports no regressions. Give two different reasons that can be true and
   worthless.

### Review Answers

1. It gives the **names** of the kinds of wrong, and it does not give their **order** — and the
order is what chapter 30's *What To Actually Do* ends on, at step 8, *then fix the largest mode*.
Forty real outputs from a working system are not forty failures: here they were eight, because the
system fails on about a fifth of what it is asked, so chapter 30's forty failures is two hundred
answers read. Eight failures group into five modes with three of them resting on a single answer,
which is a guess about a kind rather than a kind, so I read forty more and got to seventeen
failures and six modes. On seventeen the six names are established, every one with a worked
example, and nothing about their order is: the top two hold five failures each, the resampled gap
between them runs from −0.353 to +0.353, and the mode the first forty called largest comes third on
the eighty. **What the names buy is the checks**, and a check does not need to know which mode is
biggest — three code checks built from one mode's name closed that mode outright. What the order
would buy is knowing which mode to spend a fortnight on, and that costs about a hundred failures,
which is about four hundred and seventy answers read. Chapter 31 prices labelling failures as the
expensive part of validating a judge; the bill arrives one step earlier, at the taxonomy, before
any judge exists.
2. Whether there is a largest — read the counts before acting on their order. Here the first two
modes hold five each, so which one the table prints first is the sort order and nothing else. Then
put chapter 20's resampling on the failures and ask the three questions the table invites
separately: is the first bigger than the second (no, and more failures will not change it, because
the resample draws from a pair that is exactly equal); is the third bigger than the singletons (its
low end is −0.118 at seventeen, zero at forty and +0.060 at a hundred, so not yet and affordably);
and are the three I call large the three largest (in 83 per cent of resamples at seventeen, 97 at
forty). Then test the table against the labels it rests on, because that is where it is most
fragile: four arguable labels each change the top on their own — two give 5, 4, 4, one gives 5, 5, 5
and one gives 5, 5, 4 — and the two that produce an order name **different** modes, so one reading
either way is enough to lose the direction as well as the shape. And check the modes with one member in them, because
a singleton is a guess: three of the first forty's five were singletons and only one survived
contact with another forty answers.
3. By what the check needs in order to return a verdict, which is chapter 31's rule and is
mechanical rather than a matter of taste. If the comparison is between two things that are both
literally present — a string against a list of ids, a quote against a passage, the last character
of the answer, a digit against a passage — then code decides it, and code is cheap, identical every
time, and has no verdict of its own to validate. If it needs entailment, aboutness, or how many
cases a question has, there is no substring test and you need a judgement. What it decided here:
three of my six modes have a part code can decide — four of the seven modes the table covers,
which includes one chapter 30 has and these eighty answers do not — against chapter 31's seven of
eight, because three of my six are about meaning from end to end. The code half caught six of the
seventeen failures, and **the rule *inside* each check turned out to matter as much as which column
it was in**: a length threshold for *Not an answer at all* rejected six correct short answers and no
failures, and the longest it rejected was twelve characters where the one real stub is forty-nine;
and the quote check compared as it stands fired on eight answers, six of them failures, where
trimming a trailing full stop made it fire on five and all five were failures. Two checks I was
confident about covered nothing — the invented-figure check fired on none of the eighty, and the
refusal detector fired three times on three correct refusals, which is also why it is not in the
regression verdict.
4. Ask what the baseline is, and then stop quoting the 64 per cent. A judge that says pass to
everything agrees with me on 75 of 80, which is 94 per cent, because the mode is rare — so 64 per
cent is **thirty points worse than doing nothing**. Then split it: of the five failures it caught
five, and of its 34 alarms five were real. The catch rate reads 100 per cent with an interval of 100
to 100, and that is not a measurement: nothing was missed on five labels, so the resample has
nothing to vary and reports no spread — a width of zero is the absence of evidence and not
certainty, which is chapter 41's ceiling with no discriminating cases.
What to do is to fix the instructions rather than label more cases, which is the Tip after chapter
31's step 10 — a judge answering a question about print order cannot be rescued by more labelling.
Reading its own `why` field says what is wrong: on the judge this figure came from, 18 of 29 false
alarms carry the words *instead of*, and on the judge it was built from, 37 of 45 — the shape the
instruction's own examples of the fault suggested, so the examples became a template. One sentence
aimed at that moved the agreement figure twenty points without rescuing it. And the measurement
that settles it needed no labels at all: print the answer before the question instead of after and
31 of 80 verdicts change, so the verdict is partly about the print order. The one honest use left is
as a sieve — flag 34 of 80, read those, find all five of that mode's failures having read 42 per
cent of the output — and that is a decision about which error you can afford, not a number to
report.
5. **One: the set cannot contain the case that broke.** If it was built from the cases that failed,
a case that has never failed is not in it, and a regression is by definition a case that passed
before. In this chapter's run the past-failures set of seventeen reported two fixes and zero
regressions against one real breakage, because that case passed version 1 — and chapter 33 shows
the same arithmetic does not improve when the regression is made five times worse. **Two: the set's
verdict cannot see the kind of failure that happened.** The verdict here is five code checks, which
fire on some failure of two of the six modes and on none of the other four, so eleven of the
seventeen known failures are invisible: a regression in any of those modes passes silently and the
report comes back green. That is not hypothetical in this run — one case went from a correct refusal
to the wrong product's price in all three repeats of one version and to an irrelevant fact in all
three of the other, and every check passed all six times. The two reasons have different fixes: the first is fixed by keeping passing cases, which costs
cases, and the second only by building the check, which no number of cases touches. **And a third,
which this run produced and I would now check for by habit:** a majority verdict over repeats throws
away the rate, so three of eighty cases moved between failing twice in three and failing three times
in three and all three were reported as no change. The cheap fixes are to record the fail count and
not only the verdict, and to record the answer text — eight of eighty answers came back different on
a re-run and the verdict saw one of them.

> **You understand this when** you can say what a taxonomy built on seventeen failures does and
> does not establish, and name the two measurements worth making on a judge before you label a
> single case.
