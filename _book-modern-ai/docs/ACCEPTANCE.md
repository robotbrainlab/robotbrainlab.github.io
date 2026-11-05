# The acceptance questions

The standard each chapter has to meet. **Written before any chapter is drafted**, which is the
whole of why it works.

## Why the order matters more than the content

A question written **after** a chapter can only ask about what the chapter happens to contain. It
cannot test whether anything is missing, because it was derived from what is there. A question
written **before** the chapter is a requirement the chapter has to satisfy.

So: these are written at step 9 of `ROADMAP.md`, from `PLAN.md`'s subjects, **before step 11
drafts anything.** A question added later is marked `late:` and is understood to be weaker, for
exactly this reason.

## What a question is

**A question a competent person would ask you about this subject, which you should be able to
answer out loud in about a minute.** Not a quiz item, not a definition prompt, not a recall check.

| Not this | This |
|---|---|
| "What is X?" | "Why would you use X rather than Y, and what does it cost you?" |
| "List the three types of X" | "You have measured an improvement of 3%. How do you know it is real?" |
| "Define X" | "Walk me through something you built with X, and tell me the numbers you got" |
| "When was X introduced?" | "What is still unsettled about X, and what would settle it?" |

**One question per row, keyed to the chapter that must answer it.**

## The acceptance rule

> **A chapter is not finished until each of its questions can be answered from the chapter
> alone — or until a question is answered by a dispute record that says the answer is not
> settled, and says so explicitly.**

That second clause is the change this book needs and a settled-subject book does not. For a
disputed subject the honest answer is *"this is contested, here is the state of the dispute, and
here is what would settle it."* **That is a real answer and the rule accepts it**, as long as the
chapter says plainly that it is answering that way. What the rule does not accept is silence
dressed as completeness.

## How a chapter is tested against them

At close, in the record:

1. Find every question keyed to this chapter.
2. **Answer each one out of the chapter alone**, with nothing else open.
3. For each: `answered` · `answered-as-disputed` · `cannot`.
4. **A `cannot` means the chapter is short of something.** Reopen it, or move the question and say
   why in the record. Those are the only two options — a question is never quietly deleted.

`tools/verify-bank.py` checks the bookkeeping: that every question has an owner, that no question has
two, and that every written chapter's record names its questions.

## Deliberate exemptions

Some chapters carry no question, on purpose. Each needs a row here saying why, or
`tools/verify-bank.py` fails. The two reasons that qualify:

- **The chapter is about the book's own arrangement** — nobody asks about that.
- **The chapter's subject is tested through another chapter's questions**, named here.

Anything else is a chapter that should have a question and does not.

## The questions

| # | Question | Chapter | State |
|---|---|---|---|
| — | *Empty. Written at step 9, from `PLAN.md`, before any chapter is drafted.* | — | — |

## Exemptions

| Chapter | Why it carries no question |
|---|---|
| — | *Empty.* |

## How many

**No target.** A question exists because somebody would ask it, not to reach a count. A chapter
with two good questions is better served than one with six weak ones.

**But a chapter with none, and no exemption row, is a chapter nobody would ask about** — which is
a finding about the chapter, not about the bank.
