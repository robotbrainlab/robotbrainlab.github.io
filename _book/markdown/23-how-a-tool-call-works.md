# How a Tool Call Works, and Who Decides

*The problem.* People say the model "called an API". Models generate text, so something here is
being skipped.

*The question.* What actually happens when a model uses a tool, and at which step does something
get decided?

## Nothing Called Anything

A model emits tokens. That is the whole of what it does, and Chapter 9 is why. It has no network
access, no file handle and no way to run a function. So when somebody says the model called an
API, the sentence has compressed five steps into one, and four of them are yours.

| Step | Who does it | What it is |
|---|---|---|
| 1 | Your code | Send the tool descriptions, as text, with the prompt |
| 2 | The model | Emit tokens that your code can read as a proposal |
| 3 | Your code | Parse it, validate it, and decide whether to run it |
| 4 | Your code | Run the function and get a result |
| 5 | Your code | Send the result back as another message, and ask again |

**The model's entire contribution is step 2, and step 2 is text.** Everything that touches the
world is yours.

**So there are two decisions, not one, and conflating them is the mistake in the opening
sentence.** The model decides *what to propose*. Your code decides *what runs*. People say the
model called the API because the two decisions sit next to each other in time and the second one
is invisible — it happens inside code you wrote, so it does not feel like a decision at all.
**Only one of the two can refuse**, and this chapter is about that one. Chapter 2 drew the same
line first: both of them decide something, and the two decisions are different.

Chapter 4 owns the loop this sits inside — what makes it run again, and what stops it. This
chapter owns the five steps themselves, in detail, and it goes round twice where it has to in
order to show step 5.

## Describing a Function to a Model

Step 1. Your code has functions; the model cannot see them. What it gets is text.

```python
import json

def get_balance(account_id):
    return {"account_id": account_id, "balance_pence": 184_200}

def refund(order_id, amount_pence):
    return {"refunded": order_id, "amount_pence": amount_pence}

# What your code knows. The model never sees the functions, only the text
# rendered from the "describe" fields below.
REGISTRY = {
    "get_balance": {
        "describe": "Return the balance of one account.",
        "params": {"account_id": {"type": str, "max_len": 12}},
        "run": get_balance,
    },
    "refund": {
        "describe": "Refund part or all of an order.",
        "params": {"order_id":     {"type": str, "max_len": 12},
                   "amount_pence": {"type": int, "min": 1, "max": 50_000}},
        "run": refund,
    },
}
```

Three things are in each entry and they go to three different places. The `describe` text and
the parameter *names and types* are sent to the model, and together they are the **tool
description**. The constraints — the maximum length, the range — are not sent; they are for your
code. And `run` never leaves your process.

```python
import json
from tools import REGISTRY

def render(name):
    """The text your code sends. The model sees this, never the function."""
    spec = REGISTRY[name]
    params = {k: r["type"].__name__ for k, r in spec["params"].items()}
    return json.dumps({"name": name,
                       "description": spec["describe"],
                       "parameters": params})

for name in REGISTRY:
    spec = REGISTRY[name]
    print(f"  {name}")
    print(f"    {spec['describe']}")
    for k, r in spec["params"].items():
        print(f"    {k}: {r['type'].__name__}")
    print(f"    -> {len(render(name))} characters as sent")
```

```text
  get_balance
    Return the balance of one account.
    account_id: str
    -> 113 characters as sent
  refund
    Refund part or all of an order.
    order_id: str
    amount_pence: int
    -> 126 characters as sent
```

**That is the whole of "giving a model tools".** It is a paragraph of text per function, placed
in the input. There is no registration, no handshake and no capability granted. Chapter 18's
message list gained a block, and that is all that happened.

> **Note:** How providers carry that text differs — a dedicated `tools` field, or the system
> message, with their own field names and their own way of marking the proposal when it comes
> back. The arrangement varies and will keep varying. What does not vary is that it is input
> going in and text coming out, which is why this chapter is about the shape rather than the
> field names.

## The Proposal

Step 2, the model's only step. What comes back is tokens, and your code reads them as a proposal:

```text
  {"tool": "refund",
   "arguments": {"order_id": "ORD-9", "amount_pence": 2500}}
```

**Three things about that are worth being exact about.**

It is a **proposal**, not a call. Nothing has happened. Chapter 2 put it exactly: a proposed call
is a suggestion arriving in text.

It can be anything the model can emit. A tool you never described. An argument of the wrong
type. A refund of nine thousand pounds. Or a sentence instead of a proposal — *I will now issue
the refund for order ORD-9* — which is the most instructive failure, because it shows there was
never a mechanism to begin with, only a convention the model was following.

And **a provider's strict mode can make the proposal reliably parseable**, which is Chapter 22,
and worth having. It constrains the *shape*. It has nothing to say about whether `amount_pence`
should be 2,500 or 900,000.

## Your Code Decides

Step 3, and this is the chapter. Here is what your code checks, and then the **dispatcher** —
the code that takes a proposal, validates it, and either runs the function or refuses.

```python
def validate(name, args):
    """What your code checks before anything runs. Not a complete list:
    it accepts an unexpected key at the top level, and an empty string
    where a schema would want a minimum length."""
    if name not in REGISTRY:
        return f"no such tool: {name}"
    spec = REGISTRY[name]["params"]
    missing = sorted(set(spec) - set(args))
    if missing:
        return f"missing argument: {missing[0]}"
    extra = sorted(set(args) - set(spec))
    if extra:
        return f"unexpected argument: {extra[0]}"
    for key, rule in spec.items():
        v = args[key]
        if type(v) is not rule["type"]:     # type, not isinstance: ch 21
            return f"{key}: wanted {rule['type'].__name__}"
        if "max_len" in rule and len(v) > rule["max_len"]:
            return f"{key}: longer than {rule['max_len']}"
        if "min" in rule and not rule["min"] <= v <= rule["max"]:
            return f"{key}: outside {rule['min']} to {rule['max']}"
    return None

def handle(proposal):
    """Parse, validate, decide, and run or refuse."""
    try:
        call = json.loads(proposal)
    except json.JSONDecodeError:
        return "not JSON", None
    if not isinstance(call, dict):
        return "not a proposal", None      # valid JSON, wrong shape
    name = call.get("tool")
    args = call.get("arguments") or {}
    if not isinstance(name, str) or not isinstance(args, dict):
        return "not a proposal", None
    why = validate(name, args)
    if why:
        return why, None
    return None, REGISTRY[name]["run"](**args)
```

Six proposals, of the kinds you actually get:

```python
PROPOSALS = [
    '{"tool": "get_balance", "arguments": {"account_id": "ACC-00041"}}',
    '{"tool": "refund", "arguments": {"order_id": "ORD-9", "amount_pence": 2500}}',
    '{"tool": "refund", "arguments": {"order_id": "ORD-9", "amount_pence": 900000}}',
    '{"tool": "drop_table", "arguments": {"name": "orders"}}',
    '{"tool": "refund", "arguments": {"order_id": "ORD-9"}}',
    'I will now issue the refund for order ORD-9.',
]

if __name__ == "__main__":
    for i, p in enumerate(PROPOSALS, 1):
        why, result = handle(p)
        print(f"  {i}  {'REFUSED  ' + why if why else 'ran -> ' + json.dumps(result)}")
```

```text
  1  ran -> {"account_id": "ACC-00041", "balance_pence": 184200}
  2  ran -> {"refunded": "ORD-9", "amount_pence": 2500}
  3  REFUSED  amount_pence: outside 1 to 50000
  4  REFUSED  no such tool: drop_table
  5  REFUSED  missing argument: amount_pence
  6  REFUSED  not JSON
```

**Two ran and four did not, and the four are the chapter.**

Proposal 3 is well-formed, correctly typed, names a real tool — and asks for nine thousand
pounds. Chapter 21's layers again: it passes the shape checks and fails on range, and the range
check is one line that nobody puts in until the first time it is needed.

Proposal 4 is the one to remember. `drop_table` was never described to the model and does not
exist in the registry. The model produced it anyway, because producing plausible text is what it
does, and `drop_table` is extremely plausible text. A **registry** lookup is what stands between
that proposal and a **dispatcher** that does
something clever with names.

Proposal 5 is missing an argument. Proposal 6 is not a proposal at all.

**Then step 5 closes the loop.** The result — or the refusal — goes back as a message, and the
model's next turn sees it as more input. Chapter 18 named that role and owns it: a tool message is a
result your code returns after the model asked for something. Send the refusal text, not a generic
failure: *amount_pence: outside 1 to 50000* lets the model propose 50,000 instead, and *that was
invalid* does not. The edge on that advice is Chapter 4's: a specific refusal also tells the
model exactly where the fence is, and a loop that is refused and then tries a slightly different
route to the same place has been inconvenienced rather than controlled. Say the limit, and keep
the limit.

> **Warning:** A refusal is still an outcome, and the loop can spin. If the model proposes an
> out-of-range refund three times, something is wrong with the prompt or with the limit, and
> Chapter 4's step limit is what stops you paying to find out forever.

## Why Validation Cannot Live in the Instructions

This is the second question, and the answer people give is usually a preference. It is not a
preference, and the reason is mechanical.

Chapters 2 and 4 both state the rule — Chapter 4's approval point has to be in your code and not
in the instructions. Here is the mechanism underneath it, which the five steps make plain:
**nothing in the loop compares a proposal's *values* against your instructions except your own
code.** Be precise about that, because Chapter 22 has just shown you the exception that proves
the shape of the rule: a strict mode genuinely does check the model's emission during step 2 —
against a *schema*. It can hold a proposal to a shape, and to a closed set of values where you can enumerate
them — Chapter 22's enum, its easy case. What it does not do is hold a *number* inside a range
you decided: nothing in principle forbids it, and Chapter 22's rule is that the features which
survive the compilation are the features an engine supports, so assume a bound you did not see
enforced is not enforced. And nothing at all can check a value against the world — whether this
order exists, whether it has already been refunded, whether this caller may refund it. Those are
the limits that matter, and they are all yours. Look at the
table again. Step 1 is you sending text. Step 2 is the model
emitting text. Steps 3, 4 and 5 are yours. An instruction saying *never refund more than £500*
is input at step 1; it influences what is likely at step 2; and nothing anywhere compares step
2's output against it. If your code does not check, the check does not exist.

**And here is the second reason.** Your instruction is text in the input, and so is everything
else in there — the retrieved document, the user's message, the previous tool result. Nothing
marks one of those as an instruction and the rest as data; they arrive as one sequence of tokens.
So your instruction is not only unenforced, it is competing. Chapter 51 is where that becomes a
security problem rather than a reliability one, and it owns the question properly.

**And a third, which is the one that catches careful people.** Suppose the model complies
perfectly, every time, for a year. You still have no limit. You have a correlation, and the
first time the input is unusual — a document that mentions a large refund, a user who asks
twice, a model version change — the correlation is what you find out you were relying on.
Chapter 21's language for this: a validator that has never fired has also never been tested.

So the rule, in a form you can say:

**Validation belongs in your code because your code is the only participant that can refuse.**
Instructions shape what gets proposed, which is worth doing and is not a control. The limit is
the line of code that returns before the function runs.

## What the Model Sees Next

Step 5 deserves its own look, because it is where the loop actually closes. The result does not go back as a return value. It goes back as a
message in the list, and the model's next turn reads it as input like everything else.

Chapter 18 defined that role and pointed here for the mechanism. Here it is, as `exchange.py`,
over one exchange that needs two calls — the second because the customer asked for two things:

```python
import json
from tools import handle

# What the model would emit at each turn, written out so the exchange is
# deterministic. Turn 3 quotes turns 1 and 2's results, which is the point.
TURNS = [
    '{"tool": "get_balance", "arguments": {"account_id": "ACC-00041"}}',
    '{"tool": "refund", "arguments": {"order_id": "ORD-9", "amount_pence": 2500}}',
    "Your balance is GBP 1842.00 and I have refunded GBP 25.00.",
]

messages = [
    {"role": "system", "content": "You help customers with orders."},
    {"role": "user",   "content": "What is my balance, and refund ORD-9 GBP 25."},
]

for turn in TURNS:
    messages.append({"role": "assistant", "content": turn})
    why, result = handle(turn)
    if why == "not JSON":
        break                              # the model answered in prose: done
    messages.append({"role": "tool",
                     "content": json.dumps(result) if why is None else why})

for m in messages:
    body = m["content"]
    print(f"  {m['role']:9} {body[:46]}")
print(f"\n  {len(messages)} messages, {sum(len(m['content']) for m in messages)}"
      f" characters of content")
```

```text
  system    You help customers with orders.
  user      What is my balance, and refund ORD-9 GBP 25.
  assistant {"tool": "get_balance", "arguments": {"account
  tool      {"account_id": "ACC-00041", "balance_pence": 1
  assistant {"tool": "refund", "arguments": {"order_id": "
  tool      {"refunded": "ORD-9", "amount_pence": 2500}
  assistant Your balance is GBP 1842.00 and I have refunde

  7 messages, 369 characters of content
```

**Read the roles down the left.** A proposal is an `assistant` message — it is the model
talking. In the text convention this chapter models, the only thing that makes it a tool call is
that your code recognised it as one; where a provider marks the proposal for you, as the earlier
Note says they do, the recognising is done before your code sees it and the deciding still is
not. A result is a `tool` message, written by you. They alternate, and the alternation is the loop.

**The last turn is prose, and nothing stopped it.** The model was free to answer at every step
and chose to call a tool twice and then answer — which is Chapter 4's first stopping reason, the
model finishing, seen from inside step 5. Your dispatcher's `not JSON` branch is how the
program notices that no tool was proposed — which is the same branch that handled proposal 6,
being used for a success this time rather than a failure. **That is worth knowing, and it is a smell rather than a virtue.** *The model answered* and *the
model emitted something I could not parse* arrive at your code through the same door, because
both of them fail to parse as a proposal. A truncated reply — `{"tool": "refund", "arguments":` —
therefore ends the loop and becomes the last thing the user sees.

**And you cannot separate them by looking at the text**, which is the part to get right. There
are three cases, not two: a reply that parses as a proposal, a reply that is a plain answer, and
a reply that is neither because it was cut off. The first is obvious. For the other two, Chapter
21 already named the signal — read the response's own **finish reason**, which says whether the
model stopped because it had finished or because it hit the token cap. Only the second is a
failure, and nothing in the reply's characters tells you which of the two you are holding.

**And every one of those seven messages is sent on the next call**, along with the tool
descriptions: the system message, the user's question, both proposals, both results, and the
answer it finally gave. Chapter 18's arithmetic for a
conversation applies, and a tool exchange fills one faster than talking does. Count it here: the
user wrote one message of 44 characters, and what came back was five further messages and 294
characters, none of it from the user. A plain question and its answer would have added two.

> **Note:** How a result is tied back to the call it answers differs between providers — an id
> on the proposal that the result quotes, or simply the order of the messages. You need some
> such mechanism as soon as a model proposes two calls at once, which providers also handle
> differently — and when it does, two results go back before the model emits again, so it is not
> one message each. The role *names* vary too: a result may come back as its own role or inside a
> user-role message. What does not vary is whose contribution comes next — the model emits, then
> your code puts results in, then the model again.

## What the Descriptions Cost

One last mechanical fact, and it follows from Chapter 18. The descriptions are input, and input
is sent on *every call*.

```python
total = sum(len(render(n)) for n in REGISTRY)
each = total / len(REGISTRY)
print(f"\n  {len(REGISTRY)} tools = {total} characters, on every call")
for n in (2, 8, 30):
    print(f"  {n:2d} tools ~ {each*n:5.0f} characters ~ {each*n/4:4.0f} tokens")
```

```text
  2 tools = 239 characters, on every call
   2 tools ~   239 characters ~   60 tokens
   8 tools ~   956 characters ~  239 tokens
  30 tools ~  3585 characters ~  896 tokens
```

> **Note:** Treat the token column as an estimate and the character column as a measurement.
> Four characters to the token is a rule of thumb, not a result: Chapter 10 is why the real number
> depends on the tokeniser and on the text, and it can err either way — densely punctuated JSON
> and ordinary prose do not tokenise at the same rate. The characters are solid, and they are
> what to reason with. The more important correction is that `render` is this book's shape, kept
> short to fit the page. A real tool definition carries a nested schema with `type`,
> `properties` and `required`, and the same two functions written that way measure 190 and 231
> characters rather than 113 and 126 — about 210 a tool, so thirty tools is nearer 6,300
> characters than 3,600, and the token figure moves with it.

**Thirty tools is of the order of a thousand tokens on every call** — nearer fifteen hundred
with a real schema, as the Note works out — including the calls that need no tool at all, and
before the conversation has said anything. Two consequences, and only the first
one is obvious.

**You are paying for capability you mostly do not use.** The user asking *what is my balance*
pays for the refund tool's description, the escalation tool's, and the twenty-seven others'.

**And the model is choosing from thirty things.** That is the cost people do not count: a longer
menu is a harder choice, and Chapter 16's finding about uneven use of a long input applies to the
tool block like any other input. What to do about either is split: fewer, more purposeful tools
and a description the model chooses well from is Chapter 36's, and a routing step or tools
selected per request is Chapter 34's and Chapter 52's. The arithmetic is here so the decision is informed.

## Lab: Run the Five Steps by Hand

Three programs, pure Python, nothing to install. Forty minutes, and there is a key for every
step. Work in a new empty folder.

**Step 1.** Build `tools.py` from three of this chapter's code blocks, in this order: the one
beginning `import json` and `def get_balance`, the one beginning `def validate`, and the one
beginning `PROPOSALS = [`. Run it.

*Expected result:* the six lines in the chapter: two ran, four refused, each refusal naming its
own reason.

**Step 2.** Save the `render` block and the cost block together as `describe.py`, in the same
folder, and run it. Then
answer: which parts of the registry did the model never see?

*Expected result:* the chapter's output. The model never saw `run`, nor `max_len`, nor the `min`
and `max` on `amount_pence`. It saw two names, two sentences and three parameter names with
their types — 239 characters in total. Everything that stops a bad call is on your side of that
line.

**Step 3.** Delete the registry lookup — the two lines beginning `if name not in REGISTRY` — and
run `tools.py` again. What happens to proposal 4, and what would happen in a dispatcher that
looked tools up by
name?

*Expected result:* proposals 1, 2 and 3 print as before and then the program dies with
`KeyError: 'drop_table'` raised inside `validate`, because it now goes straight to
`REGISTRY[name]["params"]`. Here that is a crash, which is survivable. The point is what the same
missing line does in a dispatcher built to be helpful — one that falls back to a naming
convention, or searches a module for a matching function. Then the model's invented name is a
lookup key into your code, and `drop_table` is a plausible name for a real function somewhere.

**Step 4.** Put the line back. Now raise `amount_pence`'s maximum to 1,000,000 and run it again.

*Expected result:* proposal 3 runs and refunds £9,000. Nothing else changed — the proposal was
always well-formed, correctly typed and named a real tool. The only thing that ever stood between
it and your payment processor was a number in a dictionary in your code. Put the 50,000 back
before you go on.

**Step 5.** Change the instructions instead. Add to `tools.py` a module-level string
`INSTRUCTIONS = "Never refund more than 500 pence."` and run it again. What changed?

*Expected result:* nothing at all, which is the point of the exercise. The string is not read by
anything. In a real system it *would* be read — it would be sent to the model and would change
what step 2 proposes — and it still would not be a limit, because nothing in the loop compares
the proposal's values against it. Keep the dictionary value.

**Step 6.** Proposal 6 is prose. Change the dispatcher to look for the word "refund" in a
non-JSON proposal and act on it. Then say why you should not.

*Expected result:* you get part of the way and then stop, and where you stop is the lesson.
*I will now issue the refund for order ORD-9* gives you the word "refund" and an order id a
regular expression can find. It does not give you an amount — the only digit in the sentence is
the `9` of `ORD-9` — so `refund(order_id, amount_pence)` cannot be called without you inventing
a sum of money. That is the moment to stop. You have replaced a contract with a guess, which is
Chapter 21's rule about never trusting prose, now attached to something that moves money. And
the sentence *I will not issue the refund* contains the same word.

**Step 7.** Your service has 30 tools. A user says "hello". Roughly what does that cost, and
what are the two separate costs?

*Expected result:* about 3,600 characters by the chapter's renderer, so of the order of 900
tokens — and nearer 5,900 characters and 1,500 tokens with a real tool schema, which is the
number to quote. Either way it is sent before the user's word is even considered. The two costs
are the input you pay for on
every call, and the harder choice the model is making from a longer menu. The first is money, the
second is accuracy, and only the first shows up on the bill.

**Step 8.** Save the exchange program as `exchange.py` and run it. Then truncate the second
turn, cutting it down to `{"tool": "refund", "arguments":` and no more, and run it again.

*Expected result:* first the chapter's seven messages. After the truncation the loop stops at
that turn, because `handle` returns `not JSON` and the program treats that as *the model
answered*. The broken fragment is now the last assistant message, and in a real system it is
what the user sees. You cannot fix this by inspecting the text, because the prose answer and the
truncated proposal both fail to parse in exactly the same way — check it yourself by passing each
to `handle`. The fix is the response's finish reason, which Chapter 21 named: it says whether the
model stopped because it was done or because it ran out of tokens.

**Step 9.** Feed the dispatcher some valid JSON that is not a proposal — `[1,2,3]`, `"hello"`,
`null`, and a proposal whose `tool` is a list. Then feed it a well-formed refund proposal with an
extra key beside `tool` and `arguments`.

*Expected result:* the first four all return `not a proposal`, which is what the `isinstance`
guards are for — every one of them is valid JSON, so the `JSONDecodeError` branch never sees
them. The one with an extra top-level key *runs*, because nothing checks for unexpected keys
there; the check only covers the inside of `arguments`. That is a real gap in the validator this
chapter prints, which is why its docstring says the list is not complete. Decide whether you want
that check — and notice that you have just done the thing the chapter asks of you, which is to
read the validator rather than trust it.

**Step 10.** A colleague says their agent "has access to the database". Rewrite that sentence
accurately.

*Expected result:* their code has access to the database, and the model has a sentence describing
a function their code will run if it decides to. The rewrite matters because the first version
suggests the model holds a capability that could be taken away or misused directly, and the
second locates the capability where it is — and therefore where the limit has to go.

## Summary, Key Terms, and Review Questions

### Summary

A model emits tokens and nothing else, so "the model called an API" has compressed five steps
into one and four of them are yours: you send the **tool descriptions** as text, the model emits
a **proposal**, and your code parses it, validates it, decides, runs the function, and sends the
result back as a tool message — Chapter 18's word for it. **There are two decisions and only
one of them can refuse** — the
model decides what to propose, your code decides what runs, and the second is invisible because
it happens in code you wrote. Describing a function is a paragraph of text per function placed in
the input: 113 and 126 characters for the two here, and the model never sees the function, the
maximum length or the range. A proposal can be anything the model can emit — a tool you never
described, an argument of the wrong type, a refund of nine thousand pounds, or a sentence instead
of a proposal — and of the chapter's six, two ran and four were refused, by a registry lookup, a
range, a missing argument and a parse. **Validation cannot live in the instructions, and the
reason is mechanical**: nothing in the loop compares a proposal's values against your
instructions except your own code — a strict mode can hold a proposal to a shape, and to an
enumerated set of values, and neither of those is a limit on a number or a check against the
world — your instruction is competing with every other piece of
text in the input because nothing in the input marks one part as the instruction, and a year of compliance is
a correlation rather than a limit. **Your code is the only participant that can refuse.** And the
descriptions are input, so they are sent on every call: thirty tools is of the order of
fifteen hundred tokens before the conversation starts, which costs money on calls that need no tool and
also makes the model choose from a longer menu.

### Key Terms

| Term | Meaning |
|---|---|
| **Tool description** | The text your code sends about one function: a name, a sentence and the parameter names and types. Not the function, and not your constraints |
| **Proposal** | What the model emits — tokens your code reads as a request to run something. Nothing has happened yet |
| **Registry** | The map from a name to a function your code is willing to run. The lookup that refuses a name the model invented |
| **Dispatcher** | The code that takes a proposal, validates it, decides, and runs the function or refuses. The only participant that can refuse |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The five steps | You send · model proposes · **you validate and decide** · you run · you return |
| Who decides | The model decides what to *propose*. Your code decides what *runs* |
| Why not in the instructions | Nothing in the loop checks a proposal's *values* against them except your code. A strict mode holds a shape, and an enum; not a range, and never a fact about the world |
| What the model never sees | The function, and every constraint you kept on your side |
| Description cost | Input on every call. A real tool schema is around 200 characters, so 30 tools is of the order of 1,500 tokens |
| The refusal to send back | The specific reason, so the next proposal can be better |

### Review Questions

1. Walk me through a tool call. Who decides what runs?
2. Where does validation of a tool call belong, and why not in the instructions?
3. The model proposes a tool your code has never heard of. What happens, and what should?
4. Your agent has thirty tools and most requests use none of them. What is that costing you?
5. A colleague says the model "has access to the database". What is wrong with the sentence?

### Review Answers

1. Five steps, and the model is responsible for one. Your code sends the tool descriptions as
text along with the prompt. The model emits tokens that your code reads as a proposal — a name
and some arguments. Your code parses that, validates it, and decides whether to run it. Your
code runs the function. Your code sends the result back as a tool message, and the model's next
turn sees it as more input. **Who decides what runs is your code, always**, and the thing to say
next is why the question gets asked at all: there are two decisions sitting next to each other,
the model's about what to propose and yours about what to execute, and the second is invisible
because it happens inside code you wrote. The model has no network, no file handle and no way to
run anything; a tool call is a convention over text, which is why a proposal can also arrive as
a plain sentence.
2. In your code, and the reason is mechanical rather than stylistic. Walk the loop: step 1 is
your code sending text, step 2 is the model emitting text, and steps 3 to 5 are your code.
Nothing in that compares a proposal's *values* against what you told the model — a strict mode
can hold it to a shape, which is a different thing from a limit. An
instruction like *never refund more than £500* is input — it changes what is likely at step 2,
which is worth having — but nothing enforces it, so if your code does not check, the check does
not exist. Two more reasons worth adding. Your instruction is competing: it is text in the input
alongside the retrieved document, the user's message and the last tool result, and the whole
lot arrives as one sequence of tokens with nothing marking which part is the instruction — which is
also the mechanism behind a proposal that is there because something the model read told it to
ask, and that is Chapter 51's subject. And compliance is not a limit: a model that has obeyed for a
year has given you a correlation, and you discover what you were relying on the first time the
input is unusual. The short form is that your code is the only participant that can refuse.
3. It arrives like any other proposal, as text, and whether anything bad happens depends
entirely on your dispatcher. What *should* happen is a registry lookup that fails and a refusal
sent back naming the unknown tool. What can happen instead is the problem: a dispatcher that is
clever about names — one that falls back to a naming convention, or searches a module for a
matching function — turns the model's invented name into a lookup key into your code. The
chapter's example is `drop_table`, which was never described to the model and is extremely
plausible text, which is exactly why the model produced it. So the answer to give is the
registry: an explicit map from a name to a function you are willing to run, with the lookup
before anything else, and no path that constructs a target from the name the model supplied.
4. Two costs, and only one of them shows up on the bill. The descriptions are input and input is
sent on every call, so thirty tools at around 200 characters each — which is what a real schema
with its `type`, `properties` and `required` comes to — is roughly 6,000 characters, of the order
of 1,500 tokens, paid before the user's message is considered and including on every request that
uses no tool at all. The second cost is accuracy: the model is choosing from a
thirty-item menu, and a longer input is used less evenly than a short one. What to do about it is
a design question rather than a trick — fewer tools, a routing step, or selecting the tools for a
request — and the arithmetic is what tells you whether it is worth doing.
5. Their *code* has access to the database. The model has a sentence describing a function their
code will run if it decides to. The distinction is not pedantry, because the first version
locates a capability in the model, and if that is where you think it lives then that is where you
will try to control it — with an instruction, which cannot refuse anything. Put the capability
where it actually is, in the dispatcher, and the limit goes in the same place.

> **You understand this when** somebody says the model called an API and you can name which of
> the five steps they skipped.
