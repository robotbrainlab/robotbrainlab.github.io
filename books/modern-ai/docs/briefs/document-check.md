# Document check

**The one instrument that reads what Claude writes.** Every other brief here checks an agent, and
every gate checks a chapter. **Nothing read the governance prose** — the assessments, validations,
diagnoses and roadmap edits — until `../POSTMORTEM-2026-11-11.md` found five errors in it, spanning
three classes this project had already recorded. **The newest of the three was written down the day
before it was broken**, so the rules had not faded; nothing read the prose they govern.

**Why it is a separate agent.** It is the same rule this project applies everywhere else: *report,
then consolidate — two agents, never one*, and *a reporter that filters cannot be checked*
(`README.md`). The author of a document cannot check it, because the reasoning that produced the
error is the reasoning that would review it. **This run is given the document and the files it
cites, and none of the reasoning behind it**, on purpose.

**What it is not.** It is not a reviewer of quality, style, structure or whether the argument is
good. **It answers three mechanical questions**, and anything outside them is out of scope — a
longer remit would make it a second author.

## How to fill this in

Replace `<DOCUMENT>` and `<CITED-FILES>`. **Change nothing else.**

- **`<DOCUMENT>`** is the absolute path of the one document to check.
- **`<CITED-FILES>`** is the absolute path of every file it cites, **including the ones it cites by
  section**. Give the whole file, never the section: the run has to be able to see that a cited
  section says something other than what cites it, and a section handed to it in isolation cannot
  show that.

**Run it before a document is called finished** (`../POSTMORTEM-2026-11-11.md` §5), and again after
any change to a rule.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Does this document say things its own cited sources do not support, contradict decisions recorded
elsewhere, or generalise beyond the evidence it names?

**WHAT TO DO**

Read `<DOCUMENT>` in full. Then read every file in `<CITED-FILES>` in full. Then report **three
things and nothing else.**

1. **Citations that do not support the sentence citing them.** For every citation in the document —
   a file, a file and section, or a named rule — **open the cited place and read what is there.**
   Report it when the cited text does not support the claim, when it supports a weaker claim, when
   it says the opposite, or when it has been superseded or retracted by a later statement in the
   same file. **Quote the citing sentence and the cited text side by side.** A citation that is
   simply correct is not reported.

   **Watch for the stale citation in particular**: a citation that was true when written and became
   false when the cited section changed. It is invisible to the author, because the citation is
   what makes the sentence look settled.

2. **Statements that contradict a marked decision.** Several of these files mark statements
   `[STATED]`, `[AGREED]`, `[I RECOMMEND]`, `[OPEN]` or `[DEFAULTED]`. **Report every statement in
   the document that conflicts with a marked statement in a cited file** — quoting both, with the
   marker and the date of the marked one. **`[STATED]` and `[AGREED]` matter most**: those are the
   owner's, and a document that contradicts one is overriding him in prose.

   **Do not report a difference in wording.** Report a difference in what is claimed.

3. **Claims that generalise past their evidence.** A claim about what always happens, what a method
   does, what a class of thing is like, or what cannot be done, **where the document itself names
   fewer instances than the claim covers.** Report the claim, the number of instances it actually
   names, and what it would take to support it. **"Two runs did X" does not support "the method does
   X."**

**OUTPUT**

```
## Citations that do not hold
One entry each: the citing sentence quoted; the cited text quoted; the file
and section it was read in; and which of the four cases it is — unsupported,
weaker, opposite, or superseded. "None found" if none.

## Contradictions with a marked decision
One entry each: the document's sentence quoted; the marked statement quoted,
with its marker and date and where it is; and one line on what is actually in
conflict. "None found" if none.

## Claims past their evidence
One entry each: the claim quoted; how many instances the document names; and
what would support it. "None found" if none.

## What I could not check
Every citation you could not resolve, and why. Every file in the list you
could not read in full, and how much of it you read. Any project file in your
context that was not given to you, named, with what it told you.
```

**Return this report. Write no file.**

**TARGET**

**Three lists, and nothing else.** There is no target number of findings, and **"None found" on all
three is a real and expected result** — say it plainly rather than manufacturing a finding to look
useful.

**BUDGET**

No searches and no fetches. **You add no evidence.** The document and its cited files are everything.
A citation to something outside them — a web page, a paper — is reported under *What I could not
check*, not chased.

**FORBIDDEN**

- **Substituting a search, a pattern, a count or a lookup for reading.** You read and you judge.
  **A pattern match tells you where a string is; it cannot tell you what the thing means**, and
  every question in this brief is about meaning. Where you do run a search or a count, it is a
  **hint about where to read** and never the finding itself. **A citation is checked by opening the
  cited place, never by matching the section number.**
- **Reviewing the document's quality, style, structure, length or usefulness.** Three questions,
  nothing else. A good argument with a bad citation is a finding; a weak argument with sound
  citations is not.
- **Proposing rewrites, fixes or better wording.** You report what does not hold. What to do about
  it belongs to the author and the owner.
- **Judging whether a decision is right.** A marked decision is the owner's. Your job is to report
  that the document contradicts it, never to say which of them should win.
- **Accepting a citation because it looks authoritative.** A section number beside a claim is the
  most persuasive thing in these documents and the easiest to be wrong.

**PARTIAL**

If you cannot read every cited file in full, report the findings you have and **name every file you
did not finish, with how far you got.** A partial check that says where it stopped is a result. One
that does not is worse than none, because it will be read as a clean bill.

**STOPPING RULE**

Stop when every citation in the document has been resolved or reported as unresolvable, every cited
file has been read in full or reported as unfinished, and the three lists are written. **There is
nothing to search for, so there is no reason to continue past that point.**

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
citation you flag wrongly costs one reading. A citation you pass wrongly becomes the authority for
the next document, and the one after that.

**DELEGATION: ZERO.** Do not start any sub-agent.
