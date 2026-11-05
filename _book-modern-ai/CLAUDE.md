# Modern AI: Research, Science and Engineering — session instructions

## This file can be out of date. The repository cannot.

Where this file and the actual state of the repository disagree, **the repository wins**. Check
what the files actually say before you act on an instruction here. Do not change the repository to
match this file. Say that this file looks out of date, and ask.

Why this rule exists: measured on 40 projects and 320 runs, coding agents followed a stale
instruction file over the existing code **90.1%** of the time. One agent reported the conflict in 79
of 80 runs and followed the file anyway. One sentence giving the code precedence moved
code-following from 4.2% to 91.4% ([arXiv 2610.30571](https://arxiv.org/abs/2610.30571), verified
2026-11-03).

## First thing in every session

Read `ROADMAP.md`. It says which of the eleven steps we are on and what the next action is.

Then read, in this order, only what the current step needs:

| Read | For |
|---|---|
| `GOAL.md` | What the book is for, and why. **Every statement is marked** as the owner's words, agreed, my recommendation, or open. Nothing is a decision unless it says so |
| `PROCESS.md` | How the book gets built: the cycle, the chapter loop, the passes, the agents, the gates, the brief schema |
| `ROADMAP.md` | The eleven steps, and where we are |
| `CLAIMS.tsv` | Every load-bearing claim, with its source, its strength and its review date |
| `briefs/TEMPLATE-area-research.md` | The research brief. Fill it in; do not rewrite it |
| `research/` | What the research has returned so far |

## Precedence, when two documents disagree

1. **The repository** beats every document.
2. **A machine-checked file** (`CLAIMS.tsv`, `OWNERSHIP.tsv`, `records/`) beats prose.
3. **`GOAL.md`** beats everything else on *what the book is for*.
4. **`PROCESS.md`** beats everything else on *how it gets built*.

A rule that appears in two files is a defect. Fix it by deleting one, not by editing both.

## The rules that are easy to break

- **The new book has no connection to *Modern AI Engineering from Zero*** in content, scope,
  structure or progression. It is independent and self-contained. Only two things carry over: the
  **language and voice**, and the **method**. Not the four parts. See `GOAL.md` §2.4.
- **Duplication between the two books is fine.** Duplication *within* this book is a defect. These
  are different rules.
- **No topic gets less explanation because the first book covered it.**
- **The track decides the scope; self-containment decides the depth.** The book covers Modern AI
  subjects only, and teaches whatever those subjects need from zero, inline.
- **Never state a claim above the strength of its source**, and quote the source.
- **Every size claim names what it is a share of.** "Growing fast" is not a finding.
- **A search summary is not a source.** Fetch the page.
- **Every brief has a stopping rule and an output shape.** No agent delegates; depth is zero.
- **Research output goes to a file**, never into the conversation. Agents return a summary only.
- **Structure follows the subjects.** Do not choose the parts before the research names them.
- **Page estimates never decide scope.**
- **Nothing is drafted until the table of contents is approved.**
- **One chapter at a time. Never a part at a time.**
- **The repository is public.** Scan for secrets before every commit. Never push as the
  `dlakshmizlk` account.

## Style, in everything the owner reads

Plain, controlled English — about 80% ASD-STE100. Short sentences. Active voice. The answer first,
then what was done and decided, then the explanation. Tables where they carry the information
better than prose. No internal codes or shorthand: name things.

## The eight classes of mistake already made

`GOAL.md` §11 records them, each with its instances and the practice that follows. Read it before
assessing anything. The shortest summary: **do not claim what you have not read**, and **do not
assess a thing with an instrument that does not sample it**.
