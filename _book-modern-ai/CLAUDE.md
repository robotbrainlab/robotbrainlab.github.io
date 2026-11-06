# Modern AI: Research, Science and Engineering — session instructions

## This file can be out of date. The repository cannot.

Where this file and the actual state of the repository disagree, **the repository wins**. Check
what the files actually say before acting on an instruction here. Do not change the repository to
match this file. Say that this file looks out of date, and ask.

Why the rule exists: a preprint reports that coding agents followed a stale instruction file over
the existing code **90.1%** of the time across 40 projects and 320 runs; that one agent reported the
conflict in 79 of 80 runs and followed the file anyway; and that one sentence giving the code
precedence moved code-following from 4.2% to 91.4%
([arXiv 2610.30571](https://arxiv.org/abs/2610.30571), read 2026-11-03). **A single preprint, so
recorded at that strength** — but the rule costs nothing and the failure it prevents is expensive.

## First thing in every session

**Read `docs/ROADMAP.md`.** It says which of the eleven steps we are on and what the next action is.
Then read only what that step needs:

| Read | For |
|---|---|
| `docs/GOAL.md` | What the book is for, and why. **Every statement is marked** as the owner's words, agreed, my recommendation, or open. Nothing is a decision unless it says so. §11 holds the eleven classes of mistake already made |
| `docs/GUIDE.md` | What the book **is**: scope, voice, chapter anatomy, labs, length, conventions |
| `docs/PROCESS.md` | How it gets built: the cycle, the chapter loop, the four passes, the agents, the brief schema |
| `docs/GATES.md` | What each gate reads, fails on and prints — and the policy for a claim's review date |
| `docs/ACCEPTANCE.md` | The questions each chapter must answer, written **before** any chapter is drafted |
| `docs/PLAN.md` | The spine and this cycle's subjects. **Empty, and says why** |
| `docs/CLAIMS.tsv` | Every load-bearing claim, with its source, strength, maturity and review date. **Empty** |
| `docs/briefs/` | One brief per agent role. Fill one in; do not rewrite it |
| `research/` `records/` `data/` | What the research returned, the per-chapter records, the labs' data. **No content yet; each holds a `README.md` saying what goes in it** |

## Precedence, when two documents disagree

1. **The repository** beats every document.
2. **A machine-checked file** — `docs/CLAIMS.tsv`, `docs/OWNERSHIP.tsv`, `records/` — beats prose
   about its own contents.
3. **`docs/GOAL.md`** beats everything else on *what the book is for*.
4. **`docs/GUIDE.md`** beats everything else on *what the book is* — scope, voice, anatomy, labs.
5. **`docs/PROCESS.md`** beats everything else on *how it gets built*.
6. **`docs/GATES.md`** beats everything else on *what a check does*.

**A rule may be cited from several files; it may be stated in only one.** A second statement is a
defect while the two still agree, because they will drift. Cite the owning file and section.

**Two exceptions, because without them the rule cannot be obeyed:**

1. **A brief in `docs/briefs/` is self-contained.** The agent filling it is forbidden from reading
   project files, so it cannot be sent to an owning document. A brief may therefore carry any rule
   or vocabulary its agent needs — **copied word for word, never summarised**, so a drift is a
   difference anyone can see.
2. **This file may state the rules easiest to break**, in the list below, because its job is to be
   read first and in full. Each entry names its owning file.

**Everywhere else a second statement is a defect**, and a *summary* of a rule is a second
statement of it.

## The rules that are easy to break

- **The book is fully independent and self-contained.** Not a continuation, extension or revision of
  any earlier work, and no connection to one in content, scope, structure or progression. The voice
  is specified in `docs/GUIDE.md` §4, the method in `docs/PROCESS.md`; both stand as rules in their
  own right, with nothing to consult. See `docs/GOAL.md` §2.4.
- **Duplication with anything outside this book is fine and expected. Duplication *within* this book
  is a defect** — one concept, one owning chapter (`docs/OWNERSHIP.tsv`). Two different rules.
- **No topic gets less explanation because something else covered it.**
- **The scope boundary.** Stated in full in `docs/GUIDE.md` §3 and nowhere else, **including not in
  short form here** — read it there before deciding anything is in or out.
- **Never state a claim above the strength of its source**, and quote the source.
- **Give a count with its source, or a ratio against a denominator somebody else defined.** Never a
  share of "the field": nobody can define that denominator, so nobody can check it.
- **A search summary is not a source.** Fetch the page — it may have been revised, corrected,
  retracted or withdrawn since it was indexed.
- **Every brief has an output shape and a stopping rule with a fixed point.** No agent delegates.
- **Research output goes to a file**, never into the conversation. An agent returns a summary only.
- **Structure follows the subjects.** Do not choose the parts before the research names them.
- **Page estimates never decide scope.**
- **Nothing is drafted until `docs/PLAN.md` is approved.**
- **One chapter at a time. Never a part at a time.**
- **The repository is public.** Scan for secrets before every commit. **Push only to the
  `github-robotbrainlab` remote**, which is the `robotbrainlab` account; never as the
  `dlakshmizlk` account, which has write access and is the wrong identity for this work.

## Style, in everything the owner reads

Plain, controlled English — about 80% ASD-STE100. Short sentences. Active voice. The answer first,
then what was done and decided, then the explanation. Tables where they carry the information
better than prose. **No internal codes or shorthand: name things.**

## Before claiming anything about a file

**Open it.** `docs/GOAL.md` §11 records eleven classes of mistake made on this project, and the
largest is claiming what was not read. The two shortest rules from it:

- **Do not claim what you have not read.** A summary of a document tells you only that the document
  exists.
- **Do not assess a thing with an instrument that does not sample it.** Name the instrument and
  what it samples, before the claim.
