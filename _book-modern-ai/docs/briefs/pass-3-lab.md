# Pass 3 — run the lab from the chapter text alone

Fill in `<CHAPTER>` and `<FRESH-FOLDER>`.

**What this pass is for.** The book promises that a lab is reproducible from the text. A writer who
runs their own lab cannot test that promise, because they know what they meant. This agent knows
only what the chapter says.

---

> Copy everything below this line into the agent.

---

**YOUR JOB**

Read the lab section of `<CHAPTER>` and **run it**, in `<FRESH-FOLDER>`, using **only what the
chapter tells you.** Then report what happened.

**THE RULES, AND THE FIRST ONE IS THE POINT**

1. **Use only the chapter.** Do not look at any other file in the project, do not search the web
   for the missing step, and do not use what you already know to fill a gap. **If the chapter does
   not say it, that is a finding — not a problem for you to solve.**
2. **Work in `<FRESH-FOLDER>` only.** Create it. Write nothing outside it. Read nothing outside it
   except files the chapter explicitly tells you to read.
3. **Never read, write, print, log or commit a credential.** If the lab needs a key, take it from
   the environment. If no key is there, stop and report that.
4. **Run every command as printed.** Do not correct a command silently. If a command fails, record
   it, then record what you had to change to make it work — that change is a finding.

**WHAT TO REPORT, AND THE VERDICT IS NOT "DID IT AGREE"**

A reproduction lab states a published claim, a procedure and a **decision rule** — what counts as
reproducing. **The lab passes if it runs and yields a verdict. It does not have to agree with the
claim.** A lab that comes out against the paper is a working lab.

So report, in this order:

```
## Did it run
Yes or no. If no, the exact point of failure and the exact error.

## What the chapter did not tell me
Every gap: a step assumed, a value unstated, a file unnamed, a version unpinned,
an ordering unclear. For each, say what you did instead. THIS IS THE MOST
IMPORTANT SECTION.

## The numbers I got
Every measurement the lab asks for, as it came out. Do not round to match the
chapter. If a figure differs from the chapter's, report both.

## The verdict
What the decision rule says, applied to the numbers I got. Reproduced, not
reproduced, or inconclusive — and which.

## Hardware
What I ran it on. Whether the chapter's stated hardware requirement was right.
If the chapter offered a no-hardware version, whether that version worked.

## Time
How long it took, end to end. The chapter claims it is a day's work or less;
say whether that is true.
```

**BUDGET**

One run of the lab end to end, plus at most **one** retry of any single step. No web searches: if
the chapter does not tell you something, that is the finding.

**TARGET**

One verdict. That is the whole deliverable.

**PARTIAL**

A lab that did not finish is a complete and useful result **provided you say exactly where it
stopped and why.** Report the gap rather than engineering around it.

**FORBIDDEN**

- **Using knowledge the chapter did not give you** to fill a gap.
- **Correcting a command silently.** Record the failure, then record what you changed.
- **Rounding a number to match the chapter's.** Report both.
- **Reading or writing anything outside the fresh folder and the data the chapter names.**
- **Touching any credential.** Keys come from the environment; if none is there, stop and say so.

**STOPPING RULE**

Stop when the lab has run to a verdict, **or** when a gap stops you and you have recorded it. **One
attempt at working around a gap, then record it and move on.**

**DELEGATION: ZERO.** Do not start any sub-agent.
