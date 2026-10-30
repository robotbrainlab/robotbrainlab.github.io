# Security: What Can Go Wrong, and What Limits the Damage

Chapter 50 attacked a working system and found one thing that worked. This chapter is the
framework that result belongs to: what can go wrong in a system built around a model, which
of those things your code can refuse, and what you do about the ones it cannot. By the end
you will be able to answer the question in the title about a system you are responsible for,
and to say which of your answers is a measurement and which is a decision.

*The problem.* Someone told me a web page could hijack my agent. I'd like to know whether
that's true and what I do about it.

*The question.* What can go wrong here, and what limits the damage?

## The Answer, First

It is partly true, and the useful part of the answer is about which part.

A page your system retrieves can certainly get an instruction in front of the model. That is
not a flaw anybody introduced and it is not a model defect: it is Chapter 23's mechanism.
Your instruction is text in the input, the page is text in the input, and the whole lot
arrives as one sequence of tokens with nothing marking which part is yours.

What the page cannot do by itself is make anything *happen*. The registry is a map from a
name to a function your code is willing to run, so a name the model was told to ask for is
refused by the lookup before anything executes. Chapter 50 measured that end of it: across
thirty-six runs in which an injected instruction asked the system to call a tool that did not
exist, no run ever proposed it, and if one had, four lines of dispatcher would have refused
it. **That is the case the architecture covers: a page asking for a tool you do not have.** Be
exact about the edge, because the chapter's own worked case below turns on it — the registry
refuses a *name* it does not hold, and runs a name it does hold with whatever arguments it was
given. So what the lookup covers is the invented tool, and what it does not cover is your own
tool pointed somewhere else.

What the page *did* do in that lab is take away a rule. An instruction appended to a
retrieved passage told the model to stop citing its sources, and the citation requirement went
on four of four questions, all twelve runs — with replies that read perfectly, because correct
prose with an empty citation list looks exactly like correct prose. The figure to carry is the
four, not the twelve: the twelve is those four questions asked three times each, and the rule
from Chapter 20 is that repeats are averaged within a case so that one case stays one row,
because three rows for one case triple the apparent case count while adding no new
input. The rule it removed was the one rule
in that system that existed only as an instruction.

So the shape of the honest answer, and it is worth being able to say in this order:

1. Yes, text your system reads can reach the model as though you had written it.
2. No, that text cannot act. Only your code acts, and only through a name it holds.
3. But it can stop your system doing something you told it to do, and the thing most
   likely to stop is whatever you only asked for.

**The rest of this chapter is what follows from those three sentences.** It is a framework
rather than a measurement, and that is a real distinction: Chapter 50 produced numbers from
one system, and almost nothing here is a number. What it is instead is a set of decisions,
each of which you can make once and then check.

## Why a Model Cannot Reliably Tell an Instruction from Data

This is the rule underneath everything else in the chapter, and it is mechanical.

Chapter 23 gave the mechanism and handed the consequence here. Take it in three steps, each
of which is something an earlier chapter established.

**One: the context is one sequence of tokens.** Chapter 2's three pieces — the instructions,
the added material, the request — are a convenient way for *you* to think about what you
sent. What goes over the wire is text, assembled by your code, in an order your code
chose. Chapter 18
established what that list of messages is and that the roles mean something to the model because
its training put them there. The point this chapter needs is the one that follows and is its own:
a role is a strong hint about who wrote a piece of text, and a hint is not a partition.

**Two: the model has no channel for metadata.** Chapter 9 is the reason. A token is a
position in a vocabulary and a vector of coordinates, and there is no field beside it saying
where it came from. Whatever the model learns about which parts of an input to treat as
authoritative, it learns from the text itself — from a heading, a role marker, a position, a
tone. Those are features of the text, and anything that can write text can write them.

**Three: so the distinction you want is not available to the component you are asking.** A
model asked to follow your instructions and ignore instructions in the documents is being
asked to tell apart two things that arrive the same way. It will often succeed, because the
features correlate with the truth most of the time. Chapter 23 already named what that is
worth: a year of compliance is a correlation rather than a limit.

That is the rule, and it deserves one more sentence about what it is *not*. It is not a claim
that models are bad at this, and it is not a prediction that they will stay bad at it. A
model that resisted every injection anybody could write would still give you a correlation,
because the thing you want is a guarantee about a boundary and what you would have is a
measurement of a component's behaviour. Chapter 3's sentence about checking applies without
modification here: a confident answer and a confident check are the same kind of object.

**The practical consequence is a change of question.** *Can the model be made to tell them
apart?* is the wrong question, and it is the one most of the writing on this subject answers.
The question that has an answer is: *given that it cannot reliably tell them apart, what is
my system still unable to do?* Everything in this chapter is an answer to the second one.

## Every Channel the Model Reads Is Input

The rule above is about text the model reads. So the first practical job is knowing what text
that is, and the usual answer is too short.

People draw the boundary at the user's message, because that is the part a stranger obviously
writes. Here is the longer list, with who writes each one and where this book establishes it.

| Channel | Who can write it | Where it was established |
|---|---|---|
| The request | The user, who may be a stranger | Chapter 2 |
| A retrieved passage | Whoever wrote the document you indexed | Chapters 27 and 28, attacked in Chapter 50 |
| A tool result | Whatever system the tool reads from | Chapter 36 |
| A document's title, filename or header, carried in a result | Whoever wrote the document | Chapter 27, attacked in Chapter 50 |
| A tool *description* | Whoever runs the server it came from | Chapter 36 |
| A note the agent wrote earlier | The same process that produced everything else | Chapter 35 |
| A sub-agent's return value | A run whose context the parent cannot see | Chapter 35 |
| A summary made by compaction | A model call, over text that may itself be injected | Chapter 35 |
| An earlier turn of the conversation | The user again, on a previous visit | Chapter 18 |
| A file, page or document the loop opened for itself | Whoever put it there | Chapter 4 |

Four of those are worth dwelling on, because they are the ones people leave off.

**A tool description is input.** Chapter 36 owns this case and states it exactly: a
description that arrives from a server you do not control is placed in the same input as your
system message, with nothing distinguishing them. Notice which way the exposure runs. The
worry everybody has about a third-party tool server is that it will misuse what you send it.
The mechanical exposure is the other direction: it supplies text that goes into your prompt,
on every call.

**An agent's own note is input.** Chapter 35 owns this one and gives the reason: a note is a
claim with no evidence attached, written by the same process that produced everything else in
the context, and read back later as though somebody had checked it. Chapter 50 injected one
and the model ignored it in all forty-eight runs — four payload shapes over four questions and
three trials — which establishes nothing general about notes on one system, but the channel is
real whatever that run showed.

**A compaction summary is input twice over.** Chapter 35's compaction reads a context and
writes a shorter one with a model call. If the long context held an injected instruction, the
summary is the output of a model that read it, and it is then trusted by every later step as
your own record of what happened.

**And a document's own metadata is input**, which is the one most likely to be missed because it
does not look like text at all. Chapter 27 established that a parser gives you strings and
positions; a title lifted out of a header and put into a tool result is one of those strings,
and your code passes it on without reading it. That was Chapter 50's second channel, and the
reason it is worth naming separately is that it reaches the model through a field your code
treats as a label.

**So the discipline is a list, written down.** For a system you are responsible for, write out
every channel by which text that neither you nor your code composed reaches the model. The
list is short and nobody has it. Chapter 50's lab is what it looks like when you make one, and
it is worth knowing what making one cost there: of its three channels, one had to be *built*
first — the pipeline read no titles until the chapter needed a title channel to attack, and an
earlier draft described the three lines that read them before they existed. Writing the list
down is not an inventory of what you have; it is also a question about what you have not
implemented yet. The lab then attacked three channels and left the user's own request alone,
which is a choice rather than an absence.

**And the list is what makes the next decision possible**, because the decision is about
combinations.

## The Design Rule

Here is the one rule in this chapter worth memorising, and it is a rule about combinations
rather than about components.

> Never combine untrusted input, sensitive access and external action in one session without
> approval.

Three ingredients. A **session** here is one run of your system that shares a context: a
single request and its answer, or an agent's whole loop from the user's message to its last
step. The ingredients are:

| Ingredient | What it means | What makes it present |
|---|---|---|
| Untrusted input | Text the model reads that neither you nor your code composed | Any channel from the table above |
| Sensitive access | Something in the context, or reachable by a tool, that not everybody may see | Retrieved records, a key, another customer's data |
| External action | A tool that affects something outside your process and is not easily undone | Sending, posting, paying, deleting, writing |

**The claim is that the three together are the hazard, and that any two of them are
ordinarily survivable.** That is not a measurement and this chapter will not dress it up as
one. It is a derivation from the three sentences this chapter opened with, and the derivation
is worth following, because it is what tells you which ingredient to remove.

- **Untrusted input and sensitive access, no external action.** The injected text can make the
  model say something, and what it says goes back to the caller. If the caller is the attacker
  they learn what was in the context — which is real and is the reason the next section's list
  has an entry for it — but nothing leaves your system by a route the attacker chose.
- **Untrusted input and external action, no sensitive access.** The injected text can get an
  action proposed, and your code decides whether to run it. What the attacker can reach is
  bounded by what the tools can reach, and the tools reach nothing worth taking. Chapter 50's
  lab is not even this cell, which is worth saying because it is the reason that lab was safe
  to run a hundred times a day: its one tool returns a hard-coded dictionary, so it has no
  external action at all and no sensitive access either. It holds untrusted input alone, which
  is why the only thing it could measure is what the model did.
- **Sensitive access and external action, no untrusted input.** This is ordinary software. It
  has all of ordinary software's problems and none of this chapter's.
- **All three.** Now the injected text has something to ask for *and* a way to send it, and
  the two are joined by a model that cannot tell the request from the data. The attacker does
  not need your code to run a tool it does not have. They need it to run a tool it *does*
  have, with arguments they chose.

Here is the case an interviewer will put to you, and it is exactly this one, so work it
properly: *a web page your agent reads tells it to send your customer list somewhere.*

**What happens.** The page is untrusted input, which arrives because your loop opened it. The
customer list is sensitive access — either sitting in the context from an earlier retrieval
step, or reachable by a tool the agent holds. Sending is an external action, and it is
external in the strict sense: once a message has left, no later action recalls it, which is
Chapter 3's irreversible action. The model reads the page's sentence in the same input as
your instruction, proposes the send, and your dispatcher — which holds a `send_email` because
somebody wanted the agent to be able to reply to customers — looks the name up, finds it,
validates the arguments, and sends.

Notice what did *not* go wrong. Nothing talked the model out of a refusal it would otherwise
have made, because sending an email is a thing it was built to do and there was no refusal to
talk it out of. The dispatcher was
not bypassed; it worked exactly as written. No validator failed, because the proposal was
well-formed and named a real tool with real arguments. **Every component behaved as
specified and the customer list left the building.** That is why this is a design rule and not
a bug to fix.

**What would have stopped it.** Four answers: two remove an ingredient, one shrinks it, and one
adds the approval.

1. **Remove the external action.** The agent drafts and a person sends. This is Chapter 3's
   cheapest safety measure — declining to give a tool an irreversible action — and it is the
   one most often available, because a great deal of what people want from an agent is a draft.
2. **Shrink the sensitive access.** The tool that reads customer records is scoped to the one
   customer this request is about, which is the third section on from here. Be exact about what
   that buys: the injected instruction now reaches one record rather than the list, and that
   record still leaves by the attacker's route, because the attacker is whoever wrote the page
   and the caller is the person being helped. This fix shrinks the loss rather than removing
   the ingredient, and it is the one most often available.
3. **Remove the untrusted input.** Do not let the loop open arbitrary pages. This is the
   narrowest of the four and it is often the one you cannot have, because opening pages was
   the point.
4. **Add the approval.** The send stops and waits for a person, which is Chapter 2's fifth
   part arriving where it was needed. Chapter 2 promised this chapter would show what goes
   wrong when the approval step is missing from a place that needed one, and this is it: the
   place that needed one is any tool that satisfies the third ingredient while the other two
   are present.

**Approval is the weakest of the four wherever the action is frequent, and that is the case to
plan for.** Chapter 3 is why: show a reviewer a hundred confident proposals an hour and most are
approved, which is rubber-stamping, and you then pay the whole cost of review for very little of
its value. So a design that relies on approval for something that happens all day has chosen the
only one of the four answers that degrades with volume — removing a capability does not degrade.
For a rare action with a large consequence the ordering reverses and approval is the right
answer, which is Chapter 3's own framing: the question was never *should a person review this?*
but which cases, how many an hour, and with what put in front of them.

**And the general form of the first fix is the one to reach for first.** Chapter 5 gave the
practical version as a tip and it is worth restating as a rule: the cheapest version of this
work is subtraction. A tool that
only reads cannot change anything. A tool whose scope is one customer's records cannot touch
another's. Much of the safety in a well-built system comes from what its tools were never
allowed to do rather than from checks catching them doing it — and the reason that is the first
fix rather than the best-sounding one is that it is one of the two in the list of four that
remove a capability rather than add a check — the other being not reading the untrusted thing
— and a capability that is not there does not have to work correctly at the moment of the
attack.

**And the rule tells you something about the shape of your tool set**, which is the part that
survives into design reviews. A tool set where every tool reads and one tool sends has a
single place to put the decision. A tool set where six tools can each reach outside has six.
Chapter 36's advice to write a few purposeful tools rather than one per endpoint was argued
there on how well the model chooses; this is a second reason for the same shape, and the two
reasons agree.

## The Risk Lists, and What a List Is Worth

The field keeps two catalogues of what goes wrong, and an interviewer may well ask whether you
know them. They are worth knowing and they are worth knowing the limits of, in that order.

**The first is for applications that generate**, which means anything where the model produces
text your system uses — an answer, a summary, a classification, a query. The current edition is
the *OWASP Top 10 for LLM Applications 2026*, published in early August 2026 by the OWASP GenAI
Security Project.

| Entry | What it is, in one line |
|---|---|
| LLM01 Prompt Injection | An instruction reaching the model through a channel meant to carry data |
| LLM02 Sensitive Information Disclosure | The system reveals something the caller should not have seen |
| LLM03 Excessive Agency | The system can do more than the task needs, so a wrong decision reaches further |
| LLM04 Supply Chain | A model, package, dataset or tool server you did not write, trusted because it was convenient |
| LLM05 Data and Model Poisoning | Training or reference data arranged by somebody else to change what comes out |
| LLM06 Unbounded Consumption | Work the caller can cause without limit — tokens, calls, loop steps, money |
| LLM07 Misinformation | Confident wrong output taken as fact, including by another part of your own system |
| LLM08 Hidden Context Exposure | The part of the input the user cannot see — instructions, tool schemas, retrieved policy — read back out |
| LLM09 Vector and Embedding Weaknesses | The index as an attack surface: what is in it, who may retrieve from it, what it leaks |
| LLM10 Improper Output Handling | Model output reaching a component that renders or executes it |

**The second is for agents**, and it exists because a loop that chooses its own steps has
exposures the single call does not. It is the *OWASP Top 10 for Agentic Applications*, version
2026, released on 9 December 2025 by the same project — a version named for the year after the
one it came out in, which is worth knowing before you quote either — and it extends the first
list rather than replacing it.

| Entry | What it is, in one line |
|---|---|
| ASI01 Agent Goal Hijack | The loop's objective changed by text it read, rather than by the user |
| ASI02 Tool Misuse and Exploitation | A tool the agent legitimately holds, used for something it was not meant for |
| ASI03 Identity and Privilege Abuse | The agent acting with rights that are not the caller's |
| ASI04 Agentic Supply Chain Vulnerabilities | Tool servers, skills and components added to the loop from outside |
| ASI05 Unexpected Code Execution | Code the model wrote, run somewhere that matters |
| ASI06 Memory and Context Poisoning | What the agent wrote down, or retrieves, arranged to steer a later run |
| ASI07 Insecure Inter-Agent Communication | What passes between agents, trusted because it came from one of yours |
| ASI08 Cascading Failures | One wrong step carried forward by every step after it |
| ASI09 Human-Agent Trust Exploitation | A person approving because the system was confident |
| ASI10 Rogue Agents | An agent operating outside its policy through drift, design or compromise |

**Now read the twenty against this book, because that is what makes a list useful.** Of the
twenty, thirteen are answered by sections of this chapter, four by chapters elsewhere in the
book, and three this chapter does not reach.

| Entry | Where it is answered |
|---|---|
| LLM01 Prompt Injection · ASI01 Agent Goal Hijack | The design rule above, and Chapter 50's measurement |
| LLM03 Excessive Agency · ASI02 Tool Misuse | The design rule: remove the external action, or the access |
| LLM02 Sensitive Information Disclosure · LLM09 Vector and Embedding Weaknesses · ASI03 Identity and Privilege Abuse | Per-user tool authorisation, and the same scoping applied to retrieval |
| LLM10 Improper Output Handling | Model output as input to the next component |
| LLM04 Supply Chain · ASI04 Agentic Supply Chain | A tool server you did not write, with Chapter 54 for the pinning |
| ASI05 Unexpected Code Execution | Sandboxing what the model wrote |
| LLM08 Hidden Context Exposure | Its credential half, in Secrets, and the rule that the context is not a place to keep one. The rest of it — your instructions and tool schemas read back out — this chapter only gestures at, in the design rule's first pair |
| ASI06 Memory and Context Poisoning | Every channel the model reads is input — Chapter 35's notes, attacked in Chapter 50 |
| LLM06 Unbounded Consumption | Chapter 4's step limit and Chapter 53's bill; the time and memory limits in the sandbox table |
| LLM07 Misinformation | Chapter 16, under another name |
| ASI08 Cascading Failures | Chapter 4's compounding error, with its arithmetic |
| ASI09 Human-Agent Trust Exploitation | Chapter 3's rubber-stamping, which is a well-studied effect in people supervising automated systems rather than a new one |
| LLM05 Data and Model Poisoning · ASI07 Insecure Inter-Agent Communication · ASI10 Rogue Agents | Not reached here, and said so at the end |

**A risk list is a vocabulary as much as it is a catalogue**, and that table is most of what
reading one is worth: four of the twenty are things this book teaches under its own names
rather than these, and the ones you cannot place are the ones to go and read.

### A Checklist, Not a Certificate

Now the limits, because a list invites a use it cannot support.

**A list is a set of kinds.** Chapter 46 named the blind spot exactly, about its own regression
set: a blindness to kinds, which no number of cases fixes. A catalogue of twenty kinds has the
same property one level up. It tells you twenty questions to ask and says nothing about the
twenty-first, and Chapter 50's lab is a small demonstration — the thing that worked there is
LLM01, which is the first entry on the first list, and the chapter still found it by attacking
its own system rather than by reading the entry.

**A list goes out of date, and more quickly than you would guess.** This is worth being
concrete about, because the concrete version is what stops you quoting a retired edition in an
interview.

| Entry | 2025 | 2026 | |
|---|---|---|---|
| Prompt Injection | LLM01 | LLM01 | unchanged |
| Sensitive Information Disclosure | LLM02 | LLM02 | unchanged |
| Supply Chain | LLM03 | LLM04 | |
| Data and Model Poisoning | LLM04 | LLM05 | |
| Improper Output Handling | LLM05 | LLM10 | five places |
| Excessive Agency | LLM06 | LLM03 | three places |
| System Prompt Leakage | LLM07 | LLM08 | *renamed* Hidden Context Exposure |
| Vector and Embedding Weaknesses | LLM08 | LLM09 | |
| Misinformation | LLM09 | LLM07 | |
| Unbounded Consumption | LLM10 | LLM06 | four places |

**Eight of the ten changed number in one edition.** Only prompt injection and sensitive
information disclosure kept theirs, and the largest single move is five places — improper
output handling, from the middle of the list to the end of it. One entry was also renamed, and
the renaming is the interesting one,
because it is a widening rather than a tidy-up: *system prompt leakage* is about one thing a
system has, and *hidden context exposure* is about every part of the input the user cannot
see — your instructions, the tool schemas, the retrieved policy text, the configuration. The
new name is a better description of what Chapter 2's context actually is, and it arrived two
editions late.

Go back a further two editions and almost nothing survives. The 2023 list had entries for
insecure plugin design, model theft and overreliance; none of the three is on the current list
under that name. **A candidate who memorised the numbering has memorised the part that
changes.**

**And the list is harder to check than it looks.** On 30 October 2026, the project's own
landing page for the LLM list still showed the ten 2025 entries, while the current release —
named as such on the project's repository and front page — was the 2026 edition. So two
numberings were in circulation at once, on the same site, and either of them could have been
read off as current. The agentic list is distributed as a download rather than as a web page,
which makes its exact wording harder still to quote with confidence; the titles in the table
above are as published and are worth re-reading from the source before you rely on the exact
words.

None of that is a complaint about the lists, which are careful work by a lot of people. It is
the reason for the sentence this section exists for:

**A risk list is a checklist and never a certificate.** It is a prompt to ask twenty questions
about your own system. It is not evidence that your system has any of those problems, and
passing all twenty is not evidence that it does not.

Chapter 6's ladder is the right place to put it. The tell for settled practice, that chapter
said, is written-down failure modes — so a published risk list is close to the strongest
*kind* of evidence that this field has met these failures and agreed on their names. What it
is not is evidence about *your* system, and the two are easy to confuse because the list is
the more authoritative-looking document. Your evidence about your own system comes from
attacking it, which is the last section of this chapter.

## Model Output Is Input to the Next Component

The lists have an entry for the direction almost nobody checks, and it is worth its own
section because the fix is not an AI technique at all.

Everything so far has been about text going *into* the model. **Insecure output handling** is
what happens on the way out: model output reaching a component that renders it, executes it,
or uses it to build an instruction for something else. The 2026 list calls it improper output
handling and puts it last; the 2025 list had it fifth, and the demotion says nothing about how
often it happens.

Here is the shape, in the four places it actually turns up.

| Where the output goes | What the component does with it | What goes wrong |
|---|---|---|
| A page in a browser | Renders it as part of the document | Output that contains markup is treated as markup |
| A database query | Runs it, or builds a query around it | Output that contains query syntax changes the query |
| A command line | Executes it | Output that contains command syntax runs a second command |
| A file path, or a URL your code fetches | Opens it | Output that names something else reaches something else |

Here are the first three of those four, run. The reply is written out rather than generated, so
the demonstration is deterministic; what it contains is the kind of thing a reply carries when
part of its content came from a document somebody else wrote.

```python
"""One model reply, three places it goes, each the wrong way and the right.

    python3 sinks.py

Nothing here calls a model. The reply is written out so the demonstration
is deterministic, and it is the kind of reply chapter 50's lab produced:
correct-looking text whose content came partly from a document somebody
else wrote.
"""
import html
import shlex
import sqlite3
import subprocess

#  What the model returned. Three fields, and every one of them is a
#  string your code is about to hand to something that acts on it.
REPLY = {
    "answer": 'Your parcel is with Carrick Express<script>steal()</script>',
    "carrier": "Carrick' OR '1'='1",
    "filename": "tracking.pdf; rm -rf /tmp/demo",
}

DB = sqlite3.connect(":memory:")
DB.execute("CREATE TABLE carriers (name TEXT, phone TEXT)")
DB.executemany("INSERT INTO carriers VALUES (?, ?)",
               [("Pellworth Logistics", "0300 000 0001"),
                ("Carrick Express",     "0300 000 0002"),
                ("Dunmore Freight",     "0300 000 0003")])


def into_a_page(text):
    """A page: concatenated, then escaped at the boundary."""
    bad = f"<p>{text}</p>"
    good = f"<p>{html.escape(text)}</p>"
    return bad, good


def into_a_query(name):
    """A query: built from text, then given the value as a parameter."""
    bad = DB.execute(
        f"SELECT name FROM carriers WHERE name = '{name}'").fetchall()
    good = DB.execute(
        "SELECT name FROM carriers WHERE name = ?", (name,)).fetchall()
    return bad, good


def into_a_command(filename):
    """A command: a line a shell would lex, then an argument list.

    The lexer does the splitting a shell does - `punctuation_chars`
    makes `;` a token of its own rather than part of a word - so the
    command count below is a lexer result and not a split on ';'.
    Nothing destructive runs on either path: the command is `echo`,
    so the worst case is a word printed.
    """
    line = f"echo opening {filename}"
    lexer = shlex.shlex(line, punctuation_chars=True)
    lexer.whitespace_split = True
    tokens = list(lexer)
    commands = 1 + tokens.count(";")
    good = subprocess.run(["echo", "opening", filename],
                          capture_output=True, text=True).stdout.strip()
    return commands, tokens, good


if __name__ == "__main__":
    bad, good = into_a_page(REPLY["answer"])
    print("  INTO A PAGE")
    print(f"    concatenated   ...{bad[38:66]}")
    print(f"    escaped        ...{good[38:66]}")
    print(f"    a live tag in the first: {'<script>' in bad}")
    print(f"    and in the second:       {'<script>' in good}")

    bad, good = into_a_query(REPLY["carrier"])
    total = DB.execute("SELECT count(*) FROM carriers").fetchone()[0]
    print("\n  INTO A QUERY, asking for one carrier by name")
    print(f"    built from text   {len(bad)} row(s) of {total}")
    print(f"    parameterised     {len(good)} row(s) of {total}")

    n, tokens, good = into_a_command(REPLY["filename"])
    after = tokens[tokens.index(";") + 1] if ";" in tokens else None
    print("\n  INTO A COMMAND")
    print(f"    lexed as a shell lexes it  {n} command(s), the")
    print(f"                               second starting {after!r}")
    print(f"      {' | '.join(tokens)}")
    print(f"    as an argument list        1 command, and the")
    print(f"                               name arrives whole:")
    print(f"      {good[8:]!r}")
```

```text
  INTO A PAGE
    concatenated   ...<script>steal()</script></p>
    escaped        ...&lt;script&gt;steal()&lt;/sc
    a live tag in the first: True
    and in the second:       False

  INTO A QUERY, asking for one carrier by name
    built from text   3 row(s) of 3
    parameterised     0 row(s) of 3

  INTO A COMMAND
    lexed as a shell lexes it  2 command(s), the
                               second starting 'rm'
      echo | opening | tracking.pdf | ; | rm | -rf | /tmp/demo
    as an argument list        1 command, and the
                               name arrives whole:
      'tracking.pdf; rm -rf /tmp/demo'
```

**The query is the one to look at twice.** The code asked for one carrier by name. Built from
text, it returned all three rows in the table, because the name it was given closed the quote
and added a condition that is true of everything. Parameterised, the same name returned
nothing — which is the correct answer, since no carrier is called `Carrick' OR '1'='1`. Notice
that the parameterised version did not detect an attack and did not reject anything. It
treated the string as a value, which is what it was, and the question of whether the string was
hostile never arose.

The command is the same shape, and the program lexes the line rather than asserting what a
shell would do with it: `shlex` with shell punctuation turns the semicolon into a token of its
own, so the seven tokens it prints contain a separator and the line asks for two commands, the
second starting `rm`. As an argument list there is one command and the filename arrives whole —
semicolon included, now part of a name rather than a separator. And the page is the familiar
one: the tag is live in the concatenated version and inert in the escaped one.

Chapter 21 established the rule this is a special case of: never trust prose, parse a contract.
What this chapter adds is the direction. Chapter 21 was about your code being unable to *read*
the model's output reliably. This is about your code reading it perfectly well and then handing
it to something that acts on it.

**The thing to notice is that the model is not the attacker here.** It does not need to be.
Model output is a function of model input, and Chapter 50's lab is the proof of concept: text
that reached the model through a document changed what the model wrote. So if an attacker can
influence the input and your code puts the output somewhere that executes, the attacker has a
path to that executor through two components that each behaved as specified.

**And the fix is the ordinary one**, which is good news and is also the reason this entry is
easy to forget. It is the discipline that web and database engineering settled on long before
any of this: escape at the boundary where the text becomes part of a document, pass values as
parameters rather than building a statement out of text, and give a command its arguments as a
list rather than composing a line for a shell to split. Those are not AI techniques and the
model's involvement does not change them. The only thing that changes is which strings you had
classified as yours.

**The one case that does not have an ordinary fix is a URL**, and it is worth a paragraph
because it is how data leaves. If your code, or the model's own browsing tool, fetches a URL
the model produced, then the model can send a request to an address of somebody else's
choosing — and a request carries whatever the model put in it. That is the third ingredient of
the design rule arriving through a channel nobody listed as a tool. A system where the model
can cause an outbound request to an arbitrary address has an external action whether or not
there is a tool called `send`. The decision, like every decision in this chapter, is made in
code: an allowed list of addresses, or no fetching of addresses the model composed.

## A Tool Acts With the Caller's Rights

Chapter 5's lab ended on a failure that none of its five causes explained, and said this
chapter owned it. Here is the paragraph it ended on: a support assistant showed a customer the
correct details of an order that was not theirs, because the lookup took an order number and
never checked whose order it was.

Nothing about that failure is specific to models, and that is the first thing to say about it.
A web page with the same bug has the same bug. What the model adds is a detail that changes how
you have to write the tool: **the model composes the arguments.** So the subject of the action
— *whose* order, *whose* record, *which* account — arrives in text that an attacker may have
influenced, which the previous sections have established at length.

**Per-user tool authorisation** is the rule that follows: a tool acts with the rights of the
caller on whose behalf the request is being handled, and not with the rights of the service
that runs it. Two tools, to make the difference exact.

```python
#  Acts with the service's rights. The caller is nowhere in it.
def get_order(order_id):
    return DB.fetch("orders", order_id)

#  Acts with the caller's. The caller comes from the session, never
#  from the proposal, and the join is checked before anything is read.
def get_order(caller_id, order_id):
    row = DB.fetch("orders", order_id)
    if row is None or row["customer_id"] != caller_id:
        return None, "not your order"
    return row, None
```

Two things about the second version are the whole of the rule. Then the same scoping has to go
somewhere else as well, which is the rest of this section.

**The caller's identity does not come from the model.** It comes from wherever your service
already knows who is calling — the session, the request's credentials, whatever your
application used before any of this existed. Chapter 23's registry holds the function; the
dispatcher holds the caller. A tool signature that takes `customer_id` as a parameter the model
fills in is a tool with no authorisation, however carefully the instructions ask the model to
fill it in correctly, and for the mechanical reason Chapter 23 gave: your instruction is not a
limit, and nothing in the loop compares the proposal's values against it.

**The check is in the tool, not in the instruction and not in the prompt.** This is the same
rule as everything else in the book, and it is worth saying again in this specific place
because the temptation is strongest here. It is very easy to write *only answer about the
customer who is asking* in the instructions and feel that something has been decided. Nothing
has been decided. Chapter 23's five steps are the proof: steps 3, 4 and 5 are your code, and
if your code does not compare, no comparison happens.

**And retrieval has exactly the same problem, which is Chapter 29's and is already measured
there.** Chapter 3 gave the half of the data gap that does not shrink, and one of its three
parts is that your data is different per reader: a model's knowledge is one body of knowledge,
identical for everyone who calls it. Chapter 29 is where that becomes a retrieval decision, and
it owns the names — pre-filtering, post-filtering, the metadata filter, multi-tenant retrieval —
along with the arithmetic for what each costs. Two of its findings are the ones to carry into
this chapter:

**Filtering by ownership is a correctness requirement and not a quality one.** That is Chapter
29's sentence, and it is about the filter rather than about where you put it: another tenant's
document in your context is a disclosure, not a worse answer. So this is the one retrieval
decision in the book that is settled by this chapter's subject rather than by a measurement.

**And where you put it decides whether the caller gets an answer.** Chapter 29's arithmetic is
the thing to carry: a post-filtered search returns about the *fetch* times the share that
survives, so fetching a hundred where this caller owns one per cent gives about one back when
you asked for ten. Post-filtering is safe — the other customer's record never reaches the
context — and it is safe at the price of quietly answering a narrower question for exactly the
callers whose share is smallest, unless the fetch is large enough to carry them. Pre-filtering
has no such arithmetic to get right, and Chapter 29 is where the choice is made.

**The quiet version of this failure is the one worth looking for**, because it does not look
like an attack. Chapter 5's paragraph 12 had no attacker in it. Somebody asked an ordinary
question, the model proposed a plausible order number, and the tool answered. A system with no
per-caller scope leaks by accident long before anybody tries to make it leak, which is the
best argument for fixing it: the test case does not need an adversary.

## Code the Model Wrote Has to Run Somewhere Harmless

Some systems run code the model produced. A data-analysis assistant that writes a query and
charts the result, an agent that writes a script to rename a thousand files, a coding tool that
runs its own tests — Chapter 2's last row in the arrangements table is this shape, and it is a
tool like any other, with one property no other tool has.

**Its reach is not the reach of a function you wrote. It is the reach of whatever that code
can do.** A tool that fetches an order touches orders. A tool that runs arbitrary code touches
everything the process it runs in can touch, which is a different kind of statement.

The tempting answer is to check the code before running it. That answer is wrong for a reason
this book has already established twice. A check on the code is a check on text, and Chapter
21's rule applies: you are parsing prose rather than reading a contract. Worse, the thing you
would be checking for is *intent*, which is the thing text does not carry — a program that
reads a file and a program that exfiltrates it are the same program with a different second
line. **A validator that reads generated code for safety is the same mistake as a validator in
an instruction**, made one level further out: it is a judgement about text, standing where a
limit should be.

The limit that works is the process. **Sandboxing** is running the generated code somewhere
that cannot reach anything you mind about, and the list of what that means is short and
concrete:

| Limit | Why |
|---|---|
| No network, or an allowed list of addresses | Without this, everything else leaks out through a request |
| No credentials in the environment | Chapter 40 put a key in a shell's environment; generated code in that shell reads it |
| A filesystem it may read, and one directory it may write | So a write cannot change what the next run reads |
| A time limit and a memory limit | Otherwise the caller decides how much your machine does — the list's unbounded-consumption entry |
| Nothing of production in it: no live database, no real customer data | So the worst case is a lost sandbox |
| Thrown away after the run | A sandbox that persists is a place for the next run to find something |

Two notes on that table, because it is the kind of list that gets copied without its reasons.

The second row is the one people get wrong, and Chapter 40 is where the reader has already
met it. That chapter's warning was about not writing a key into a file in the project folder.
The sandbox version is sharper: a key in the environment of a process is readable by anything
running in that process, and generated code runs in that process. So an agent that both holds
your provider key and runs code the model wrote has handed the key to the code. The key does
not need to be in the context to leak; it needs to be in the environment.

And the whole table is a *reach* decision rather than a *correctness* decision, which is why
none of it depends on the code being bad. The code is usually fine. The sandbox is what makes
the question of whether it is fine stop being load-bearing.

## A Tool Server You Did Not Write Is a Dependency

Chapter 36 took the protocol apart and established the mechanical fact: a tool description from
a server you do not control arrives in the same input as your system message, and the
specification says so about itself, telling implementers to treat a server's annotations as
untrusted unless the server is one they trust. That chapter also drew the conclusion this one
agrees with — the limit stays where Chapter 23 put it, because your registry decides what
exists and your dispatcher decides what runs, and neither of them reads the description.

What this chapter adds is the framing the risk lists use, and it is a useful one because it
tells you which existing discipline to apply. A tool server you added is a **supply-chain
dependency**: a thing your system's behaviour depends on, which somebody else writes, versions
and ships. Four exposures, and only the first is specific to models:

1. **Its text is in your prompt on every call.** Chapter 36's case, and Chapter 23's
   arithmetic for what the descriptions cost applies to it.
2. **Its code decides what a tool returns.** A tool result is a channel from this chapter's
   first table, so a server that changes what it returns changes what the model reads.
3. **It sees what you send it.** Every argument your dispatcher passes, which for a tool that
   takes a customer's details is the customer's details.
4. **It can change without a release of yours.** This is the one that makes it a supply chain
   rather than a library: a server you call over a network is a dependency whose version you
   may not be choosing.

So the discipline is the ordinary one, and it is the same discipline you would apply to any
dependency that can execute in your context: know who publishes it, pin what you can pin,
read what it sends you at least once, and have a way to notice when it changed. Chapter 54
owns the mechanics of pinning and of gating an upgrade, and a tool server belongs in that
system rather than in a separate one.

**The part that is genuinely different is consent.** Chapter 36 noted that the specification
requires a host to obtain explicit consent from the user before invoking any tool at all —
Chapter 4's approval point arriving as a protocol requirement. That is the design rule's fourth
answer written into a standard, and it is worth knowing both that it is there and what it is
worth: a consent prompt on every call is a prompt that gets clicked through, which is Chapter
3's rubber-stamping under a different name and the list's human-trust entry.

## Why a Filter Is Never the Boundary

A **guardrail** is the field's word for a check placed around a model call to catch bad input
or bad output: a classifier that reads the user's message and decides whether it contains an
injection, a filter on the reply, a second model asked whether anything untoward is happening.
They are worth having, and they do not replace the boundary — the argument has three steps that
the book has already made separately.

Be exact about which kind of check the argument is about, because the word covers two things.
A rule your code can state exactly — this tool takes an id of this shape, this field is one of
four values, this address is on the allowed list — is the top of Chapter 2's table of checks,
and it is a limit in code like any other. Those are not what people mean by a guardrail
and nothing below applies to
them. What the word usually names is a judgement about natural language, and that is a check
whose verdict is approximate.

**One: a guardrail is a check, so it has a check's costs.** Chapter 2 put checks in a table
from cheap and certain to expensive and approximate, and a classifier reading prose for
hostile intent sits at the expensive, approximate end. Chapter 3 then named the two costs that
every check carries: it only catches what somebody thought to write down, and tightening it
rejects good input along with bad. A filter tuned to catch instructions hidden in documents
will refuse documents that discuss instructions, which for a company whose documents are
policies is most of them.

**Two: a model-based guardrail shares the failure modes of the thing it is guarding.**
Chapter 3's structural point, stated there about self-checking, applies to any check built
from the same kind of component: it will tend to be wrong in the same places, for the same
reasons. And Chapter 31 is a whole chapter on what it takes to earn the right to believe a
model judge — self-agreement, a baseline, position bias — none of which a guardrail usually
has behind it before it is deployed.

**Three: and the attack that matters may not look like an attack.** This is the step Chapter
50 contributes, and it is the sharpest of the three. The payload that worked in that lab was
178 characters sitting inside a 1,181-character document, and what it asked for was an
*omission* — stop citing your sources. A filter looking for hostile instructions would have had
to pick that sentence out of a document whose own text already says *follow the instructions on
the card* — a planted property the corpus README records, so that the injected sentence does not
read as out of place. And the reply it produced was correct prose with an
empty citation list, so an output filter looking for something wrong in the answer would have
found nothing wrong in the answer.

Treat that as a judgement rather than a result, because it is one: no filter was built, here or
in Chapter 50, so what the paragraph establishes is the size of the problem a filter would face
rather than a measured failure rate. The sizes are measurements; the inference from them is not.

So what is a guardrail worth? Two things, honestly stated, and Chapter 50's four-line citation
check is the model for both. It raises the cost of the attacks it knows about, which is real
and is not a boundary. And **it turns a failure that was served into a failure that was
logged**, which is the sentence that chapter arrived at and is the right expectation to carry.
Nothing in the four lines prevents an injection: by the time the check runs, the model has read
the injected text and the citations are already gone.

**The boundary is what your code can refuse.** The registry, the per-caller scope, the sandbox,
the tool you did not build. Guardrails sit on top of that and are worth their cost when the
thing underneath is already decided. A system whose only answer to this chapter is a filter has
no boundary at all; it has a component that is usually right, which is where this chapter
started.

## Secrets and Credentials

Chapter 40 put a provider key in a shell's environment and warned the reader not to solve the
inconvenience by writing it into a file in the project folder. That warning becomes a subject
here, and the subject is small enough to state completely.

A **secret** is a value that grants access by being known: a provider key, a database password,
a signing key, a session token. Three properties follow from that definition and they are the
whole of why secrets are handled the way they are.

**It is a bearer credential.** Whoever holds it can do what it authorises, with no further
question asked. There is no second factor on an API key and no record of who copied it.

**It is long-lived unless somebody made it short-lived.** A key issued once and pasted into a
configuration file keeps working for years, including after the person who created it has left
and after the laptop it was on was sold.

**Its scope is whatever it was issued for, and that is the only limit on the damage.** This is
the one with a design consequence, and it is the same consequence as every other section in
this chapter: you cannot make a leak less likely by being careful, so you make it cost less by
scoping. A key that can spend money and read every customer's data is worth more than a key
that can call one model with a monthly cap.

So: where a key lives.

| Where | Verdict |
|---|---|
| A secret manager, or the environment of the process, set from outside the project | The two reasonable answers |
| A file inside the project folder | No. It is the place most likely to be committed, which Chapter 40 said |
| Anywhere in the repository, including a configuration example | No, and deleting it later does not help: the history keeps it |
| In the model's context | No. It is then input, and the list's hidden-context entry is the reason |
| In the environment of a process that runs generated code | No, for the reason the sandbox table gave |
| In a log, a trace or an error message | No, and this is the one that happens by accident |

The last row is the one that needs the extra sentence, because it is where this book's own
advice can turn into a leak. Chapter 33 argues for recording what actually happened on each
request so a failure can be traced rather than argued about, and Chapter 49 wrote whole runs
to files to price them. A trace is a complete record of the input, which means a trace is
where secrets and customer data accumulate, in a file nobody classified as sensitive because
it was written for debugging. The decision is made where the trace is written: record what the
request *was*, and keep the credential out of the record by never putting it in the part of the
request you record.

**And what a leaked key reaches is the question to ask before you need the answer.** It is a
better question than how to avoid leaking one, because it has a concrete answer you can change
today. Work it through for the three a system like this one holds:

- *A provider key* reaches your balance, so somebody else's traffic appears on your bill, and
  Chapter 53's budget is the thing that notices. Depending on how the account is set up it may
  also reach the console that lists what you have been sending, which is to say your prompts
  and your retrieved passages. A key scoped to one project with a spending cap reaches much
  less than an organisation-wide one, and the two cost the same to issue.
- *A database password* reaches every row the account it belongs to can read, which for an
  application account is usually every customer. A read-only replica for the retrieval side
  reaches the same rows and cannot change them.
- *A tool's own credential* — the thing a `send_email` or a payments tool authenticates with
  — reaches whatever that service lets it do, and this is the one where the design rule and
  the key meet: a tool scoped to one mailbox and one sender address is a smaller loss than a
  tool holding the credential your whole company sends mail with.

The pattern across the three is the same and it is the pattern of this whole chapter: the thing
you can decide in advance is reach. Rotation is the part everybody plans for, and it is also
the part that is useless if you do not know which key went — which is the practical argument
for a key per environment and per service, since it is what turns *something leaked* into a
list of what to turn off.

## An Attack Suite Is How You Find Out It Decayed

Every defence in this chapter is a decision made once. A tool was not given a send. A lookup
took the caller's id. A sandbox had no network. The registry held one name.

**Decisions made once decay, and they decay for ordinary reasons rather than dramatic ones:**
somebody adds a tool, somebody widens a scope to fix a bug, somebody passes a customer id
through because the signature was convenient, a tool server ships a new description. None of
those is a mistake at the time. Together they turn a system that satisfied the design rule into
one that does not, and nothing announces it — which is Chapter 5's point about this whole field,
that the failures do not announce themselves the way a crash does.

Chapter 50 built the thing that notices. What belongs here is what it is *for* and what it may
claim, because that chapter had to learn both the hard way.

**What an attack suite is for.** It runs your own injections against your own system on every
change, beside the regression set rather than in a separate command, because a team with two
commands runs the cheap one on every change and the expensive one before a release — and the
release is then where you find out. It has to be cheap and safe enough to run a hundred times
a day, or it is not a suite.

**What it may assert.** Chapter 50 owns this and it is worth repeating exactly, because two of
the three are easy to get wrong. Invariants *against the code* — the dispatcher is called, and
refuses a name the registry does not hold. Controls — a clean run triggers none of the
detectors, without which no figure means anything. Coverage — every success the measurement
found is one a check catches, which is a claim about your checks and not about the model.

**And what it must not assert: that the model does not comply.** It sometimes complies. A gate
on that fails on every run and is deleted inside a week, so the counts get printed instead.
Chapter 50's harder lesson is worth carrying too: its first invariant read a boolean out of
stored runs, and a dispatcher rewritten to run anything still passed it. **A gate over stored
evidence cannot test code**, and a gate that cannot fail is worse than none, because it gets
cited as a defence.

Chapter 54 owns the other half of this, and the join is worth naming: a provider's model
update is a change to your system that you did not make, so it has to pass this suite like any
other change. A defence that depended on a model's behaviour — and the marker payloads in
Chapter 50's grid are exactly that, zero because the model declined — is a defence whose
evidence expires with the version.

## What This Chapter Has Not Told You

Four things, deliberately.

**The entries of the two lists this chapter does not reach.** Data and model poisoning is about
material arranged by somebody else before you ever ran anything, which is a supply-chain
question about weights and training sets rather than about a request; Chapter 39 is the nearest
this book comes to it. Inter-agent communication is Chapter 37's arrangement with this
chapter's rule applied to it, and this book does not build one. Rogue agents, in the sense the
list means — an agent operating outside its policy through drift — needs a system large enough
to drift.

**How to build a filter.** This chapter argues about what one is worth and does not build one.
If you want one, Chapters 30 and 31 are the method: read real failures, name the modes, write
the check per mode, and validate the judge before believing it. A filter built without those is
a component whose accuracy nobody knows.

**Threat modelling as a discipline.** There is a whole practice of enumerating attackers,
assets and paths systematically, and it is worth learning if security becomes your job. The
design rule in this chapter is a small, specific substitute that covers the case this book is
about.

**And anything that is law rather than engineering.** Which data you may hold, where it may be
processed, what you must disclose after a breach — those are real constraints on a system and
they are not in this book. Chapter 3's note is the right framing: the legal floor is not yours
to move, and everything above it is a design decision you own.

One more thing, which is not an omission but a property: **the lists in this chapter will have
moved by the time you read it**, and the rule will not. That is why the rule was written down
separately from the catalogue.

## Summary and Key Terms

### Summary

A page your system reads can get an instruction in front of the model, because your
instruction is text in the input and so is the page, and nothing in one sequence of tokens
marks which part is yours — Chapter 23's mechanism, and the general rule is that **a model
cannot reliably tell an instruction from data**, which is not a defect that better models close
but a property of a component that has no channel for metadata. What such text cannot do is
act: only your code acts, and only through a name its registry holds. What it can do is take
away a rule that exists only as an instruction, which Chapter 50 measured on four of four
questions and all twelve of their runs.
**Every channel the model reads is input** — the request, a retrieved passage, a tool result, a
tool *description*, a note the agent wrote, a sub-agent's return, a compaction summary — and the
job is to write that list down for your own system. The design rule is about combinations:
**never combine untrusted input, sensitive access and external action in one session without
approval**, because any two are ordinarily survivable and the three together give injected text
something to ask for and a way to send it; the four fixes are removing one of the three,
shrinking one, or adding the approval, and approval is the weakest wherever the action is
frequent, because volume turns review into rubber-stamping. The field's two catalogues —
the *OWASP Top 10 for LLM Applications 2026* and
the *OWASP Top 10 for Agentic Applications* version 2026 — are a vocabulary worth knowing and
**a checklist rather than a certificate**: eight of the LLM list's ten entries changed number in
one edition, one was renamed and widened, and two numberings were in circulation on the
project's own site at once, so the numbering is the part that changes. On the way out,
**insecure output handling** is model output reaching something that renders or executes it, and
the fix is the ordinary escaping and parameterising that web and database engineering settled
long ago, plus a decision about URLs the model composes, because an outbound request is an
external action with no tool. **Per-user tool authorisation** means a tool acts with the
caller's rights and not the service's: the caller's identity comes from the session and never
from the proposal, the check lives in the tool, and retrieval needs the same scoping before the
passages reach the context. Code the model wrote needs **sandboxing** rather than inspection,
because a validator reading generated code for safety is a judgement about text standing where
a limit should be — no network, no credentials in the environment, nothing of production, thrown
away after. A third-party tool server is a supply-chain dependency on four counts, and Chapter
54's pinning and gating is where it belongs. A **guardrail** is a check and carries a check's
costs, shares the failure modes of what it guards, and would have had to find 178 characters
inside a 1,181-character document to catch Chapter 50's attack — so what it buys is that a
failure is logged rather than served, and the boundary is what your code can refuse. A
**secret** is a bearer credential, long-lived unless you make it otherwise, and bounded only by
its scope, so it goes in a secret manager or the process environment and never in the
repository, the context, a sandbox's environment or a trace. And because every defence here is
a decision made once, and decisions decay, the last part is an attack suite that runs on every
change — asserting invariants against the code, controls and coverage, and never that the model
does not comply.

### Key Terms

| Term | Meaning |
|---|---|
| **Session** | One run of a system that shares a context: a request and its answer, or an agent's loop from the user's message to its last step. The unit the design rule is about |
| **Insecure output handling** | Model output reaching a component that renders it, executes it or builds an instruction from it — a page, a query, a command line, a URL your code fetches. Called improper output handling on the current risk list |
| **Per-user tool authorisation** | A tool acting with the rights of the caller on whose behalf the request is handled, rather than with the rights of the service. The caller's identity comes from the session, never from the model's proposal |
| **Sandboxing** | Running code the model wrote in a process that cannot reach anything you mind about: no network, no credentials, no production data, discarded after the run. A limit on reach rather than a judgement about the code |
| **Supply-chain dependency** | Something your system's behaviour depends on that somebody else writes, versions and ships — a tool server, a package, a model. A server you call over a network is one whose version you may not be choosing |
| **Guardrail** | A check placed around a model call to catch bad input or bad output — usually a judgement about natural language rather than a rule your code can state exactly. Worth having and not a boundary: it raises the cost of the attacks it knows and turns a served failure into a logged one |
| **Secret** | A value that grants access by being known — a key, a password, a token. A bearer credential, long-lived unless made otherwise, and bounded only by what it was issued for |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The design rule | Never combine *untrusted input*, *sensitive access* and *external action* in one session without approval. Remove one of the three, shrink one, or add the approval — and approval is the weakest wherever the action is frequent, because it degrades with volume |
| The four fixes | No such tool · do not read the untrusted thing · scope the access to the caller · a person approves. The first two remove a capability, so nothing has to work at the moment of the attack |
| The two current lists | *OWASP Top 10 for LLM Applications 2026*, LLM01–LLM10, published early August 2026. *OWASP Top 10 for Agentic Applications* version 2026, ASI01–ASI10, released 9 December 2025 |
| What a list's numbering is worth | 8 of the LLM list's 10 entries changed number between the 2025 and 2026 editions; the largest move is 5 places. Quote the entry, not the number |
| Where the caller's identity comes from | The session. Never a parameter the model fills in |
| What a guardrail buys | The attacks it knows, and a failure logged instead of served. Chapter 50's payload was 178 characters inside a 1,181-character document. A rule your code states exactly is a different object, and is a limit |
