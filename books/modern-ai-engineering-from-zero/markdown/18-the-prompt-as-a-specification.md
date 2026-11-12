# The Prompt as a Specification

Part I was about what the thing is. Part II is about driving it, and this is the first
control. The chapter's claim is that a prompt is not a magic phrase you discover by rubbing
it, but a document with parts, each of which does a different job and can be changed on its
own — and that most of what makes a prompt work is not the wording at all.

*The problem.* I keep rewriting my instructions until something works, and I couldn't tell
you what I changed or why it helped.

*The question.* What is a prompt actually made of, what is the thing I am really changing
when I edit one, and how do I find out whether a change helped?

## Four Separable Parts

Chapter 2 named everything sent on a call the **context**, and split it into instructions,
added material and the request. That was the right split for understanding what a system is
*for*. For editing one the cut falls differently: the instructions turn out to be three
separate things, and the added material and the request turn out to be one — because what
matters now is not who wrote a piece but how often it changes. (Chapter 2 keeps the word
*context* for everything sent, because *prompt* is used three ways. This chapter says *prompt*
where the thing being edited is the specification, which is the third of those three and the
one a person means when they say they are writing one.) Writing and revising that
specification is what the field calls **prompt engineering**, and that is the phrase an
interviewer will use for everything in this chapter.

| Part | What it does | How often it changes |
|---|---|---|
| **Instructions** | What to do, what not to do, who to be | Rarely — it is your specification |
| **Examples** | What a good answer looks like, shown rather than described | Rarely |
| **Output format** | The shape the answer must take | Rarely |
| **Supplied information** | The request, and the material it is about | Every request |

The first three are the *specification*. They are written once, changed deliberately, and
belong in version control next to your code. The fourth is *data*, and it is different on
every call.

**Separating them matters for three concrete reasons**, and none of them is tidiness.

**You can change one and measure it.** If the instructions, the examples and the format are
tangled into one paragraph, "I changed the prompt" is all you can say about a change. If they
are separate blocks, you can change the examples and leave everything else alone — which is
the only way to find out what the examples were doing.

**You pay for the first three on every single call.** Chapter 1 did this arithmetic and
Chapter 10 gave it its unit: a page of standing instructions is a page of input tokens on
every request for the lifetime of the feature. Knowing which block is which is knowing where
your bill is.

**And three of the four are the same for every user.** That matters more than it sounds,
because a prefix that never changes is exactly the thing a provider can cache — which is
Chapter 52's lever, and it only works if the unchanging part is actually at the front.

> **Tip:** Put them in that order — instructions, examples, format, then the supplied
> information — and the stable part is at the front by construction, which is where it is
> cheapest to leave alone. Chapter 52 is what a provider will do with that, and what it takes
> to qualify.

Here is one pulled apart. The four blocks are marked; nothing else about it is special.

```text
INSTRUCTIONS
  You classify support messages. Answer with one category and
  nothing else. If none fits, answer "other".

EXAMPLES
  "my card was declined"        -> billing
  "the app crashes on startup"  -> bug
  "how do I export my data?"    -> question

OUTPUT FORMAT
  One word, lower case, from: billing, bug, question, other.

SUPPLIED INFORMATION
  "I was charged twice this month."
```

The first three are 332 characters, so eighty-odd tokens by Chapter 10's rule, and they never
change. The fourth is a line of about thirty characters, so eight or so tokens, and it changes
every time.

> **Note:** A prompt carrying examples like those three is called **few-shot**; one carrying
> none is **zero-shot**. The *shot* is an example, so the two words count the examples in the
> specification and say nothing else about it — which is worth knowing, because an interviewer
> asking whether you tried few-shot is asking whether you showed the model what a good answer
> looks like.

## The Message List

What you actually send is not one block of text. It is a list of messages, each with a role,
and the roles mean something to the model because its training put them there.

| Role | Who it is | What goes in it |
|---|---|---|
| **System** | You, the operator | The specification — instructions, usually the format, and often the examples. Set once per conversation |
| **User** | The person, or your code on their behalf | The supplied information — the request and the material it is about |
| **Assistant** | The model | What it said last time. You send its own replies back to it |
| **Tool** | Your code | The result of something the model asked for. Chapter 23 |

The classification above, as a message list:

```text
  system     You classify support messages... (instructions,
             examples and format)
  user       I was charged twice this month.
```

That is the shape, and this is roughly what goes over the wire — the same two messages, as a
client library takes them. Providers differ in the details; several carry the system text as a
field of its own rather than as an entry in the list, which changes nothing about the idea:

```json
[
  {"role": "system", "content": "You classify support messages..."},
  {"role": "user",   "content": "I was charged twice this month."}
]
```

And a second turn, after the model has answered:

```text
  system     You classify support messages...
  user       I was charged twice this month.
  assistant  billing
  user       What about "the export button does nothing"?
```

**Look at the third line of that four-message list.** The model's own previous answer is in the
input, sent by you. It did not remember saying it. Chapter 1 said the model carries nothing from
one call to the next, and this is what that looks like in practice: **the conversation is a list your
code keeps and re-sends.**

> **Note:** Where the examples go is a real choice and not a settled one. They can sit in the
> system message, or as alternating user and assistant messages that look like a conversation
> that already happened. Both are in use. The second often works better for chat-trained
> models, which is a current convention rather than a law, and the thing to do is try both and
> measure — which is the next section but one.

## Every Turn Re-Sends Everything

Now the arithmetic, because it is the thing people are most surprised by and it falls straight
out of the list above.

A **turn** is one exchange: the user's message and the model's reply to it. A conversation is
a list of them, and the list is what gets re-sent.

Take a conversation with a 200-token system message, 100-token user turns and 150-token
replies. Every turn re-sends the whole list.

```text
  turn   input   output
     1     300      150
     2     550      150
     3     800      150
     4   1,050      150
     5   1,300      150
     6   1,550      150
     7   1,800      150
     8   2,050      150
     9   2,300      150
    10   2,550      150
         ------   ------
         14,250    1,500
```

Check turn 3 by hand: 200 for the system message, three user turns at 100, two replies at 150
— `\(200 + 300 + 300 = 800\)`{=latex}. Each turn adds one user message and one reply, so each
row is 250 more than the one above it.

Two numbers to take away.

**Turn ten's input is 8.5 times turn one's** — 2,550 tokens against 300 — for a question that
is no longer and no harder.

**And the ten turns together take 14,250 input tokens**, where ten independent questions with
the same system message would take 3,000. **A conversation's input is about five times the
input of the same questions asked separately** — the replies are the same 1,500 tokens either
way, and Chapter 1 is the reminder that they are the dearer half, so the bill does not rise by
five. Nobody is being overcharged; you are re-sending a
growing document every time, because that is the only way the model can see it.

> **Warning:** This is why "it's just a chat" is a dangerous sentence in a cost estimate. The
> input of each call grows by a fixed amount per turn, so the total you pay for over
> `\(n\)`{=latex} turns grows like `\(n^2\)`{=latex} — and Chapter 15 adds
> that the attention cost inside each of those calls is growing too.

## When the History Will Not Fit

Eventually the list exceeds the window, and something has to go. Chapter 16 said this happens;
here is what to do about it, because it is your decision and not the provider's.

**Four strategies, and each loses something different.**

| Strategy | What it does | What it loses |
|---|---|---|
| Drop oldest | Remove turns from the front | Your specification, if it is in the list rather than pinned |
| Keep a window | Last `\(k\)`{=latex} turns, always | Anything established early — the specification too, unless pinned |
| Summarise | Replace old turns with a summary | Whatever the summary left out, silently |
| Start again | New conversation, carry nothing | Everything, but visibly |

The one rule that comes closest to not being a trade-off: **never drop your specification.**
That is the system message — and the example turns too, if that is where your examples live.
It is a small share of a long list, and dropping any of it changes the behaviour of everything
that follows. Pin it and truncate around it.

The one that catches people: **summarising is lossy and the loss is silent.** A summary is
itself model output, with every property Chapter 16 gave it, and nothing tells you what it
dropped. If you
summarise, you need a way to find out what was lost, which is Chapter 35's subject and not a
detail.

**Which to choose, in one line each.** The real difference between the first two is
predictability: drop-oldest keeps as much history as fits, so the input and the cost per turn
keep rising until the window is full; a fixed window of the last `\(k\)`{=latex} turns makes
the cost of a turn the same every time. So keep a window when you need a predictable bill or a
predictable latency, and drop oldest when you would rather use whatever room is going and only
lose the oldest when you must. Summarise when
early turns *do* matter and you can afford a mechanism that proves what survived, which is
Chapter 35 and is more work than it sounds. Start again when the task has changed — more often
than people admit, and the only one of the four whose loss the user can see.

> **Tip:** Decide this before you need it. A truncation strategy chosen in production at the
> moment a conversation first overflows is chosen by whoever is on call, and it is usually
> "drop oldest", which is the one that can silently delete your instructions.

## Change One Thing at a Time

The opening problem of this chapter is a process problem, and it has a process answer.

Rewriting a prompt until something works is a search with no record. You cannot say what
helped, you cannot undo the part that hurt, and you cannot tell whether the last edit did
anything at all — because one run of a prompt is one sample, which Chapter 13 made the case
for at length.

So: **change one block, keep the others fixed, and run it more than once.** That is the whole
discipline, and the four-part split is what makes it possible. "I added two examples" is a
change you can describe, repeat and reverse. "I rewrote the prompt" is not.

What this gets you is not rigour for its own sake. It is the ability to answer "why is this
prompt like this?" six months later — which is a question somebody will ask, probably you.

> **Note:** Running it more than once, and knowing how many times is enough, is Chapter 20.
> This chapter asks only that you change one thing; Chapter 20 is how you find out whether the
> change was real.

## What Current Practice Actually Weights

A last thing, and it is the one that most changes how people spend their time.

An enormous amount of writing about prompts is about *wording*: the phrasing that unlocks
better answers, the magic preamble, the role to assign. Some of it has an effect. Very little
of it has as much effect as **what information is in the request at all.**

The ordering that practitioners converge on, roughly:

1. **Is the information the model needs actually in the request?** If it is not, no wording
   fixes it — Chapter 1's point, and the reason Part II spends chapters 24 to 29 on retrieval.
2. **Is the task clearly specified, with the output shape stated?** Ambiguity costs far more
   than infelicity.
3. **Are there examples?** Showing beats describing for anything with a format or a style.
4. **Is the wording good?** Last, and a real but smaller lever.

In Chapter 6's terms that ordering is a **current convention** resting on a **practitioner
report**, and short of settled practice because Chapter 6's tell for settled practice is written-down
failure modes, and nobody has written down where this ordering stops holding — though its
first item is a derivation from Chapter 1 and needs no survey. It is also the opposite of how most
beginners allocate their afternoon.

> **Warning:** The corollary is uncomfortable. If a prompt is failing and the information it
> needs is not in the request, you can rewrite it for a week without improving it — and you
> will feel busy the whole time. The first question is always what the model was given, not
> how it was asked.

## Lab: Take a Prompt Apart

Pen and paper, then a calculator. Twenty-five minutes, and there is a key for every step.

Here is a prompt somebody wrote in one go:

```text
  You are an expert technical writer with 20 years of
  experience. Read the release note below and write a
  changelog entry. Make it concise and professional. Use the
  past tense. For example, if the note says "we fixed the
  thing where saving failed", you'd write "Fixed an error
  that prevented documents from saving." Output just the
  entry, no preamble. Release note: {note}
```

**Step 1.** Split it into the four parts. Which sentences belong to which?

*Expected result:* **Instructions** — "You are an expert technical writer…", "Read the release
note below and write a changelog entry", "Make it concise and professional", "Use the past
tense". **Examples** — the "for example" sentence. **Output format** — "Output just the entry,
no preamble". **Supplied information** — `{note}`. The format instruction is at the end and the
supplied information follows it, which is the wrong way round for caching and makes the format
easy to miss.

**Step 2.** Rewrite it as four labelled blocks in the order this chapter recommends, changing
no wording.

*Expected result:* instructions, examples, format, then the note. The point of the step is that
you changed nothing and the prompt is already better to work with: you can now see that there
is exactly one example, and that "concise and professional" may be doing no work the example is
not doing better — which is now a hypothesis you can test on its own.

**Step 3.** Write it as a message list.

*Expected result:* a system message holding the first three blocks, and a user message holding
the note. Optionally the example as a user/assistant pair instead — and if you do that, say
which version you would test first.

**Step 4.** The system message is 180 tokens. A user turn is 120 and a reply is 200. Compute
the input tokens for turns 1, 2 and 5 of a conversation.

*Expected result:* turn 1 is `\(180 + 120 = 300\)`{=latex}. Turn 2 is
`\(180 + 240 + 200 = 620\)`{=latex}. Turn 5 is `\(180 + 600 + 800 = 1{,}580\)`{=latex}. Each
turn adds 320 to the one before, which is one user message plus one reply.

**Step 5.** The window is 4,000 tokens. At which turn does this conversation stop fitting, and
what do you do?

*Expected result:* **turn 12.** The input at turn `\(k\)`{=latex} is
`\(180 + 320k - 200\)`{=latex}, so turn 12 is 3,820 — and the window counts the reply too
(Chapter 16), so a 200-token answer needs 4,020 and there is room for 180. Input alone passes
4,000 one turn later, at `\(180 + 4{,}160 - 200 = 4{,}140\)`{=latex}. The turn that stops
fitting is the one where the answer stops fitting, not the one where the question does. What to do is the four strategies, and
whichever you pick, the system message stays.

**Step 6.** The prompt opens "You are an expert technical writer with 20 years of experience".
Which of the four parts is that, where does it sit in the last section's ordering, and what
would you do with it?

*Expected result:* it is instructions — the *who to be* clause — and in the ordering it is item
4, wording. It is among the most repeated pieces of prompt advice in circulation, and it is a cheap thing
to test: delete it, run both versions several times, and see whether anything moves. The point
is not that personas never help. It is that this one costs tokens on every call, and the
question of whether it earns them is a measurement nobody on the team has taken.

**Step 7.** Someone proposes changing "concise and professional" to "clear, concise and
professional", and separately adding two more examples. What do you say?

*Expected result:* do them one at a time, and run each more than once. Also note which one you
would expect to matter: by this chapter's ordering, two more examples is a bigger lever than an
adjective. But the point of measuring is that expectations like that are sometimes wrong, and
one run of each tells you nothing either way.

**Step 8.** The prompt is failing on release notes that reference an internal project code
name the model has never heard of. What is the first thing to change?

*Expected result:* not the wording. The information is not in the request — the model cannot
know what the code name refers to, which is Chapter 1's point and no amount of rewriting
touches it. Put the code name's meaning in the supplied information, or retrieve it. This is
the chapter's last section as a concrete case, and it is the most common way a week is wasted.

## Summary, Key Terms, and Review Questions

### Summary

A prompt has four separable parts — **instructions**, **examples**, **output format** and
**supplied information** — and the first three are a specification that changes rarely while
the fourth is data that changes every call. Separating them lets you change one and measure
it, shows you where your bill is, and puts the unchanging part at the front where it can be
cached. What you send is a list of messages with roles: **system** for your specification,
**user** for the request, **assistant** for what the model said last time, and **tool** for
results your code returns. You send the model's own replies back to it, because it remembers
nothing. Every turn re-sends the whole list, so a ten-turn conversation's input is about five times
the input of the same ten questions asked separately, and turn ten's input is eight and a half
times turn one's. When the history will not fit, four strategies each lose something different — and
your specification is never the thing to drop — the system message, and the example
turns if that is where they live — while summarising loses things silently. Change
one block at a time and run it more than once, because one run is one sample. And current
practice weights what the model receives far above how the instruction is worded: if the
information is not in the request, no wording fixes it.

### Key Terms

| Term | Meaning |
|---|---|
| **Instructions** | What to do, what not to do and who to be. Part of the specification, so it changes rarely and is paid for on every call |
| **Examples** | What a good answer looks like, shown rather than described. Part of the specification |
| **Output format** | The shape the answer must take, stated rather than hoped for. Part of the specification |
| **Few-shot** | A prompt that carries examples of a good answer. The *shot* is an example, so the word counts them and says nothing else |
| **Zero-shot** | A prompt that carries no examples: instructions, output format and the request only |
| **System message** | The message holding your instructions and usually the output format. Your specification, set once per conversation and never the thing to drop when the history will not fit — nor are the example turns, if that is where your examples live |
| **User message** | The request and the material it is about, from the person or from your code on their behalf |
| **Assistant message** | What the model said earlier in the conversation, sent back to it by your code. The model does not remember saying it |
| **Tool message** | A result your code returns after the model asked for something. Chapter 23 |
| **Turn** | One exchange — the user's message and the model's reply to it. A conversation is a list of turns, and the whole list is re-sent on each one |
| **Supplied information** | The part of a prompt that is different on every call. The only one of the four parts that is data rather than specification |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The four parts | Instructions, examples, output format, supplied information |
| The order to put them in | Specification first, data last, so the unchanging part is at the front |
| Cost of a conversation | Every turn re-sends the whole list; the total over `\(n\)`{=latex} turns grows like `\(n^2\)`{=latex} |
| Worked: ten turns | 14,250 input tokens against 3,000 for ten separate questions |
| What never gets dropped | Your specification: the system message, and the example turns if that is where they live |
| What to change per experiment | One block |

### Review Questions

1. Which of a prompt's parts changes on every call, and what three things follow from that?
2. Why does your code send the model's own previous answers back to it?
3. A ten-turn conversation sends far more input than ten separate questions. Why, roughly how much more, and why is the bill not up by the same factor?
4. The history will not fit. Name the strategies and say what each loses.
5. Your prompt is not working. In what order do you try things?
6. A colleague has rewritten a prompt six times this afternoon and says the last version is best. What is wrong with that?

### Review Answers

1. **Supplied information** — the request and the material it is about. The other three parts
— instructions, examples and output format — are a specification that changes rarely; only the
fourth is data. Separating them
matters for three reasons that are not tidiness: you can change one block and measure it,
where "I changed the prompt" is not a change you can describe or reverse; you pay for the first
three on every request, so knowing which block is which is knowing where the bill is; and the
three that never change can be placed at the front, where a provider can cache them.
2. Because the model has no memory between calls — nothing of one request survives into the next. The conversation is a list your code keeps, and
the model's previous replies are in that list as *assistant* messages. What looks like memory
from the outside is entirely your code re-sending a growing document.
3. Because every turn re-sends the whole list, so the input grows by one user message and one
reply each time. With a 200-token system message, 100-token turns and 150-token replies, the
ten turns together take 14,250 input tokens where ten separate questions would take 3,000 —
about five times — and turn ten's input alone is 8.5 times turn one's. The bill is not up by
five, because the replies are the same 1,500 tokens either way and Chapter 1 says they are the
dearer half. The input total grows like the square of the number of turns, and Chapter 15 adds that the attention cost inside each call is growing
as well.
4. Drop the oldest turns, which loses whatever was established early and can lose your
instructions if they are in the list. Keep a fixed window of the last few turns, which loses
anything established before it. Summarise the old turns, which loses whatever the summary left
out — silently, because a summary is model output and nothing reports what it dropped. Or start
a new conversation, which loses everything but does so visibly. Your specification is never
dropped — the system message, and the example turns if that is where your examples live. Pin
them and truncate around them.
5. First, is the information the model needs actually in the request — because if it is not,
no wording will fix it. Then, is the task clearly specified with the output shape stated.
Then, are there examples, since showing beats describing for anything with a format. And last,
the wording, which is a real lever and a smaller one. In Chapter 6's terms that ordering is a current
convention resting on a practitioner report — except its first item, which is a derivation from
Chapter 1 — and it is the reverse of how most people spend the afternoon.
6. They have run a search with no record. They cannot say which change helped, cannot reverse
the one that hurt, and — because each version was run once — cannot tell whether any of the
differences they saw were real rather than the ordinary variation between two samples. The fix
is to change one block at a time and run each version more than once. Chapter 20 is how many
times is enough.

> **You understand this when** you can take somebody else's prompt, split it into four blocks
> without changing a word, and say which block you would change first and why.
