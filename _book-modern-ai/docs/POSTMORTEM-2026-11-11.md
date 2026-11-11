# Why the same mistakes recur — root cause, and the mechanism that was missing

**Written 2026-11-11, at the owner's instruction**, after he pointed out that the same failures keep
appearing although the rules that forbid them are written down. **He is right, and the rules being
written down is the finding, not the defence.**

**Method.** I opened `GOAL.md` §11, `PROCESS.md` §1, `GATES.md`'s "What no gate reads",
`briefs/README.md`, `briefs/TEMPLATE-area-consolidate.md`, `ROADMAP.md` and `GOAL.md` §3.3, and
tested each of my own errors of 2026-11-07 against them.

**Then `briefs/document-check.md` — the mechanism this document proposes — was run over this
document, and it found seven defects in it, one of them in the central section.** Everything below
is the corrected version; §7 records what the check caught and what that implies. **The first draft
of this analysis contained an error of the same class it was written to explain.**

---

## 1. The finding, in one line

**Every one of my errors is an instance of a class this project recorded weeks ago, with the
practice already written beside it. Not one of those classes has a mechanism that reads what I
write.**

| My error | The class, already recorded | Where the error lives |
|---|---|---|
| Said a standards body had defeated every run, while one run's five records sat in this repository — **contradicting V11 in the same file** | **A — claiming without reading** | `VALIDATION-2026-11-07.md` |
| Declared "the method does not converge" a property of the method, from two runs | **D — stating a claim above the strength of its evidence** | `VALIDATION-2026-11-07.md` |
| Told the owner the area cut was his; then, challenged, told him it was not and that I had been wrong — **when §3.3's own table says it is his.** The correction was the error | **A — claiming without reading**, committed on a section I had opened. I read §3.3's first forty lines and stopped above the table that settles it | Four turns of conversation, a `ROADMAP.md` edit, and §2.2 of this document as first written |
| Set a floor of 10 benchmark areas by adding two tables' rows, double-counting the three in both | **H — assessing a thing with an instrument that does not sample it** | `CHECK-run-g-2026-11-07.md` |
| Passed run `g` on coverage and floors without asking whose words its scope statements were | **H again** — my check sampled completeness, never provenance | §7 of `DIAGNOSIS-2026-11-07.md` |

**Five errors. Four classes, all written down before any of them happened. Zero mechanisms that
could have caught any of them** — because all five live in prose, and nothing in this project reads
prose I write.

**`GOAL.md` was committed on 2026-11-06**, the day before the errors. So the classes were not
written long ago and forgotten; **they were written the day before, and broken the next day.** That
is worse for me and better as evidence: it rules out the explanation that the rules had faded.

## 2. The root cause

`PROCESS.md` §1 states the principle this project is built on:

> **Convert care into mechanism.** … **Care does not survive a project that never ends.** Every rule
> in this document that could have been written as "be careful about X" is instead a script that
> refuses, a file a gate reads, or a brief that cannot be answered the wrong way.

**That principle has been applied to everything except me.** Every mechanism built so far binds one
of exactly two things:

| What is bound | By what | What it gets |
|---|---|---|
| **An agent** | One of eight briefs | A budget, a stopping rule, a forbidden list, an output shape, a statement of what one unit is, `DELEGATION: ZERO` |
| **A chapter** | Fourteen gates, four review passes, `CLAIMS.tsv`, `records/` | A script that refuses, a reviewer that reads it, a row that must carry a basis |

**The prose I write is neither.** `VALIDATION-…md`, `DIAGNOSIS-…md`, the edits to `ROADMAP.md`,
and the assessments I give in conversation: no gate reads them, no pass reviews them, no brief
constrains them, and no record requires anything of them. `briefs/README.md` says it plainly of the
one adjacent case — **"The writer has no brief here"** — and that is true of far more than chapter
writing.

**So the agents on this project are better governed than I am.** They cannot run past a budget,
cannot skip an output field, cannot delegate, and must state what they could not reach. I can write
a six-hundred-line assessment with no budget, no required fields, no stopping rule, and nothing that
reads it before the owner does. **That asymmetry is the root cause, and it is not a character
problem; it is the one place the project's own design principle was never applied.**

### 2.1 Why the written classes did not stop it

**They are in the wrong file to fire at the moment they are needed.** `../CLAUDE.md` is read first
and in full every session. Its section "Before claiming anything about a file" surfaces **three**
classes: A, H and M. The classes I broke on 2026-11-07 were **A, C, D and H**. So **C and D — two of
the four — are not in the document that is read at the start of every session.** They sit in
`GOAL.md` §11, a long section of a long file, read when a step calls for it and then reasoned from
memory.

**And the one I broke most often has no trigger I would recognise.** Class A's practice reads:
*"Before any claim about what a file, directory or document contains or omits, open it."* **"The
owner decides the area list" does not look like a claim about a file.** It is one. The trigger is
written in terms of contents and omissions, so claims about *who decides*, *what was agreed* and
*what the method is* slip past it — and those are precisely the claims that governance prose is made
of.

### 2.2 The biggest failure, traced end to end — **and this section was itself wrong**

**This section first claimed that a brief cited `GOAL.md` §3.3 for a proposition §3.3 retracts, and
that my error was inherited from a stale citation. That claim was false, and the first run of
`briefs/document-check.md` caught it.** What follows is the corrected account, which is worse.

1. `briefs/TEMPLATE-area-consolidate.md` states: *"A judgement that an area is small, quiet,
   unpromising or not worth the owner's time is **the owner's and nobody else's** (`../GOAL.md`
   §3.3)."*
2. I read that line, did not open §3.3, and told the owner four times that cutting the area list was
   his.
3. He challenged it: *"Why me?"*
4. **I then opened §3.3 — and stopped forty lines in.** What I read there is real: *"I previously
   concluded … that the owner must author the area list. **That does not follow**, and he rejected it
   more than once before I accepted it."* I took that to settle the question, told him *"It isn't
   you, and I was wrong to keep saying it was"*, rewrote this section around a false citation, and
   changed the brief.
5. **Forty lines further down, §3.3 carries its own division-of-labour table**, and it says:

   > | **A consolidation run** | … **It may reject a category for not being an area; never for being
   > unimportant.** |
   > | **The owner** | **Approves, redraws or rejects the proposed list, with the evidence for each
   > boundary in front of him**, and the reasons are recorded with it |

**So the brief's citation holds. §3.3 retracts that the owner must *author* the list — originate it
from nothing — and in the same breath assigns him approval, redrawing and rejection of the list once
it is proposed.** Those are different acts, and the section says why the distinction is the point:
*"Step 4 was the only place he was asked to originate content from nothing, and that inconsistency
was the signal that the step was wrong rather than hard."* Nobody is asking him to originate
anything. The list exists. **Ruling on it, including rejecting an entry as not worth his time, is
his, and §3.3 says so.**

**Three statements, each more confident than the last, and the middle one is where it went wrong.**
The first was right. The correction was wrong. The analysis of the correction was wrong and was
being written into the governance files when the check stopped it.

**The class is A, and class A already names this exact failure mode**: *"having the summary is worse
than having nothing, because nothing makes you look."* **A partially-read section behaves like a
summary and is more dangerous than one**, because it is quotable. I quoted §3.3 accurately and
represented it falsely, and the quotation is what made it persuasive — to him, and to me.

**What this changes about the advice he has been given.** Cutting the 63 areas *is* his, as I first
said. What is not his is authoring a partition from nothing, which was never asked of him. The
five-questions pass I proposed — applying `GOAL.md` §1.1 and §3.1 to the list — is a legitimate way
to *propose* a cut, and it does not move the ruling off him. **Both halves are true and I presented
them as alternatives.**

### 2.3 A demonstration, committed by me, in the same session

On 2026-11-07 I changed the framing stage from two runs to one. I updated the brief, `ROADMAP.md`,
`PROCESS.md` and `GOAL.md`. Then I ran this to prove the sweep was complete:

```
grep -rn 'two framing runs\|Run this brief twice\|framing runs record' docs/ research/
```

and reported "**no output above = clean**".

**Three files still carried the old rule.** Opening them today, rather than grepping, found:

| File | What it still said | Why the grep missed it |
|---|---|---|
| `briefs/README.md` line 10 | the framer runs "**twice per cycle**" | A fourth phrasing I did not think of |
| `PROCESS.md` §8, the agent table | Framer: "**Two runs**" | **Four lines above a bullet I edited in that same section on that same day.** I changed the coordination note and left the table row |
| `ROADMAP.md` step 4 part 3 | the owner rules "with … **the two runs' disagreements** beside it" | A fifth phrasing, and the clause that mattered most — it describes the evidence he was to rule with |

**That is class M — using a pattern match to answer a question about meaning — committed by me, in
the same session in which I wrote into two briefs that a pattern match can never answer a question
about meaning.** It is the clearest evidence in this document that writing a rule down does not
install it.

**And note which one the grep's failure cost most.** The `ROADMAP.md` clause told the owner he would
rule with two runs' disagreements in front of him. There is now one run per cycle, so that evidence
does not exist — and nothing would have told him until he sat down to rule and found it missing.
**The replacement is named there now**: the register's recorded floor, plus the consolidation run's
own `UNCLEAR` list, close rejections, thin merges and areas kept on thin scope.

## 3. What the audit found in the files

Three defects, all now fixed except the one that is the owner's to rule on.

| # | Defect | Where | Status |
|---|---|---|---|
| 1 | **No defect. I reported one that did not exist** (§2.2 above) — the brief's citation to §3.3 holds | `briefs/TEMPLATE-area-consolidate.md` | **Changed this morning on a false premise and changed back.** The brief now carries a note saying the citation holds and not to re-apply the change |
| 2 | **A stale rule surviving a four-file change** (§2.3 above) | `briefs/README.md` line 10, `PROCESS.md` §8's agent table, `ROADMAP.md` step 4 part 3 — **three files, not one** | **All three fixed**, and the roadmap one names what replaces the evidence it promised |
| 3 | **A question the owner should settle** | `ROADMAP.md` step 4 part 4 used to say that turning approved categories into each scout's scope is the owner's "and it is not Claude's", undated and unmarked. §3.3's reasoning about originating content from nothing may or may not reach that step — **writing a scope from an approved list is not originating from nothing**, so this is weaker than I first put it | **Marked `[OPEN 2026-11-11]`, and the clause reworded to "Somebody".** The marking is the right outcome; my reason for it was overstated |
| 4 | **Two contradictory counts of one measurement, in one file** | `VALIDATION-2026-11-07.md` said "Today's 16 findings … 3 of them" in its cost inventory and "21 findings … four" in its final assessment, of the same quantity | **Fixed to 21 and 4**, which match the file's own V1–V21. Found by the document check, not by me |

**One thing I am not claiming.** `ROADMAP.md` step 4's table says "Claude proposes · **Owner
rules**", and that is *not* in conflict with §3.3: ruling on a list is not authoring one. **My error
was reading "rules on" as "authors", not a contradiction in the documents.** Saying otherwise would
be stating a claim above its evidence inside a document about stating claims above their evidence.

## 4. The mechanisms

**Four changes. One is a mechanism; three are rules placed in the one file that is always read.**
Nothing is duplicated across files, because a second statement of a rule is a defect
(`../CLAUDE.md`, precedence).

### 4.1 The mechanism — a document check, run by an agent that has not seen my reasoning

`briefs/document-check.md`. **This is the only item here that is a mechanism rather than an
intention**, and it is the project's own best idea turned on its author: *report, then consolidate —
two agents, never one*, and *a reporter that filters cannot be checked.* Through 2026-11-07 the
agents were checked by me and **I was checked by nobody.**

It takes one document I have written and the files it cites, and reports three things only:

1. **Every citation that does not support the sentence citing it** — it opens the cited section and
   quotes what is actually there.
2. **Every statement that contradicts a marked statement elsewhere**, quoting both with their
   markers and dates.
3. **Every general claim whose evidence is fewer instances than it generalises over**, with the
   count it found.

It gets no access to my reasoning, because reasoning is what it exists to not be persuaded by.

### 4.2 Three rules, all in `../CLAUDE.md`, section "Before claiming anything about a file"

That section already exists and already surfaces classes A, H and M. It gains:

- **The citation rule.** A citation is opened at the time of writing, not inherited. **Citing a
  marked statement means quoting its marker and its date.** A citation that was true when written
  is not evidence that it is true now.
- **The change-propagation rule.** A rule change is not finished until every file that states or
  cites it has been **opened**. The set is small and nameable — `CLAUDE.md`, `GOAL.md`, `GUIDE.md`,
  `PROCESS.md`, `GATES.md`, `ROADMAP.md`, `briefs/README.md`, the briefs — and **a grep is not a
  sweep**, because it finds the phrasings you thought of.
- **Classes C and D, in one line each**, so that all four classes that fire while writing prose are
  in the file that is read first. `GOAL.md` §11 keeps the full text and stays their owner.

### 4.3 One row in `GATES.md`, "What no gate reads"

That table exists on a stated principle: *"a rule whose enforcement is assumed is worse than one
known to rest on care: the first is believed, the second is watched."* **It lists four rules — three about a
chapter, one about whoever runs `git` — and omits this entire corpus.** It gains a row saying that no gate, pass or record reads any document
in `docs/`, and that the document check is the only thing that does.

## 5. What to check before any document here is called finished

1. **Every citation in it opened**, and every marked statement quoted with its marker and date.
2. **Every general claim counted** — the number of instances stated beside the claim, in the
   sentence that makes it.
3. **`briefs/document-check.md` run over it**, and its three findings answered in the document or
   recorded as accepted.
4. **If the document changes a rule:** every file in §4.2's list opened, not grepped.

## 6. What this does not fix, said plainly

**A check does not make me careful, and this one can be wrong too.** What it changes is that one
class of error becomes visible *before* the owner reads it rather than after, and that a stale
citation can be found by something other than him noticing.

**It also does not touch the three classes with no mechanism anywhere.** `GOAL.md` §11's own table
offers mechanisms for ten of thirteen, which leaves **B** (answering an adjacent question), **E**
(rebuilding from the last correction) and **F** (private shorthand). F is stated as a style rule in
`../CLAUDE.md`, which is an intention, not a mechanism. All three need a reader, and I am naming them
rather than claiming coverage I do not have. **I wrote "two" here until the check counted.**

**The test is a number, not a promise.** On 2026-11-06 there were 43 findings, 31 of them created by
the fix rounds themselves. On 2026-11-07, 21, from running the instruments. **The measurement that
matters is how many of the next document's findings are caught by §5 before the owner sees it.** If
that number is zero again, the mechanism is theatre and should be removed rather than extended.

---

## 7. The check was run over this document, and it worked

**First use of `briefs/document-check.md`, on the document that proposes it.** It was given this
analysis and the ten files it cites, and none of my reasoning. **It found seven defects.**

| # | What it found | Verdict after I checked it at source |
|---|---|---|
| 1 | **§2.2's central claim is false.** §3.3 retracts that the owner must *author* the list; the brief's line is about *rejecting* an entry on a proposed list, which §3.3's own table assigns to him | **Correct, and it is the finding of the day.** §2.2 is rewritten and the brief is changed back |
| 2 | "Five errors, five classes" — the document names **four** classes across five errors | **Correct.** Fixed |
| 3 | `GATES.md`'s pre-existing rows are not "four chapter rules" — one is the committer's | **Correct.** Fixed |
| 4 | **Three** classes lack a mechanism, not two: B, E and **F** | **Correct.** `GOAL.md` §11's table offers mechanisms for ten of thirteen. Fixed |
| 5 | "recorded weeks ago" is unsupported; the corpus dates run 2026-11-03 to 2026-11-11 | **Correct.** `GOAL.md` was committed 2026-11-06 — **the day before the errors.** Fixed, and it makes the finding worse |
| 6 | Four passages describe the pre-fix state in the present tense while §3 and §4 call them fixed | **Correct.** Fixed |
| 7 | `VALIDATION-2026-11-07.md` states the same measurement twice with different numbers — "16 … 3" and "21 … four" | **Correct, and it is a defect in a file the owner has already read.** Fixed to 21 and 4 |

**Six of the seven are mine. The seventh is a defect in an earlier document that four days of
re-reading had not found.**

### What this demonstrates, and what it does not

**It demonstrates the root cause rather than arguing it.** This document was written *about* the
failure to read what is cited, by the person who had just committed it, with the classes open in
front of me — **and it repeated the same class, in its own central section, as part of correcting an
earlier instance of it.** No amount of care would have caught that, because care is what produced
it: I was being careful, and I was confidently wrong twice in a row. **That is precisely the case
`PROCESS.md` §1 is about** — *care does not survive a project that never ends* — and it is why the
answer had to be a mechanism and could not be another rule.

**It also shows the specific shape of the danger.** My error was not failing to read §3.3. I read
it, quoted it accurately, and stopped forty lines above the table that settles the question. **A
partially-read section is more dangerous than an unread one**, exactly as class A says of summaries:
it is quotable, so it persuades the reader and the writer at once.

**What it does not demonstrate.** One run is not a track record, and the check can be wrong — it
also has no access to anything outside the files it is handed, so everything in §6 stays true.
**The measurement stands as stated there:** the number that matters is how many defects it catches
in the next document before the owner sees it. This time the number is seven, and the owner saw
none of them.

### The one thing the owner needs from this

**My advice about the area list was right the first time and wrong when I corrected it.** Cutting
the 63 is his — §3.3 gives him "approves, redraws or rejects the proposed list, with the evidence
for each boundary in front of him". **What is not his, and was never asked of him, is authoring a
partition from nothing.** The five-questions pass can *propose* a cut; it does not move the ruling.
I presented these as alternatives and they are not.
