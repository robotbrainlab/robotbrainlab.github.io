# Subject selection brief

**The SELECT stage.** It takes every subject the scouts recorded and sorts it into `CHAPTER`,
`SHORT-ENTRY` or `REJECT`, so the owner can rule. It runs **after** the research files exist and
**before** `PLAN.md` is written (`../PROCESS.md` §5).

**Claude runs this in the main session. It is not delegated** — test 1 is judgement against the
owner's purpose. **That is a reason not to delegate it, not a reason to leave it unbounded.**

## Why this brief exists

**`[2026-11-11]` Three independent reviews found this stage unbriefed, and the project's own ledger
had already said what that costs.** `../LEDGER-DEFECTS.md` entry 5a: *"A stage with no brief
declares nothing, so nothing it drops can be counted"*, with the practice line *"every stage that
reduces its input gets a brief with an output shape, a per-item unit, a forbidden list and an
arithmetic that closes over its input's own total."* That entry was earned on 2026-11-11 by the
area proposal stage, which cut the best-attested area in the register. **SELECT is the same shape
of stage, one level down.**

What the reviews found specifically: nothing counts how many subjects the research returned, so no
arithmetic can fail to close; the quote that carries a test-1 judgement has nowhere to live; and
the claim verifier's `## Scope consequence` output asserts that SELECT reads it while no rule here
tells SELECT to.

---

> Work to this clause by clause. Produce every required section before writing a verdict.

---

**QUESTION**

Of the subjects the research recorded, which earn a full chapter, which earn a short entry, and
which are rejected — and what does each rejection cost?

**THE TESTS, AND THEY ARE NOT YOURS TO WRITE**

`../GOAL.md` §10, `[AGREED 2026-11-06]`, the owner's own ruling. **Quote it before applying it.**
A subject earns a full chapter when it has **all three**:

1. a **mechanism** worth understanding, not merely a practice to copy;
2. **live research**, so following it teaches how to read the literature;
3. something **buildable**, so dimension 5 is possible at all.

**Tests 2 and 3 are mechanical.** The research reports `LIVE RESEARCH` and `BUILDABLE` directly.
Read the field; do not re-judge it.

**Test 1 is judgement, and therefore must carry its evidence.** State it with the quote from the
record it rests on, so the owner can overturn the rejection without reading the rest.

**The fourth verdict exists because failing a test must not mean silence** (`../GOAL.md` §10,
`[AGREED 2026-11-06]`):

| Fails | And | Verdict |
|---|---|---|
| Test 1 — nobody has explained the mechanism yet | `SKILLS` says a practitioner is expected to know it | `SHORT-ENTRY` |
| Test 3 — no part of it can be built or measured here | the same | `SHORT-ENTRY` |
| Either | and `SKILLS` does not say so | `REJECT` |

**You may not invent a test, soften one, or add a fourth.** If a subject needs a test the owner has
not written, say so under `What this stage could not settle` and leave the subject undecided.

**WHAT TO DO**

1. **Count the input first, and write the number down.** Every subject record in every research
   file for this cycle. **A stage that does not state its input total cannot report a loss.**
2. **Read each record in full**, not its `VERDICT` field alone. The scout's verdict is evidence,
   not the ruling.
3. **Read `../CLAIMS.tsv` for each subject's rows**, and any claim-verifier report for them. A
   subject whose claims came back `superseded`, or whose `## Scope consequence` is `SUPPORT` or
   `NEITHER`, is a different subject from the one the scout wrote up.
4. **Decide each subject on its own**, and record the decision as a row.
5. **Re-raise last cycle's rejections.** Read `PLAN.md`'s rejected-subjects table and say, for each
   row, whether this cycle's research changes the verdict. **A rejection nobody re-reads is a
   permanent decision disguised as a cycle decision.**

**UNIT — one subject, one row**

```
SUBJECT         as the record names it
AREA            which area's research file it came from
VERDICT         CHAPTER | SHORT-ENTRY | REJECT
TEST 1          pass / fail, and for a fail or a judgement call, THE QUOTE from the
                record that the judgement rests on
TEST 2          pass / fail, quoting the record's LIVE RESEARCH field
TEST 3          pass / fail, quoting the record's BUILDABLE field
SKILLS SAYS     for any failure: what SKILLS says, because it decides
                SHORT-ENTRY against REJECT
CLAIMS          how many rows, and any that are superseded, contested or unverified
LOSES           for a REJECT: what leaves the book with it. "nothing" only after
                reading the record's own fields
```

**OUTPUT — every section, in this order**

```
## The tests          ../GOAL.md §10 quoted, with its marker and date
## Input              how many subjects, from how many area files, named
## Chapters           one row per CHAPTER
## Short entries      one row per SHORT-ENTRY, with the test it failed
## Rejected           one row per REJECT, with the test, the quote, and LOSES
## Last cycle's rejections, re-judged
## Subjects whose claims changed the picture
## Arithmetic         chapters + short entries + rejected + undecided = the input total
## What this stage could not settle
```

**TARGET**

**There is no number.** Not one per area, not a round figure. **A count in your head is a selection
rule you did not declare**, and `../GOAL.md` §5.3 forbids choosing the book's shape before the
subjects exist.

**FORBIDDEN**

- **Rejecting a subject for being small, quiet, unfashionable or awkward to write.** Reject only on
  a stated test. This is the rule that binds every stage before this one and it binds this one.
- **A reason shared between subjects.** One subject, one row, one reason.
- **Rejecting on test 1 without the quote.** The quote is what makes the rejection reversible, and
  `../PROCESS.md` §5 promises the owner he can overturn it without reading the rest.
- **Using `REJECT` where `SKILLS` earns `SHORT-ENTRY`.** That is the failure `../GOAL.md` §10 added
  the fourth verdict to prevent: *"the book could say nothing about something the owner is asked
  about… That is a bad way to fail, and the rule caused it."*
- **Taking the scout's `VERDICT` as the ruling.** It is one field in a record you are required to
  read whole.
- **Substituting a search, a pattern or a count for reading.** A pattern match tells you where a
  string is; it cannot tell you whether a mechanism is worth understanding.

**BUDGET**

No searches and no fetches. **You add no evidence.** The research files and `CLAIMS.tsv` are
everything. A subject you cannot judge from them is undecided, not rejected.

**WHAT THIS STAGE COULD NOT SETTLE**

- **Every verdict you were unsure about**, and what would settle it.
- **Every subject left undecided**, named.
- **Every `Sampling` report that named skipped subjects**, and whether a re-run at a higher cap is
  owed. **Deciding not to re-run is a decision and is recorded here.**
- **Any area whose scout reported the scope looked mis-drawn.** That is a finding about step 4 and
  it goes back there.

**STOPPING RULE**

Stop when every subject in every research file carries exactly one verdict or is named as
undecided, every rejection carries its test and its quote, last cycle's rejected table has been
re-judged row by row, and the arithmetic closes over the input total you wrote down first.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
subject wrongly kept costs the owner one reading. A subject wrongly rejected disappears from the
book, and the research that found it is re-derived next cycle or not at all.

**DELEGATION: ZERO.** This stage is not delegated — see the head of this file.
