# Modern AI: Research, Science and Engineering — session instructions

## This file can be out of date. The repository cannot.

Where this file and the actual state of the repository disagree, **the repository wins**. Check
what the files actually say before you act on an instruction here. Do not change the repository to
match this file. Say that this file looks out of date, and ask.

Why this rule exists: measured on 40 projects and 320 runs, coding agents followed a stale
instruction file over the existing code **90.1%** of the time — a single preprint, recorded at that
strength. One agent reported the conflict in 79
of 80 runs and followed the file anyway. One sentence giving the code precedence moved
code-following from 4.2% to 91.4% ([arXiv 2610.30571](https://arxiv.org/abs/2610.30571), verified
2026-11-03).

## First thing in every session

Read `docs/ROADMAP.md`. It says which of the eleven steps we are on and what the next action is.

Then read, in this order, only what the current step needs:

| Read | For |
|---|---|
| `docs/GOAL.md` | What the book is for, and why. **Every statement is marked** as the owner's words, agreed, my recommendation, or open. Nothing is a decision unless it says so |
| `docs/PROCESS.md` | How the book gets built: the cycle, the chapter loop, the passes, the agents, the gates, the brief schema |
| `docs/ROADMAP.md` | The eleven steps, and where we are |
| `docs/GUIDE.md` | What the book **is**: scope, voice, chapter anatomy, labs, length, conventions |
| `docs/GATES.md` | What each gate reads, fails on and prints — and the policy for setting a claim's review date |
| `docs/ACCEPTANCE.md` | The questions each chapter must answer, written **before** any chapter is drafted |
| `docs/CLAIMS.tsv` | Every load-bearing claim, with its source, its strength, its maturity and its review date. **Currently empty** — reset 2026-11-06 |
| `docs/briefs/TEMPLATE-area-research.md` | The research brief. Fill it in; do not rewrite it |
| `research/` | What the research has returned. **Currently empty** |
| `discarded/` | Pre-consensus research. **Read the README before opening anything in it** |

## Precedence, when two documents disagree

1. **The repository** beats every document.
2. **A machine-checked file** (`docs/CLAIMS.tsv`, `docs/OWNERSHIP.tsv`, `records/`) beats prose.
3. **`docs/GOAL.md`** beats everything else on *what the book is for*.
4. **`docs/GUIDE.md`** beats everything else on *what the book is* — its scope, voice, chapter
   anatomy and labs.
5. **`docs/PROCESS.md`** beats everything else on *how it gets built*.

**A rule may be referred to from several files; it may be stated in only one.** A second statement
is a defect even while the two agree, because they will drift. Cite the owning file and section
instead.

## The rules that are easy to break

- **All research conducted before 2026-11-06 is discarded.** The owner's instruction: it was done
  before we reached a consensus on the goal, the method and the scope. See `discarded/README.md`.
  **No figure from it may be cited, and it may not be used to choose or rank a research area.**
  Only two things survived, and both are about the instrument rather than about AI: the brief
  terminates and keeps an agent honest about its sources, and it has four fixes. **"Areas should be
  small" is withdrawn** — it was a conclusion about how many subjects an area holds, which is a
  claim about the field drawn from a discarded run. The brief caps subjects per area and requires
  the agent to report what it skipped; the fresh research calibrates the cap.
- **The book is fully independent and self-contained.** It is not a continuation, an extension or
  a revision of any earlier work, and has no connection to one in content, scope, structure or
  progression. The voice is specified in `docs/GUIDE.md` §4 and the method in `docs/PROCESS.md`; both are
  stated as rules in their own right, with nothing to consult. See `docs/GOAL.md` §2.4.
- **Duplication between the two books is fine.** Duplication *within* this book is a defect. These
  are different rules.
- **No topic gets less explanation because something else covered it.**
- **Scope is a property of the subject, not a position in any curriculum.** The book is about what
  is currently moving; it is not about settled foundations. Stated in full in `docs/GUIDE.md` §3 and
  nowhere else. The book covers Modern AI
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

## The eleven classes of mistake already made

`docs/GOAL.md` §11 records them, each with its instances and the practice that follows. Read it before
assessing anything. The shortest summary: **do not claim what you have not read**, and **do not
assess a thing with an instrument that does not sample it**.
