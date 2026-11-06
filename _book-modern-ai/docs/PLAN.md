# The plan — what the book contains

**Status: empty, and nothing may be drafted until it is filled and approved.**

This file is the table of contents. It has two halves that change at completely different rates,
and keeping them apart is the point of the file.

---

## Part one — the spine

**Changes rarely. Approved once, then revised only by a `NEW QUESTION` or `RECARVE` operation.**

The spine is a set of **durable questions** (`PROCESS.md` §5.2). A question is the book's unit of
structure because it outlives every answer it will carry: a new subject goes to the question it
answers, and a subject that dies leaves its question standing.

| # | Durable question | Owning chapter | Added in cycle |
|---|---|---|---|
| — | *Empty. The questions come from the research, not from before it.* | — | — |

**Why this is empty and must stay empty for now.** The spine is a claim about how the material
divides, and the material is not known until the research has run. A spine written now would be
written from assumptions about what the research will find, which is the specific failure recorded
in `GOAL.md` §11 class C.

---

## Part two — this cycle's subjects

**Changes every cycle. Approved every cycle.**

| Subject | Answers question | Chapter | **Must cover** | Verdict | Lab form | Source record |
|---|---|---|---|---|---|---|
| — | *Empty.* | — | — | — | — | — |

`Verdict` is from the research: `CHAPTER`, `FOUNDATIONS-ONLY`, `SHORT-ENTRY` or `REJECT`
(`GOAL.md` §10). A `SHORT-ENTRY` row names the chapter whose section will hold it, or `pending` if
no chapter owns a question it bears on yet.
`Lab form` is `construct` or `reproduce` (`GUIDE.md` §6).
`Source record` is the research file the subject came from.
**`Must cover`** is what the chapter is required to contain, drawn from the subject record. It is
what `tools/verify-coverage.py` reads, and it is the only promise a chapter can be found short of.

---

## Rejected subjects, and why

**Kept, not deleted.** A subject rejected this cycle may qualify next cycle, and the reason it was
rejected is the only way to tell whether anything has changed.

| Subject | Cycle | Failed which test | Reason |
|---|---|---|---|
| — | *Empty.* | — | — |

The three tests are in `GOAL.md` §10: a **mechanism** worth understanding, **live research**, and
something **buildable**.

---

## How this file gets filled

| Step | What happens | Who approves |
|---|---|---|
| 1 | The research returns subject records, one file per area | — |
| 2 | Each subject is scored against the three tests. Rejections are recorded above with reasons | **Owner** |
| 3 | The surviving subjects are grouped by the question each answers. **New questions are proposed here, and a new question is a structural change** | **Owner** |
| 4 | Questions become chapters, in an order. Concept ownership is assigned in `OWNERSHIP.tsv` | **Owner** |
| 5 | Acceptance questions are written for each chapter, **before any chapter is drafted** | — |

**Then, and only then, chapter one is written.**

---

## The open decisions this file is waiting on

From `GOAL.md` §10 and `GUIDE.md`. **Three need the subjects and two do not** — `ROADMAP.md`'s
open-decisions table owns which step closes each:

| Decision | Needs the subjects? |
|---|---|
| The book's shape — breadth against depth | **Yes** |
| The structure — five candidates in `GOAL.md` §5.3 | **Yes** |
| How deep the mathematics goes — three candidates | **Yes** |
| Whether cross-references go by chapter or by concept | **No**, and `GUIDE.md` §7 says it is expensive to reverse — so it should be settled early rather than left to this file |
| Whether the book is for one reader or more | **No** |

**Only the three marked Yes block this file**, and they wait on the research returning subjects
(`ROADMAP.md` step 6).
