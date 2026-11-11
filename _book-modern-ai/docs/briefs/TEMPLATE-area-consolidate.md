# Area consolidation brief

**The consolidation run.** It takes what the framing runs reported and turns it into one candidate
area list the owner can rule on. It runs **after** `TEMPLATE-area-frame.md` and **before** the
owner's decision at step 4 (`../ROADMAP.md`).

**Why it exists, and why it is a separate agent.** A framing run must report what the field files,
faithfully and without filtering — that is the whole reason its brief forbids any selection rule of
its own. **But a faithful report of filing categories is not a list of research areas.** Venues file
by submission routing, so their categories include application domains, session formats, audience
labels and one organisation's product names. The first framing runs reported all of those correctly,
and the result was a list in which roughly a quarter of the rows were not areas of AI at all.

**Putting the rejection rule into the framing brief would have made the reporter the judge**, which
is the defect that brief exists to prevent. So the two jobs are two agents: one records, one
consolidates, and **the consolidator's output can be checked against the record it came from.**

## The one line this run must not cross

> **It may reject a row for not being an area. It may never reject a row for being unimportant.**

A kind error — this is a domain, a format, an audience, a product name — is this run's to fix. A
judgement that an area is small, quiet, unpromising or not worth the owner's time is **the owner's
and nobody else's** (`../GOAL.md` §3.3). Every rejection and every merge is listed with its reason
so he can reverse either without reading the raw files.

**[2026-11-11] This paragraph was changed earlier today on the claim that its citation was false, and
changed back, because the citation holds.** §3.3's own division-of-labour table gives the
consolidation run "**may reject a category for not being an area; never for being unimportant**" and
gives the owner "**approves, redraws or rejects the proposed list, with the evidence for each
boundary in front of him**". What §3.3 retracts is that the owner must *author* the list — a
different act, and one nobody asks of him, since the list is proposed to him. The error was mine and
is recorded in `../POSTMORTEM-2026-11-11.md` §2.2; **do not re-apply the change.**

## How to fill this in

Replace `<FRAME-FILES>`, `<OUTFILE>` and `<AREA-RULE>`. **Change nothing else.**

- **`<FRAME-FILES>`** is every framing run's output file for this cycle, by absolute path. **All of
  them**, including runs whose lists were superseded — a category only one run found is still
  evidence, and dropping a whole run is a selection rule.

  **[2026-11-07] That is now one file per cycle**, because framing runs no longer come in pairs
  (`../DIAGNOSIS-2026-11-07.md` §5.3). **It is this cycle's run only.** The six runs of 2026-11-06
  and 2026-11-07 are history, not input: what they found that matters is carried forward in
  `../../research/frames/SOURCES.md`, which the framing run reads, so **a current run that misses
  something an old run had is a failure to be fixed at the framing stage — not a hole for this run to
  patch from an old file.** This run still adds no category of its own.
- **`<OUTFILE>`** is `../../research/frames/CONSOLIDATED-YYYY-MM-DD.md`, relative to `docs/briefs/`.
- **`<AREA-RULE>`** is the owner's definition of what counts as an area for this book, pasted in
  whole. **This run cannot start without it**, because every rejection it makes is an application of
  that rule and nothing else.

**[AGREED 2026-11-07] The rule is the book's own title.** *Research, Science and Engineering* are
three modes, not a slogan, and a category is an area if it belongs to at least one of them.

> **Keep a category if it belongs to the science of AI, the research in AI, or the engineering of
> AI — and engineering includes its tools, its measurement and its operation.**
>
> **Drop it if it belongs to none of the three:** AI applied to another field's problems, a report
> on AI's effect on the world, a meeting format or audience, or an organisation.
>
> **A product or tool name is not dropped. It is reported as the engineering area it instances**,
> with the product named as evidence.
>
> **Tag every surviving area with the mode or modes it serves.**

**Why the three modes and not a flat test.** An earlier draft of this rule asked only whether AI
itself advances somewhere, and it had five holes. It deleted a benchmark suite's name when the work
behind it — measuring inference by deployment target — is how engineering knows anything. It
deleted a domain label when the work behind it was a real area. It had no verdict at all for a
standards body's working groups. **Engineering requires tools, so a tool category is an engineering
area rather than an exception to be rescued by a clause.**

**Why the mode tag matters more than it looks.** `../GOAL.md` §3.2 requires every subject to carry
science *and* research *and* engineering. **So an area list that comes back all science and no
engineering cannot deliver what the book exists for** — and without the tag, nothing would say so
until chapters were being written.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Of the categories these framing runs recorded, which are research areas for this book, which are
not, and which are the same area under different names?

**THE RULE YOU APPLY**

`<AREA-RULE>`

**This is the only rule you apply.** You do not add to it, soften it, or supplement it with your own
sense of what matters.

**WHAT TO DO**

1. **Read every framing file in `<FRAME-FILES>`**, in full. Each category has a record: its name,
   the level of its source's hierarchy, every source, what it includes, what it excludes, what it
   overlaps and where sources disagree. **Judge from the record, not from the name.** A name that
   looks like an application may have a record showing the methods do not transfer; a name that
   looks like an area may have a record showing it is a session format.
2. **Classify every category** into exactly one of:

   | Verdict | Means |
   |---|---|
   | `AREA` | Passes the rule. A place AI itself advances |
   | `DOMAIN` | Ordinary AI pointed at another field's data |
   | `RECORD` | About AI's effect on the world rather than about AI |
   | `FORMAT` | A session shape, a track slot, an audience, a company size, a working arrangement |
   | `PRODUCT` | One organisation's branded suite or tool, not a category of work |
   | `UNCLEAR` | **The record does not settle it.** Say what would |

   **A record that carries no scope cannot be an `AREA`.** Where `INCLUDES` says the source gave a
   name and a level and nothing more, the record does not settle anything, so the verdict is
   `UNCLEAR` and what would settle it is "a scope statement from the source". **This holds even when
   the name looks unambiguous**, and especially then: a `WHY` that paraphrases the name is the name
   being used as the record. One run of this brief gave `AREA` to fourteen such records — among them
   *Graphs*, justified as "learning on graph-structured data", and *Harness Engineering*, justified
   as "the harness a model runs inside" — and said in its own coverage section that `AREA` on those
   meant no more than "a track name that denotes AI engineering". **It is the owner's business
   whether a bare track title becomes an area of his book, not this run's.**

3. **Merge categories that are the same area under different names**, and **only** on evidence from
   the records: the same sources, or `ALSO CALLED` naming the other, or `INCLUDES` that match. Give
   the kept name, every name merged into it, and the evidence. **Two names you merely think are
   similar stay separate.**
4. **Resolve the resolution problem.** The framing runs reported at different depths — one took a
   venue's twelve top-level topics, another its thirty-seven subject areas. **Pick the coarsest
   level at which the areas still differ in what work goes in them**, state which level you picked,
   and record every finer category under the area that contains it rather than dropping it.
5. **Carry each surviving area's evidence forward.** Its sources, its source count, its includes and
   excludes, and whether academic or applied sources named it.

**OUTPUT**

**Write the consolidated list to `<OUTFILE>`.** Create it.

**Return to me only this:**

1. `## Areas` — one line each: name, source count, whether academic sources, applied sources or both
   name it, and one clause of what it covers. **Alphabetical. No ordering by anything else.**
2. `## Rejected` — one line each: name, verdict, and **the clause of the rule it fails.** Grouped by
   verdict.
3. `## Merged` — one line each: the kept name, the names merged into it, and the evidence.
4. `## Unclear` — every `UNCLEAR`, with what would settle it. **These go to the owner undecided.**
5. `## Level` — which level you picked and why, and what sits below it.
6. `## What this run could not settle` — in full, as specified below.
7. `## Written to` — the path and the counts.

**UNIT — one surviving area**

```
NAME            the name you kept
VERDICT         AREA
WHY             the clause of the rule it passes, in one sentence
SOURCES         carried forward from the framing records, with their kinds
ATTESTED BY     how many sources, and which. Carried forward, not recomputed
COVERS          what work goes in it, from the records' INCLUDES
EXCLUDES        what goes elsewhere, from the records' EXCLUDES
MERGED FROM     every framing-run name folded into this one, or "none"
BELOW           finer categories the framing runs reported that sit inside this
                area at a lower level. Named, never dropped
FAMILY          academic / applied / both, from which kinds of source named it
```

**TARGET**

**Every category in every framing file gets exactly one verdict.** No category may be left
unaccounted for. **There is no target number of areas** — the number is whatever the rule yields.

**BUDGET**

No searches and no fetches. **You add no new evidence.** Everything you need is in the framing
files, and a category you cannot judge from them is `UNCLEAR`, not researched further.

**WHAT THIS RUN COULD NOT SETTLE**

- **Every `UNCLEAR`**, and what evidence would settle it.
- **Every rejection you were unsure about.** Name it and say why it was close. **A borderline
  rejection the owner never sees is a decision taken from him.**
- **Any merge you made on thin evidence**, so he can split it again.
- **Whether the level you picked loses something**, and what.
- **Any project file visible in your context**, named, with what it told you.

**FORBIDDEN**

- **Substituting a search, a pattern, a count or a lookup for reading.** You read and you judge.
  **A pattern match tells you where a string is; it cannot tell you what the thing means**, and
  every question in this brief is about meaning. Where you do run a search or a count, it is a
  **hint about where to read** and never the finding itself — a phrasing you did not think of has no
  string to search for. **Automation gives no context, which is the whole of what you were asked
  for.**
- **Rejecting a category for being unimportant, small, quiet, unfashionable, or not worth covering.**
  That is the owner's judgement and this run must not make it. Reject only on kind.
- **Adding a category no framing run reported.** If the rule implies an area the runs missed, say so
  under `What this run could not settle` — never as an area.
- **Any new research.** No searches, no fetches, no recall. The framing files are the evidence.
- **Ordering by anything but the alphabet**, and any score, rank or priority.
- **Dropping a finer category instead of filing it under `BELOW`.**
- **Dropping a whole framing run**, or preferring one run's list to another's.
- **Softening or extending the rule you were given.**

**PARTIAL**

If you cannot finish, report the verdicts you reached and name every category still unjudged.
**An unjudged category is not a rejection.**

**STOPPING RULE**

Stop when every category in every framing file carries exactly one verdict, every merge has its
evidence, and every `UNCLEAR` has what would settle it. **There is nothing to search for, so there
is no reason to continue past that point.**

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
category you marked `UNCLEAR` costs the owner one reading. A category you rejected wrongly
disappears from the book without him ever seeing it.

**DELEGATION: ZERO.** Do not start any sub-agent.
