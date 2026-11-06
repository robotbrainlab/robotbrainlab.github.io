# Pass 3 — run the lab from the chapter text alone

Fill in `<CHAPTER>`, `<FRESH-FOLDER>`, `<LAB-FORM>` (`construct` or `reproduce`, from the chapter's
row in `../PLAN.md`), and `<HARDWARE-AVAILABLE>`.

**What this pass is for.** The book promises a lab is reproducible from its own text. A writer who
runs their own lab cannot test that promise, because they know what they meant. This agent knows
only what the chapter says.

---

> Copy everything below this line into the agent.

---

**QUESTION**

Can this lab be run, to a verdict, by someone who has only the chapter?

**YOUR JOB**

Read the lab section of `<CHAPTER>` and **run it**, in `<FRESH-FOLDER>`, using only what the chapter
tells you. Then report what happened — including, and especially, everything the chapter failed to
tell you.

**WHICH KIND OF LAB THIS IS: `<LAB-FORM>`**

The two forms are judged differently and the chapter's row says which this is.

| Form | What the chapter should give you | What a verdict is |
|---|---|---|
| **`construct`** | A thing to build, a procedure, and the measurement it should yield | **Your measurement, beside the chapter's.** They may differ; say by how much |
| **`reproduce`** | A published claim, a procedure, and a **decision rule** — what counts as reproducing | **Reproduced, not reproduced, or inconclusive**, by the chapter's own decision rule |

**For a `reproduce` lab, the verdict does not have to agree with the published claim.** A lab that
comes out against the paper is a working lab. If you find yourself adjusting anything to make the
numbers agree, stop — that is the one failure this pass exists to prevent.

**WHAT THE CHAPTER WAS REQUIRED TO GIVE YOU**

You are testing a promise, so here is the promise. The specification requires every lab to:

- **ship its own data**, in a directory the chapter names. No lab may say "use your own files";
- **pin every version**, and pin any model to a dated snapshot;
- **print the identifier that came back** beside any figure that depends on it;
- **state the hardware it needs**, and where the full experiment needs more than the reader is
  likely to have, give a reduced version that fits — or say plainly that there is none;
- **never promise exact output from a stochastic system.** It may say what shape the output takes,
  which assertion must pass, or give a range;
- **take any credential from the environment.** Never from a file, and never printed or logged;
- **declare what the book planted** in data it built itself — every property put there
  deliberately, so no lab can report as a discovery something the data was built to contain.

**Each of these is a thing to check.** A lab that breaks one of them is a finding even if it runs.

**THE RULES**

1. **Use only the chapter.** Do not read another file in the project, do not search the web for a
   missing step, and do not use what you already know to supply one. **If the chapter does not say
   it, that is a finding.**
2. **You may make one attempt to continue past a gap**, so that the run reaches as far as it can —
   and **the gap is still the finding**. Record what was missing and what you did instead. **If one
   attempt does not get you past it, stop and report.** Do not engineer your way through.
3. **Work in `<FRESH-FOLDER>` only.** Create it. Write nothing outside it. Read nothing outside it
   except the data directory the chapter names.
4. **Never read, write, print, log or commit a credential.** If the lab needs a key, take it from
   the environment. If none is there, stop and report that.
5. **Run every command as printed.** Never correct one silently. If a command fails, record the
   failure, then record what you changed — that change is a finding.

**OUTPUT**

```
## Did it run
Yes or no. If no, the exact point of failure and the exact error.

## What the chapter did not tell me
Every gap: a step assumed, a value unstated, a file unnamed, a version unpinned,
an ordering unclear, a decision rule missing. For each: what was missing, and
what you did instead. THIS IS THE MOST IMPORTANT SECTION — it is the one
nobody else can produce.

## Promises kept and broken
One line for each of the seven requirements above: kept, broken, or not applicable.
Quote the chapter where it is broken.

## The numbers I got
Every measurement the lab asks for, as it came out. Do not round to match the
chapter. Where a figure differs from the chapter's, report both.

## The verdict
For a construct lab: my measurement beside the chapter's.
For a reproduce lab: reproduced, not reproduced, or inconclusive, by the
chapter's own decision rule — and quote the rule you applied.

## Hardware
What I ran it on, against what the chapter said it needs.
If the chapter's requirement exceeds <HARDWARE-AVAILABLE>: say so, run the
reduced version if the chapter offers one, and report whether that worked. If
the chapter offers none, that is the result — report it and do not
substitute a smaller experiment of your own.

## Time
How long it took, end to end. If the chapter states an expected effort,
say whether that held. If it states none, report the time and say nothing
about whether it should have been faster.

## Coverage
What you ran, what you skipped, and why.
```

**BUDGET**

One run of the lab end to end, plus at most one retry of any single step, plus the one gap attempt
allowed by rule 2. **No web searches.**

**TARGET**

One verdict. That is the whole deliverable.

**PARTIAL**

A lab that did not finish is a complete and useful result **provided you say exactly where it
stopped and why.** Report the gap rather than engineering around it.

**FORBIDDEN**

- **Using knowledge the chapter did not give you** to supply a missing step.
- **Correcting a command silently.**
- **Rounding a number to match the chapter's**, or adjusting anything to make a `reproduce` lab
  agree with its claim.
- **Reading or writing anything outside the fresh folder and the data directory the chapter names.**
- **Touching any credential.**
- **Substituting a smaller experiment of your own** when the hardware is not available. Report it.

**STOPPING RULE**

Stop when the lab has reached a verdict, **or** when a gap has stopped you and you have recorded it.
One retry per step and one attempt per gap, then stop.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent.
