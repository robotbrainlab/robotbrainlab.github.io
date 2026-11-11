# Area framing brief

**The framing run.** It proposes the area list that step 4 rules on. **It decides nothing**, and it
does not look for subjects — one scout per approved area does that afterwards
(`TEMPLATE-area-research.md`).

**Why it exists.** A brief that names no areas at all measures the search index rather than the
field (`../GOAL.md` §3.3). The areas are a coverage device that forces attention somewhere the index
does not point. **This run gets that device from the categories the field already files its own work
under**, so the boundaries come from evidence with a source rather than from anybody here.

## `[STATED 2026-11-11]` Every run is independent. Nothing is carried forward.

**The owner revoked the source register, and his reasoning stands on its own:** a fixed list of
sources decides what can be found, which makes it scope, not method. A later run inheriting it is
not an independent reading of the field; it is a re-reading of one earlier run's idea of where the
field lives. **He revoked his own agreement to it, which is his to do.**

So: **this run is given no sources, no routes, no levels, no counts and no previous output.** It
finds its own sources, reports them, and stands on its own.

**What that costs, recorded honestly rather than argued away.** The register was built because six
independent runs produced six incomparable lists — only two sources were common to all six, four
venues were read at different editions, and a route around a blocked page that one run found was
unavailable to the next, which hit the same block and called it the biggest hole in its list. **Those
costs come back.** They are paid for by the two restorations below, which is a worse trade on
efficiency and a better one on independence, and the owner made that trade knowingly.

**Two things the register had replaced, and which return with it gone:**

1. **The floors.** Without a fixed list, a run that opens two listings and fills every field has
   obeyed the brief exactly, and a thin list is indistinguishable from a thorough one. The floors
   below are weak instruments, and they are what there is.
2. **More than one run per cycle.** A division produced once cannot be told from an artefact of
   whichever sources that run happened to open. **The register removed that reason; its removal
   restores it.** Runs are unioned, never intersected — a category one run found and another missed
   is still a category the field files.

## How to fill this in

Replace `<FIELD>`, `<OUTFILE>` and `<RUN-ID>`. **Change nothing else, and add no examples.** If a
change is needed, change this file and say in the commit what it fixes.

- **`<FIELD>`** is the field being divided, in the exact words the agent will be given. **It is the
  single input that most determines the answer**, because different wordings return different
  category lists from the same sources. The brief requires the agent to copy it back verbatim, so
  every run's output records the question it was actually asked. **Runs are comparable only if this
  string is identical in all of them**, and it is the one thing that is held constant across a
  cycle's runs.
- **`<OUTFILE>`** is `../../research/frames/YYYY-MM-DD-<RUN-ID>.md`, relative to `docs/briefs/`. The
  `frames/` subdirectory keeps these out of the scouts' namespace, where a dated filename is read as
  an area slug (`../../research/README.md`).
- **`<RUN-ID>`** is the next unused letter. **At least two runs per cycle, launched separately and
  unaware of each other.** How often framing happens at all is `../PROCESS.md` §5's: at step 4, and
  after that only when a `RECARVE` is approved.
- **There is no cap on candidate areas.** The first two runs ever made each had one, each hit it,
  and **each invented its own rule for cutting the list down** — an attestation threshold in one, a
  tiebreak in the other. Neither was asked for, and one reported that a different tiebreak over the
  same sources would have produced a different list. **A cutting rule is a decision this run is not
  positioned to make**, because a reporter that filters cannot be checked against what it filtered.
  The cut happens twice afterwards and never here: Claude proposes it against the book's stated
  purpose, and the owner approves, redraws or rejects that proposal (`../GOAL.md` §3.3).

**Where to run it.** **In a fresh session outside this repository**, with no project file in its
context. Telling an agent to ignore files already attached to it does not work: it cannot unread
them. This is the only way the isolation is real rather than requested.

**This brief names no area, no subject, no category, no source and no expected outcome, and it must
stay that way.** An instrument told what to expect finds it.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Under what categories does **`<FIELD>`** currently file, review and present its own work — and what
does each category include and exclude?

You are describing how this subject is already organised, **by the people who work in it**. You are
not proposing how it should be organised, and you are not saying which parts matter.

**WHAT TO DO**

1. **Find the filing systems yourself.** Nobody has given you a list, and that is deliberate: a list
   would decide your answer before you started. Look for places where the people who do this work
   have already had to sort it into categories. **Five kinds count:**

   | Kind | What it is |
   |---|---|
   | `review-venue` | The submission or review categories of a venue that refereed the work |
   | `index` | The subject classification of an archive, index or catalogue |
   | `programme` | The session or track groupings of a meeting |
   | `survey` | The standing sections of a field-wide survey **of the work itself**. **One author group's expository choice, so weaker than the others** — never your only kind. **An annual report that measures the subject's effect on the world does not qualify**, however standing its chapters: its sections file measurements, not submissions |
   | `practitioner` | A taxonomy used to organise this work in industry: a named job board's categories, a named standards body's or trade group's classification, a named vendor-neutral benchmark suite's divisions. **These carry the applied and operational categories the academic kinds have no submission category for, so a list without them under-reports engineering** |

   A source that sells a product in this subject is marked `vendor` whatever else it is, and is the
   weakest kind.

   **THE SOURCE FLOOR — at least eight sources, spanning at least four of the five kinds.** Below
   that, say so plainly in your coverage section and report what you have. A list drawn from one
   kind describes that kind's habits, not the field.

   **THE SEARCH FLOOR — at least ten searches spent on finding sources and routes.** A run that
   opens the first two listings it thinks of has measured its own priors.

2. **Open each source and read the level you take, exhaustively.**

3. **Take the category names from the sources**, not from your own sense of how the subject
   divides, and not from any teaching sequence, course, roadmap, syllabus or textbook contents page.

4. **Say which level of each source's hierarchy you took, and why** — and how many categories that
   level holds. A level is a choice you are making, so it is reported as one.

5. **Where sources disagree about a boundary, report the disagreement** rather than resolving it.

6. **Merge only where two names are plainly the same category** under different labels, and say
   which two and on what basis. **Split a source's category only if a different source splits it**,
   and name that source. Do not split on your own judgement.

7. **Report what you could not reach**, and what your sources, as a set, systematically miss.

**OUTPUT**

**Write the candidate list to `<OUTFILE>`.** Create it, and its directory if it does not exist.

**Everything below goes in that file, not only in your reply.** A coverage report that exists only
in a conversation is re-derived next cycle or lost.

1. `## The question I was asked` — **`<FIELD>`** copied back exactly, character for character.
2. `## Sources used` — one line each: what it is, its URL, its date, its kind, **why you chose it**,
   and `FETCHED` or `RECALLED`.
3. `## Sources I looked for and could not use` — blocked, paywalled, moved, or not a filing system
   after all. **With what you tried.**
4. `## Candidate areas` — one line per area: its name, the level you took it from, and one clause of
   what it includes and one of what it excludes. No counts and no scores on this line.
5. `## Disagreements` — boundaries the sources draw differently. `none found` if none.
6. `## What this run could not see` — in full, as specified below.
7. `## Written to` — the file path and the number of areas in it.

**UNIT — one candidate area**

```
NAME            the category name, as its source calls it. Not a name you coined
LEVEL           where this sits in its source's own hierarchy: which level you took,
                what the level above groups it under, and roughly how many
                categories the level below splits it into. Write "flat" if the
                source has only one level
SOURCES         one line each: what it is, its URL, its date, its kind, and
                FETCHED or RECALLED. At least one must be FETCHED with a URL,
                or this category is not reportable — drop it
ALSO CALLED     other names the same category appears under, with their sources
INCLUDES        what work is filed here, in the source's own terms
EXCLUDES        what is filed elsewhere, naming where it goes. Where it goes to
                something not on your list, write "off-list: <name>".
                Do NOT add that name as a candidate area to make this field work
OVERLAPS        any other candidate area whose INCLUDES overlap this one, and how.
                "none found" is a complete answer
SIZE SIGNAL     an absolute count with its source, or a ratio against a denominator
                the source itself defines. NEVER a share of "the field" or of the
                whole subject: nobody can define that denominator, so nobody can
                check it. Write "none available" rather than estimating
SOURCE DISAGREES  where another source splits, merges or omits this category
                differently. "none found" is a complete answer
ATTESTED BY     how many of your sources name this category, and which ones.
                A count, for the owner to cut on. NOT a score: you may not
                order by it, drop anything for a low one, or comment on it
```

**TARGET**

**Every category your sources name, with no exceptions and no selection rule of your own.**

**Having chosen a level in a source, report every category at that level, and say how many that
level holds.** A partial read of the level you chose is the one incompleteness nothing downstream
can detect: the list looks deliberate. A run that took a source's twelve named suites and reported
ten lost the only two that measured something other than speed — and the coarser level, read in
full, carried more than the finer level read in part. **If you cannot read a level exhaustively,
take the level above it and say so.**

**`INCLUDES` is quotation or it is an admission. It is never your gloss.** Either give the source's
own words for what the category covers, or write that **the source gives the name and the level and
no scope statement** — in those words. **A sentence that restates the name is the name being used as
the scope**, and it is worse than an empty field, because the next stage cannot tell it from a real
one: it has no source to check and nothing in it is false enough to notice. One run wrote "product
management of AI products" for a track called *Product Management*, and "graph-shaped data and
knowledge in AI applications" for a track called *Graphs*, where both sources give a bare label and
no description at all. **An earlier run got this right** on a thinner page — "the source gives the
track name only and no scope statement; nothing inferred here" — and that is the wording to copy.

**Where a source files items under a bare label**, the items are evidence of what goes in it and you
may report them — **as the items, named, and attributed to the item and not to the category.** "Three
of the twelve sessions under this track are about X" is a finding. "This track covers X" is not,
unless the source says so.

**Why this one matters more than it looks.** The next stage is forbidden to call a category an area
when the record carries no scope; such a record goes to the owner undecided instead. **An invented
scope defeats that rule silently**, because the next stage has no sources and cannot tell your
sentence from the source's.

**Every label at the level you took goes in the main list, including the ones you judge are not
subjects.** A room name, a stage, a day, an audience, a job title, a company size, a session format
or a branded product at that level is still a label the source puts at that level, so it is reported
as a unit — **with its nature said plainly in `INCLUDES`, and never moved to an appendix or a
separate section.** Deciding that a label is a format rather than an area is the next stage's job,
not yours (`TEMPLATE-area-consolidate.md` gives it six verdicts for exactly this), and the owner
reverses those verdicts from one list. **One run put 32 such labels into appendices with its reasons
given in full** — nothing was hidden, and it is still a decision taken one stage too early. **A label
genuinely *below* the level — an individual talk, a dataset, a standards project — is a different
matter and is not a unit at all.**

**You may not filter the list.** Not by how many sources attest a category, not by a tiebreak, not
by your sense of what belongs together, not to keep the list a readable length. **If your sources
name forty categories, report forty.** A long list with source counts is exactly what the owner
needs in order to cut it himself; a short list cut by your rule tells him nothing about what you
removed.

**Each unit carries `ATTESTED BY`** — how many of your sources name this category, and which. That
number is what he cuts on. **It is not a score and you may not order by it.**

**Account for every source you used by name**, and every one you tried and could not use.

**BUDGET**

25 searches, 25 fetches. **At least ten searches go to finding sources and routes** — that is a
floor, not a target. A long page read in two parts spends two fetches.

**A blocked source is not a lost source until you have tried another route to it**: a mirror the
body itself publishes, a different page of the same site, the listing quoted in full by the
organisation that owns it, an archived copy. Report both the block and whether the route worked.

**WHAT THIS RUN COULD NOT SEE**

Required, and judged as strictly as the list itself. **An honest account of what the instrument
missed is worth more than a longer list.**

- **Searches used, of 25. Fetches used, of 25. Sub-agents started (must be zero).**
- **Whether you met the source floor** — eight sources across four kinds — and if not, which kinds
  you have none of. **A set drawn from two kinds is a finding about this run, not about the field.**
- **How you chose your sources**, in your own words. This is the question the next reader most needs
  answered and the one only you can answer.
- **Which categories rest on a `RECALLED` source** — one you did not open in this run. List them by
  name.
- **What your sources, as a set, systematically miss.** Unpublished work; categories named only in
  languages you did not search; anything newer than your newest source; roles and occupations, if no
  `practitioner` source covered them.
- **Recency.** Each source's date as you read it. A category established since your newest source
  will not appear.
- **Anything you could not fetch**, and what you lost by it.

**FORBIDDEN**

- **Substituting a search, a pattern, a count or a lookup for reading.** You read and you judge.
  **A pattern match tells you where a string is; it cannot tell you what the thing means**, and
  every question in this brief is about meaning. Where you do run a search or a count, it is a
  **hint about where to read** and never the finding itself — a phrasing you did not think of has no
  string to search for. **Automation gives no context, which is the whole of what you were asked
  for.**
- **Proposing a category no source carries.** If you think the subject is missing one, say so under
  `What this run could not see` — never as a candidate area.
- **Using a curriculum, course, syllabus, roadmap, textbook contents page or learning path** as a
  source of categories. Those are teaching orders built for somebody else's purpose. A `survey`'s
  standing sections are permitted and are marked as such; a book's table of contents is not.
  **A faithful reproduction of a named body's own classification is not caught by this rule, wherever
  it is hosted** — including on a teaching site, and including when a teaching order has been
  annotated onto it. Name the classifying body as the source, name the page you read as the route,
  and ignore the annotations. Two runs of this brief split on exactly this point, and the one that
  refused such a page lost two real categories it had suspected were there. **What is forbidden is
  taking somebody's teaching order as a taxonomy, not reading a taxonomy on a teacher's website.**
- **A search-result summary treated as a source.** A snippet tells you something was said. Fetch the
  page before you quote it: a source can have been revised, corrected, retracted or withdrawn since
  it was indexed. A category you did not open is marked `RECALLED` and listed as such.
- **Saying which areas are most important, most active, most promising or most worth studying.**
  Not in the list, not in the summary, not in passing. An ordering is an argument disguised as a
  report.
- **Ordering the list by anything but the alphabet.**
- **Any selection rule of your own** — a threshold, a tiebreak, a minimum source count, a judgement
  that two categories are "really" one beyond the merge rule above, or any cut made to keep the list
  short. **Report everything your sources name.** Deciding which categories survive happens in two
  later steps — a proposal, then the owner's ruling on it — and is the single thing this run must
  not do.
- **Abandoning a blocked source without searching for another route to it.**
- **A number without what it is a ratio of**, and any share of the whole subject.
- **Resolving a disagreement between sources** by picking the one you find more convincing.
- **Splitting a source's category on your own judgement.** Only another source may split it.
- **Reading any file in this repository**, if you can see one. Open no file except the one you are
  told to write.

**PARTIAL**

If the budget runs out, report the complete units you have and **name every source you had found but
not opened.** **A short list with an honest coverage section is a complete result**; a short list
that does not say what is missing from it is not a result at all.

**STOPPING RULE**

Stop when the source floor is met or honestly reported as unmet, every source you opened is
accounted for, and every category those sources name has `NAME`, `LEVEL`, `SOURCES`, `INCLUDES`,
`EXCLUDES` and `ATTESTED BY` filled, with the remaining fields filled or honestly marked
`none found` / `none available` — **or** when the budget is spent. **There is no better carving to
find, only more sources**, and the coverage section is where that is reported.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
boundary reported as disputed costs one reading. A boundary reported as settled, wrongly, becomes a
research area and then a part of a book.

**DELEGATION: ZERO.** Do not start any sub-agent.
