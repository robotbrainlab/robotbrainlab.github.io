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
| `docs/GOAL.md` | What the book is for, and why. **Every statement is marked** as the owner's words, agreed, my recommendation, open, or **defaulted** — mine, acted on because the decision was waiting. Nothing is a decision unless it says so. §11 holds the thirteen classes of mistake already made |
| `docs/HOW-IT-WORKS.md` | **For the owner, in plain language**: the eleven steps, the repeating cycle, and the five points where he decides something. `[2026-11-12]` **A map, not an authority** — it states no rule and names the owning file for each step |
| `docs/GUIDE.md` | What the book **is**: scope, voice, chapter anatomy, labs, length, conventions |
| `docs/PROCESS.md` | How it gets built: the cycle, the chapter loop, the four passes, the agents, the brief schema |
| `docs/GATES.md` | What each gate reads, fails on and prints — and the policy for a claim's review date |
| `docs/ACCEPTANCE.md` | The questions each chapter must answer, written **before** any chapter is drafted |
| `docs/PLAN.md` | The spine and this cycle's subjects. **Empty, and says why** |
| `docs/CLAIMS.tsv` | **Every claim a scout returns**, with its source, strength, maturity and review date — not only the load-bearing ones (`docs/PROCESS.md` §4.1). **Empty** |
| `docs/briefs/` | One brief per agent role. Fill one in; do not rewrite it |
| `records/` `data/` | The per-chapter records and the labs' data. **No content yet; each holds a `README.md` saying what goes in it** |
| `research/` | What the research returned. **`frames/` holds this cycle's two framing runs** — `2026-11-11-h.md` and `2026-11-11-i.md`, about 4,400 lines — **and `CONSOLIDATED-2026-11-12.md`, their union: 223 distinct categories from 307 records, of which 99 are `UNCLEAR`** `[2026-11-12]`. The proposal built from it is `docs/PROPOSAL-areas-2026-11-12.md` and the owner has ruled on it; **`docs/ROADMAP.md`'s first section says what to do next.** **`frames/superseded/` holds the other eleven runs and lists** `[2026-11-12]`, each with a dated line saying what superseded it; **it is input to nothing**, and that includes `SOURCES.md`, the source register the owner revoked on 2026-11-11 (`docs/GOAL.md` §3.3). One scout has run — a validation run of its brief, on an area the owner has not approved (`research/README.md`) |
| `practice/` | **The only record of what the owner has worked through.** `DRILL.tsv` holds the drill outcome per question. **It may be read to judge the book and the pace, never to judge the reader** — `practice/README.md` owns that rule |

## Precedence, when two documents disagree

1. **The repository** beats every document.
2. **A machine-checked file** — `docs/CLAIMS.tsv`, `docs/OWNERSHIP.tsv`, `records/` — beats prose
   about its own contents.
3. **`docs/GOAL.md`** beats everything else on *what the book is for*.
4. **`docs/GUIDE.md`** beats everything else on *what the book is* — scope, voice, anatomy, labs.
5. **`docs/PROCESS.md`** beats everything else on *how it gets built*.
6. **`docs/GATES.md`** beats everything else on *what a check does*.

**Rules 4 to 6 disappear when those three files merge** into one specification after step 7
(`docs/PROCESS.md` §11). Most of the drift three audits found sat exactly on the boundaries this
ordering exists to arbitrate.

**A rule may be cited from several files; it may be stated in only one.** A second statement is a
defect while the two still agree, because they will drift. Cite the owning file and section.
**`[STATED 2026-11-12]` `docs/briefs/document-check.md` checks this**, as its fourth finding type.
It had no instrument until then, and an independent review found seven drifted wordings. **A
program cannot do it** — whether two paragraphs state one rule is a question about meaning.

**Two exceptions, because without them the rule cannot be obeyed:**

1. **A brief in `docs/briefs/` whose agent cannot read project files is self-contained.** That
   agent cannot be sent to an owning document, so its brief may carry any rule or vocabulary it
   needs — **copied word for word, never summarised**, so a drift is a difference anyone can see.
   **`[2026-11-12]` Five of the thirteen briefs are run by Claude in the main session**, where the
   owning document is open: `area-proposal.md`, `confirm-claims.md`, `select-subjects.md`,
   `plan-chapters.md` and `document-check.md`. **The premise does not hold for them, so they cite rather than copy** — and
   a copy in one of those would be the second statement this rule forbids
   (`docs/briefs/README.md`).
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
- **No topic gets less explanation because something else covered it** (`docs/GOAL.md` §2.4).
- **The scope boundary.** Stated in full in `docs/GUIDE.md` §3 and nowhere else, **including not in
  short form here** — read it there before deciding anything is in or out.
- **Never state a claim above the strength of its source**, and quote the source (`docs/GUIDE.md`
  §5).
- **Give a count with its source, or a ratio against a denominator somebody else defined.** Never a
  share of "the field": nobody can define that denominator, so nobody can check it
  (`docs/GUIDE.md` §5).
- **A search summary is not a source.** Fetch the page — it may have been revised, corrected,
  retracted or withdrawn since it was indexed (`docs/GOAL.md` §3.4).
- **Every brief has an output shape and a stopping rule with a fixed point.** No agent delegates
  (`docs/PROCESS.md` §4.6).
- **No agent — and not you either — substitutes a search, a pattern or a count for reading.**
  Automation may check form; it may never judge content. A count is a hint about where to read
  (`docs/briefs/README.md`). `[STATED 2026-11-11]` The owner kept this rule when offered the faster
  alternative, and the owning statement now says in its own words that it binds the main session —
  it said only "an agent" until then, so this bullet's "and not you either" had nothing behind it.
- **Research output goes to a file**, never into the conversation. An agent returns a summary only
  (`docs/briefs/TEMPLATE-area-research.md`). **`[STATED 2026-11-11]` The three main-session
  reducing stages now name an output file too** — the area proposal, SELECT and PLAN — and the
  consolidator must put its coverage section in its file, not only in its reply. A main-session
  stage has no agent boundary to force the write, which is why none of the three had one.
- **A superseded document moves to `superseded/` in the commit that supersedes it**, so a live
  directory lists only what may be read as current. Nothing is deleted, and the sweep that catches
  what the move missed runs at `CLOSE`, every cycle (`docs/PROCESS.md` §11.1).
- **Structure follows the subjects.** Do not choose the parts before the research names them
  (`docs/GOAL.md` §5.3).
- **The owner is never handed an unrecommended list.** Where he rules on something, somebody
  proposes it first, with a reason per item, and that somebody is you. A run that reports or sorts
  has not proposed anything (`docs/GOAL.md` §3.3, `[AGREED 2026-11-11]`). **He approves, redraws or
  rejects a proposal; he does not originate one.** This was broken at step 4 for four days: an
  inventory of 63 areas was put to him as if it were a recommendation, and he said so four times
  before it was heard.
- **A stage that reduces its input must close its arithmetic over the input's own total**, not over
  the part it chose to handle, and must name what every removal takes with it — the `BELOW`
  children, the single-source subjects, the items an earlier stage flagged
  (`docs/briefs/area-proposal.md`). **The stage with no brief is the one that loses things**, and
  because it declares no total, nothing it drops can be counted
  (`docs/LEDGER-DEFECTS.md` entry 5a).
- **Page estimates never decide scope** (`docs/GUIDE.md` §9).
- **Nothing is drafted until `docs/PLAN.md` is approved** (`docs/ROADMAP.md`, step 8).
- **A decision waiting more than seven days is acted on and marked `[DEFAULTED]`** — but **never
  push, never spend money, never discard finished work, never override something the owner
  reserved, and `[STATED 2026-11-12]` never change a statement marked `[STATED]` or `[AGREED]`**
  (`docs/PROCESS.md` §2.1).
- **An `[I RECOMMEND]` item is put to the owner before the first time it binds something real**, and
  named as mine in the same message as the thing it binds. **Never in a batch**: about fifty stand,
  and he ruled that a rule ruled on in the abstract is approved from its wording
  (`docs/GOAL.md` §0).
- **One chapter at a time. Never a part at a time** (`docs/PROCESS.md` §2).
- **The repository is public.** Scan for secrets before every commit. **Push only to the
  `github-robotbrainlab` remote**, which is the `robotbrainlab` account; never as the
  `dlakshmizlk` account. **No gate checks either of these** (`docs/GATES.md`, "What no gate
  reads") — they are the committer's, and nothing in the book can see them.

## Style, in everything the owner reads

Plain, controlled English — about 80% ASD-STE100. Short sentences. Active voice. The answer first,
then what was done and decided, then the explanation. Tables where they carry the information
better than prose. **No internal codes or shorthand: name things.**

## Before claiming anything about a file

**Open it.** `docs/GOAL.md` §11 records thirteen classes of mistake made on this project, and the
largest is claiming what was not read. **Class M is the other one to know: a pattern match answers a
question about strings, never one about meaning.** The seven shortest rules — the first three are
about evidence, the last four about the record, and **all seven have been broken on this project**:

- **Do not claim what you have not read.** A summary of a document tells you only that the document
  exists.
- **Do not assess a thing with an instrument that does not sample it.** Name the instrument and
  what it samples, before the claim.
- **Do not substitute a search or a count for reading.** Automation may check form; it may never
  judge content.
- **Do not inherit a citation's authority without opening the citation.** A section number beside a
  claim is the most persuasive thing in these documents and the easiest to be wrong. **Citing a
  marked statement means quoting its marker and its date.**
- **Read the whole section, not the part that settles it for you.** `GOAL.md` §3.3 retracts one
  thing in its opening and assigns the opposite in a table forty lines below. Reading the first part
  and stopping produced a confident correction of a statement that had been right
  (`docs/POSTMORTEM-2026-11-11.md` §2.2). **A partially-read section is more dangerous than an
  unread one, because it is quotable** — class A says the same of summaries: *having the summary is
  worse than having nothing, because nothing makes you look.*
- **Do not decide what the record has already decided, in either direction.** Class C is usually
  taking the owner's decision; **it is the same error to hand him one the record never took off
  him.** Before saying who decides anything, open the marked statement that says so **and read it to
  the end.**
- **Do not state a property from instances.** Two runs doing something is not what the method does
  (class D). Give the count in the sentence that makes the claim.

**A rule change is not finished until every file that states or cites it has been opened** —
`CLAUDE.md`, `docs/GOAL.md`, `docs/GUIDE.md`, `docs/PROCESS.md`, `docs/GATES.md`,
`docs/ROADMAP.md`, `docs/briefs/README.md` and the briefs. **A grep is not a sweep**: it finds the
phrasings you thought of. On 2026-11-07 a four-file change was declared complete by a grep for three
phrasings, and `docs/briefs/README.md` kept the old rule under a fourth.

**Before any document in `docs/` is called finished**, run `docs/briefs/document-check.md` over it.
It is the only instrument on this project that reads what Claude writes; everything else checks an
agent or a chapter (`docs/POSTMORTEM-2026-11-11.md`).
