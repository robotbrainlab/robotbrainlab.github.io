# Chapter plan brief

**The PLAN stage.** It turns approved subjects into `PLAN.md` rows: one chapter each, with what that
chapter is required to contain. It runs **after** the owner's ruling at SELECT and **before** any
chapter is drafted (`../ROADMAP.md` step 8; nothing is drafted until `PLAN.md` is approved).

**Claude runs this in the main session. It is not delegated.** The same reason as SELECT, and the
same answer: bounded, not unbounded.

## Why this brief exists, and why it matters more than it looks

**This is the narrowest point in the whole pipeline.** A subject record holds nine researched
fields. `PLAN.md` compresses it into one cell:

> **`Must cover`** is what the chapter is required to contain, drawn from the subject record. **It
> is what `tools/verify-coverage.py` reads, and it is the only promise a chapter can be found short
> of.**

**So everything in the record that does not reach that cell is unchecked from that moment on** — by
every gate, every pass and every ledger. Gate 6 compares the chapter against `Must cover`; it cannot
see what `Must cover` lost. `ACCEPTANCE.md`'s questions are written from `PLAN.md`, so the
acceptance bank inherits the same thinning, and so does the drill — which means **the only
instrument that samples whether a chapter taught anything cannot ask about what this stage dropped.**

`../LEDGER-DEFECTS.md` entry 1 describes this failure one level up: *"A rule explained in prose can
vanish with no term missing. A whole section of method can disappear while every keyword it used
survives elsewhere."* Its practice is manual triage of the coverage gate's list — which compares
chapter against `Must cover`, and therefore cannot reach this.

---

> Work to this clause by clause. Produce every required section before writing a `PLAN.md` row.

---

**QUESTION**

What must each chapter contain, drawn from the subject record, such that nothing the research found
is lost without being named?

**WHAT TO DO**

1. **Count the input.** Every subject the owner approved at SELECT, by name. **Write the number
   down before you start.**
2. **For each subject, open its record in full** — all nine fields, not the scout's summary.
3. **Write `Must cover` from the record, field by field**, and for every field, record what you
   carried and what you did not. `WHY IT MATTERS`, `FOUNDATIONS`, `LIVE RESEARCH`, `TRANSITION`,
   `ENGINEERING` and `SKILLS` are six of them, and `../GOAL.md` §3.2 `[STATED]` requires every
   subject to carry scientific foundations, ongoing research, engineering and the
   research-to-engineering connection. **A `Must cover` cell that drops one of those drops a stated
   requirement, not a detail.**
4. **Fill `Source record`** — the path to the research file. **The chapter's writer is told to read
   it**, so a row without it severs the chapter from its evidence.
5. **Decide `Lab form`** — `construct` or `reproduce` — from the record's `BUILDABLE` field, and say
   which sentence decided it. `[2026-11-11]` No stage owned this before; the research field reports
   cost, the smallest teaching experiment and hardware, not the form.
6. **Seed the inputs vocabulary.** `../GATES.md` gate 8 requires that *"every term appearing in a
   `NAME` field of a subject record, plus every term in a `CLAIMS.tsv` claim"* goes into
   `tools/field-terms.txt` when the plan is approved. **That extraction is this stage's.**
7. **Check the other direction.** Every approved subject has a row, and every row names an approved
   subject. Nothing else runs SELECT → PLAN.

**UNIT — one subject, one row, plus its carry record**

```
SUBJECT         as SELECT approved it
CHAPTER         the chapter it becomes, or SHORT-ENTRY, or `pending`
ANSWERS         the durable question from ACCEPTANCE.md
MUST COVER      what the chapter is required to contain
CARRIED         per record field: what of it reached MUST COVER
NOT CARRIED     per record field: what did not, and why it need not
LAB FORM        construct | reproduce, and the BUILDABLE sentence that decided it
SOURCE RECORD   the path to the research file
```

**`NOT CARRIED` is the point of this brief.** "Nothing" is an answer only after you have read the
field and can say why it needs no coverage. **A field you did not read cannot be marked carried.**

**`[STATED 2026-11-11]` Write every section below to `../PLAN-RECORD-YYYY-MM-DD.md` before any of
it is put to the owner.** A stage that runs in the main session has no agent boundary to force the
write, so the rule has to be stated here. A result that lives in a conversation cannot be read
next cycle, cannot be cited, and cannot be checked against what it claimed — and the stage that
lost robotics was a main-session stage whose working was never written down. **`## Rows`
additionally becomes `../PLAN.md`'s rows once the owner approves them**; the other eight sections
live only in the record, which is the only place the fields a row dropped are named.

**OUTPUT — every section, in this order**

```
## Input              approved subjects, counted and named
## Rows               one per subject, the UNIT above
## What each chapter does not carry   gathered, so it can be read in one place
## Dimensions check   for each subject, which of GOAL.md §3.2's five are in MUST COVER
## Short entries and pendings
## Vocabulary seeded  the terms extracted for gate 8, and from where
## Arithmetic         rows + short entries + pendings = approved subjects
## What this stage could not settle
```

**FORBIDDEN**

- **Writing `Must cover` from the scout's summary, the subject name, or memory.** From the record,
  field by field, or not at all.
- **Dropping a record field silently.** Every field is either carried or named under `NOT CARRIED`.
  **A silent drop here is invisible to every instrument downstream** — that is the whole reason this
  brief exists.
- **Choosing the book's structure before the subjects exist.** `../GOAL.md` §5.3: structure follows
  the subjects.
- **Letting a page estimate decide what a chapter covers.** `../GUIDE.md` §9. `../PROCESS.md` §2
  says this one can only be caught by looking at what was dropped — which is what `NOT CARRIED` is.
- **Leaving an approved subject without a row**, or inventing a row for a subject SELECT did not
  approve.
- **Substituting a search, a pattern or a count for reading.** A keyword survives while the method
  it belonged to disappears; `../LEDGER-DEFECTS.md` entry 1 is exactly that.

**BUDGET**

No searches and no fetches. The research records, `CLAIMS.tsv` and SELECT's output are everything.

**WHAT THIS STAGE COULD NOT SETTLE**

- **Every field marked `NOT CARRIED` that you are unsure about.**
- **Every subject you could not give a durable question.**
- **Every `pending` short entry**, and what would give it a host chapter.
- **Any subject whose record was too thin to plan from.** That is a finding about the research, and
  it goes back to the scout stage rather than being absorbed here.

**STOPPING RULE**

Stop when every approved subject has a row or is named as pending, every record field is carried or
listed under `NOT CARRIED`, the five dimensions are checked per subject, the vocabulary is
extracted, and the arithmetic closes over the approved count you wrote down first.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
`Must cover` cell that asks for too much costs one argument at review. One that asks for too little
is never detected by anything, and the book is quietly thinner than its own research.

**DELEGATION: ZERO.**
