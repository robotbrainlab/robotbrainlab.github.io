# Lab: Context and Tools, Measured

Chapter 35 measured where a loop's context goes and gave four things to do about it. Chapter 36
gave the shape of a tool and how to find out which one to fix. Both chapters are unusually honest
about what their own evidence was worth, and that honesty is this chapter's brief. Chapter 35
labelled its compaction finding a [**demonstration**]{.noindex} on Chapter 6's ladder and said why: two
summaries written by hand, two dropped facts, the whole sample. It even named the doubt — three
facts that survived were not events either, so having nothing to narrate might not be what
separated them. Chapter 36 wrote its candidate sets and its defect labels into its programs as
judgements so the counts on top of them could be checked, and said that establishing what a model
actually picks is Chapter 20's method applied to a real registry.

This chapter is that method, applied to three of their claims on one real agent over the shipped
corpus. It is the first chapter in the book whose job is to go back and measure what an earlier
chapter chose not to.

*The problem.* My agent forgets things, and I rewrote a tool description on a hunch.

*What is not in scope, and who owns it.* No new lever, and two new terms rather than none —
**pairable difference** and **note scope**, both earned by a measurement here and both in Key
Terms. Everything else is borrowed. Chapter 35 owns context
engineering, just-in-time retrieval, compaction, the must-keep list, the structured note,
provenance and the sub-agent, and Chapter 36 owns the purposeful tool, the namespaced name, the
tool defect and everything about the Model Context Protocol. Chapter 23 owns the five steps, the
registry and the dispatcher, and nothing here touches them. No sub-agent and no second window —
Chapter 35 names the arrangement and Chapter 37 prices running several. No judge: every check
here is code, and where a judge is the instrument that would settle something, this chapter says
so and stops. No cost reduction, which is Chapter 49, and no attack on the notes store, which is
Chapter 50 and is the reason that store exists here. No retrieval measurement: Chapters 44 and 45
did that and this chapter reuses the pipeline they settled without re-arguing it.

## Step 1: Build the Record a Run Actually Leaves

Compaction needs something that happened. So the first program is one customer case worked by a
loop with two tools over the forty documents in `labs/corpus` — a search that returns ids and
titles, and a read that returns one document in full.

Three things about it are decisions rather than defaults.

**The read returns the whole document.** Chapter 36's rule is to return what the task reads plus
anything the model would need a second call to work out, and a policy's exclusions are exactly
the part a reader needs and would not have asked for. It is also what makes this record long
enough to be worth compacting, which is the chapter's subject — so the decision and the
convenience agree here, and it is worth saying that rather than pretending only the rule was in
play.

**The catalogue is delivered a search at a time, not carried.** Chapter 35's catalogue is one line
a document held for the whole run, so a step can choose without opening everything, and it calls
that the price of the arrangement. **This lab does not do that, and the first draft of this
chapter said it did.** The forty ids and titles come to 1,775 characters and are in no prompt:
`tool_search` returns five ids *with their titles*, so the choosing material arrives per call and
is paid for per call. Which of the two is cheaper depends on how many searches a run makes, and
nothing here measures it — Chapter 35's crossover arithmetic is where that question belongs. What
matters for this chapter is that the 1,775 characters are not in the denominator of the next
table, and the program says so where it prints them.

**And the search tool is filtered to ids the read tool can serve.** The index over this corpus
also holds the awkward PDF that Chapter 45 parsed, and `read` cannot open it. The first run of
this program died on exactly that: a search offering an id the next tool refuses. By Chapter 36's
definition that is a tool defect, and its cause is worth naming because it is so ordinary — two
tools built over two different views of one corpus.

```python
"""The run whose record gets compacted. A real loop, real tools.

Compaction needs something that actually happened. So this is one
case worked by a loop over the corpus with two tools - a search and a
document read - and the record it leaves is what the next program
summarises. Chapter 4 owns the loop and all three of its stopping
conditions are here; chapter 23 owns the five steps and the registry
that refuses a name the model invented.

The case touches the five documents facts.py draws from, because a
fact not IN the record cannot be kept by a summary of it and
measuring it would be measuring nothing. The next program checks
that rather than assuming it: see record_holds().

Why a document read returns the WHOLE document: chapter 36's rule is
to return what the task reads plus what the model would need a second
call to work out, and a policy's exclusions are the part a reader
needs and would not have asked for. It is also what makes this record
long enough to need compacting, which is the chapter's subject.
"""
import json
import pathlib
import re

import call
import search

DOCS = pathlib.Path("corpus/docs")
OUT = pathlib.Path("record.json")
TERSE_OUT = pathlib.Path("record-terse.json")
STEP_LIMIT = 16

CASE = (
    "A customer bought a clearance kettle, HL-2208, on an order "
    "totalling 128.40 pounds delivered to an IV postcode. It arrived "
    "9 days ago, unused, still boxed. They want to return it and they "
    "want the money rather than account credit. The card they paid "
    "with has since been closed. Work out what to tell them: whether "
    "they can return it, who pays the postage, how the money reaches "
    "them, how long it takes, and what the delivery charge means for "
    "the total."
)

PROTOCOL = (
    "You have two tools.\n"
    "  {\"search\": \"<words>\"}        find documents\n"
    "  {\"read\": \"<document id>\"}    read one in full\n"
    "  {\"done\": \"<your answer>\"}   when you can answer\n"
    "Reply with JSON, exactly one of those three keys."
)

#  TERSE is the instruction that describes the task. DETAILED is the
#  same instruction at the level of detail chapter 35 says pays: it
#  names what each part of the case depends on, says what a dead end
#  looks like, and says what not to repeat. Chapter 35's measurement
#  is that an instruction's LENGTH is not a context problem and its
#  level of detail is what earns its keep; both are run here, because
#  the terse one is the one I wrote first and what it did is the
#  reason the detailed one exists.
TERSE = (
    "You are working one customer case. " + PROTOCOL + " Read a "
    "document before relying on it. Do not read the same document "
    "twice."
)

DETAILED = (
    "You are working one customer case. " + PROTOCOL + "\n"
    "The case has five parts and each rests on a different document. "
    "Read a document in full before relying on it, and do not read "
    "the same one twice. Do not answer any part from the product "
    "page or from a help article where a policy covers it. Before "
    "you finish, you must have read the policy that governs the "
    "return window and the postage, the policy that governs where "
    "refund money goes and how long it takes, the document that "
    "gives the delivery charge for the postcode, and the help "
    "article for a card that has been closed. If a search returns "
    "nothing you can use, search different words rather than reading "
    "the nearest thing it offered."
)
INSTRUCTION = DETAILED


def titles():
    """The id and title of every document, used by the TOOLS and not
    put in the prompt.

    Chapter 35's catalogue is one line a document carried for the
    whole run, so a step can choose without opening everything. This
    lab does NOT do that, and the first version of this chapter said
    it did. What it does instead is deliver the catalogue a search at
    a time: `tool_search` returns five ids WITH their titles, so the
    choosing material arrives per call and is paid for per call
    rather than carried from step 1. Which of the two is cheaper
    depends on how many searches a run makes, and nothing here
    measures it - chapter 35's crossover arithmetic is the place that
    question is answered.
    """
    out = {}
    for p in sorted(DOCS.glob("*.md")):
        body = p.read_text()
        m = re.search(r"^title: (.+)$", body, re.M)
        out[p.stem] = m.group(1) if m else p.stem
    return out


CATALOGUE = titles()


def tool_search(words, cache):
    #  Only ids `read` can serve. The index also holds the corpus's
    #  awkward PDF, which this case has no use for and `read` cannot
    #  open - and a search that offers an id the next tool refuses is
    #  a tool defect in chapter 36's sense, caused here by two tools
    #  built over two different views of the same corpus. The filter
    #  is the fix; the first run of this program crashed on it.
    order, _ = search.dense(words, cache)
    seen, docs = set(), []
    for cid in order:
        doc = cid.split("#")[0]
        if doc in CATALOGUE and doc not in seen:
            seen.add(doc)
            docs.append(doc)
        if len(docs) == 5:
            break
    return [{"id": d, "title": CATALOGUE[d]} for d in docs]


def tool_read(doc_id):
    #  Chapter 23's registry: a name the model invented is refused
    #  here and nowhere else, and the refusal says what to do next,
    #  which is chapter 36's rule for a message.
    if doc_id not in CATALOGUE:
        near = [d for d in CATALOGUE if doc_id.split("-")[0] in d][:3]
        return {"error": f"no document {doc_id!r}; search returns ids "
                         f"you can read" + (f"; near: {near}" if near
                                            else "")}
    return {"id": doc_id,
            "text": (DOCS / f"{doc_id}.md").read_text()}


def run(instruction=None, out=None):
    instruction = instruction or INSTRUCTION
    out = out or OUT
    cache = search.vectors()
    steps, read, msgs = [], set(), []
    for n in range(1, STEP_LIMIT + 1):
        prompt = (f"{instruction}\n\nThe case:\n{CASE}\n\n"
                  f"What has happened so far:\n"
                  + ("\n".join(msgs) if msgs else "nothing yet")
                  + "\n\nYour next reply:")
        r = call.chat(prompt, json_mode=True, max_tokens=700)
        d = call.as_json(r["text"])
        if d is None:
            steps.append({"step": n, "tool": None, "ended": "unparsed",
                          "result": r["text"][:200]})
            break                              # chapter 4: code refuses
        if "done" in d:
            steps.append({"step": n, "tool": "done",
                          "target": None,
                          "result": str(d["done"]),
                          "tokens": r["prompt_tokens"]})
            break                              # chapter 4: model done
        if "search" in d:
            words = str(d["search"])
            res = tool_search(words, cache)
            steps.append({"step": n, "tool": "search", "target": words,
                          "result": json.dumps(res),
                          "tokens": r["prompt_tokens"]})
            msgs.append(f"step {n}: searched {words!r} -> "
                        + ", ".join(x["id"] for x in res))
        elif "read" in d:
            doc = str(d["read"])
            res = tool_read(doc)
            steps.append({"step": n, "tool": "read", "target": doc,
                          "result": json.dumps(res),
                          "tokens": r["prompt_tokens"]})
            if "error" in res:
                msgs.append(f"step {n}: read {doc!r} -> {res['error']}")
            else:
                read.add(doc)
                msgs.append(f"step {n}: read {doc!r} in full:\n"
                            f"{res['text']}")
        else:
            steps.append({"step": n, "tool": None, "ended": "no key",
                          "result": r["text"][:200]})
            break
    data = {"case": CASE, "steps": steps, "read": sorted(read),
            "instruction": instruction,
            "ended": steps[-1]["tool"] or steps[-1].get("ended")}
    out.write_text(json.dumps(data, indent=1))
    return data


def record(out=None):
    out = out or OUT
    if out.exists():
        return json.loads(out.read_text())
    return run(TERSE if out is TERSE_OUT else INSTRUCTION, out)


def as_text(data):
    """The record as the thing to be compacted: every step, the whole
    of every result. This is what is in the context at the end of the
    run, and chapter 35's first finding is that the results are
    almost all of it."""
    out = [f"The case: {data['case']}", ""]
    for s in data["steps"]:
        out.append(f"step {s['step']}: {s['tool']} {s.get('target') or ''}")
        out.append(s["result"])
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    terse = record(TERSE_OUT)
    d = record()
    body = as_text(d)
    print(f"  Two runs of one case, differing only in the"
          f" instruction.\n")
    print("  instruction   words   steps   documents read")
    for name, r, i in (("terse", terse, TERSE),
                       ("detailed", d, INSTRUCTION)):
        print(f"  {name:<14}{len(i.split()):>5}{len(r['steps']):>8}"
              f"{len(r['read']):>16}")
    print(f"\n  The terse instruction is {len(TERSE.split())} words and the"
          f" detailed one")
    print(f"  {len(INSTRUCTION.split())}. What the extra words say is which"
          f" document each")
    print("  part of the case rests on - which is chapter 35's level")
    print("  of detail, not its length.\n")
    print(f"  The detailed run: {len(d['steps'])} steps, ended by"
          f" {d['ended']}.\n")
    print("   step  tool    target")
    for s in d["steps"]:
        t = str(s.get("target") or "")[:34]
        print(f"   {s['step']:>4}  {s['tool'] or '-':<7} {t}")
    print(f"\n  Documents read in full: {len(d['read'])}")
    for r in d["read"]:
        print(f"    {r}")
    #  Chapter 35's breakdown, on a record rather than a table of
    #  plausible numbers: where did the context actually go?
    instr = len(INSTRUCTION) + len(CASE)
    cat = sum(len(f"{k}: {v}") for k, v in CATALOGUE.items())
    results = sum(len(s["result"]) for s in d["steps"])
    decisions = sum(len(str(s.get("target") or "")) for s in d["steps"])
    total = instr + results + decisions
    print(f"\n  Where this record's characters came from.\n")
    print("  source                     chars    share")
    for name, n in (("instruction and case", instr),
                    ("the model's own decisions", decisions),
                    ("tool results", results)):
        print(f"  {name:<24}{n:>8,}{n / total * 100:>8.1f}%")
    print(f"  {'-' * 24}{'-' * 8}{'-' * 8}")
    print(f"  {'the record':<24}{total:>8,}{100.0:>8.1f}%")
    print(f"\n  The {len(CATALOGUE)} ids and titles come to {cat:,}"
          f" characters and are")
    print("  NOT in any prompt: the search tool returns five of them")
    print("  at a time, so this lab pays for the catalogue per")
    print("  search rather than carrying it. The figure is here to")
    print("  be compared with what the searches cost, which the")
    print("  result characters above include.")
    big = sorted(d["steps"], key=lambda s: -len(s["result"]))[:3]
    share = sum(len(s["result"]) for s in big)
    print(f"\n  The 3 largest results are {share:,} of {results:,}"
          f" result characters,")
    print(f"  {share / results * 100:.0f}% of them, from"
          f" {len(big)} of {len(d['steps'])} steps:\n")
    for s in big:
        print(f"    step {s['step']:>2}  {s['tool']:<7}"
              f" {str(s.get('target') or '')[:22]:<22}"
              f" {len(s['result']):>6,}")
```

```text
  Two runs of one case, differing only in the instruction.

  instruction   words   steps   documents read
  terse            51       4               2
  detailed        155      14               5

  The terse instruction is 51 words and the detailed one
  155. What the extra words say is which document each
  part of the case rests on - which is chapter 35's level
  of detail, not its length.

  The detailed run: 14 steps, ended by done.

   step  tool    target
      1  search  return window policy
      2  search  returns-standard
      3  search  refunds-policy
      4  search  return window policy
      5  search  return window policy
      6  search  returns-clearance
      7  read    returns-clearance
      8  read    refunds-policy
      9  read    delivery-fees
     10  search  refunds-faq
     11  read    refunds-faq
     12  search  delivery exceptions
     13  read    delivery-exceptions
     14  done    

  Documents read in full: 5
    delivery-exceptions
    delivery-fees
    refunds-faq
    refunds-policy
    returns-clearance

  Where this record's characters came from.

  source                     chars    share
  instruction and case       1,338    11.0%
  the model's own decisions     211     1.7%
  tool results              10,666    87.3%
  ----------------------------------------
  the record                12,215   100.0%

  The 40 ids and titles come to 1,775 characters and are
  NOT in any prompt: the search tool returns five of them
  at a time, so this lab pays for the catalogue per
  search rather than carrying it. The figure is here to
  be compared with what the searches cost, which the
  result characters above include.

  The 3 largest results are 4,838 of 10,666 result characters,
  45% of them, from 3 of 14 steps:

    step  8  read    refunds-policy          1,823
    step  7  read    returns-clearance       1,518
    step 13  read    delivery-exceptions     1,497
```

**The first run of the case is the one to look at first, and it is the one I did not plan.** With
the terse instruction — fifty-one words, the one that describes the task — the loop answered a
five-part question after four steps and two documents. It had a step limit of sixteen and a
catalogue of forty. Chapter 47 measured the same shape and named it: a loop declining the freedom
the design exists for. This chapter does not re-measure it, and it is the reason the second
instruction exists.

**The detailed instruction is three times the words and the difference is not its length.** What
the extra hundred words say is which document each part of the case rests on, that a product page
does not answer a question a policy covers, and what to do when a search returns nothing useful.
Chapter 35's finding is that an instruction's length is not a context problem — 2.6 per cent of
its worked run — and that its level of detail is what pays.

**And this is the weakest evidence in the chapter, which is worth saying in the chapter that
spends seventy pages on how weak evidence looks.** It is one run each, with no repeats and no
grader. Two runs differing in an instruction and in everything a loop does differently on a
second attempt. The terse run's answer is not even uniformly wrong — it has the postage right and
invents a prepaid label the clearance policy does not offer — and nothing here scored it, so even
that is a reading rather than a measurement. What the two runs are for is producing a record worth
compacting, and the contrast is reported because it is what made me write the second instruction
rather than because it establishes anything. A measured version is three arms, twelve tasks and a
grader, which is Step 6's shape applied to instructions instead of tool descriptions.

**And the shape Chapter 35 told you to carry is here, while the percentages are not comparable.**
Tool results are 87.3 per cent of this record and three of fourteen steps carry 45 per cent of the
result characters, which is the shape: results dominating, and a few steps dominating those.
Chapter 35's 91.5 per cent is a different fraction of a different thing, and three ways. **Its
denominator includes the tool definitions and this one excludes the ids and titles** — put the
1,775 characters back and tool results are 76.2 per cent of 13,990 rather than 87.3 of 12,215.
**Its instruction bucket is the instruction; this one is the instruction and the case**, and 452
of the 1,338 characters are the case. **And its record is twenty steps where this one is
fourteen.** So *corroborates* is too strong for the numbers and right for the shape, which is what
Chapter 35 itself said to carry, since its own figures were plausible rather than measured.

A note on the word *record*, because two numbers in this chapter carry it. Step 1's table counts
12,215 characters — the instruction, the case, the decisions and the results. Step 3 compacts
11,585, which is what `as_text` produces: the case, every step and every result, without the
instruction, which is sent on each call rather than accumulated. Both are right about what they
measure and only the second is the thing a summary replaces.

> **Note:** Read steps 1, 4 and 5 of the detailed run. The loop searched the identical words —
> *return window policy* — three times, with nothing in between that could have changed the
> answer. That is this chapter's opening problem, the second half of it, arriving on schedule and
> on its own: a loop repeating itself. Nothing in the loop remembers what it has already asked,
> which is the same gap Chapter 35 found for documents already open and fixed the same way, with
> four lines of code. It is not measured here and it is not hypothetical either — it is three of
> fourteen steps in the only run this chapter had to produce.

## Step 2: Name the Facts Before You Summarise, and Cross Them

Chapter 35's mechanism is a list: name the facts the rest of the task depends on *before* the
summary is written, then check the summary against it. Its Warning is the part that matters and it
is not process hygiene — a list written afterwards is written *from* the summary, so it holds what
the summary kept, and the check then passes on a summary that dropped something.

So the list comes first, and it has one more property than Chapter 35's did.

**Thirty-eight of the forty facts are in a corpus document rather than invented**, and the program
checks that rather than claiming it: it reads each named document and looks for the fact's own
probes in it. The other two are this case's own particulars — the order total and the item — which
are in the record and not in the corpus, so there is nothing to check them against. Those two are
also excluded from every rate in the next step, and the reason is in the Warning below.

**And the twenty are crossed two ways.** Chapter 35 suspected its own result and said so: three
facts that survived were not events either, so *being about a path not taken* might be doing the
work rather than *being a negative*. There is a second candidate it did not name, and it is the
one this corpus makes obvious. Most of the negatives in these policies carry no number —
*postage is not paid by us*, *no label is issued*, *a refund cannot go to a different card* — and
most of the positives are figures. So a list split only by polarity would measure polarity and
numeracy together, and whichever name you gave the result would be the name you had chosen in
advance.

Chapter 47's lesson, one chapter old: two arms differing in two ways answer neither question. The
fix is to cross them. Five facts in each of four cells — negative with a number, negative in
prose, positive with a number, positive in prose — which means hunting for negatives that carry
figures and positives that carry none, and both exist in this corpus.

```python
"""The must-keep list, drawn from the corpus and crossed two ways.

Chapter 35 named the facts a later step depends on BEFORE summarising
and then checked the summary against them, and found that the two
facts its naive summary dropped were both about something that is NOT
so. It labelled that a demonstration and said why: two hand-written
summaries, two dropped facts, and it even named the doubt - three
facts that survived are not events either, so having no event to
narrate may not be what separated them.

This is that claim measured. Every fact below is in a corpus document
rather than invented, and the set is CROSSED two ways, because
chapter 47's lesson is that two arms differing in two ways answer
neither question:

    polarity   does the fact say something is NOT so?
    form       does it carry a number, or only prose?

Four cells, five facts each. Without the second column a negative
result could be read off the first, and most negatives in these
documents happen to carry no number - so polarity and numeracy would
have been measured together and credited to polarity.

Each fact carries a SET of probes, any one of which counts as kept.
The set is written against the documents, not against any summary:
chapter 41's rule is that a grader's repair has to be justified by
the source rather than by which side it helps, and no summary existed
when these were written.
"""
import pathlib
import re

DOCS = pathlib.Path("corpus/docs")

#  fact, polarity, form, probes, the document it comes from
FACTS = [
    # --- negative, carries a number ---
    ("a clearance return is 14 days, not the standard 30",
     "negative", "number", {"14 day", "14-day", "fourteen day"},
     "returns-clearance"),
    #  `delivered` alone was in the probe set and the CASE says
    #  "it arrived 9 days ago ... delivered", so every summary
    #  scored this kept without saying anything about when the
    #  window starts. Tightened to phrases that assert the start,
    #  which is what the fact is - and the tightening came from the
    #  case-satisfaction audit below, not from a score.
    ("the 14 days run from delivery, not from dispatch",
     "negative", "number", {"from the date the parcel was delivered",
                            "from delivery", "from the date of deliv",
                            "from when it was delivered",
                            "run from delivery"},
     "returns-clearance"),
    ("goodwill is capped at 20 pounds and is not a refund",
     "negative", "number", {"20 pound", "20 GBP", "twenty pound",
                            "cap"},
     "refunds-policy"),
    ("a bank transfer takes up to 10 working days, not 3",
     "negative", "number", {"10 working day", "ten working day",
                            "10 day"},
     "refund-to-a-closed-card"),
    #  `arriv` matched "arrived" anywhere, including in the case.
    #  And the document was mislabelled: this run never opened
    #  where-is-my-refund, but refunds-policy carries the same rule
    #  in its own words, so the fact is in the record through the
    #  document now named.
    ("the 14 days do not start until the warehouse books it in",
     "negative", "number", {"books the parcel in", "books it in",
                            "warehouse books", "booked in",
                            "booked it in"},
     "refunds-policy"),

    # --- negative, prose only ---
    ("postage on a clearance return is not paid by us",
     "negative", "prose", {"paid by the customer", "customer pays",
                           "not paid by", "at the customer"},
     "returns-clearance"),
    ("no postage label is issued for a clearance return",
     "negative", "prose", {"no label", "no postage label",
                           "label is not", "without a label"},
     "returns-clearance"),
    ("a refund cannot go to a different card",
     "negative", "prose", {"different card", "same card",
                           "card that paid", "the way it came"},
     "refunds-policy"),
    ("final-sale items cannot be returned at all",
     "negative", "prose", {"final sale", "cannot be returned",
                           "excluded", "exclusion"},
     "returns-clearance"),
    ("opening the box to look does not make an item used",
     "negative", "prose", {"opening", "look at", "does not make"},
     "returns-clearance"),

    # --- positive, carries a number ---
    ("the surcharge to an IV postcode is 9.50 pounds",
     "positive", "number", {"9.50", "9,50", "9.5 pound"},
     "delivery-exceptions"),
    ("standard delivery is 3.99 pounds under 40 pounds",
     "positive", "number", {"3.99"},
     "delivery-fees"),
    ("a refund is issued within 14 days of arrival",
     "positive", "number", {"within 14 day", "14 day", "fourteen day"},
     "refunds-policy"),
    ("the bank may take three further working days",
     "positive", "number", {"three working day", "3 working day",
                            "further three"},
     "where-is-my-refund"),
    #  TRIVIAL: the case says "an order totalling 128.40 pounds",
    #  and the case is the first line of the record, so every
    #  summary restates it and no summary could drop it. A fact a
    #  summariser cannot drop measures nothing about summarising, so
    #  this one and the kettle below are excluded from every rate -
    #  see TRIVIAL and the audit.
    ("the order total is 128.40 pounds",
     "positive", "number", {"128.40", "128,40"},
     None),

    # --- positive, prose only ---
    ("a return reference begins RET-",
     "positive", "prose", {"ret-", "return reference"},
     "returns-clearance"),
    #  `credit` is in the case ("they want the money rather than
    #  account credit"), so the probe tested the case rather than
    #  the fact. The fact is what credit DOES, so the probes are now
    #  the two properties the document gives it.
    ("account credit is immediate and does not expire",
     "positive", "prose", {"does not expire", "doesn't expire",
                           "never expires", "immediate"},
     "refund-to-a-closed-card"),
    ("the warehouse inspects every return on arrival",
     "positive", "prose", {"inspect", "inspection"},
     "returns-clearance"),
    ("the item is a clearance kettle, HL-2208",
     "positive", "prose", {"hl-2208", "kettle"},
     None),
    #  `the money` and `rather than` are both in the case verbatim.
    #  What a summary has to carry forward is the remedy that
    #  follows from the preference, so the probe is the remedy.
    ("the customer wants the money rather than credit",
     "positive", "prose", {"bank transfer", "transfer to a bank",
                           "transfer instead"},
     "refunds-faq"),
]

#  --- the second batch -------------------------------------------
#
#  Written AFTER the first twenty had been scored, and the order of
#  events is on the record because it is the only thing that makes
#  this legitimate or not.
#
#  AND IT IS NOT A MUST-KEEP LIST. That is the thing to read before
#  any figure that uses it. Chapter 35's definition is "the facts the
#  rest of the task depends on", and these twenty are facts that
#  merely APPEAR in the record: the Northern Ireland surcharge, the
#  price of next-day delivery, what two-person delivery costs. This
#  case is an IV postcode and a clearance kettle. None of that
#  governs it.
#
#  I wrote them to buy units for the polarity question and only saw
#  afterwards that I had changed the question. Keeping them is worth
#  more than deleting them, because the gap between the two batches
#  turned out to be larger than either thing the cells were built to
#  separate - so the batch label is carried through every reading
#  below and no figure pools them without saying so.
#
#  Why it was done. Chapter 20's row says what repeats and units each
#  buy: units buy the range of inputs, repeats buy one unit's own
#  certainty, and two or three repeats then stop. Twelve trials over
#  twenty facts spent the budget the wrong way round - and the thing
#  that makes it plainly a mistake rather than a trade is that a fact
#  costs NO model call. The summaries already exist; a new fact is a
#  substring test against text on disk. So the first twenty were
#  twenty because I stopped writing, not because twenty was what the
#  question needed.
#
#  Why it is not cherry-picking, and the conditions it has to meet.
#  Not one fact below was chosen by consulting a score. Each is drawn
#  by the same rule as the first twenty - in a document this run read,
#  five to a cell, probes written from the document - and the batch is
#  ONE batch. There is no third. Both results are reported, the
#  twenty and the forty, and if the forty had reversed the twenty that
#  is what the chapter would say.
SECOND = [
    # --- negative, carries a number ---
    ("named-day delivery is not available in a surcharged area",
     "negative", "number", {"named-day", "named day"},
     "delivery-exceptions"),
    ("standard delivery to those areas is 5 to 7 days, not 3 to 5",
     "negative", "number", {"5 to 7", "five to seven",
                            "5-7"},
     "delivery-exceptions"),
    ("the 19.99 charge is not waived by order value",
     "negative", "number", {"19.99", "not waived", "flat"},
     "delivery-fees"),
    #  `40 pound` is in the case ("a 20 pound order"? no - but
    #  "40 pounds" is not; the audit flagged it because the case
    #  says "totalling 128.40 pounds" and `40 pound` is a substring
    #  of "128.40 pounds"). A substring probe has to be read as a
    #  substring, which is the whole lesson of this file.
    ("free delivery does not apply under 40 pounds",
     "negative", "number", {"under 40", "40 or more", "below 40",
                            "less than 40"},
     "delivery-fees"),
    ("a goodwill payment does not change the refund owed",
     "negative", "number", {"does not change", "separate",
                            "not a refund"},
     "refunds-faq"),

    # --- negative, prose only ---
    ("the surcharge is not shown in the delivery charges document",
     "negative", "prose", {"not shown", "depends on the postcode",
                           "listed in"},
     "delivery-fees"),
    ("nothing in the delivery charges document covers return postage",
     "negative", "prose", {"return postage", "covered by the returns"},
     "delivery-fees"),
    ("two-person delivery is not available to the Channel Islands",
     "negative", "prose", {"channel islands", "not available"},
     "delivery-exceptions"),
    ("the surcharge carries no mark-up",
     "negative", "prose", {"mark-up", "markup", "passed on"},
     "delivery-exceptions"),
    ("a return cannot be sent without a reference",
     "negative", "prose", {"without a reference", "do not send",
                           "cannot match"},
     "returns-clearance"),

    # --- positive, carries a number ---
    ("next-day delivery is 7.99 pounds",
     "positive", "number", {"7.99"},
     "delivery-fees"),
    ("named-day delivery is 5.99 pounds",
     "positive", "number", {"5.99"},
     "delivery-fees"),
    ("the Northern Ireland surcharge is 6.50 pounds",
     "positive", "number", {"6.50"},
     "delivery-exceptions"),
    ("two-person delivery is 19.99 pounds",
     "positive", "number", {"19.99"},
     "delivery-fees"),
    ("most refunds are processed within 30 days of arrival",
     "positive", "number", {"30 day", "thirty day"},
     "refunds-faq"),

    # --- positive, prose only ---
    ("the delivery charge is refunded on a whole-order return",
     "positive", "prose", {"whole order", "whole of the order",
                           "entire order"},
     "refunds-policy"),
    ("credit can be spent on any order",
     "positive", "prose", {"any order", "spent on"},
     "refunds-policy"),
    #  The probes here were corrected once, before any score from
    #  this batch had been read: the document says "the card or
    #  account used to pay", so "card used to pay" was not in it and
    #  grounded() said so. Chapter 41's condition is met - the repair
    #  is justified by the source and not by which side it helps.
    ("a refund goes back to the card that paid",
     "positive", "prose", {"card or account used to pay",
                           "card that paid", "returned to the card",
                           "the way it came"},
     "refunds-policy"),
    ("the customer may ask for a bank transfer instead",
     "positive", "prose", {"bank transfer", "transfer"},
     "refunds-policy"),
    ("checkout applies the surcharge automatically",
     "positive", "prose", {"automatically", "checkout applies"},
     "delivery-fees"),
]

ALL = FACTS + SECOND

#  Which batch a fact is in, and what that means: "needed" is a fact
#  a later step of THIS case depends on, which is chapter 35's
#  definition; "present" is a fact that is in the record and that no
#  step of this case needs.
BATCH = {f: "needed" for f, _, _, _, _ in FACTS}
BATCH.update({f: "present" for f, _, _, _, _ in SECOND})

CELLS = sorted({(p, f) for _, p, f, _, _ in ALL})


#  The three facts that are the CASE's own particulars. Excluded from
#  every rate, and the reason is the only principled one available: a
#  must-keep check measures whether a summary dropped a fact, and the
#  case is the first line of the record, so a fact the case states is
#  one every summary restates and none can drop. Scoring it is
#  scoring the summariser's ability to copy the question.
#
#  The third one arrived late and by a better route than the first
#  two. Its probes were RETARGETED rather than excluded: the case
#  says "they want the money rather than account credit", so no
#  probe for the preference can escape the case, and the repair
#  pointed the probes at the remedy instead - `bank transfer`. That
#  passed the case audit and was still wrong twice over. It no
#  longer tests the fact, which is a preference and not a remedy, so
#  a summary mentioning a transfer and never saying what the
#  customer asked for would score it kept. And it shares `bank
#  transfer` with a present-batch fact, so one phrase scores two
#  facts in two batches. The fact is a case particular and belongs
#  here; retargeting a probe to pass an audit is how you keep a fact
#  you should have dropped.
TRIVIAL = {"the order total is 128.40 pounds",
           "the item is a clearance kettle, HL-2208",
           "the customer wants the money rather than credit"}

SCORED = [r for r in ALL if r[0] not in TRIVIAL]


def norm(s):
    return re.sub(r"\s+", " ", s).lower()


def kept(summary, probes):
    body = norm(summary)
    return any(p in body for p in probes)


def case_satisfied(case):
    """Probe sets the CASE STATEMENT alone satisfies.

    This audit exists because it found six. Every summary restates
    the case, so a probe the case satisfies scores kept without
    testing anything about compaction - and the probes that did it
    were loose fragments rather than the fact: `delivered` for a
    fact about when a window starts, `arriv` for one about the
    warehouse booking a parcel in, `credit` for one about what
    credit does, `the money` and `rather than` lifted straight out
    of the case, and `40 pound` matching inside "128.40 pounds".

    All five were tightened against their documents. What remains
    is the two facts in TRIVIAL, which are the case's own
    particulars and are excluded rather than tightened, because
    there is no tighter probe for a fact the case states outright.

    A WIDE probe set makes a summary look better than it was. That
    is the risk this file's Warning did not name, and it is the
    larger of the two.
    """
    body = norm(case)
    return [(f, sorted(p for p in probes if p in body))
            for f, _, _, probes, _ in ALL
            if any(p in body for p in probes)]


def grounded(facts=None):
    """Every fact that names a document is in that document.

    Two facts name none: they are this case's own particulars, the
    order total and the item, which are in the record rather than in
    the corpus. The assertion below holds for the other eighteen and
    the count is printed, because a must-keep list that quietly
    drifted from its sources would be a list of things I believe.
    """
    facts = ALL if facts is None else facts
    checked = missing = 0
    for fact, _, _, probes, doc in facts:
        if doc is None:
            continue
        body = norm((DOCS / f"{doc}.md").read_text())
        checked += 1
        if not any(p in body for p in probes):
            missing += 1
            print(f"    NOT IN {doc}: {fact}")
    return checked, missing


if __name__ == "__main__":
    print(f"  {len(ALL)} facts in two batches, crossed two ways.\n")
    print("  polarity   form      first   second   all")
    for pol, form in CELLS:
        a = sum(1 for _, p, f, _, _ in FACTS if (p, f) == (pol, form))
        b = sum(1 for _, p, f, _, _ in SECOND if (p, f) == (pol, form))
        print(f"  {pol:<10} {form:<9} {a:>5}{b:>9}{a + b:>6}")
    print(f"  {'-' * 10} {'-' * 9} {'-' * 5} {'-' * 8}{'-' * 6}")
    print(f"  {'':10} {'':9} {len(FACTS):>5}{len(SECOND):>9}"
          f"{len(ALL):>6}")
    print("\n  Why crossed: most negatives in these documents carry")
    print("  no number, so polarity and numeracy would be measured")
    print("  together and the result credited to polarity. The cell")
    print("  counts above are what makes the two separable.")
    print("\n  Why two batches, and in which order: read the comment")
    print("  above SECOND in this file. The short form is that a")
    print("  fact costs no model call, so twenty was the wrong")
    print("  number and twelve trials were too many - which is")
    print("  chapter 20's own arithmetic, read before writing this")
    print("  and applied after.")

    checked, missing = grounded()
    print(f"\n  {checked} of {len(ALL)} facts name a corpus document"
          f" and")
    print(f"  {checked - missing} of those {checked} were found in"
          f" it; {missing} were not.")
    own = [f for f, _, _, _, d in ALL if d is None]
    print(f"  The other {len(own)} are this case's own particulars:")
    for f in own:
        print(f"    {f}")

    print("\n  The probes are substrings, so each fact carries a set")
    print("  and any one counts. They were written from the")
    print("  documents before any summary of theirs was read, which")
    print("  is the condition chapter 41 puts on a grader.")
    widest = max(ALL, key=lambda r: len(r[3]))
    print(f"\n  The widest set is {len(widest[3])} probes, on:")
    print(f"    {widest[0]}")
    for probe in sorted(widest[3]):
        print(f"      {probe!r}")
```

```text
  40 facts in two batches, crossed two ways.

  polarity   form      first   second   all
  negative   number        5        5    10
  negative   prose         5        5    10
  positive   number        5        5    10
  positive   prose         5        5    10
  ---------- --------- ----- --------------
                          20       20    40

  Why crossed: most negatives in these documents carry
  no number, so polarity and numeracy would be measured
  together and the result credited to polarity. The cell
  counts above are what makes the two separable.

  Why two batches, and in which order: read the comment
  above SECOND in this file. The short form is that a
  fact costs no model call, so twenty was the wrong
  number and twelve trials were too many - which is
  chapter 20's own arithmetic, read before writing this
  and applied after.

  38 of 40 facts name a corpus document and
  38 of those 38 were found in it; 0 were not.
  The other 2 are this case's own particulars:
    the order total is 128.40 pounds
    the item is a clearance kettle, HL-2208

  The probes are substrings, so each fact carries a set
  and any one counts. They were written from the
  documents before any summary of theirs was read, which
  is the condition chapter 41 puts on a grader.

  The widest set is 5 probes, on:
    the 14 days run from delivery, not from dispatch
      'from delivery'
      'from the date of deliv'
      'from the date the parcel was delivered'
      'from when it was delivered'
      'run from delivery'
```

**Each fact carries a set of probes and any one counts as kept.** A faithful summary can say *14
days*, *fourteen days* or *14-day window*, and a probe that accepted only the first would score a
true summary as a loss. The sets were written from the documents before any summary existed,
which is the condition Chapter 41 puts on a grader: a repair has to be justified by the source
rather than by which side it helps.

**And there is a second batch of twenty, written after the first twenty had been scored.** Why,
and why that is on the record: Chapter 20's own row says what units and repeats each buy — units
buy the range of inputs, repeats buy one unit's own certainty, and two or three repeats then stop.
Twelve trials over twenty facts spent the budget the wrong way round, and the thing that makes it
a mistake rather than a trade is that **a fact costs no model call at all.** The summaries already
existed; a new fact is a substring test against text on disk. So the first twenty were twenty
because I stopped writing, not because twenty was what the question needed.

**And the second batch is not a must-keep list**, which I saw only after writing it. Chapter 35's
definition is *the facts the rest of the task depends on*, and these twenty are facts that merely
appear in the record: the price of next-day delivery, the Northern Ireland surcharge, what
two-person delivery costs. The case is an IV postcode and a clearance kettle, and none of that
governs it. Keeping them turned out to be worth more than deleting them, for a reason the next
step reports, so every reading carries the batch label and no figure pools them without saying so.

**And the probes themselves needed auditing, which found six that measured nothing.** The record
begins with the case statement, and every summary restates the case — so a probe the *case alone*
satisfies scores the fact kept without saying anything about what the summary did. Six of the
forty were in that position, five of them on facts the case depends on, and the loose part was
never the fact: `delivered` for a fact about when a window *starts*;
`arriv` for one about the warehouse booking a parcel in; `credit` for one about what credit
*does*; `the money` and `rather than`, lifted out of the case word for word; and `40 pound`,
matching inside *128.40 pounds*.

Five were tightened against their documents. The sixth and seventh are the case's own particulars
— the order total and the item — and there is no tighter probe for a fact the case states
outright, so they are excluded from every rate instead. `facts.case_satisfied` is the audit, it
runs every time, and it exists because it found these.

**What that cost is reported rather than buried, because it is most of this step's result.** Before
the tightening the needed-against-present difference was +0.43 and cleared zero. After it the same
comparison is +0.21, from −0.017 to +0.444, and does not. The naive polarity difference fell from
+0.34 to +0.15, and the form difference rose from +0.34 to +0.49 and became the only one of the two
that clears zero. **A probe set that is too wide makes a summary look better than it was**, and the
error is not symmetric: it inflates whichever group holds the loose probes, which here was the
group I most wanted to be different.

> **Warning:** This chapter's first version of that Warning named only one risk to a probe set —
> widening it *after* seeing a score — and it is the smaller one. The larger is a probe that was
> never specific enough to test its fact, which you can write in complete good faith before any
> score exists, and which no amount of discipline about the order of events will catch. The test
> is not *when* did I write this probe. It is: **could this probe be satisfied by text that is not
> the fact?** Run it against the question, against the instruction, against the case. One probe
> set was also corrected for the opposite reason, and the file says so beside it: the grounding
> check found that *card used to pay* is not in `refunds-policy`, which says "the card or account
> used to pay". Both repairs are justified by the documents rather than by which side they help,
> which is Chapter 41's condition.

## Step 3: Compact It Twenty-Four Times, and Count

Now the measurement. Two summary instructions, twelve summaries each, and every scored fact
checked against every summary: thirty-seven facts, 888 pairs, read as two batches of seventeen
and twenty. Three of the forty are excluded, and the Warning above says why.

**Neither instruction names a single fact from the list.** That is the whole mechanism — the list
is what you *check* with, and a list handed to the summariser measures obedience rather than
summarising. The naive instruction is what people write. The warned instruction adds one sentence
asking for the things that are not so.

```python
"""Compaction run on a real record, and measured.

Chapter 35 built the mechanism - name the facts a later step depends
on BEFORE summarising, check the summary against them afterwards -
and demonstrated it on two summaries written by hand. It said in so
many words what that was worth: a demonstration on chapter 6's
ladder and no higher, two dropped facts the whole sample. It also
named its own doubt, that three surviving facts were not events
either, so having nothing to narrate might not be what separated
them.

So this program does three things chapter 35 could not:

  1. the summaries are written by the model, not by me
  2. there are many of them, so a rate has an interval
  3. the facts are crossed by polarity AND form (facts.py), so a
     result about negatives is not a result about numbers

Two summary instructions. NAIVE is what people write. WARNED adds
one sentence asking for what is not so. Neither names a single fact
from the must-keep list, which is the whole point of the mechanism:
the list is what you CHECK with, and a list fed to the summariser
measures nothing but obedience.
"""
import json
import pathlib
import random

import call
import facts
import record

OUT = pathlib.Path("summaries.json")
TRIALS = 12
RESAMPLES = 10_000
SEED = 48

NAIVE = (
    "Below is the record of a customer-service run. Summarise it so "
    "that a later step can carry on working the case without the "
    "full record."
)

WARNED = (
    NAIVE + " Keep anything a later step would get wrong without it, "
    "including the things that are NOT so: what is ruled out, what "
    "is not allowed, what is not included, and what does not apply."
)

PROMPTS = {"naive": NAIVE, "warned": WARNED}


def run():
    body = record.as_text(record.record())
    out = []
    for name, instruction in PROMPTS.items():
        for trial in range(1, TRIALS + 1):
            r = call.chat(f"{instruction}\n\n---\n{body}\n---\n\n"
                          f"Your summary:", max_tokens=700)
            out.append({"prompt": name, "trial": trial,
                        "summary": r["text"],
                        "words": len(r["text"].split()),
                        "output_tokens": r["output_tokens"],
                        "finish_reason": r["finish_reason"]})
            #  Chapter 47's lesson, entry 69's shape: save every
            #  trial as it lands rather than the batch at the end.
            OUT.write_text(json.dumps(out, indent=1))
            print(f"    {name} {trial}: {r['output_tokens']} tokens")
    return out


def summaries():
    return json.loads(OUT.read_text()) if OUT.exists() else run()


def graded(rows, which=None):
    """Every fact against every summary. One row per pair.

    `which` defaults to facts.SCORED. It is a parameter because the
    sensitivity block below has to score a fact the headline
    excludes - and the first version of that block read the headline
    table instead, so the fact it meant to include came back as a
    silent 0.0 from `rate`'s empty-selection branch. That is the
    same mistake twice in ten lines: an exclusion applied in one
    place and not in every place that reads the data.
    """
    out = []
    for s in rows:
        for fact, pol, form, probes, _ in (which or facts.SCORED):
            out.append({"prompt": s["prompt"], "trial": s["trial"],
                        "fact": fact, "polarity": pol, "form": form,
                        "batch": facts.BATCH[fact],
                        "kept": facts.kept(s["summary"], probes)})
    return out


def rate(rows, **where):
    sel = [r for r in rows
           if all(r[k] == v for k, v in where.items())]
    return (sum(r["kept"] for r in sel) / len(sel), len(sel)) if sel \
        else (0.0, 0)


def per_fact(rows, prompt, batch=None):
    """One rate per fact, trials averaged within it.

    The fact is the unit chapter 20's interval resamples, because
    the facts are what a different must-keep list would have drawn
    differently - the trials are repeats of one fact rather than
    extra facts, which is chapter 20's rule about where repeats go.
    """
    out = {}
    for fact, pol, form, _, _ in facts.SCORED:
        if batch and facts.BATCH[fact] != batch:
            continue
        r, n = rate(rows, prompt=prompt, fact=fact)
        out[fact] = (r, pol, form)
    return out


def interval(pairs, rounds=RESAMPLES, seed=SEED):
    """Chapter 20's paired bootstrap, resampling the unit."""
    rng = random.Random(seed)
    n = len(pairs)
    means = []
    for _ in range(rounds):
        drawn = [pairs[rng.randrange(n)] for _ in range(n)]
        means.append(sum(b - a for a, b in drawn) / n)
    means.sort()
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


def unpaired(a_rows, b_rows, rounds=RESAMPLES, seed=SEED):
    """Two groups with no pairing between them, resampled
    independently.

    This function exists because the first version of this program
    sorted both groups and zipped them, which pairs the smallest
    negative with the smallest positive. That is not chapter 20's
    paired bootstrap - it invents a pairing the data does not have,
    and it reported an interval several times narrower than the one
    below. Ten negative facts and ten positive facts are not ten
    pairs: nothing links the third negative to the third positive.
    """
    rng = random.Random(seed)
    na, nb = len(a_rows), len(b_rows)
    means = []
    for _ in range(rounds):
        ma = sum(a_rows[rng.randrange(na)] for _ in range(na)) / na
        mb = sum(b_rows[rng.randrange(nb)] for _ in range(nb)) / nb
        means.append(mb - ma)
    means.sort()
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


def says(lo, hi, a, b):
    if lo > 0:
        return f"{b} keeps more"
    if hi < 0:
        return f"{a} keeps more"
    return "cannot tell"


if __name__ == "__main__":
    rows = summaries()
    g = graded(rows)
    print(f"  {len(rows)} summaries of one record, "
          f"{TRIALS} per instruction,")
    print(f"  checked against {len(facts.SCORED)} facts: "
          f"{len(g):,} fact-and-summary pairs.\n")

    left = facts.case_satisfied(record.record()["case"])
    scored_left = [f for f, _ in left if f not in facts.TRIVIAL]
    print(f"  Probe sets the CASE STATEMENT alone satisfies:"
          f" {len(left)},")
    print(f"  of which {len(scored_left)} are scored and"
          f" {len(left) - len(scored_left)} are excluded as the")
    print("  case's own particulars. Every summary restates the")
    print("  case, so a probe the case satisfies measures nothing.")
    print("  This audit found six and five were tightened; what")
    print("  is left is in facts.TRIVIAL.\n")
    print("  0. THE TWO BATCHES, which have to be read apart.\n")
    print("     A must-keep list is chapter 35's definition: the")
    print("     facts the rest of the task depends on. The first")
    print(f"     {len(facts.FACTS)} facts are that. The second"
          f" {len(facts.SECOND)} are facts that")
    print("     merely APPEAR in the record and that no step of")
    print("     this case needs - the Northern Ireland surcharge,")
    print("     on a case about an IV postcode. I wrote them to")
    print("     buy units and changed the question doing it.\n")
    print("     instruction   words   needed   present   both")
    for name in PROMPTS:
        w = [s["words"] for s in rows if s["prompt"] == name]
        a, _ = rate(g, prompt=name, batch="needed")
        b, _ = rate(g, prompt=name, batch="present")
        c, _ = rate(g, prompt=name)
        print(f"     {name:<14}{sum(w) / len(w):>5.0f}{a:>9.0%}"
              f"{b:>10.0%}{c:>7.0%}")
    #  facts.SCORED, not facts.BATCH. BATCH holds all 40 and the
    #  excluded facts are not in `g`, so `rate` returned (0.0, 0)
    #  for each and ungraded facts entered this mean as zeros. It
    #  reported +0.21 not clearing zero where the figure clears it.
    #  The fix-verification pass found that, and the shape of the
    #  mistake is worth more than the figure: an exclusion applied
    #  in one place and not in every place that reads the data.
    nd = [rate(g, fact=f)[0] for f, _, _, _, _ in facts.SCORED
          if facts.BATCH[f] == "needed"]
    pr = [rate(g, fact=f)[0] for f, _, _, _, _ in facts.SCORED
          if facts.BATCH[f] == "present"]
    lo, hi = unpaired(pr, nd)
    d = sum(nd) / len(nd) - sum(pr) / len(pr)
    print(f"\n     needed - present  {d:+.2f}"
          f"   {lo:+.3f} to {hi:+.3f}"
          f"   {says(lo, hi, 'present', 'needed').split()[0]}")
    clears = lo > 0 or hi < 0
    print(f"\n     That difference"
          f" {'clears' if clears else 'does NOT clear'} zero.")
    print("     A summary drops what the task does not need,")
    print("     which is what a summary is")
    print(f"     FOR, so some gap here is expected. The two")
    print("     batches are still reported apart rather than")
    print("     pooled, because they answer different questions.")
    #  How much of that verdict is the probe audit and how much is
    #  the exclusion, computed both ways. The point is not which
    #  figure to quote: it is that a one-fact judgement moves the
    #  verdict, which is what an unestablished difference looks
    #  like from the inside.
    two = {f for f in facts.TRIVIAL
           if f != "the customer wants the money rather than credit"}
    g3 = graded(rows, [r for r in facts.ALL if r[0] not in two])
    nd3 = [rate(g3, fact=f)[0] for f, _, _, _, _ in facts.ALL
           if facts.BATCH[f] == "needed" and f not in two]
    pr3 = [rate(g3, fact=f)[0] for f, _, _, _, _ in facts.ALL
           if facts.BATCH[f] == "present" and f not in two]
    lo3, hi3 = unpaired(pr3, nd3)
    d3 = sum(nd3) / len(nd3) - sum(pr3) / len(pr3)
    print("\n     Before any of this it was +0.43 and cleared zero.")
    print("     Two things moved it, and the program reports both,")
    print("     because which of them you stop at decides the")
    print("     verdict:\n")
    print("       the audit - five loose probe sets tightened,")
    print("         every summary restating the case")
    print("       the exclusion - three facts the CASE states")
    print("         outright, which no summary could drop")
    print()
    def verdict(a, b):
        return "clears zero" if (a > 0 or b < 0) else "cannot tell"

    print(f"       3rd fact scored   {d3:+.2f}"
          f"  {lo3:+.3f} to {hi3:+.3f}  {verdict(lo3, hi3)}")
    print(f"       3rd excluded too  {d:+.2f}"
          f"  {lo:+.3f} to {hi:+.3f}  {verdict(lo, hi)}")
    if verdict(lo3, hi3) == verdict(lo, hi):
        print(f"\n     Both say {verdict(lo, hi)}, so the one-fact")
        print("     judgement does not decide it. What decided it")
        print("     was the probe audit, which moved +0.43 to under")
        print(f"     {max(abs(d), abs(d3)):.2f} either way.")
    else:
        print("\n     One judgement about one fact is the difference")
        print("     between a verdict and none, which is not a")
        print("     reason to pick the one you prefer.")
    print(f"\n     So nothing here is safe to quote: {len(nd)} facts")
    print(f"     against {len(pr)} put the verdict inside the width of")
    print("     one decision about one fact. A gap between a case's")
    print("     own facts and facts merely in its record is one")
    print("     anybody would expect; what this measurement can")
    print("     carry is the mechanism and not the number.")
    print("\n     What survives is the list's real use, which does")
    print("     not need a rate at all. Not catching a summariser")
    print("     careless about negatives: telling you which of the")
    print("     facts YOU need are among the ones it dropped.\n")

    docs = {b: {d for f, _, _, _, d in facts.SCORED
                if facts.BATCH[f] == b and d}
            for b in ("needed", "present")}
    shared = docs["needed"] & docs["present"]
    nd2 = [rate(g, fact=f)[0] for f, _, _, _, d in facts.SCORED
           if facts.BATCH[f] == "needed" and d in shared]
    pr2 = [rate(g, fact=f)[0] for f, _, _, _, d in facts.SCORED
           if facts.BATCH[f] == "present" and d in shared]
    lo2, hi2 = unpaired(pr2, nd2)
    d2 = sum(nd2) / len(nd2) - sum(pr2) / len(pr2)
    print("     The batches are not matched on which document a")
    print(f"     fact came from. Restricted to the {len(shared)}"
          f" documents")
    print(f"     both draw on ({len(nd2)} needed,"
          f" {len(pr2)} present):")
    print(f"       needed - present  {d2:+.2f}"
          f"   {lo2:+.3f} to {hi2:+.3f}"
          f"   {says(lo2, hi2, 'present', 'needed').split()[0]}")
    one = [(b, f) for b in ("needed", "present")
           for f, _, _, _, _ in facts.SCORED
           if facts.BATCH[f] == b and rate(g, fact=f)[0] == 1.0]
    print(f"\n     {len(one)} facts are kept by every summary:"
          f" {sum(1 for b, _ in one if b == 'needed')} needed and")
    print(f"     {sum(1 for b, _ in one if b == 'present')} present,"
          f" so the batches are not cleanly")
    print("     separated by difficulty either. Crossing fixes the")
    print("     confounds you name, and nothing else.\n")
    print("  1. THE CROSSED TABLE, which is why the facts were")
    print("     chosen in four cells rather than two.")
    print("     The NEEDED batch only - the must-keep list.\n")
    for name in PROMPTS:
        print(f"     {name}")
        print("       polarity    number     prose       all")
        for pol in ("negative", "positive"):
            cells = []
            for form in ("number", "prose"):
                r, n = rate(g, prompt=name, polarity=pol,
                            form=form, batch="needed")
                cells.append(f"{r:>8.0%}")
            allr, _ = rate(g, prompt=name, polarity=pol,
                           batch="needed")
            print(f"       {pol:<10}{cells[0]}{cells[1]}{allr:>10.0%}")
        print()
    #  The two margins, printed once: a cell table invites reading a
    #  difference off two cells, and the margin is the comparison.
    print("     the margins, per instruction:\n")
    for name in PROMPTS:
        m = {}
        parts = []
        for key, levels in (("polarity", ("negative", "positive")),
                            ("form", ("number", "prose"))):
            for lv in levels:
                m[lv], _ = rate(g, prompt=name, batch="needed",
                                **{key: lv})
        print(f"       {name}")
        print(f"         polarity  negative {m['negative']:.0%}"
              f"   positive {m['positive']:.0%}")
        print(f"         form      prose    {m['prose']:.0%}"
              f"   number   {m['number']:.0%}")
        same = (round(m["negative"], 4) == round(m["prose"], 4)
                and round(m["positive"], 4) == round(m["number"], 4))
        if same:
            print("         the two margins are the SAME pair of")
            print("         numbers, so neither of them says which")
            print("         column is doing the work.")
        else:
            gap_p = m["positive"] - m["negative"]
            gap_f = m["number"] - m["prose"]
            bigger = "form" if gap_f > gap_p else "polarity"
            print(f"         the form gap is {gap_f:+.2f} and the")
            print(f"         polarity gap {gap_p:+.2f}, so {bigger} is")
            print("         the larger of the two here - and section")
            print("         2 is whether either is established.")
        print()
    worst = min(((p_, f_, rate(g, polarity=p_, form=f_,
                               batch="needed")[0])
                 for p_ in ("negative", "positive")
                 for f_ in ("number", "prose")),
                key=lambda r: r[2])
    print(f"     Over both instructions the lowest cell is"
          f" {worst[0]} AND")
    print(f"     {worst[1]}, at {worst[2]:.0%}. A margin is an average"
          f" over a row")
    print("     or a column, and the loss here is in one cell.")

    print("\n  2. IS THE POLARITY DIFFERENCE REAL. One FACT to a")
    print("     row, trials averaged within the fact, and the two")
    print("     groups resampled INDEPENDENTLY, because a")
    print("     fact's polarity is a property of the fact, so the")
    print("     two groups are two samples and not pairs.\n")
    print("     instr    neg   pos   diff   95% interval   says")
    for name in PROMPTS:
        pf = per_fact(g, name, batch="needed")
        neg = [r for r, p, _ in pf.values() if p == "negative"]
        pos = [r for r, p, _ in pf.values() if p == "positive"]
        lo, hi = unpaired(neg, pos)
        d = sum(pos) / len(pos) - sum(neg) / len(neg)
        verdict = says(lo, hi, 'negative', 'positive').split()[0]
        print(f"     {name:<9}{sum(neg) / len(neg):>4.0%}"
              f"{sum(pos) / len(pos):>6.0%}{d:>7.2f}"
              f"  {lo:+.3f} to {hi:+.3f}"
              f"  {verdict}")
    #  The same question asked of FORM, because the margins above
    #  show the two are the same size and only one of them is
    #  chapter 35's claim.
    print("\n     and the same question asked of form, which the")
    print("     margins say is the comparable difference:\n")
    print("     instr    pro   num   diff   95% interval   says")
    for name in PROMPTS:
        pf = per_fact(g, name, batch="needed")
        num = [r for r, _, fm in pf.values() if fm == "number"]
        pro = [r for r, _, fm in pf.values() if fm == "prose"]
        lo, hi = unpaired(pro, num)
        d = sum(num) / len(num) - sum(pro) / len(pro)
        verdict = says(lo, hi, 'prose', 'number').split()[0]
        print(f"     {name:<9}{sum(pro) / len(pro):>4.0%}"
              f"{sum(num) / len(num):>6.0%}{d:>7.2f}"
              f"  {lo:+.3f} to {hi:+.3f}"
              f"  {verdict}")

    print("\n  3. DOES THE WARNING RECOVER THEM. The same facts under")
    print("     the two instructions, paired by fact.\n")
    print("     batch     facts      n   diff   95% interval"
          "    says")
    #  By FORM as well as by polarity, because section 2 says form
    #  is the difference with evidence behind it - so the question
    #  is no longer only whether the warning recovers negatives.
    a = per_fact(g, "naive", batch="needed")
    b = per_fact(g, "warned", batch="needed")
    for group in ("prose", "number"):
        pairs = [(a[f][0], b[f][0]) for f in a if a[f][2] == group]
        lo_, hi_ = interval(pairs)
        d_ = sum(y - x for x, y in pairs) / len(pairs)
        print(f"     {'needed':<10}{group:<8}{len(pairs):>3}{d_:>7.2f}"
              f"  {lo_:+.3f} to {hi_:+.3f}"
              f"  {says(lo_, hi_, 'naive', 'warned').split()[0]}")
    print()
    for batch in ("needed", "present", None):
        a = per_fact(g, "naive", batch=batch)
        b = per_fact(g, "warned", batch=batch)
        for group in ("all", "negative", "positive"):
            pairs = [(a[f][0], b[f][0]) for f in a
                     if group == "all" or a[f][1] == group]
            lo, hi = interval(pairs)
            d = sum(y - x for x, y in pairs) / len(pairs)
            verdict = says(lo, hi, 'naive', 'warned').split()[0]
            print(f"     {batch or 'both':<10}{group:<8}"
                  f"{len(pairs):>3}{d:>7.2f}"
                  f"  {lo:+.3f} to {hi:+.3f}  {verdict}")
        print()
    #  And cell by cell, because the two margins above put the
    #  loss and the recovery in different places and a margin
    #  cannot show that.
    print("     and cell by cell, which is where the two findings")
    print("     stop agreeing:\n")
    print("     cell          naive  warned   change")
    moves = {}
    for pol in ("negative", "positive"):
        for form in ("number", "prose"):
            x, _ = rate(g, prompt="naive", batch="needed",
                        polarity=pol, form=form)
            y, _ = rate(g, prompt="warned", batch="needed",
                        polarity=pol, form=form)
            moves[(pol, form)] = y - x
            print(f"     {pol[:3]}/{form[:3]:<9}{x:>6.0%}{y:>8.0%}"
                  f"{y - x:>+9.0%}")
    top = max(moves, key=lambda k: moves[k])
    rest = max(k for k in moves if k != top)
    print(f"\n     The whole recovery is in one cell,"
          f" {top[0][:3]}/{top[1][:3]}, at")
    print(f"     {moves[top]:+.0%}. No other cell moves by more than")
    print(f"     {max(abs(moves[k]) for k in moves if k != top):.0%}.")
    print("     So the loss and the recovery are not the same")
    print("     shape: under the naive instruction BOTH prose")
    print("     cells are empty, and the warning refills the one")
    print("     that is also negative. A sentence asking for what")
    print("     is not so recovers prose negatives and does")
    print("     nothing for prose positives.")

    print("\n  4. THE FACTS NO SUMMARY KEPT, which is what a rate")
    print("     cannot show you.\n")
    #  A rate of 47% could be every fact kept about half the time or
    #  half the facts kept always and half never. It is nearer the
    #  second, and which it is decides what you do about it.
    print("     instruction   batch     every   none   of")
    for name in PROMPTS:
        for batch in ("needed", "present"):
            pf = per_fact(g, name, batch=batch)
            never = sum(1 for r, _, _ in pf.values() if r == 0)
            always = sum(1 for r, _, _ in pf.values() if r == 1)
            print(f"     {name:<14}{batch:<10}{always:>5}"
                  f"{never:>7}{len(pf):>5}")
    print("\n     The NEEDED facts no summary kept, which is the")
    print("     list a must-keep check exists to produce:\n")
    for name in PROMPTS:
        pf = per_fact(g, name, batch="needed")
        never = [(f, p, fm) for f, (r, p, fm) in pf.items() if r == 0]
        print(f"     {name}, {len(never)} of {len(pf)}:")
        for f, p, fm in never:
            print(call.wrap(f"{p[:3]}/{fm[:3]}  {f}",
                            "       ", "                ", 44))
        print()
    print("\n  5. WHAT THE PROBE CANNOT SEE, AND WHY THIS RUN")
    print("     COULD NOT SHOW IT. A probe is a string and not a")
    print("     reader, so every rate above is an upper bound: a")
    print("     summary can hold a probe's words and say the wrong")
    print("     thing with them. The case was supposed to carry a")
    print("     trap for that - the standard return window is 30")
    print("     days and this item is clearance, so 14 - and the")
    print("     trap was not in the record. The run never read")
    print("     returns-standard, so the 30-day window is not in")
    print("     the text being summarised, and the only 30 days")
    print("     that IS there is a different quantity: how long a")
    print("     refund takes. A hit would have been ambiguous")
    print("     rather than wrong.\n")
    FACT = "a clearance return is 14 days, not the standard 30"
    probes = next(p for f, _, _, p, _ in facts.ALL if f == FACT)
    print("     instr      probe hit   says 30 days   both")
    for name in PROMPTS:
        sel = [s for s in rows if s["prompt"] == name]
        hit = [s for s in sel if facts.kept(s["summary"], probes)]
        thirty = [s for s in sel
                  if "30 day" in facts.norm(s["summary"])
                  or "thirty day" in facts.norm(s["summary"])]
        both = [s for s in hit if s in thirty]
        print(f"     {name:<11}{len(hit):>9}{len(thirty):>15}"
              f"{len(both):>7}")
    wrong = sum(1 for s in rows
                if "30 day" in facts.norm(s["summary"])
                or "thirty day" in facts.norm(s["summary"]))
    body = record.as_text(record.record())
    in_record = facts.norm(body).count("30 day")
    read = record.record()["read"]
    print(f"\n     Out of {TRIALS} summaries each, {wrong} of"
          f" {len(rows)} say 30 days.")
    print(f"     The record says it {in_record} time(s), and"
          f" returns-standard")
    print(f"     is {'' if 'returns-standard' in read else 'not '}"
          f"among the {len(read)} documents this run read.")
    print("\n     So the gap is not measured here and the design")
    print("     is what failed rather than the mechanism: a trap")
    print("     for a confusion needs BOTH of the things being")
    print("     confused in front of the summariser, and one of")
    print("     them was in a document the run never opened. The")
    print("     probe being an upper bound stays an argument from")
    print("     what a substring test can do. A judge is the")
    print("     instrument that would settle it, which is chapter")
    print("     31's and this lab's declared non-scope.")

    body = record.as_text(record.record())
    print("\n  6. WHAT COMPACTION BOUGHT. The record against the")
    print("     summaries that replace it.\n")
    print(f"     the record            {len(body):>6,} characters")
    for name in PROMPTS:
        w = [len(s["summary"]) for s in rows if s["prompt"] == name]
        mean = sum(w) / len(w)
        r, _ = rate(g, prompt=name)
        print(f"     {name + ' summary':<22}{mean:>6,.0f}"
              f"  a factor of {len(body) / mean:>2.0f}"
              f"   {r:.0%} of facts")
    print("\n     The warning costs characters and the factor falls")
    print("     with them. Whether that trade is worth taking is")
    print("     the one thing this program cannot tell you, because")
    print("     it depends on what the next step needs - and the")
    print("     must-keep list is how you decide it rather than")
    print("     guess it.")
```

```text
  24 summaries of one record, 12 per instruction,
  checked against 37 facts: 888 fact-and-summary pairs.

  Probe sets the CASE STATEMENT alone satisfies: 2,
  of which 0 are scored and 2 are excluded as the
  case's own particulars. Every summary restates the
  case, so a probe the case satisfies measures nothing.
  This audit found six and five were tightened; what
  is left is in facts.TRIVIAL.

  0. THE TWO BATCHES, which have to be read apart.

     A must-keep list is chapter 35's definition: the
     facts the rest of the task depends on. The first
     20 facts are that. The second 20 are facts that
     merely APPEAR in the record and that no step of
     this case needs - the Northern Ireland surcharge,
     on a case about an IV postcode. I wrote them to
     buy units and changed the question doing it.

     instruction   words   needed   present   both
     naive           112      26%       10%    17%
     warned          232      38%       11%    23%

     needed - present  +0.21   -0.017 to +0.444   cannot

     That difference does NOT clear zero.
     A summary drops what the task does not need,
     which is what a summary is
     FOR, so some gap here is expected. The two
     batches are still reported apart rather than
     pooled, because they answer different questions.

     Before any of this it was +0.43 and cleared zero.
     Two things moved it, and the program reports both,
     because which of them you stop at decides the
     verdict:

       the audit - five loose probe sets tightened,
         every summary restating the case
       the exclusion - three facts the CASE states
         outright, which no summary could drop

       3rd fact scored   +0.25  +0.013 to +0.477  clears zero
       3rd excluded too  +0.21  -0.017 to +0.444  cannot tell

     One judgement about one fact is the difference
     between a verdict and none, which is not a
     reason to pick the one you prefer.

     So nothing here is safe to quote: 17 facts
     against 20 put the verdict inside the width of
     one decision about one fact. A gap between a case's
     own facts and facts merely in its record is one
     anybody would expect; what this measurement can
     carry is the mechanism and not the number.

     What survives is the list's real use, which does
     not need a rate at all. Not catching a summariser
     careless about negatives: telling you which of the
     facts YOU need are among the ones it dropped.

     The batches are not matched on which document a
     fact came from. Restricted to the 4 documents
     both draw on (14 needed, 18 present):
       needed - present  +0.20   -0.054 to +0.451   cannot

     6 facts are kept by every summary: 4 needed and
     2 present, so the batches are not cleanly
     separated by difficulty either. Crossing fixes the
     confounds you name, and nothing else.

  1. THE CROSSED TABLE, which is why the facts were
     chosen in four cells rather than two.
     The NEEDED batch only - the must-keep list.

     naive
       polarity    number     prose       all
       negative       40%      0%       20%
       positive       60%      0%       35%

     warned
       polarity    number     prose       all
       negative       43%     35%       39%
       positive       56%      8%       36%

     the margins, per instruction:

       naive
         polarity  negative 20%   positive 35%
         form      prose    0%   number   49%
         the form gap is +0.49 and the
         polarity gap +0.15, so form is
         the larger of the two here - and section
         2 is whether either is established.

       warned
         polarity  negative 39%   positive 36%
         form      prose    25%   number   49%
         the form gap is +0.24 and the
         polarity gap -0.03, so form is
         the larger of the two here - and section
         2 is whether either is established.

     Over both instructions the lowest cell is positive AND
     prose, at 4%. A margin is an average over a row
     or a column, and the loss here is in one cell.

  2. IS THE POLARITY DIFFERENCE REAL. One FACT to a
     row, trials averaged within the fact, and the two
     groups resampled INDEPENDENTLY, because a
     fact's polarity is a property of the fact, so the
     two groups are two samples and not pairs.

     instr    neg   pos   diff   95% interval   says
     naive     20%   35%   0.15  -0.257 to +0.548  cannot
     warned    39%   36%  -0.03  -0.443 to +0.383  cannot

     and the same question asked of form, which the
     margins say is the comparable difference:

     instr    pro   num   diff   95% interval   says
     naive      0%   49%   0.49  +0.157 to +0.778  number
     warned    25%   49%   0.24  -0.155 to +0.619  cannot

  3. DOES THE WARNING RECOVER THEM. The same facts under
     the two instructions, paired by fact.

     batch     facts      n   diff   95% interval    says
     needed    prose     8   0.25  +0.031 to +0.531  warned
     needed    number    9  -0.00  -0.056 to +0.056  cannot

     needed    all      17   0.12  +0.005 to +0.265  warned
     needed    negative 10   0.19  +0.017 to +0.425  warned
     needed    positive  7   0.01  -0.071 to +0.107  cannot

     present   all      20   0.01  +0.000 to +0.037  cannot
     present   negative 10   0.00  +0.000 to +0.000  cannot
     present   positive 10   0.03  +0.000 to +0.075  cannot

     both      all      37   0.06  +0.007 to +0.135  warned
     both      negative 20   0.10  +0.004 to +0.221  warned
     both      positive 17   0.02  -0.020 to +0.069  cannot

     and cell by cell, which is where the two findings
     stop agreeing:

     cell          naive  warned   change
     neg/num         40%     43%      +3%
     neg/pro          0%     35%     +35%
     pos/num         60%     56%      -4%
     pos/pro          0%      8%      +8%

     The whole recovery is in one cell, neg/pro, at
     +35%. No other cell moves by more than
     8%.
     So the loss and the recovery are not the same
     shape: under the naive instruction BOTH prose
     cells are empty, and the warning refills the one
     that is also negative. A sentence asking for what
     is not so recovers prose negatives and does
     nothing for prose positives.

  4. THE FACTS NO SUMMARY KEPT, which is what a rate
     cannot show you.

     instruction   batch     every   none   of
     naive         needed        4     12   17
     naive         present       2     18   20
     warned        needed        5      7   17
     warned        present       2     17   20

     The NEEDED facts no summary kept, which is the
     list a must-keep check exists to produce:

     naive, 12 of 17:
       neg/num the 14 days run from delivery, not
                from dispatch
       neg/num goodwill is capped at 20 pounds and
                is not a refund
       neg/num the 14 days do not start until the
                warehouse books it in
       neg/pro postage on a clearance return is
                not paid by us
       neg/pro no postage label is issued for a
                clearance return
       neg/pro a refund cannot go to a different
                card
       neg/pro final-sale items cannot be returned
                at all
       neg/pro opening the box to look does not
                make an item used
       pos/num the bank may take three further
                working days
       pos/pro a return reference begins RET-
       pos/pro account credit is immediate and
                does not expire
       pos/pro the warehouse inspects every return
                on arrival

     warned, 7 of 17:
       neg/num the 14 days run from delivery, not
                from dispatch
       neg/num goodwill is capped at 20 pounds and
                is not a refund
       neg/pro no postage label is issued for a
                clearance return
       neg/pro opening the box to look does not
                make an item used
       pos/num the bank may take three further
                working days
       pos/pro account credit is immediate and
                does not expire
       pos/pro the warehouse inspects every return
                on arrival


  5. WHAT THE PROBE CANNOT SEE, AND WHY THIS RUN
     COULD NOT SHOW IT. A probe is a string and not a
     reader, so every rate above is an upper bound: a
     summary can hold a probe's words and say the wrong
     thing with them. The case was supposed to carry a
     trap for that - the standard return window is 30
     days and this item is clearance, so 14 - and the
     trap was not in the record. The run never read
     returns-standard, so the 30-day window is not in
     the text being summarised, and the only 30 days
     that IS there is a different quantity: how long a
     refund takes. A hit would have been ambiguous
     rather than wrong.

     instr      probe hit   says 30 days   both
     naive             12              0      0
     warned            12              0      0

     Out of 12 summaries each, 0 of 24 say 30 days.
     The record says it 1 time(s), and returns-standard
     is not among the 5 documents this run read.

     So the gap is not measured here and the design
     is what failed rather than the mechanism: a trap
     for a confusion needs BOTH of the things being
     confused in front of the summariser, and one of
     them was in a document the run never opened. The
     probe being an upper bound stays an argument from
     what a substring test can do. A judge is the
     instrument that would settle it, which is chapter
     31's and this lab's declared non-scope.

  6. WHAT COMPACTION BOUGHT. The record against the
     summaries that replace it.

     the record            11,585 characters
     naive summary            653  a factor of 18   17% of facts
     warned summary         1,466  a factor of  8   23% of facts

     The warning costs characters and the factor falls
     with them. Whether that trade is worth taking is
     the one thing this program cannot tell you, because
     it depends on what the next step needs - and the
     must-keep list is how you decide it rather than
     guess it.
```

**Chapter 35's claim is not established and the alternative it half-suspected is.** On the batch
that is a must-keep list, the one difference that clears zero is *form*: under the naive
instruction, **not one prose fact survived a single summary** — 0 of 96 observations, eight facts
over twelve trials — against 53 of 108 for the facts carrying a number. That is +0.49 with 95 per
cent from +0.157 to +0.778. Polarity is +0.15 from −0.257 to +0.548, and under the warned
instruction it is −0.03. **What this summariser drops is what has no number in it**, and whether a
fact is about something that is not so cannot be shown to matter at ten facts against seven.

**Chapter 35 suspected exactly this and could not name it.** Its own paragraph says three of the
facts its naive summary kept were not events either, so *being about a path not taken* might be
doing the work rather than being a negative. It had the doubt and no way to test it, because its
list was not crossed. The crossed list is what turns the doubt into a measurement, and the
measurement says the other thing.

**And the recovery is not the same shape as the loss, which is the finding a margin cannot
produce.** Read the cells before and after the warning. Both prose cells are empty under the
naive instruction. The warning refills *one* of them — negative-and-prose goes from 0 to 35 per
cent — and no other cell moves by more than eight points. So:

- what a summary drops is *prose*, both polarities, completely;
- what one sentence asking for the things that are not so recovers is *prose negatives*, and
  it does nothing measurable for prose positives (+8 points) or for anything with a number
  (+3 and −4).

Paired by fact, that is +0.25 on prose from +0.031 to +0.531 and −0.00 on numbers from −0.056 to
+0.056. **The instruction recovers exactly the cell that was empty and that it asked about**, which
is a better result than either margin alone and is invisible in both of them.

**The needed-against-present difference is the one I would most like to have, and it is the one to
distrust.** Facts the case depends on are kept 26 and 38 per cent under the two instructions;
facts that merely appear in the record, 10 and 11. The program reports it two ways on purpose,
because the verdict moves with one judgement: score the third case particular and it is +0.25 from
+0.013 to +0.477, clearing zero; exclude it and it is +0.21 from −0.017 to +0.444, clearing
nothing. **One decision about one fact is the width of the verdict.** That is not a reason to pick
the reading you prefer; it is what an unestablished difference looks like from the inside. Before
the probe audit it was +0.43 and comfortably clear.

**What survives from the batch mistake needs no rate at all.** It is what the must-keep list is
for, and it is the other way round from the way I had been reading it. Not *catching a summariser
that is careless about negatives*. **Telling you which of the facts you need are among the ones it
dropped** — a use the list can only have if it is the list Chapter 35 defines, and mine was half
something else until I looked.

**Chapter 35's advice comes out intact from a measurement that refuses its claim.** Read by
polarity the warning is worth +0.19 on negatives, 95 per cent from +0.017 to +0.425, and +0.01 on
positives from −0.071 to +0.107; over all seventeen needed facts +0.12, from +0.005 to +0.265. The
number of needed facts no summary kept at all falls from twelve to seven. So put the sentence in.
What you cannot do is quote the reason: the effect lives in the cell that is both negative and
prose, so *asking for negatives* and *asking for the thing with no number in it* are the same
instruction on this data and nothing here separates them.

**Why that comparison answers and the other two do not is worth more than the result.** The
warning comparison puts the same twenty facts on both sides, so the unit resampled is a fact
measured twice and the fact's own difficulty cancels. The polarity comparison cannot do that,
because a fact's polarity is a property of the fact: ten negatives and eight positives are two
samples, not pairs, and the pairing does not exist to be used. **Whether you can pair is a
property of the question and not a choice of method.** That sentence is the reason this chapter's
three measurements come out so differently from one another, and it is the thing to carry out of
it.

Be exact about what else differs, because the pairing is not the only thing. The warning
comparison also estimates a smaller quantity, and the polarity comparison is confounded with form
while the warning comparison is not. Three reasons, not one. What makes the pairing worth naming
first is that it is the only one of the three you decide before you have any data.

> **Warning:** The first version of this program got that wrong in the most tempting way
> available. It sorted the negative rates and the positive rates and zipped them, which pairs the
> smallest with the smallest and feeds Chapter 20's *paired* bootstrap a pairing the data does not
> have. On the figures it was run against it reported +0.017 to +0.167 where the honest interval
> is −0.292 to +0.483 — a verdict instead of a refusal, 5.2 times narrower by width, and arrived
> at by an edit that looked like tidying. The function that replaced it carries that history in
> its docstring, because the next person to reach for `zip(sorted(a), sorted(b))` will be me.

> **Note:** The needed-against-present comparison carries a confound of its own that the cells do
> not cover, and it is worth naming even though the comparison gives no verdict. The two batches
> are not matched on which document a fact came from: every fact with a keep rate of 1.00 is in
> the needed batch, and thirteen of the twenty present facts come from the two documents with the
> lowest rates of all. Restricted to the five documents both batches draw on, the difference is
> +0.346 from +0.083 to +0.610 — larger and clearing zero, on fewer facts. So the honest summary
> is that a document effect and a needed effect are tangled here, this chapter cannot separate
> them, and the crossed design that handles polarity and form does nothing for a third factor
> nobody thought of. Which is the general shape of the thing: **crossing fixes the confounds you
> name.**

> **Note:** Section 5 was meant to be a trap for the probe's own limit and the trap was not in the
> record. The idea was sound: the standard return window is 30 days and this item is clearance, so
> 14, and a summary saying 30 would have the window wrong while the 14-day probe said nothing
> about it. But the run never read `returns-standard`, so the 30-day window is not in the text
> being summarised — and the one *30 days* that is in the record is a different quantity, how long
> a refund takes. So a hit would have been ambiguous rather than wrong, and there were none
> anyway. **A trap for a confusion needs both of the confused things in front of the summariser**,
> and the design of this one depended on a document the loop chose not to open. The claim that a
> string probe is an upper bound on what survived therefore stands as an argument about what a
> substring test can do, and *nothing in this chapter measures the gap*. A judge would, which is
> Chapter 31's instrument and this chapter's declared non-scope.

## Step 4: Write Notes the Agent Reads Back

Chapter 35's other arrangement puts facts outside the window: the agent writes a key and a value,
and reads it back on a later run. The chapter's claim about it is precise and it is about *who the
two fields are for* — provenance does not make a note true, it tells *you* which notes can
expire and which were never checked.

That is testable, and testing it needs three arms rather than two.

```python
"""A structured-notes store the agent writes to and reads back.

Chapter 35 owns the term and the two fields. What it says about them
is the thing this chapter tests: provenance does not make a note
true, it tells YOU which notes can expire and which were never
checked. So the question is whether handing those fields to the model
does anything, and the answer needs a third arm - your code checking
the note before the model ever sees it - because a comparison
between hiding the fields and showing them cannot tell you what
checking them is worth. That is chapter 47's lesson, applied before
the runs rather than after.

Every note below is one the agent could plausibly have written on an
earlier case in this corpus, and each is labelled with what is
actually so, read from the document named. The labels are the
grader, not the input: no arm sees the `truth` or `doc` field.
"""
import pathlib
import re
from datetime import date

DOCS = pathlib.Path("corpus/docs")
TODAY = date(2026, 10, 30)

#  key, what the note says, written, source, what is so, document
NOTES = [
    ("standard_return_days", "30", date(2026, 2, 3), "read",
     "30", "returns-standard"),
    ("clearance_return_days", "30", date(2026, 2, 3), "inferred",
     "14", "returns-clearance"),
    ("clearance_postage", "free", date(2026, 4, 19), "inferred",
     "paid by the customer", "returns-clearance"),
    ("refund_days", "14", date(2026, 1, 11), "read",
     "14", "refunds-policy"),
    ("goodwill_cap_pounds", "20", date(2026, 3, 8), "read",
     "20", "refunds-policy"),
    ("iv_surcharge_pounds", "6.50", date(2026, 5, 2), "told",
     "9.50", "delivery-exceptions"),
    ("transfer_working_days", "10", date(2026, 6, 14), "read",
     "10", "refund-to-a-closed-card"),
    ("credit_expires", "no", date(2026, 6, 14), "read",
     "no", "refund-to-a-closed-card"),
]

#  What each source word tells you, which is chapter 35's table and
#  is reproduced in the prompt for the provenance arm WORD FOR WORD,
#  so that arm is given the best version of the advice rather than a
#  hint of it. If showing the model provenance helps at all, this is
#  the arrangement in which it would.
MEANS = {
    "read": "was true of a document on the date written",
    "inferred": "was never checked against anything",
    "told": "is as good as whoever said it",
}


def norm(s):
    return re.sub(r"\s+", " ", str(s)).lower()


def verdict(note):
    """correct, stale or wrong - and the distinction is chapter 35's.

    A note that was true when written and has been overtaken is
    stale; one that was false the day it was written is wrong. This
    corpus has no dated changes in it, so every incorrect note here
    is WRONG rather than stale, and saying so is better than
    labelling one of them stale to fill the cell.
    """
    _, says, _, _, truth, _ = note
    return "correct" if norm(says) == norm(truth) else "wrong"


def grounded():
    """Every note's truth field is in the document it names."""
    bad = []
    for note in NOTES:
        key, says, _, _, truth, doc = note
        body = norm((DOCS / f"{doc}.md").read_text())
        if norm(truth) not in body:
            bad.append((key, truth, doc))
    return bad


def render(arm):
    """The notes as one arm puts them in the context.

    bare        key = value, which is chapter 35's first table
    provenance  the two fields, and what each source word means
    checked     your code re-reads the document and drops a note it
                cannot find there - so the model is handed fewer
                notes rather than better-labelled ones
    """
    lines = []
    for note in NOTES:
        key, says, written, source, truth, doc = note
        if arm == "bare":
            lines.append(f"  {key} = {says}")
        elif arm == "provenance":
            age = (TODAY - written).days
            lines.append(f"  {key} = {says}   [source: {source}, "
                         f"{MEANS[source]}; written {age} days ago]")
        elif arm == "checked":
            body = norm((DOCS / f"{doc}.md").read_text())
            if norm(says) in body:
                lines.append(f"  {key} = {says}   [checked against "
                             f"{doc} today]")
        else:
            raise ValueError(arm)
    return "\n".join(lines)


def kept_by_checked():
    """Which notes survive the checked arm, and why that is not a
    free lunch: the check is a substring test against one named
    document, so it keeps a note whose words appear there for some
    other reason and drops one phrased differently from a document
    that agrees with it."""
    out = []
    for note in NOTES:
        key, says, _, _, _, doc = note
        body = norm((DOCS / f"{doc}.md").read_text())
        out.append((key, norm(says) in body, verdict(note)))
    return out


ARMS = ("bare", "provenance", "checked")


if __name__ == "__main__":
    print(f"  {len(NOTES)} notes an agent wrote on earlier cases.\n")
    print("  note                    says   source      verdict")
    for note in NOTES:
        key, says, _, source, _, _ = note
        print(f"  {key:<23} {str(says):<6} {source:<11} "
              f"{verdict(note)}")
    wrong = [n for n in NOTES if verdict(n) == "wrong"]
    print(f"\n  {len(wrong)} of {len(NOTES)} are wrong:")
    for note in wrong:
        key, says, _, source, truth, doc = note
        print(f"    {key}")
        print(f"      says {says}, source {source}")
        print(f"      {doc} says {truth}")

    bad = grounded()
    print(f"\n  Every note's truth field checked against the document")
    print(f"  it names: {len(NOTES) - len(bad)} of {len(NOTES)} found,"
          f" {len(bad)} not.")

    print("\n  What each arm puts in the context.\n")
    for arm in ARMS:
        body = render(arm)
        n = len([l for l in body.splitlines() if l.strip()])
        print(f"    {arm:<11} {n} notes, {len(body):>4} characters")
    print()
    for arm in ARMS:
        print(f"    {arm}")
        for line in render(arm).splitlines():
            print(f"    {line[:58]}")
        print()

    k = kept_by_checked()
    dropped = [(key, v) for key, ok, v in k if not ok]
    print(f"  The checked arm drops {len(dropped)} of {len(NOTES)}"
          f" notes:")
    for key, v in dropped:
        print(f"    {key} ({v})")
    right = sum(1 for _, ok, v in k if ok and v == "correct")
    kept_wrong = [key for key, ok, v in k if ok and v == "wrong"]
    print(f"\n  Of the {len(NOTES) - len(dropped)} it keeps,"
          f" {right} are correct and {len(kept_wrong)}"
          f" {'is' if len(kept_wrong) == 1 else 'are'} wrong.")
    if kept_wrong:
        print("  The wrong one it keeps is the check's own limit: a")
        print("  substring test finds the words somewhere in the")
        print("  document and does not read them in context.")
        for key in kept_wrong:
            print(f"    {key}")
```

```text
  8 notes an agent wrote on earlier cases.

  note                    says   source      verdict
  standard_return_days    30     read        correct
  clearance_return_days   30     inferred    wrong
  clearance_postage       free   inferred    wrong
  refund_days             14     read        correct
  goodwill_cap_pounds     20     read        correct
  iv_surcharge_pounds     6.50   told        wrong
  transfer_working_days   10     read        correct
  credit_expires          no     read        correct

  3 of 8 are wrong:
    clearance_return_days
      says 30, source inferred
      returns-clearance says 14
    clearance_postage
      says free, source inferred
      returns-clearance says paid by the customer
    iv_surcharge_pounds
      says 6.50, source told
      delivery-exceptions says 9.50

  Every note's truth field checked against the document
  it names: 8 of 8 found, 0 not.

  What each arm puts in the context.

    bare        8 notes,  209 characters
    provenance  8 notes,  852 characters
    checked     6 notes,  424 characters

    bare
      standard_return_days = 30
      clearance_return_days = 30
      clearance_postage = free
      refund_days = 14
      goodwill_cap_pounds = 20
      iv_surcharge_pounds = 6.50
      transfer_working_days = 10
      credit_expires = no

    provenance
      standard_return_days = 30   [source: read, was true of a
      clearance_return_days = 30   [source: inferred, was neve
      clearance_postage = free   [source: inferred, was never 
      refund_days = 14   [source: read, was true of a document
      goodwill_cap_pounds = 20   [source: read, was true of a 
      iv_surcharge_pounds = 6.50   [source: told, is as good a
      transfer_working_days = 10   [source: read, was true of 
      credit_expires = no   [source: read, was true of a docum

    checked
      standard_return_days = 30   [checked against returns-sta
      refund_days = 14   [checked against refunds-policy today
      goodwill_cap_pounds = 20   [checked against refunds-poli
      iv_surcharge_pounds = 6.50   [checked against delivery-e
      transfer_working_days = 10   [checked against refund-to-
      credit_expires = no   [checked against refund-to-a-close

  The checked arm drops 2 of 8 notes:
    clearance_return_days (wrong)
    clearance_postage (wrong)

  Of the 6 it keeps, 5 are correct and 1 is wrong.
  The wrong one it keeps is the check's own limit: a
  substring test finds the words somewhere in the
  document and does not read them in context.
    iv_surcharge_pounds
```

**Eight notes, three of them wrong, and the store knows which because each note names the
document that contradicts it.** Those labels are the grader and no arm sees them.

**All three wrong notes are wrong rather than stale, and that is a limit worth stating.** Chapter
35's distinction is sharp — a note true when written and overtaken by a change is *stale* and a
date catches it; a note false the day it was written is *wrong* and no date ever will. This corpus
has no dated changes in it, so it can produce the second kind and not the first. Labelling one of
these three stale to fill the cell would have been inventing the evidence for the more
interesting half of Chapter 35's claim. So the half about staleness is not tested here, and the
reason is the corpus rather than the method.

**The third arm is your code doing the work.** Two arms — notes bare, and notes with the two
fields — would have measured only whether telling the model helps. The arm that matters is the
one where your code re-reads the document and drops a note it cannot find there, because that is
what the fields are *for* on Chapter 35's own account. Three arms make the two questions
separable: bare against provenance is telling the model, provenance against checked is checking
instead of telling.

**And the check's own limit shows up before any model is called.** It drops two of the three
wrong notes and keeps the third. `iv_surcharge_pounds = 6.50` passes a substring check against
`delivery-exceptions`, because 6.50 is in that document — it is the Northern Ireland surcharge,
and the note is about an IV postcode, which is 9.50. A check that asks *are these words in the
document* and not *do these words mean this here* will pass a note built from the right document
and the wrong line. That is the same verdict Chapter 28 reached about a mechanical citation check
and Chapter 35 about the must-keep probe, and it is the third time this book has arrived at it
from a different direction.

## Step 5: Find Out What Provenance Is Worth

Six questions, three of which hinge on a note that is wrong and three on a note that is correct.
The second group is the control: without it, an arm that answered worse in general would read as
an arm that distrusted its notes.

**The agent has both tools in every arm and nothing stops it looking.** That is the measurement.

```python
"""Does the agent act on a note that is wrong, and what changes it.

Chapter 35 says a note is model output read back as though somebody
had checked it, and that provenance does not make a note true - it
tells YOU which notes can expire and which were never verified. That
is a claim about who the two fields are for, and it is testable: show
them to the model and see whether anything moves.

Three arms, because two could not separate the two questions:

    bare        key = value
    provenance  the two fields and what each source word means
    checked     your code re-reads the document and drops a note it
                cannot find there

bare against provenance is telling the model. provenance against
checked is your code doing the work instead. Everything else is held:
the same questions, the same tools, the same instruction, the same
corpus, and the notes themselves are identical apart from what the
arm is allowed to say about them.

The agent has the tools to check every note it is given. Nothing
stops it looking. That is the point of the measurement.
"""
import json
import pathlib

import call
import record
import search
import store

OUT = pathlib.Path("trust.json")
TRIALS = 3
STEP_LIMIT = 8

#  id, question, the phrases that MEAN the noted value, the phrases
#  that mean what is so, the note it hinges on.
#
#  Both are SETS, and the first version of this program used single
#  strings. That version scored six runs `neither` when every one of
#  them said "the retailer pays return postage on a clearance item",
#  which is the wrong note restated - it just does not contain the
#  word "free". A grader that tests one spelling of an answer
#  reports a paraphrase as a non-answer, and chapter 41's rule is
#  that the repair has to be justified by what the grader is meant
#  to detect. These sets are that repair; the phrases came from
#  reading the stored answers for what they MEAN, not for which arm
#  they help.
TASKS = [
    ("q1", "A customer wants to return a clearance item delivered "
           "9 days ago. How many days do they have?",
     {"30 day", "thirty day", "21 day", "twenty-one day",
      "30 standard"},
     {"14 day", "fourteen day", "5 day", "five day"},
     "clearance_return_days"),
    ("q2", "Who pays return postage on a clearance item?",
     {"free", "we pay", "retailer pays", "harbour lane pays",
      "no cost to the customer", "prepaid"},
     {"customer pays", "paid by the customer",
      "the customer is responsible", "customer bears",
      "at their own cost", "they pay"},
     "clearance_postage"),
    ("q3", "What surcharge applies to a delivery to an IV postcode?",
     {"6.50"}, {"9.50"},
     "iv_surcharge_pounds"),
    ("q4", "How many days after the return arrives is a refund "
           "issued?",
     {"14 day", "fourteen day"}, {"14 day", "fourteen day"},
     "refund_days"),
    ("q5", "What is the cap on a goodwill payment?",
     {"20 pound", "20 GBP", "twenty pound", "£20"},
     {"20 pound", "20 GBP", "twenty pound", "£20"},
     "goodwill_cap_pounds"),
    ("q6", "How long does a bank transfer take?",
     {"10 working day", "ten working day"},
     {"10 working day", "ten working day"},
     "transfer_working_days"),
]

PROTOCOL = (
    "You have two tools.\n"
    "  {\"search\": \"<words>\"}        find documents\n"
    "  {\"read\": \"<document id>\"}    read one in full\n"
    "  {\"done\": \"<your answer>\"}   when you can answer\n"
    "Reply with JSON, exactly one of those three keys."
)

#  Built by concatenation rather than str.format, because the
#  protocol itself contains braces and format reads them as fields.
#  The first run of this program died on it.
def instruction(notes_block):
    return (
        "You are answering one question about this retailer's "
        "policies. " + PROTOCOL +
        "\n\nYou also have notes from earlier cases:\n"
        + notes_block + "\n\nAnswer the question."
    )


def hinges(tid):
    return next(t for t in TASKS if t[0] == tid)


def grade(answer, noted, truth):
    """Which value the answer carries, read as two independent tests.

    A reply can hold both, and counting it as one or the other would
    be a choice the data does not support - so both columns are
    reported and `both` is its own outcome. `neither` now means
    neither reading is present, which on this data is a run that
    gave no answer at all; before the phrase sets above it also
    held every paraphrase.
    """
    body = store.norm(answer)
    said_truth = any(store.norm(p) in body for p in truth)
    said_note = any(store.norm(p) in body for p in noted)
    if noted == truth:
        return "agrees" if said_truth else "neither"
    if said_truth and said_note:
        return "both"
    if said_truth:
        return "corrected"
    if said_note:
        return "trusted"
    return "neither"


def one(question, notes_block, cache):
    msgs, steps, searched = [], [], 0
    for n in range(STEP_LIMIT):
        prompt = (instruction(notes_block)
                  + f"\n\nThe question: {question}\n\n"
                  + "What has happened so far:\n"
                  + ("\n".join(msgs) if msgs else "nothing yet")
                  + "\n\nYour next reply:")
        r = call.chat(prompt, json_mode=True, max_tokens=700)
        d = call.as_json(r["text"])
        if d is None:
            return {"answer": r["text"], "steps": steps,
                    "searches": searched, "ended": "unparsed",
                    "chat_calls": n + 1}
        if "done" in d:
            return {"answer": str(d["done"]), "steps": steps,
                    "searches": searched, "ended": "answered",
                    "chat_calls": n + 1}
        if "search" in d:
            res = record.tool_search(str(d["search"]), cache)
            searched += 1
            steps.append(("search", str(d["search"])))
            msgs.append(f"searched {d['search']!r} -> "
                        + ", ".join(x["id"] for x in res))
        elif "read" in d:
            doc = str(d["read"])
            res = record.tool_read(doc)
            steps.append(("read", doc))
            if "error" in res:
                msgs.append(f"read {doc!r} -> {res['error']}")
            else:
                msgs.append(f"read {doc!r}:\n{res['text']}")
        else:
            return {"answer": r["text"], "steps": steps,
                    "searches": searched, "ended": "no key",
                    "chat_calls": n + 1}
    return {"answer": "", "steps": steps, "searches": searched,
            "ended": "step limit", "chat_calls": STEP_LIMIT}


def run():
    cache = search.vectors()
    blocks = {arm: store.render(arm) for arm in store.ARMS}
    out = []
    for arm in store.ARMS:
        for tid, q, noted, truth, note_key in TASKS:
            for trial in range(1, TRIALS + 1):
                r = one(q, blocks[arm], cache)
                reads = [t for k, t in r["steps"] if k == "read"]
                row = {"arm": arm, "task": tid, "trial": trial,
                       "note": note_key,
                       "noted": noted, "truth": truth,
                       "answer": r["answer"],
                       "searches": r["searches"],
                       "reads": reads,
                       "chat_calls": r["chat_calls"],
                       "ended": r["ended"],
                       "outcome": grade(r["answer"], noted, truth)}
                out.append(row)
                OUT.write_text(json.dumps(out, indent=1))
                print(f"    {arm:<11} {tid} t{trial}: "
                      f"{row['outcome']:<10} "
                      f"{len(reads)} read, {r['searches']} search")
    return out


def rows():
    return json.loads(OUT.read_text()) if OUT.exists() else run()


if __name__ == "__main__":
    rs = rows()
    #  Re-grade every stored answer with the CURRENT grader rather
    #  than trusting the verdict written when the run happened,
    #  which is chapter 45's habit and the reason the repair above
    #  could be made without re-running anything.
    moved = []
    for r in rs:
        tid = r["task"]
        _, _, noted, truth, _ = hinges(tid)
        now = grade(r["answer"], noted, truth)
        if now != r["outcome"]:
            moved.append((tid, r["arm"], r["trial"],
                          r["outcome"], now))
        r["outcome"] = now
    bad = [t for t in TASKS if t[2] != t[3]]
    good = [t for t in TASKS if t[2] == t[3]]
    if moved:
        print(f"  Re-graded with the phrase sets: {len(moved)} of"
              f" {len(rs)} verdicts move.\n")
        for tid, arm, trial, was, now in moved:
            print(f"    {tid} {arm} t{trial}: {was} -> {now}")
        print()
    print(f"  {len(rs)} runs: {len(store.ARMS)} arms x {len(TASKS)}"
          f" questions x {TRIALS} trials.")
    print(f"  {len(bad)} questions hinge on a note that is WRONG and"
          f" {len(good)}")
    print("  on one that is correct - the second group is there so a")
    print("  drop in one arm can be told from an arm that answers")
    print("  worse in general.\n")

    print("  1. WHAT THE ANSWER CARRIED, on the three questions")
    print("     whose note is wrong.\n")
    print("     arm          trusted   corrected   both  neither")
    for arm in store.ARMS:
        sel = [r for r in rs if r["arm"] == arm
               and r["note"] in {t[4] for t in bad}]
        c = {k: sum(1 for r in sel if r["outcome"] == k)
             for k in ("trusted", "corrected", "both", "neither")}
        print(f"     {arm:<13}{c['trusted']:>6}{c['corrected']:>12}"
              f"{c['both']:>7}{c['neither']:>9}")
    print(f"\n     Out of {len(bad) * TRIALS} runs each.\n")

    print("  2. AND ON THE THREE WHOSE NOTE IS CORRECT, which is")
    print("     the arm's general accuracy and not the question.\n")
    print("     arm          agrees   neither")
    for arm in store.ARMS:
        sel = [r for r in rs if r["arm"] == arm
               and r["note"] in {t[4] for t in good}]
        ag = sum(1 for r in sel if r["outcome"] == "agrees")
        print(f"     {arm:<13}{ag:>6}{len(sel) - ag:>10}")

    print("\n  3. DID IT GO AND LOOK. The agent had the tools to")
    print("     check every note it was given.\n")
    print("     arm          reads   searches   runs that read 0")
    for arm in store.ARMS:
        sel = [r for r in rs if r["arm"] == arm]
        reads = sum(len(r["reads"]) for r in sel)
        srch = sum(r["searches"] for r in sel)
        none = sum(1 for r in sel if not r["reads"])
        print(f"     {arm:<13}{reads:>5}{srch:>11}{none:>19}")

    print("\n  4. THE SAME QUESTION PER TASK, because a rate over")
    print("     three questions hides which one moved.\n")
    print("     task  note                     bare  prov  chkd")
    for tid, q, noted, truth, key in TASKS:
        cells = []
        for arm in store.ARMS:
            sel = [r for r in rs if r["arm"] == arm
                   and r["task"] == tid]
            c = sum(1 for r in sel
                    if r["outcome"] in ("corrected", "agrees"))
            cells.append(f"{c}/{len(sel)}")
        mark = " " if store.norm(noted) == store.norm(truth) else "*"
        print(f"     {tid}{mark}  {key:<24}"
              + "".join(f"{c:>6}" for c in cells))
    print("\n     * the note is wrong. The cell is how many runs")
    print("       gave the value the document gives.")

    print("\n  5. HOW THE RUNS ENDED, and what the arms cost.\n")
    print("     arm          answered   step limit   chat calls")
    for arm in store.ARMS:
        sel = [r for r in rs if r["arm"] == arm]
        ans = sum(1 for r in sel if r["ended"] == "answered")
        lim = sum(1 for r in sel if r["ended"] == "step limit")
        print(f"     {arm:<13}{ans:>8}{lim:>13}{sum(r['chat_calls'] for r in sel):>13}")

    print("\n  6. WHAT THIS CAN AND CANNOT ESTABLISH.\n")
    looked = sum(1 for r in rs if r["reads"])
    print(f"     {looked} of {len(rs)} runs opened a document. That is a")
    print(f"     count over {len(rs)} runs and needs no interval: the")
    print("     agent had the tools to check every note it was")
    print("     given, in every arm, and all but")
    print(f"     {looked} runs answered without looking.")
    print()
    print(f"     The outcome table above rests on {len(bad)} questions.")
    print("     Three questions cannot carry chapter 20's interval -")
    print("     the unit it resamples is the question, and three of")
    print("     them resample to almost nothing. So read sections 1")
    print("     and 4 as counts, and the thing to carry is the")
    print("     mechanism in section 4 rather than any rate: which")
    print("     questions moved, and why that one did.")
```

```text
  Re-graded with the phrase sets: 6 of 54 verdicts move.

    q2 bare t1: neither -> trusted
    q2 bare t2: neither -> trusted
    q2 bare t3: neither -> trusted
    q2 provenance t1: neither -> trusted
    q2 provenance t2: neither -> trusted
    q2 provenance t3: neither -> trusted

  54 runs: 3 arms x 6 questions x 3 trials.
  3 questions hinge on a note that is WRONG and 3
  on one that is correct - the second group is there so a
  drop in one arm can be told from an arm that answers
  worse in general.

  1. WHAT THE ANSWER CARRIED, on the three questions
     whose note is wrong.

     arm          trusted   corrected   both  neither
     bare              9           0      0        0
     provenance        7           0      0        2
     checked           6           3      0        0

     Out of 9 runs each.

  2. AND ON THE THREE WHOSE NOTE IS CORRECT, which is
     the arm's general accuracy and not the question.

     arm          agrees   neither
     bare              9         0
     provenance        9         0
     checked           9         0

  3. DID IT GO AND LOOK. The agent had the tools to
     check every note it was given.

     arm          reads   searches   runs that read 0
     bare             0          0                 18
     provenance       0         16                 18
     checked          3          3                 15

  4. THE SAME QUESTION PER TASK, because a rate over
     three questions hides which one moved.

     task  note                     bare  prov  chkd
     q1*  clearance_return_days      0/3   0/3   0/3
     q2*  clearance_postage          0/3   0/3   3/3
     q3*  iv_surcharge_pounds        0/3   0/3   0/3
     q4   refund_days                3/3   3/3   3/3
     q5   goodwill_cap_pounds        3/3   3/3   3/3
     q6   transfer_working_days      3/3   3/3   3/3

     * the note is wrong. The cell is how many runs
       gave the value the document gives.

  5. HOW THE RUNS ENDED, and what the arms cost.

     arm          answered   step limit   chat calls
     bare               18            0           18
     provenance         16            2           32
     checked            18            0           24

  6. WHAT THIS CAN AND CANNOT ESTABLISH.

     3 of 54 runs opened a document. That is a
     count over 54 runs and needs no interval: the
     agent had the tools to check every note it was
     given, in every arm, and all but
     3 runs answered without looking.

     The outcome table above rests on 3 questions.
     Three questions cannot carry chapter 20's interval -
     the unit it resamples is the question, and three of
     them resample to almost nothing. So read sections 1
     and 4 as counts, and the thing to carry is the
     mechanism in section 4 rather than any rate: which
     questions moved, and why that one did.
```

**Three of fifty-four runs opened a document.** That is the finding, and it needs no interval
because it is a count. In all three arms, on five of the six questions, with a search tool and a read tool described in
the instruction — and in the arm that labels its notes, with two of them saying in so many words
that they were *inferred* and *never checked against anything* — the agent answered without
opening a document. The exception is the one place anything was corrected, and it is the checked
arm on the postage question: three runs, three document opens, three right answers. Those are the
three. Chapter 35's sentence is
that a note is read back *as though somebody had checked it*; what fifty-four runs show is that
the model will not be the one who checks, and will not be made to by being told.

**Showing the model the two fields corrected nothing.** Bare trusted the wrong note in nine of
nine runs and provenance in seven of nine, and neither produced a single corrected answer.
Provenance's other two runs gave no answer at all: they spent eight chat calls searching, never
opened a document, and hit the step limit. So the fields did change the behaviour, and not in the
direction the label asks for — sixteen searches against bare's zero, and nothing read.

**Both of those runs are the same question, and the label on its note is not the one you would
guess.** They are the surcharge question, whose note is sourced `told` and rendered *is as good as
whoever said it*. The two notes labelled `inferred, was never checked against anything` produced
no extra searching at all. So the searching-without-reading belongs to the hearsay label on one
question, from two runs, and attributing it to the never-verified label — which is what the first
draft of this paragraph did — credits a behaviour to a cause that did not produce it.

> **Warning:** Those nine-of-nine and seven-of-nine figures are a repair to this lab's grader, and
> the first version of them was six and four. Every one of the six runs it scored as giving
> *neither* value said *the retailer pays return postage on a clearance item* — which is the wrong
> note restated, and simply does not contain the word `free` the grader was testing for. A grader
> that tests one spelling reports a paraphrase as a non-answer, and it does so in the direction
> that flatters the arm you are examining. The repair is phrase sets, written by reading the
> stored answers for what they *mean*; it moved six of fifty-four verdicts and the program prints
> which. Chapter 41's condition is met — the repair is justified by what the grader is meant to
> detect rather than by which arm it helps — and `neither` now means what it says, a run that gave
> no answer.

**Your code dropping the note is what moved an answer, and only where it dropped the right one.**
The checked arm corrected three of nine, and all three are the same question — the postage note,
which the check dropped. The surcharge question stays wrong in all three arms because the check
kept that note, which is step 4's limit arriving with a cost attached.

**And the return-window question is the one to read twice.** The check dropped its wrong note too,
and the checked arm still answered 30 days, three times out of three. Read the answer: *a total of
30 standard return days*. With the clearance note gone, the agent reached for
`standard_return_days = 30`, which the check kept because it is *true* — of standard items.
So the wrong answer survived the removal of the wrong note, supplied by a correct note applied
outside its scope.

**That is the most useful thing in this step and it is not about provenance at all.** A note has
a [**note scope**]{idx="note scope"} — the condition under which it applies — and nothing in this store records it.
`standard_return_days` is true, was read from a document, is current, and passed the check; what
it lacks is any way to say *not for clearance items*, which is a statement about a sibling note
rather than about itself. Chapter 36's six things for a tool description
include *when not to use it*, and say it is the line a wrapper generated from one endpoint cannot
write because it is a statement about the *other* tools. A note needs the same field for the same
reason, and `standard_return_days` has no way to say *not for clearance* — which is a fact about
a sibling note. Chapter 35 gives a note two fields; this run says a third is missing, and names
it from Chapter 36 rather than inventing it.

> **Note:** Every arm answered all three control questions correctly, nine of nine, so nothing
> above is an arm that is simply worse. And the outcome table rests on three questions, which
> cannot carry Chapter 20's interval: the unit it resamples is the question, and three of them
> resample to almost nothing. So the counts are counts. What carries this step is the mechanism —
> which question moved, and why the two that did not are two different failures — rather than any
> rate.

## Step 6: Rewrite One Tool, One Change at a Time

Chapter 36's Covers list ends on improving tools by measuring use, and its worked log is the
sharpest number in that chapter: 58 of 79 defects across a whole registry were one cause, a
policy name the model invented, and one list added to one description would have removed them. It
also said what the log's labels were — a judgement written into the program so the counts could be
checked — and what would make them a measurement.

So one tool, the document reader, because this corpus has that exact failure available: the
reader refuses an id that is not in the catalogue, and the thin description does not say which ids
exist. Five versions, each meant to add one change.

**What is identical in every version** is the registry, the dispatcher, the function that reads
the file, the search tool, the questions, the grader and the step limit. That is what makes the
comparison about the description: Chapter 23's point is that your code is the only participant
that can refuse, so a difference between these arms can only be a difference in what the model
*proposed*.

```python
"""One tool, five versions, each adding one of chapter 36's changes.

Chapter 36 found that 58 of 79 defects in a whole log were one cause
- the model asking for a policy name that does not exist - and that
one list added to one description would have removed them. It said
plainly what that was: the candidate sets and the defect labels were
judgements written into the program so the counts could be checked,
and establishing what a model actually picks is chapter 20's method
applied to a real registry. This is that.

The tool is the document reader, because this corpus has chapter
36's exact defect in it: a reader refuses an id the model invented,
and nothing in the first version's description says which ids exist.

Five versions, each adding ONE change, so no result has to carry
two:

    endpoint    GET /documents/{id}, one sentence, status codes
    renamed     + a namespaced task name
    listed      + the ids, and nothing else
    documented  + the rest of chapter 36's six things, including
                  when NOT to call it
    actionable  + errors that say what to do next

AND ONE OF THEM CHANGES TWO THINGS, which is worth reading before
the table that comes out of it. refuse() below returns a status
code for endpoint, renamed and listed, then NAMES THE FAULT for
documented, then says what to do next for actionable. So
listed -> documented is the description's other five things AND the
first of chapter 36's two message improvements, not one change.

It is empirically moot here - that arm refused nothing, so its
message never fired - and it is left as it ran rather than quietly
rewritten, because the data was produced by this code. But it is
the exact confound this chapter is about, inside the program built
to demonstrate avoiding it, and the chapter says so rather than
reporting four clean steps.

The `listed` arm was added after the first four had run, and the
reason is in the result: `documented` moved two questions and it
changes six things at once, so attributing the move to any one of
them would be the mistake this chapter is about. `listed` is the
thin description plus the one change chapter 36's own worked log
points at - the list of ids - so `renamed -> listed` is that change
and `listed -> documented` is the other five. Adding an arm after
seeing a result is legitimate here and would not be if it were a new
measure or a new grader: the questions, the trials, the grader and
every other arm are untouched, and the four original arms are
re-reported unchanged beside it.

What is IDENTICAL in all five: the registry, the dispatcher, the
corpus, the search tool, the instruction around it, and the function
that actually reads the file. Chapter 23 is why that matters - the
only participant that can refuse is your code, and none of these
changes touches it. A difference between these arms is a difference
in what the model proposes, which is the only thing a description
can move.
"""
import pathlib
import re

DOCS = pathlib.Path("corpus/docs")

def catalogue():
    out = {}
    for p in sorted(DOCS.glob("*.md")):
        body = p.read_text()
        m = re.search(r"^title: (.+)$", body, re.M)
        out[p.stem] = m.group(1) if m else p.stem
    return out


CATALOGUE = catalogue()
POLICIES = sorted(k for k in CATALOGUE
                  if "policy" in CATALOGUE[k].lower()
                  or k.startswith(("refund", "return", "delivery",
                                   "cancellation")))

#  --- the five descriptions ---------------------------------------
ENDPOINT_DESC = (
    "GET /documents/{id}\n"
    "  Fetch a document by id.\n"
    "  id: string"
)

RENAMED_DESC = (
    "policy.read\n"
    "  Fetch a document by id.\n"
    "  id: string"
)

ID_LINES = ("  The policy ids are:\n"
            + "\n".join(f"    {', '.join(POLICIES[i:i + 3])}"
                        for i in range(0, len(POLICIES), 3)))

LISTED_DESC = RENAMED_DESC + "\n" + ID_LINES

#  Chapter 36's six things. The list of ids is the change its own
#  worked log says removes the defect, and the when-NOT line is the
#  one it says a wrapper generated from an endpoint cannot write,
#  because it is a statement about the other tools.
DOCUMENTED_DESC = (
    "policy.read\n"
    "  What it does: returns one of this retailer's documents in\n"
    "    full - a policy, a help article or a product page.\n"
    "  When to use it: when you need the wording of a rule, or a\n"
    "    figure a policy sets.\n"
    "  When NOT to use it: do not call it to find out WHICH\n"
    "    document covers something. policy.search answers that and\n"
    "    returns ids this tool accepts. Do not call it twice on the\n"
    "    same id; you already have the text.\n"
    "  id: the exact id policy.search returned, lower case with\n"
    "    hyphens. The policy ids are:\n"
    + "\n".join(f"    {', '.join(POLICIES[i:i + 3])}"
                for i in range(0, len(POLICIES), 3)) + "\n"
    "    There are " + str(len(CATALOGUE)) + " documents in all and\n"
    "    nothing outside the list policy.search returns exists.\n"
    "  What it returns: the whole document, including its\n"
    "    exclusions, which are the part you did not ask for and\n"
    "    need.\n"
    "  What it refuses: any id not in the catalogue. It does not\n"
    "    guess."
)

ACTIONABLE_DESC = DOCUMENTED_DESC

DESCRIPTIONS = {
    "endpoint": ENDPOINT_DESC,
    "renamed": RENAMED_DESC,
    "listed": LISTED_DESC,
    "documented": DOCUMENTED_DESC,
    "actionable": ACTIONABLE_DESC,
}

NAMES = {
    "endpoint": "GET /documents/{id}",
    "renamed": "policy.read",
    "listed": "policy.read",
    "documented": "policy.read",
    "actionable": "policy.read",
}

SEARCH_NAMES = {
    "endpoint": "GET /search",
    "renamed": "policy.search",
    "listed": "policy.search",
    "documented": "policy.search",
    "actionable": "policy.search",
}

ARMS = tuple(DESCRIPTIONS)


def near(doc_id):
    """Ids that share a word with the one asked for. Used only by
    the actionable error, and computed rather than listed, so the
    message is right for an id nobody anticipated."""
    words = {w for w in re.split(r"[^a-z0-9]+", doc_id.lower()) if w}
    scored = []
    for k in CATALOGUE:
        have = {w for w in re.split(r"[^a-z0-9]+", k) if w}
        shared = len(words & have)
        if shared:
            scored.append((shared, k))
    scored.sort(key=lambda r: (-r[0], r[1]))
    return [k for _, k in scored[:3]]


def refuse(arm, doc_id):
    """The refusal, three ways over five arms. Chapter 23 put it in your
    code and said to send the specific reason back; chapter 36's
    three styles are a status code, naming the fault, and saying
    what to do next."""
    if arm in ("endpoint", "renamed", "listed"):
        return "404"
    if arm == "documented":
        return f"no such document: {doc_id}"
    hits = near(doc_id)
    msg = f"no document {doc_id!r} exists."
    if hits:
        msg += f" Did you mean {', '.join(hits)}?"
    return (msg + f" {SEARCH_NAMES[arm]} returns ids this tool "
                  f"accepts; call it rather than guessing another.")


def read(arm, doc_id):
    #  Identical in every arm. Chapter 23's registry lookup, and the
    #  only place anything is refused.
    if doc_id not in CATALOGUE:
        return {"error": refuse(arm, doc_id)}
    return {"id": doc_id, "text": (DOCS / f"{doc_id}.md").read_text()}


if __name__ == "__main__":
    print(f"  One tool, {len(ARMS)} versions, one change each.\n")
    print("  arm          name                 description")
    for arm in ARMS:
        print(f"  {arm:<13}{NAMES[arm]:<21}{len(DESCRIPTIONS[arm]):>5}"
              f" chars")
    print(f"\n  {len(POLICIES)} of the {len(CATALOGUE)} documents are"
          f" policies, and the")
    print("  documented version lists them. That is the change")
    print("  chapter 36's log says removes the defect.\n")
    for arm in ARMS:
        print(f"    {arm}")
        for line in DESCRIPTIONS[arm].splitlines():
            print(f"      {line[:56]}")
        print()
    styles = len({refuse(a, "x") for a in ARMS})
    print(f"  The same refusal, {styles} distinct ways over"
          f" {len(ARMS)} arms. The id")
    print("  asked for is one a model would plausibly invent.\n")
    for bad in ("returns-policy", "clearance-returns"):
        print(f"    asked for {bad!r}")
        for arm in ARMS:
            msg = refuse(arm, bad)
            print(f"      {arm:<12} {len(msg):>3} chars")
            for line in __import__("call").wrap(msg, "        ",
                                                "        ", 48
                                                ).splitlines():
                print(line)
        print()
    print("  Nothing above changes the registry, the dispatcher or")
    print(f"  the function that reads the file. All {len(ARMS)} arms")
    print("  refuse exactly the same ids; what differs is the name,")
    print("  the description and the words of the refusal - and")
    print("  `documented` changes the description AND the message,")
    print("  which the module docstring says and the table cannot.")
```

```text
  One tool, 5 versions, one change each.

  arm          name                 description
  endpoint     GET /documents/{id}     58 chars
  renamed      policy.read             50 chars
  listed       policy.read            274 chars
  documented   policy.read           1016 chars
  actionable   policy.read           1016 chars

  10 of the 40 documents are policies, and the
  documented version lists them. That is the change
  chapter 36's log says removes the defect.

    endpoint
      GET /documents/{id}
        Fetch a document by id.
        id: string

    renamed
      policy.read
        Fetch a document by id.
        id: string

    listed
      policy.read
        Fetch a document by id.
        id: string
        The policy ids are:
          cancellations, delivery-exceptions, delivery-fees
          delivery-time-estimates, refund-to-a-closed-card, re
          refunds-policy, return-postage-labels, returns-clear
          returns-standard

    documented
      policy.read
        What it does: returns one of this retailer's documents
          full - a policy, a help article or a product page.
        When to use it: when you need the wording of a rule, o
          figure a policy sets.
        When NOT to use it: do not call it to find out WHICH
          document covers something. policy.search answers tha
          returns ids this tool accepts. Do not call it twice 
          same id; you already have the text.
        id: the exact id policy.search returned, lower case wi
          hyphens. The policy ids are:
          cancellations, delivery-exceptions, delivery-fees
          delivery-time-estimates, refund-to-a-closed-card, re
          refunds-policy, return-postage-labels, returns-clear
          returns-standard
          There are 40 documents in all and
          nothing outside the list policy.search returns exist
        What it returns: the whole document, including its
          exclusions, which are the part you did not ask for a
          need.
        What it refuses: any id not in the catalogue. It does 
          guess.

    actionable
      policy.read
        What it does: returns one of this retailer's documents
          full - a policy, a help article or a product page.
        When to use it: when you need the wording of a rule, o
          figure a policy sets.
        When NOT to use it: do not call it to find out WHICH
          document covers something. policy.search answers tha
          returns ids this tool accepts. Do not call it twice 
          same id; you already have the text.
        id: the exact id policy.search returned, lower case wi
          hyphens. The policy ids are:
          cancellations, delivery-exceptions, delivery-fees
          delivery-time-estimates, refund-to-a-closed-card, re
          refunds-policy, return-postage-labels, returns-clear
          returns-standard
          There are 40 documents in all and
          nothing outside the list policy.search returns exist
        What it returns: the whole document, including its
          exclusions, which are the part you did not ask for a
          need.
        What it refuses: any id not in the catalogue. It does 
          guess.

  The same refusal, 3 distinct ways over 5 arms. The id
  asked for is one a model would plausibly invent.

    asked for 'returns-policy'
      endpoint       3 chars
        404
      renamed        3 chars
        404
      listed         3 chars
        404
      documented    32 chars
        no such document: returns-policy
      actionable   181 chars
        no document 'returns-policy' exists. Did you
        mean gift-returns, refunds-policy,
        returns-clearance? policy.search returns ids
        this tool accepts; call it rather than guessing
        another.

    asked for 'clearance-returns'
      endpoint       3 chars
        404
      renamed        3 chars
        404
      listed         3 chars
        404
      documented    35 chars
        no such document: clearance-returns
      actionable   186 chars
        no document 'clearance-returns' exists. Did you
        mean returns-clearance, gift-returns,
        returns-standard? policy.search returns ids
        this tool accepts; call it rather than guessing
        another.

  Nothing above changes the registry, the dispatcher or
  the function that reads the file. All 5 arms
  refuse exactly the same ids; what differs is the name,
  the description and the words of the refusal - and
  `documented` changes the description AND the message,
  which the module docstring says and the table cannot.
```

**One of the five changes two things, and the program says so because the table cannot.** The
refusal text moves twice, not once: a status code for the first three versions, then *naming the
fault* for `documented`, then *saying what to do next* for `actionable`. So `listed → documented`
is the description's other five things *and* the first of Chapter 36's two message improvements.
It is empirically moot — that version refused nothing, so its message never fired — and it is left
as it ran rather than quietly rewritten, because the data came out of this code. But it is the
confound this chapter is about, inside the program built to demonstrate avoiding it, and it got
there the ordinary way: I wrote `refuse()` as a ladder of `if` branches and the ladder has four
rungs for five arms.

**The fifth version was added after the other four had run, and the reason is the point of the
chapter.** With four arms the result was that the documented description took the pass rate from
19 of 24 to 24 of 24 — and that description changes six things at once. Crediting the move to any
one of them would have been the mistake this chapter is about, so `listed` is the thin
description plus the single change Chapter 36's own log points at, the list of ids, and nothing
else.

Adding an arm after seeing a result is worth being careful about and it is legitimate here: the
questions, the trials, the grader and the other four arms are untouched, the four original arms
are re-reported from their original runs rather than re-generated, and the arm was added to split
a change rather than to find a better number. The program says so where it appends rather than
replaces, and a cached file that reports the old data without a word is the trap Chapter 35's own
Tip names — so the cache is checked against the arms the program now has instead of against its
own existence.

```python
"""Five versions of one tool, measured on what the model proposes.

Chapter 36 ranked tools by DEFECTS rather than by failure rate and
defined the term: a failure the tool or its description could have
prevented, as against a refusal your code made correctly. Every
refusal here is a defect by that definition, because every one is
the model asking for a document id that does not exist and the
catalogue is knowable - which is chapter 36's own worked cause, 58
of 79 defects in one log.

What changes between arms is the tool's name, its description and
its refusal text. What does not change is the registry, the
dispatcher, the reader, the search tool, the questions, the
instruction or the step limit. So a difference here is a difference
in what the model proposed, which is the only thing a description
can move - chapter 23's point, and the reason the arms are built
this way.

The unit is the question. Eight questions, three trials, five arms
- and the fifth was added after the other four had run, which
`run()` and `rows()` both say in their own words.
"""
import json
import pathlib

import call
import search
import toolset

OUT = pathlib.Path("defects.json")
TRIALS = 3
STEP_LIMIT = 8
RESAMPLES = 10_000
SEED = 48

#  id, question, phrases a right answer carries (any one counts)
#
#  d7 and d8 are why these are sets. Both wanted the single string
#  "no", and "no" is a substring of "cannot", "not" and "none" - so
#  every answer passed whatever it said, and six of the 24 passes in
#  every arm were guaranteed. A grader that cannot fail is not a
#  grader, and two of the eight questions were not being measured at
#  all. The phrase sets below say what a right answer asserts.
QUESTIONS = [
    ("d1", "How many days do I have to return a clearance item?",
     {"14 day", "fourteen day"}),
    ("d2", "Who pays return postage on a clearance item?",
     {"customer pays", "paid by the customer", "you pay",
      "at your own cost", "your own expense",
      "the customer is responsible"}),
    ("d3", "What surcharge applies to a delivery to an IV "
           "postcode?", {"9.50"}),
    ("d4", "How long after my return arrives is a refund issued?",
     {"14 day", "fourteen day"}),
    ("d5", "What is the cap on a goodwill payment?",
     {"20 pound", "20 GBP", "twenty pound", "£20"}),
    ("d6", "My card is closed. How long does a bank transfer "
           "take?", {"10 working day", "ten working day"}),
    ("d7", "Can I return a personalised item?",
     {"cannot be returned", "can't be returned",
      "not be returned", "cannot return", "cannot accept",
      "are excluded", "is excluded", "not returnable"}),
    ("d8", "Is the delivery charge refunded if I send back one "
           "item of three?",
     {"not refunded", "is not refunded", "will not be refunded",
      "no refund of the delivery", "not be refunded",
      "does not refund"}),
]


def instruction(arm):
    return (
        "You are answering one question about this retailer's "
        "documents, using the two tools described below.\n\n"
        + f"{toolset.SEARCH_NAMES[arm]}\n"
          "  Find documents. Returns up to 5 ids and titles.\n"
          "  words: string\n\n"
        + toolset.DESCRIPTIONS[arm] + "\n\n"
        + "Reply with JSON, exactly one of:\n"
          "  {\"search\": \"<words>\"}\n"
          "  {\"read\": \"<document id>\"}\n"
          "  {\"done\": \"<your answer>\"}\n"
          "Answer only from a document you have read."
    )


def tool_search(words, cache):
    order, _ = search.dense(words, cache)
    seen, docs = set(), []
    for cid in order:
        doc = cid.split("#")[0]
        if doc in toolset.CATALOGUE and doc not in seen:
            seen.add(doc)
            docs.append(doc)
        if len(docs) == 5:
            break
    return [{"id": d, "title": toolset.CATALOGUE[d]} for d in docs]


def one(arm, question, cache):
    msgs, proposals, refusals = [], [], []
    reads, searches = [], 0
    for n in range(STEP_LIMIT):
        prompt = (instruction(arm)
                  + f"\n\nThe question: {question}\n\n"
                  + "What has happened so far:\n"
                  + ("\n".join(msgs) if msgs else "nothing yet")
                  + "\n\nYour next reply:")
        r = call.chat(prompt, json_mode=True, max_tokens=700)
        d = call.as_json(r["text"])
        if d is None:
            return {"answer": r["text"], "ended": "unparsed",
                    "proposals": proposals, "refusals": refusals,
                    "reads": reads, "searches": searches,
                    "chat_calls": n + 1}
        if "done" in d:
            return {"answer": str(d["done"]), "ended": "answered",
                    "proposals": proposals, "refusals": refusals,
                    "reads": reads, "searches": searches,
                    "chat_calls": n + 1}
        if "search" in d:
            res = tool_search(str(d["search"]), cache)
            searches += 1
            msgs.append(f"{toolset.SEARCH_NAMES[arm]} "
                        f"{d['search']!r} -> "
                        + ", ".join(x["id"] for x in res))
        elif "read" in d:
            doc = str(d["read"])
            proposals.append(doc)
            res = toolset.read(arm, doc)
            if "error" in res:
                refusals.append(doc)
                msgs.append(f"{toolset.NAMES[arm]} {doc!r} -> "
                            f"{res['error']}")
            else:
                reads.append(doc)
                msgs.append(f"{toolset.NAMES[arm]} {doc!r}:\n"
                            f"{res['text']}")
        else:
            return {"answer": r["text"], "ended": "no key",
                    "proposals": proposals, "refusals": refusals,
                    "reads": reads, "searches": searches,
                    "chat_calls": n + 1}
    return {"answer": "", "ended": "step limit",
            "proposals": proposals, "refusals": refusals,
            "reads": reads, "searches": searches,
            "chat_calls": STEP_LIMIT}


def run():
    """Run only the arms with no rows yet.

    The `listed` arm was added after the other four had run, so this
    appends to what is there rather than replacing it. The four
    original arms' numbers are the ones already reported and are not
    re-generated: re-running them would quietly change the figures
    the fifth arm was added to explain.
    """
    cache = search.vectors()
    out = json.loads(OUT.read_text()) if OUT.exists() else []
    have = {r["arm"] for r in out}
    for arm in toolset.ARMS:
        if arm in have:
            continue
        for qid, q, want in QUESTIONS:
            for trial in range(1, TRIALS + 1):
                r = one(arm, q, cache)
                ok = passes(r["answer"], want)
                out.append({"arm": arm, "question": qid,
                            "trial": trial, "want": want,
                            "answer": r["answer"],
                            "proposals": r["proposals"],
                            "refusals": r["refusals"],
                            "reads": r["reads"],
                            "searches": r["searches"],
                            "chat_calls": r["chat_calls"],
                            "ended": r["ended"], "passed": ok})
                OUT.write_text(json.dumps(out, indent=1))
                print(f"    {arm:<11} {qid} t{trial}: "
                      f"{'pass' if ok else 'FAIL'} "
                      f"{len(r['refusals'])} refused, "
                      f"{r['chat_calls']} calls")
    return out


def passes(answer, want):
    body = answer.lower()
    return any(p.lower() in body for p in want)


def rows():
    if not OUT.exists():
        return run()
    have = json.loads(OUT.read_text())
    #  An arm added later has no rows yet, and a cached file is the
    #  trap chapter 35's own Tip names: it reports the old data
    #  without a word. So the cache is checked against the arms the
    #  program now has rather than against its own existence.
    if {r["arm"] for r in have} != set(toolset.ARMS):
        return run()
    #  Re-grade every stored answer with the CURRENT grader. The
    #  grader was repaired after these runs - d7 and d8 wanted the
    #  bare string "no", which is inside "cannot" - so trusting the
    #  verdict written at run time would report the broken one.
    want = {qid: w for qid, _, w in QUESTIONS}
    moved = []
    for r in have:
        now = passes(r["answer"], want[r["question"]])
        if now != r["passed"]:
            moved.append((r["question"], r["arm"], r["trial"],
                          r["passed"], now))
        r["passed"] = now
    if moved:
        print(f"  Re-graded: {len(moved)} of {len(have)} verdicts"
              f" move. The grader for d7 and d8")
        print("  wanted the string \"no\", which is inside")
        print("  \"cannot\", so every answer to them passed.\n")
        import collections
        for q, n in sorted(collections.Counter(
                m[0] for m in moved).items()):
            print(f"    {q}: {n} of"
                  f" {len(toolset.ARMS) * TRIALS} runs change")
        print()
    return have


def per_question(rs, arm, field):
    out = {}
    for qid, _, _ in QUESTIONS:
        sel = [r for r in rs if r["arm"] == arm
               and r["question"] == qid]
        out[qid] = sum(r[field] for r in sel) / len(sel) if sel else 0
    return out


def interval(pairs, rounds=RESAMPLES, seed=SEED):
    import random
    rng = random.Random(seed)
    n = len(pairs)
    means = []
    for _ in range(rounds):
        drawn = [pairs[rng.randrange(n)] for _ in range(n)]
        means.append(sum(b - a for a, b in drawn) / n)
    means.sort()
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


if __name__ == "__main__":
    rs = rows()
    print(f"  {len(rs)} runs: {len(toolset.ARMS)} versions of one"
          f" tool x {len(QUESTIONS)}")
    print(f"  questions x {TRIALS} trials. Every refusal below is a")
    print("  defect by chapter 36's definition: the catalogue is")
    print("  knowable, so a description could have prevented it.\n")

    print("  1. THE COUNTS.\n")
    print("     arm          defects   passed   calls   reads")
    for arm in toolset.ARMS:
        sel = [r for r in rs if r["arm"] == arm]
        print(f"     {arm:<13}"
              f"{sum(len(r['refusals']) for r in sel):>6}"
              f"{sum(r['passed'] for r in sel):>9}"
              f"{sum(r['chat_calls'] for r in sel):>8}"
              f"{sum(len(r['reads']) for r in sel):>8}")
    print(f"\n     Out of {len(QUESTIONS) * TRIALS} runs each.\n")

    print("  2. WHICH CHANGE DID IT. Each arm against the one")
    print("     before it, so every row isolates one change.")
    print("     One QUESTION to a row, trials averaged within it,")
    print("     paired because every question is asked of every")
    print("     arm.\n")
    order = list(toolset.ARMS)

    def mean_per_q(arm, fn):
        return [sum(fn(r) for r in rs
                    if r["arm"] == arm and r["question"] == qid)
                / TRIALS for qid, _, _ in QUESTIONS]

    for label, fn, better in (
            ("defects", lambda r: len(r["refusals"]), "fewer"),
            ("answers right", lambda r: 1 if r["passed"] else 0,
             "more"),
            ("chat calls", lambda r: r["chat_calls"], "fewer")):
        print(f"     {label}")
        print("       change               diff   95% interval")
        for a, b in zip(order, order[1:]):
            pairs = list(zip(mean_per_q(a, fn), mean_per_q(b, fn)))
            lo, hi = interval(pairs)
            d = sum(y - x for x, y in pairs) / len(pairs)
            if lo > 0:
                says = "more" if better == "fewer" else better
            elif hi < 0:
                says = "fewer" if better == "fewer" else "fewer"
            else:
                says = "cannot tell"
            print(f"       {a[:4]} -> {b[:4]:<8}{d:>+8.2f}"
                  f"  {lo:+.2f} to {hi:+.2f}  {says[:6]}")
        print()
    #  And the whole rewrite at once, because three steps each
    #  unable to tell can still add to something that can.
    print("     all four changes together")
    print("       change               diff   95% interval")
    for label, fn in (("defects", lambda r: len(r["refusals"])),
                      ("answers right",
                       lambda r: 1 if r["passed"] else 0)):
        pairs = list(zip(mean_per_q(order[0], fn),
                         mean_per_q(order[-1], fn)))
        lo, hi = interval(pairs)
        d = sum(y - x for x, y in pairs) / len(pairs)
        says = "cannot tell" if lo <= 0 <= hi else "clears zero"
        print(f"       {label:<19}{d:>+8.2f}"
              f"  {lo:+.2f} to {hi:+.2f}  {says[:6]}")

    def tally(arm):
        sel = [r for r in rs if r["arm"] == arm]
        return (sum(len(r["refusals"]) for r in sel),
                sum(r["passed"] for r in sel),
                sum(r["chat_calls"] for r in sel),
                sum(len(r["reads"]) for r in sel))

    same = [a for a in ("listed", "documented", "actionable")
            if tally(a) == tally("listed")]
    print(f"\n     {len(same)} arms are identical on every column"
          f" above:")
    print(f"       {', '.join(same)}")
    if len(same) == 3:
        print("     So the whole of the improvement from renamed to")
        print("     actionable is the ONE change `listed` makes - the")
        print("     list of ids. The other five of chapter 36's six")
        print("     things added nothing here, and the error rewrite")
        print("     could not: no proposal was refused for a better")
        print("     message to act on. Without this arm the move")
        print("     would have been credited to the rewrite.")

    print("\n  3. THE IDS THE MODEL ASKED FOR AND DID NOT GET,")
    print("     which is the defect chapter 36's log is made of.\n")
    import collections
    for arm in toolset.ARMS:
        bad = collections.Counter(
            d for r in rs if r["arm"] == arm for d in r["refusals"])
        print(f"     {arm}: {sum(bad.values())} refusals,"
              f" {len(bad)} distinct")
        for doc, n in bad.most_common(4):
            print(f"       {n:>2}  {doc}")
        if not bad:
            print("       none")
        print()

    print("  4. WHAT A DEFECT COSTS, which is why it is worth")
    print("     counting separately from a wrong answer.\n")
    print("     arm          runs with a defect   their calls"
          "   others")
    for arm in toolset.ARMS:
        sel = [r for r in rs if r["arm"] == arm]
        bad = [r for r in sel if r["refusals"]]
        good = [r for r in sel if not r["refusals"]]
        bc = sum(r["chat_calls"] for r in bad) / len(bad) if bad else 0
        gc = (sum(r["chat_calls"] for r in good) / len(good)
              if good else 0)
        print(f"     {arm:<13}{len(bad):>14}{bc:>14.1f}"
              f"{gc:>9.1f}")
    print("\n     A defect is not a wrong answer. It is a step spent")
    print("     and a result carried, which is chapter 34's cost")
    print("     and chapter 35's context.")

    print("\n  5. WHICH QUESTIONS WERE GOT WRONG, because a pass")
    print("     rate over eight questions hides which ones.\n")
    print("     q   a right answer says  " + "".join(
        f"{a[:4]:>6}" for a in toolset.ARMS))
    for qid, q, want in QUESTIONS:
        shown = sorted(want)[0]
        cells = []
        for arm in toolset.ARMS:
            sel = [r for r in rs if r["arm"] == arm
                   and r["question"] == qid]
            cells.append(f"{sum(r['passed'] for r in sel)}/{len(sel)}")
        print(f"     {qid:<4}{shown[:18]:<19}"
              + "".join(f"{c:>6}" for c in cells))
    print("\n     The grader was repaired after these runs and the")
    print("     repair moved no verdict: d7 and d8 wanted the bare")
    print("     string \"no\", which is inside \"cannot\", so they")
    print("     could not fail - and their answers happen to say")
    print("     \"cannot be returned\" and \"is not refunded\", so")
    print("     the six guaranteed passes were right answers. The")
    print("     defect was real and the data was lucky.")
    print("\n     Every failure here is the model answering from a")
    print("     document that does not hold the answer, or saying")
    print("     the answer is not there. None of them is a refused")
    print("     id - so what this rewrite had to move was WHICH")
    print("     document the model opened, not whether it could.")

    print("\n  6. WHAT THE SEARCH TOOL ALREADY PREVENTED.\n")
    total_props = sum(len(r["proposals"]) for r in rs)
    total_ref = sum(len(r["refusals"]) for r in rs)
    print(f"     {total_props} read proposals over {len(rs)} runs,"
          f" {total_ref} refused.")
    print("     Chapter 36's worked log had 58 of 61 failures on one")
    print("     tool from one cause - a name the model invented -")
    print("     and said one list in one description would remove")
    print("     them. There is almost nothing here to remove, and")
    print("     the reason is not the description: this tool set has")
    print("     a search that returns ids the reader accepts, so the")
    print("     model is choosing from a list rather than naming a")
    print("     resource. That is chapter 36's FIRST section rather")
    print("     than its description section - the defect was")
    print("     designed out by the pair of tools.")
```

```text
  120 runs: 5 versions of one tool x 8
  questions x 3 trials. Every refusal below is a
  defect by chapter 36's definition: the catalogue is
  knowable, so a description could have prevented it.

  1. THE COUNTS.

     arm          defects   passed   calls   reads
     endpoint          1       19      84      31
     renamed           0       19      89      28
     listed            0       24      75      27
     documented        0       24      75      27
     actionable        0       24      75      27

     Out of 24 runs each.

  2. WHICH CHANGE DID IT. Each arm against the one
     before it, so every row isolates one change.
     One QUESTION to a row, trials averaged within it,
     paired because every question is asked of every
     arm.

     defects
       change               diff   95% interval
       endp -> rena       -0.04  -0.12 to +0.00  cannot
       rena -> list       +0.00  +0.00 to +0.00  cannot
       list -> docu       +0.00  +0.00 to +0.00  cannot
       docu -> acti       +0.00  +0.00 to +0.00  cannot

     answers right
       change               diff   95% interval
       endp -> rena       +0.00  -0.12 to +0.12  cannot
       rena -> list       +0.21  +0.00 to +0.50  cannot
       list -> docu       +0.00  +0.00 to +0.00  cannot
       docu -> acti       +0.00  +0.00 to +0.00  cannot

     chat calls
       change               diff   95% interval
       endp -> rena       +0.21  -0.58 to +1.29  cannot
       rena -> list       -0.58  -1.58 to +0.17  cannot
       list -> docu       +0.00  +0.00 to +0.00  cannot
       docu -> acti       +0.00  +0.00 to +0.00  cannot

     all four changes together
       change               diff   95% interval
       defects               -0.04  -0.12 to +0.00  cannot
       answers right         +0.21  +0.00 to +0.50  cannot

     3 arms are identical on every column above:
       listed, documented, actionable
     So the whole of the improvement from renamed to
     actionable is the ONE change `listed` makes - the
     list of ids. The other five of chapter 36's six
     things added nothing here, and the error rewrite
     could not: no proposal was refused for a better
     message to act on. Without this arm the move
     would have been credited to the rewrite.

  3. THE IDS THE MODEL ASKED FOR AND DID NOT GET,
     which is the defect chapter 36's log is made of.

     endpoint: 1 refusals, 1 distinct
        1  clearance

     renamed: 0 refusals, 0 distinct
       none

     listed: 0 refusals, 0 distinct
       none

     documented: 0 refusals, 0 distinct
       none

     actionable: 0 refusals, 0 distinct
       none

  4. WHAT A DEFECT COSTS, which is why it is worth
     counting separately from a wrong answer.

     arm          runs with a defect   their calls   others
     endpoint                  1           4.0      3.5
     renamed                   0           0.0      3.7
     listed                    0           0.0      3.1
     documented                0           0.0      3.1
     actionable                0           0.0      3.1

     A defect is not a wrong answer. It is a step spent
     and a result carried, which is chapter 34's cost
     and chapter 35's context.

  5. WHICH QUESTIONS WERE GOT WRONG, because a pass
     rate over eight questions hides which ones.

     q   a right answer says    endp  rena  list  docu  acti
     d1  14 day                3/3   3/3   3/3   3/3   3/3
     d2  at your own cost      3/3   3/3   3/3   3/3   3/3
     d3  9.50                  3/3   3/3   3/3   3/3   3/3
     d4  14 day                3/3   3/3   3/3   3/3   3/3
     d5  20 GBP                1/3   0/3   3/3   3/3   3/3
     d6  10 working day        0/3   1/3   3/3   3/3   3/3
     d7  are excluded          3/3   3/3   3/3   3/3   3/3
     d8  does not refund       3/3   3/3   3/3   3/3   3/3

     The grader was repaired after these runs and the
     repair moved no verdict: d7 and d8 wanted the bare
     string "no", which is inside "cannot", so they
     could not fail - and their answers happen to say
     "cannot be returned" and "is not refunded", so
     the six guaranteed passes were right answers. The
     defect was real and the data was lucky.

     Every failure here is the model answering from a
     document that does not hold the answer, or saying
     the answer is not there. None of them is a refused
     id - so what this rewrite had to move was WHICH
     document the model opened, not whether it could.

  6. WHAT THE SEARCH TOOL ALREADY PREVENTED.

     141 read proposals over 120 runs, 1 refused.
     Chapter 36's worked log had 58 of 61 failures on one
     tool from one cause - a name the model invented -
     and said one list in one description would remove
     them. There is almost nothing here to remove, and
     the reason is not the description: this tool set has
     a search that returns ids the reader accepts, so the
     model is choosing from a list rather than naming a
     resource. That is chapter 36's FIRST section rather
     than its description section - the defect was
     designed out by the pair of tools.
```

**Chapter 36's defect barely occurred, and the reason is in Chapter 36.** One refused id in 120
runs, out of 141 read proposals. Its worked log had 58 of 61 on one tool from the cause this
system is built to produce, and there was almost nothing here to remove. The reason is not the
description: this tool set has a search that returns ids the reader accepts, so the model is
choosing from a list rather than naming a resource. That is Chapter 36's *first* section — a
purposeful pair of tools — doing the work its description section was about to be credited with,
and no rewrite could have shown an effect on a failure the tool pair already prevents.

**The improvement that did happen is one line, and it is the line Chapter 36 named.** `listed`,
`documented` and `actionable` are identical on every column: the same 24 of 24 answers, the same
75 chat calls, the same 27 reads, no defects. So the whole move from `renamed` is the list of
policy ids. The other five of Chapter 36's six things — when to use it, when *not* to, what each
argument means beyond the bare list, what it returns, what it refuses — added nothing measurable
here,
and the error-message rewrite could not possibly have: there was no refusal left for a better
message to recover from. Chapter 36's table says a status code recovers none of eight failures and
saying what to do next recovers six, and every one of those six is conditional on the failure
happening.

**Two of the eight questions were being graded by a test that could not fail, and the repair
changed no verdict.** They are the two whose right answer is a refusal — can I return a
personalised item, is the delivery charge refunded on one item of three — and the grader wanted
the string `no`, which is inside *cannot* and inside *not*. So every answer to them passed
whatever it said, and six of each arm's twenty-four passes were guaranteed. The repair is phrase
sets, and re-grading all 120 stored answers with it moves nothing: the answers happen to say
*cannot be returned* and *is not refunded*. **The defect was real and the data was lucky**, which
is the only honest way to report it — a grader that cannot fail was not measuring those two
questions, and finding that out by re-grading rather than by argument is the whole of why
Chapter 45's habit of re-grading from the stored answers is worth keeping.

**And what the id list changed was which document the model opened.** The two questions that
moved are the goodwill cap and the bank-transfer window, and both have the same mechanism: with
the thin description the model read `refunds-faq`, a help article, and answered that the figure
was not there. With the ids listed it read `refunds-policy` and `refund-to-a-closed-card`, and
answered. Not one failure in the whole measurement was a refused id. **What a description moves
here is the choice among documents that all exist.** In Chapter 36 that is the menu-size column of
its first table, the one that falls from 5.4 plausible first moves to 2.0 — and the cost Chapter 23
named and said would not appear on the bill. Its defect count is a different table, the use log,
and this measurement has almost nothing in that one. The two are easy to run together because
both are headed by a word about failure; they are a choice among valid options and a proposal your
code refuses, and only the second shows up as an error.

**The aggregate refuses to call it, and the reason is a ceiling rather than noise.** Five of 24
runs changed, every one of them on two of the eight questions, and the paired interval on
`renamed → listed` runs +0.00 to +0.50 on a point estimate of +0.21. Six of the eight questions
are answered correctly by every arm, so only two can move and a resample of eight questions draws
neither of them often enough. Chapter 45 met the same shape in retrieval and called it a
candidate-set ceiling; here the ceiling is the question set, and the fix is more questions the
system gets wrong rather than more trials of the ones it gets right.

> **Note:** The one refused id in 120 runs is `clearance`, proposed by the endpoint-shaped
> version. It is worth looking at because it is the whole of Chapter 36's defect class in this
> measurement: the model took a word out of the case and offered it as an identifier. The
> namespaced name alone removed it — `renamed` has none — and one instance is one instance, so
> that is a count and not a rate.

## Step 7: What Three Measurements Say Together

Three claims went in and they came out differently, and the pattern in how they came out is worth
more than any one of them.

**The biggest thing the compaction measurement found was an error in its own grader.** Six of its
forty probe sets were satisfied by the case statement alone, and every summary restates the case,
so those six scored kept without testing anything. Five were loose fragments rather than the fact
— `delivered` for a fact about when a window starts, `credit` for one about what credit does — and
three were the case's own particulars, which no summary could drop. Tightening five and excluding
three took one headline from +0.43, clearing zero, to +0.21, which does not — and **turned the
crossed result over**, from a polarity difference that looked decisive to a form difference that is
the only one with an interval clear of zero. **A probe set that is too wide makes a summary look
better than it was**, and the error favours whichever group holds the loose probes, which was the
group I wanted to be different.

**That is the finding I would most want a reader to take**, because the discipline I had written
down was the wrong one. The Warning in the chapter's own step 2 named widening a probe *after*
seeing a score, which is the risk you can rule out by being careful about the order of events. The
risk that fired is a probe that was never specific enough, written in good faith before any score
existed, and no discipline about order touches it. The test is not *when did I write this*. It is
**could this probe be satisfied by text that is not the fact** — and you answer it by running the
probe against the question, the instruction and the case, which is four lines of code and now runs
every time.

**Chapter 35's compaction claim was not established and the alternative it half-suspected was.**
Negatives are not shown to be lost more than positives: +0.15 with 95 per cent from −0.257 to
+0.548, and −0.03 under the warned instruction. What clears zero is *form*: under the naive
instruction not one prose fact survived a single summary — 0 of 96 observations — against 53 of 108
for facts carrying a number, which is +0.49 from +0.157 to +0.778. Chapter 35 had the doubt and
no way to test it, because its list was not crossed: it wrote that three of the facts its naive
summary kept were not events either. **The crossed list is what turns that doubt into a
measurement, and the measurement says the other thing.**

**And its advice survives anyway, because the recovery is not the same shape as the loss.** Both
prose cells are empty under the naive instruction; one sentence asking for the things that are not
so refills *one* of them, negative-and-prose from 0 to 35 per cent, and no other cell moves by
more than eight points. Paired by fact that is +0.25 on prose, +0.031 to +0.531, against −0.00 on
numbers. So put the sentence in. **What you cannot do is quote the reason**: on this data, asking
for negatives and asking for the thing with no number in it are the same instruction, and nothing
here separates them.

**And Chapter 36's six things for a description came down to one line.** Of five versions of one
tool, three are identical on every column measured — the same 24 of 24 answers, the same 75 chat
calls, the same 27 reads — so the whole improvement is the list of ids, the change Chapter 36's
own log pointed at. The other five of its six things added nothing measurable here, and the error
rewrite
could not: with one refused id in 120 runs there was no failure left for a better message to
recover from. The fifth version was added after the other four had run, precisely to stop the
move being credited to a rewrite that changes six things at once — and the program that does the
isolating still bundled two changes into one of its arms, which is the lesson arriving inside the
demonstration of the lesson.

**Chapter 35's provenance claim was confirmed, and more sharply than it was made.** It said the
two fields do not make a note true and are there to tell *you* which notes can expire and which
were never checked. Fifty-four runs say the stronger thing: handing those fields to the model
corrected nothing at all, and three of fifty-four runs opened a document to check anything. The
model will not be the one who checks. That is Chapter 23's rule — your code is the only
participant that can refuse — arriving one level down, about a fact instead of a tool call, and
the arm where your code did the checking is the only arm that moved an answer.

**Chapter 36's defect claim had nothing to work on here, and the reason is in Chapter 36.** Its
worked log had 58 of 79 defects from one cause, a resource name the model invented, and one list
in one description would have removed them. This system produced one refused id in 120 runs,
because its search tool returns ids its reader accepts — so the model picks from a list instead of
naming a thing. The defect was designed out by the *pair* of tools, which is Chapter 36's first
section and not its description section, and no rewrite could have shown an effect on a failure
the tool pair already prevents.

**And the common thread is a kind of comparison rather than a subject.** A **pairable difference**
is one whose two sides can be measured on the same unit, which is what makes Chapter 20's paired
comparison available at all: the warned summary against the naive one on the same seventeen facts, or
five tool descriptions on the same eight questions. Chapter 20 says what pairing buys once you
have it — it cancels the part the two versions share. The prior question is whether you have it. A difference
between negatives and positives is not pairable, because a fact's polarity is a property of the
fact and there is no twentieth fact that is both. The three measurements in this chapter used the
same method, the same model and the same corpus, and the one that refused to give a verdict is
the one whose question had no pairing in it. **Whether a difference is pairable is decided by the
question, before you choose a method** — and the two chapters this one went back to measure both
rested on comparisons that were not.

> **Warning:** Every figure here is one system, one model, one corpus and one day. The model is
> `gpt-4o-mini-2024-07-18` at temperature zero, which Chapter 13 is clear is not a guarantee of
> the same text twice — which is why every measurement here repeats and Chapter 20 supplies the
> interval. Chapter 35's
> table was labelled plausible rather than measured and this one is measured on forty documents
> written for this book — which makes it evidence about an agent reading short policy documents
> and not about agents. What transfers is the three mechanisms: a must-keep list crossed so a
> result cannot be read off the column you picked, a notes store whose provenance is checked by
> your code rather than shown to the model, and a tool pair that makes a resource choosable
> rather than nameable. Each of those is a thing to build. None of the rates is a thing to quote.

## Summary, Key Terms, and Review Questions

### Summary

Three claims from Chapters 35 and 36, measured on one real agent over the shipped corpus, because
both chapters said in their own text what their evidence was worth. The record came from a loop
with a search and a read over forty documents, and it bore out Chapter 35's *shape* on real data:
three of fourteen steps carry 45 per cent of the result characters. Its 87.3 per cent and Chapter
35's plausible 91.5 are not comparable figures, over three different denominators. It also produced the chapter's two opening
problems unasked — a terse instruction answered a five-part case from two documents in four
steps, and the detailed one searched the identical words three times. **The largest thing the compaction step found was
an error in its own grader**: six of forty probe sets were satisfied by the case statement alone,
and every summary restates the case, so those six scored kept without testing anything. Tightening
five against their documents and excluding three that no summary could drop took one headline from
+0.43 and clearing zero to +0.21 and not, and turned the crossed result over — a probe that is too
wide makes a summary look better than it was, and the discipline that catches it is asking whether
a probe could be satisfied by text that is not the fact, not asking when you wrote it. **Compaction was measured
with twenty facts crossed two ways**, by polarity and by whether the fact carries a number,
because most negatives in these policies carry no number and a list split only by polarity would
measure both and credit one. Twenty-four model-written summaries, 888 checks over
37 scored facts: **the difference that clears zero is form, not polarity.** Under the naive
instruction not one prose fact survived a single summary — 0 of 96 observations against 53 of 108
for facts carrying a number, +0.49 with 95 per cent from +0.157 to +0.778 — while polarity is
+0.15 from −0.257 to +0.548 and −0.03 under the warned instruction. That is the alternative
Chapter 35 suspected and could not test, because its list was not crossed. **And the recovery is
not the shape of the loss**: both prose cells are empty under the naive instruction, the warning
refills only negative-and-prose, 0 to 35 per cent, with no other cell moving by more than eight
points — +0.25 on prose from +0.031 to +0.531 against −0.00 on numbers, and the needed facts no
summary kept fall from twelve of seventeen to seven. So Chapter 35's advice survives a
measurement that refuses its claim, and the reason it gave cannot be separated here from the
reason the data supports. Facts the case depends on are kept 26 and 38 per cent against 10 and 11
for facts that merely appear in the record, and that comparison is reported two ways because one
judgement about one fact moves it across zero: +0.25 (+0.013 to +0.477) with the third case
particular scored, +0.21 (−0.017 to +0.444) with it excluded. **The notes store was measured in three
arms** — bare, provenance shown to the model, and your code checking the note against its
document — and three of fifty-four runs opened a document, in any arm, with both tools available
throughout. Provenance corrected nothing and produced two runs that searched eight times, never
read, and hit the step limit. Your code dropping a note moved one question of three; a second
stayed wrong because the substring check kept a note whose figure appears in the right document
on the wrong line; and the third stayed wrong after its note was dropped, because a **correct**
note about standard items supplied the same number — a note with no **note scope**, which is the
third field Chapter 35's two do not include and Chapter 36 names for a tool. **One tool was
rewritten in five versions**, each adding one of Chapter 36's changes, with the registry, the
dispatcher and the reader identical throughout. Chapter 36's worked defect occurred once in 120
runs, because a search that returns ids the reader accepts makes a resource choosable rather than
nameable — the defect was designed out by the pair of tools, which is Chapter 36's own first
section. Three of the five versions are identical on every column measured, so the whole
improvement — 19 of 24 answers to 24 of 24, on fewer calls — is the one line listing the ids, and
the error-message rewrite could not be measured at all with no refusal left to recover from. The
fifth version was added after the other four had run, to stop a six-part rewrite taking the credit
for one line of it. And the thread through all three is the **pairable difference**: the comparisons that
gave verdicts put the same unit on both sides, and the one that refused had no pairing in its
question to use.

### Key Terms

| Term | Meaning |
|---|---|
| **Pairable difference** | A difference whose two sides can be measured on the same unit, so that unit's own difficulty cancels — two instructions on the same facts, four descriptions on the same questions. Not a choice of method: a difference between kinds of thing, like a negative fact against a positive one, has no pairing in it to use, and two samples of ten and seven will refuse what seventeen paired measurements settle |
| **Note scope** | The condition under which a structured note applies, which Chapter 35's two fields do not record. A note that is true, checked and current can still produce a wrong answer when a later step reads it outside the case it was written for. The same line Chapter 36 asks a tool description for — *when not to use this* — and a statement about the other notes rather than this one |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Measured, where Chapter 35 was plausible | The shape, not the share: 3 of 14 steps carry 45% of the result characters. 87.3% and Chapter 35's 91.5% are different denominators over different-length runs |
| Audit a probe before you trust a rate | Run it against the question, the instruction and the case. 6 of 40 here were satisfied by the case alone; the repair took one headline from +0.43 to +0.21 and turned the crossed result over |
| What a must-keep list is for | Not catching a careless summariser: telling you which of the facts *you* need are among the ones it dropped |
| What six changes to a description came to | One line. Three of five versions identical on every column; the list of ids is the whole of it, and 19 of 24 answers became 24 of 24 on fewer calls |
| What a crossed list is for | Facts in 4 cells, so a result cannot be read off the column you picked. Here polarity +0.15 (−0.257 to +0.548) cannot tell and form +0.49 (+0.157 to +0.778) can — and crossing fixes only the confounds you name |
| What a summary dropped | Everything in prose: 0 of 96 observations under the naive instruction, against 53 of 108 for facts carrying a number |
| What one sentence in the summary prompt buys | One cell: negative-and-prose 0% → 35%, with no other cell moving over 8 points. +0.25 on prose (+0.031 to +0.531), −0.00 on numbers. Needed facts kept by no summary 12 of 17 → 7 |
| What showing a model provenance buys | 0 corrections in the 9 runs that hinge on a wrong note, and 0 of its 18 runs opened a document. All 3 document opens in the whole measurement are the arm where the **code** checked |
| What a substring check on a note misses | A figure that is in the right document on the wrong line |
| The third field a note needs | Its scope — a correct note applied outside it gave the wrong answer three times of three |
| Before choosing a method | Ask whether the difference is pairable. If the two sides are kinds rather than conditions, it is not |

### Review Questions

1. Chapter 35 said negative facts are lost first when you compact. How would you find out whether that is true, and what did it turn out to be?
2. What is compaction, and how do you prove nothing important was dropped?
3. Why treat an agent's own memory as untrusted input, and what did showing the model a note's provenance actually do?
4. You rewrite a tool's name, description and error messages. How do you tell which of the three helped?
5. Two of this chapter's three comparisons gave a verdict and one refused. Why?

### Review Answers

1. Write the must-keep list first and cross it. The list has to exist before any summary, because
a list written afterwards is written from the summary and the check passes vacuously — that is
Chapter 35's own Warning. Crossing it is the part Chapter 35 did not do: most negatives in these
policy documents carry no number and most positives are figures, so a list split only by polarity
measures polarity and numeracy together and you will name the result whichever way you were
already leaning. Twenty facts, five in each of four cells, twenty-four summaries written by the
model, and — the part I would now put first — **audit every probe before you believe any rate**:
run each one against the question, the instruction and the case, because every summary restates
the case and a probe the case alone satisfies scores kept without testing anything. Six of forty
were in that position here, and fixing them moved the largest figure in the step from +0.43 to
+0.21, and turned the crossed result over.

What it turned out to be: **the polarity story is not established and the form story is.** The
naive instruction kept 20 per cent of negatives against 35 of positives, which is +0.15 from
−0.257 to +0.548 — and not one prose fact of the eight survived a single summary, 0 of 96
observations, against 53 of 108 for the nine facts carrying a number, which is +0.49 from +0.157 to
+0.778. Chapter 35 suspected exactly that and had no way to test it. And its advice survives
anyway, which is the useful half: the warning refills the one cell that was empty *and* negative,
0 to 35 per cent, worth +0.25 on prose from +0.031 to +0.531 and −0.00 on numbers. So put the
sentence in. Do not quote the reason — on this data, asking for negatives and asking for what has
no number in it are the same instruction.
2. Compaction is replacing the record of a run with a shorter one that keeps the facts later steps
need, and you prove nothing important was dropped by naming those facts before the summary is
written and checking the summary against each one afterwards. The check is a string probe, so it
catches an omission and cannot tell you the summary states a fact correctly — necessary, not
sufficient. Worth adding what measuring it showed. The probe's rate is an upper bound and *this
chapter did not measure the gap*: the corpus has a trap for exactly that failure, a 30-day
standard window against this item's 14-day clearance one — and *the trap was not in the record*,
because the run never opened the document carrying the 30-day window, so a hit could not have been
read as the error anyway. A judge is the instrument that would settle it. And the summaries that
keep more are longer: the text being compacted was 11,585 characters, the naive summaries 653 on
average and the warned ones 1,466, a factor of 18 against a factor of 8. On the facts the case
depends on those keep 30 and 41 per cent; over all 38 scored facts, 20 and 25. Whether that trade
is worth taking depends on what the next step needs, which is what the must-keep list is for
deciding.
3. Because a note is model output read back as something your code appears to have vouched for,
with no evidence attached. What showing the model its provenance did is the part worth reporting:
nothing. In eighteen runs with each note labelled by source — including *inferred, was never
checked against anything* — not one answer was corrected, and across all fifty-four runs in three
arms only three ever opened a document, with a search tool and a read tool described in the
instruction the whole time. The one arm that moved an answer is the one where the code re-read the
document and dropped a note it could not find, which is Chapter 23's rule about who can refuse,
arriving about a fact rather than a tool call. Two caveats and both are findings. The check is a
substring test, so it kept a note whose figure appears in the right document on the wrong line.
And on one question it dropped the wrong note and the answer stayed wrong, because a *correct*
note about standard items carried the same number — the missing field is the note's scope, and
nothing in Chapter 35's two fields records it.
4. Build one arm per change and add them in order, so each comparison isolates one: the name, then
the description, then the errors, with the registry, the dispatcher and the function that reads
the file identical throughout. That last part is what makes the comparison about the description
at all — Chapter 23's point is that your code is the only participant that can refuse, so a
difference between these arms can only be a difference in what the model proposed. The thing to
expect is the one this chapter found: the defect Chapter 36's log is made of — a resource name the
model invented — barely occurred, because the search tool returns ids the reader accepts, so the
model chooses from a list rather than naming a thing. That is Chapter 36's first section doing the
work its description section was being credited with, and a rewrite cannot show an effect on a
failure the tool pair already prevents. Measure the defects separately from the wrong answers,
which is Chapter 36's rule, and expect the rewrite's remaining room to be in *which* document the
model opens.
5. Because of what the two sides of each comparison were. The warned summary against the naive one
puts the same facts on both sides, so each fact's own difficulty cancels and seventeen paired
measurements settle a difference of 0.12. Negative facts against positive facts cannot do that: a
fact's polarity is a property of the fact, so ten and seven are two samples and not pairs, and the
interval runs from −0.257 to +0.548. Be exact about what else
differs, because the pairing is not the only thing: the warning comparison also estimates a
smaller quantity, and the polarity comparison is confounded with form while the warning comparison
is not. Three reasons, and the pairing is worth naming first only because it is the one you settle
before you have any data. A difference is pairable or it is not, and the question decides it. The
practical consequence is that an unpairable question needs many more units than a pairable one,
and the time to find that out is while you are still choosing what to compare.

> **You understand this when** you can say which of your own agent's remembered facts has a scope
> nothing records, and what would happen if a later step read it outside that scope.
