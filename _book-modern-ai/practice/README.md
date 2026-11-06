# What landed

**The only record of what the owner has actually worked through.** It exists because nothing else in
this project samples the learner: fourteen gates, four review passes and three ledgers all read the
*text* (`../docs/GOAL.md` §12). Without this, no cycle can tell whether the last cycle's material
was learned, so how much to produce next stays a guess.

**It is not in the book and the book never reads it.** `../docs/GOAL.md` §2.3 keeps the owner's
practice separate from the book, and that stands. This sits beside the book.

## The one rule about how it may be used

> **It may be read to judge the book and the pace. It may never be read to judge the reader.**

A question nobody could answer is a finding about the chapter that was supposed to answer it. **One
concept coming back shaky across three chapters means those chapters are bad**, and that is the
signal this file exists to give. `../docs/GOAL.md` §11 class H is the rule this comes from: do not
assess a thing with an instrument that does not sample it. This file samples chapters, through their
questions. It does not sample the owner.

**The columns enforce it rather than trusting it.** Every column holds either a date, a question id
or a concept name. **There is no field in which a judgement about the reader can be written**, and
none may be added. That is also why committing it to a public repository is safe: a question id and
a concept name are facts about the book.

## The drill

**`../docs/ACCEPTANCE.md` is the instrument and already was.** Its questions are specified as ones
*"a competent person would ask you about this subject, which you should be able to answer out loud
in about a minute."* That is a spoken drill. Nothing new had to be built.

**Answer them aloud, from memory, with the chapter closed.** Then record the outcome per question:

| Outcome | Means |
|---|---|
| `answered` | Came out, aloud, in about a minute |
| `shaky` | Came out, but slowly or incompletely |
| `not-yet` | Did not come out |

**[I RECOMMEND]** when it runs, and the owner has not ruled on the timing:

- **After working through a chapter**, which is the first and most useful reading.
- **Again at EXPIRE**, on earlier chapters. That stage already re-checks claims whose truth may have
  moved; re-drilling asks the same question of what was known. A `shaky` on a chapter that drilled
  `answered` two cycles ago is the most useful row this file can hold.

## `DRILL.tsv`

| Column | What goes in it |
|---|---|
| `chapter` | `NN-slug`, matching `markdown/` |
| `drilled_on` | The date, `YYYY-MM-DD`. One row per drill, so a re-drill is a new row |
| `answered` | The `ACCEPTANCE.md` question numbers that came out |
| `shaky` | The numbers that came out slowly or incompletely |
| `not_yet` | The numbers that did not come out |
| `weak_concept` | The concept the shaky and not-yet questions have in common, if any, and the chapter that owns it in `../docs/OWNERSHIP.tsv`. Blank where there is no pattern. **This points at a chapter, never at the reader** |

**What reads it.** The owner, at PLAN, to size the next cycle (`../docs/PROCESS.md` §10). Nothing
else does yet, and no gate reads it — it is a record, not a check.
