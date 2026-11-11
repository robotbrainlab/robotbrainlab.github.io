# Claim confirmation brief

**The CONFIRM stage.** It takes every claim the scouts returned and turns it into a `../CLAIMS.tsv`
row, then has every provisional claim verified. It runs **after** the research files exist and
**before** SELECT, because SELECT reads a claim's state to judge its subject (`../PROCESS.md` §5).

**Claude runs this in the main session. It is not delegated** — the mapping is bookkeeping, but
deciding that a scout's row is too thin to become a claim is judgement. **That is a reason not to
delegate it, not a reason to leave it unbounded.**

## Why this brief exists

**`[STATED 2026-11-12]` The owner was asked whether this stage should have a brief like every
other, and said it should.** Until then it was the last reducing stage running on a prose
description alone — `../PROCESS.md` §5.1, which is a column-mapping table. **A table says what a
row looks like. It does not say how many rows were owed**, so nothing could fail to close, and a
scout claim that never became a row would have left no trace anywhere.

`../LEDGER-DEFECTS.md` entry 5a is the general form: *"A stage with no brief declares nothing, so
nothing it drops can be counted."* It was earned by the area proposal stage, which cut the
best-attested area in the register. **CONFIRM is the same shape of stage**, and it decides which
claims get verified at all, so what it drops is invisible from that moment on.

---

> Work to this clause by clause. Produce every required section before writing a `CLAIMS.tsv` row.

---

**QUESTION**

Which of the claims the research returned become `CLAIMS.tsv` rows, what does each row say, and
which of them has been verified?

**THE MAPPING, AND IT IS NOT YOURS TO WRITE**

`../PROCESS.md` §5.1 owns the column-by-column mapping from a scout's six fields to the twelve
columns. **Open it and work from it. It is not copied here**, because this stage runs where that
file is open and a second copy of a rule is a defect (`../CLAUDE.md`).

**Two of its rules decide most of the work:**

- **`verified_on` is the date the claim verifier ran**, never the date the scout read the source. A
  row the verifier has not touched leaves it empty and carries `state = unverified`.
- **`dependents` stays empty here.** It is written from a finished chapter at CLOSE, never from a
  plan.

**WHICH CLAIMS GET VERIFIED**

**`[STATED 2026-11-12]` Every claim whose `maturity_basis` is `provisional`.** No narrower rule
is available at this stage and none may be invented.

The rule used to read *"every provisional claim a candidate chapter would rest on"*. **It could not
fire.** What a chapter rests on is `dependents`, which is empty until CLOSE — several stages later
— and SELECT and PLAN have not run, so nothing yet says which subject becomes a chapter. The owner
was given the three options and chose this one: **at CONFIRM every researched subject is still a
candidate, so "every provisional claim" is what the old rule already meant.** Verification stays
ahead of SELECT, which needs the state to judge a subject.

Run `claim-verifier.md` on each. **It is a delegated agent with its own brief and its own budget**
— fill its placeholders, do not re-specify its work here.

**WHAT TO DO**

1. **Count the input first, and write the number down.** Every claim in every research file for
   this cycle, per file and in total. **A stage that does not state its input total cannot report a
   loss.**
2. **Check that every area has a number.** Ids are `A03-001` — the area's number, a hyphen, a
   zero-padded counter — and the numbers are fixed when the owner approves the area list
   (`../ROADMAP.md` step 4). **If an area has no number, stop and say so.** Do not coin one: a
   number is never reused and never renumbered, so inventing one here cannot be undone.
3. **Open each claim in its research file**, with the subject record around it. A claim read out of
   its record is a sentence without a subject.
4. **Write one row per claim**, by §5.1's mapping.
5. **Refuse a row rather than guess a column.** A claim with no `source_quote`, no reachable
   source, or no area number is refused and named, not written with a blank.
6. **Run the claim verifier on every `provisional` row**, and write back what it returns.
7. **Close the arithmetic** over the input total from step 1.

**UNIT — one claim, one row**

```
ID              the area's number, a hyphen, a zero-padded counter
CLAIM           the scout's claim, unchanged
SOURCE          the scout's source URL, unchanged
SOURCE QUOTE    the exact sentence from the source, copied by the scout. NEVER
                written here: if the scout did not supply it, the row is refused
STRENGTH        the scout's strength field, renamed, not re-judged
MATURITY        the scout's maturity field, unchanged
MATURITY BASIS  the scout's basis field, renamed
CLASS           the scout's class field, unchanged
REVIEW BY       computed from CLASS and MATURITY by ../GATES.md's policy
VERIFIED ON     the date the verifier ran, or empty
STATE           unverified on arrival; whatever the verifier returned after it ran
DEPENDENTS      empty. Filled at CLOSE from a finished chapter
```

**`[STATED 2026-11-12]` Write every section below to `../CONFIRM-YYYY-MM-DD.md` as well as writing
the rows into `../CLAIMS.tsv`.** `CLAIMS.tsv` holds the rows that survived; **it cannot hold what
was refused, what was unsure, or what the arithmetic did not reach**, and those are the whole
reason this brief exists.

**OUTPUT — every section, in this order**

```
## Input              how many claims, from how many research files, named per file
## Rows written       one line each: id, subject, state
## Refused            one line each: the claim, and which column could not be filled
## Verified           every provisional row, with what the verifier returned
## Changed the picture  every row that came back contested or superseded, and the
                      subject it belongs to, because SELECT reads this
## Area numbers       each area, its number, and where that number was fixed
## Arithmetic         rows written + refused = the input total
## What this stage could not settle
```

**TARGET**

**There is no number.** Every claim the research returned gets a row or a named refusal.

**FORBIDDEN**

- **Writing a `source_quote` yourself.** The scout copies it from the source. This stage does not
  fetch, so a quote written here would be a quotation of nothing (`../GOAL.md` §3.4).
- **Coining an area number.** See step 2. The owner fixes them at approval.
- **Filling `verified_on` for a row the verifier did not touch**, or `dependents` for any row.
- **Re-judging a strength, a maturity or a class.** Those are the scout's, and overturning one is
  the verifier's job, not this stage's.
- **Dropping a claim because it looks weak.** A weak claim becomes a row with a weak strength and
  the book states it at that strength. Only a missing column refuses a row.
- **Substituting a search, a pattern or a count for reading.** A claim is judged against its
  record, which means opening the record.

**BUDGET**

No searches and no fetches in this stage. **You add no evidence.** The claim verifier fetches,
under its own brief and its own budget.

**WHAT THIS STAGE COULD NOT SETTLE**

- **Every refused claim**, and what would let it become a row.
- **Every claim the verifier returned `cannot-reach` for**, with what it tried.
- **Any claim that appears in two research files**, and which row you kept.
- **Any area whose number was missing**, because that blocks every id under it.

**STOPPING RULE**

Stop when every claim in every research file is a row or a named refusal, every provisional row has
a verifier verdict or a `cannot-reach`, every area used has a number fixed at approval, and the
arithmetic closes over the input total you wrote down first.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A row
written with a guessed column is worse than a refusal: the refusal is in the output, and the guess
is cited by a chapter.

**DELEGATION: ZERO.** This stage is not delegated — see the head of this file. The claim verifier
is a separate stage with its own brief, not a sub-agent of this one.
