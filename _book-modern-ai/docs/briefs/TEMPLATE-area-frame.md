# Area framing brief

**The framing run.** It proposes the area list that step 4 rules on. **It decides nothing**, and it
does not look for subjects — one scout per approved area does that afterwards
(`TEMPLATE-area-research.md`).

**Why it exists.** A brief that names no areas at all measures the search index rather than the
field (`../GOAL.md` §3.3). The areas are a coverage device that forces attention somewhere the index
does not point. **This run gets that device from the categories the field already files its own work
under**, so the boundaries come from evidence with a source rather than from anybody here.

## How to fill this in

Replace `<FIELD>`, `<OUTFILE>`, `<RUN-ID>`, `<FLOOR>` and `<SEARCH-FLOOR>`. **Change nothing else,
and add no examples.** If a change is needed, change this file and say in the commit what it fixes.

- **`<FIELD>`** is the field being divided, in the exact words the agent will be given. **It is the
  single input that most determines the answer**, because different wordings return different
  category lists from the same sources. The brief requires the agent to copy it back verbatim, so
  every run's output records the question it was actually asked. **Two runs are comparable only if
  this string is identical in both.**
- **`<OUTFILE>`** is `../../research/frames/YYYY-MM-DD-<RUN-ID>.md`, relative to `docs/briefs/`. The
  `frames/` subdirectory keeps these out of the scouts' namespace, where a dated filename is read as
  an area slug (`../../research/README.md`).
- **`<RUN-ID>`** is `a` for the first run, `b` for the second. **Run this brief twice.**
- **There is no cap on candidate areas.** The first two runs each had one, each hit it, and **each
  invented its own rule for cutting the list down** — an attestation threshold in one, a tiebreak in
  the other. Neither was asked for, and one of them reported that a different tiebreak over the same
  sources would have produced a different list. **A cutting rule is a decision about how the field
  divides, which is the owner's.** So the run reports every category its sources name, and he cuts.
- **`<FLOOR>`** is the minimum number of sources that must be fetched. **Five is the starting
  value**, raised from four because four was reachable without searching. Without a floor, a run
  that opens two listings, fills every field and stops has obeyed the brief exactly — and a thin
  list looks identical to a thorough one.
- **`<SEARCH-FLOOR>`** is the minimum number of searches that must be spent. **Ten is the starting
  value.** The first two runs used two and four of twenty-five: each hit a blocked page, recorded
  the loss, and stopped rather than looking for another route to the same taxonomy.

**Where to run it.** **In a fresh session outside this repository**, with no project file in its
context. Telling an agent to ignore files already attached to it does not work: it cannot unread
them. This is the only way the isolation is real rather than requested.

**Why twice.** A division produced once cannot be told from an artefact of whichever sources that
run happened to open. **Two runs disagreeing is a finding the owner needs before he rules.** Two
runs agreeing is weaker evidence than it looks — same model over the same prompt shares its priors
— so read agreement as "no disagreement found", not as confirmation.

**This brief names no area, no subject, no venue, no index, no vendor and no expected outcome, and
it must stay that way.** An instrument told what to expect finds it.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Under what categories does **`<FIELD>`** currently file, review and present its own work — and what
does each category include and exclude?

You are describing how this subject is already organised, **by the people who work in it**. You are
not proposing how it should be organised, and you are not saying which parts matter.

**WHAT TO DO**

1. **Find the places where this subject sorts its own work into named categories.** Five kinds
   count, and a good list draws on more than one:

   | Kind | What it is |
   |---|---|
   | `review-venue` | The submission or review categories of a venue that refereed the work |
   | `index` | The subject classification of an archive, index or catalogue |
   | `programme` | The session or track groupings of a meeting |
   | `survey` | The standing sections of a field-wide survey. **One author group's expository choice, so weaker than the others** — never your only kind |
   | `practitioner` | A taxonomy used to organise this work in industry: a named job board's categories, a named standards body's or trade group's classification, a named vendor-neutral benchmark suite's divisions. **These carry the applied and operational categories the academic kinds have no submission category for, so a list without them under-reports engineering** |

   A source that sells a product in this subject is marked `vendor` whatever else it is, and is the
   weakest kind. **You choose which sources to consult. That choice shapes the answer, so it is
   part of what you report.**

2. **Take the category names from those sources**, not from your own sense of how the subject
   divides, and not from any teaching sequence, course, roadmap, syllabus or textbook contents page.
3. **Say which level of each source's own hierarchy you took.** Filing systems are layered: one
   level may hold a handful of categories and the level below it ten times as many. **Which level
   you report decides how coarse the division is, so it is reported, never assumed.**
4. **Where sources disagree about a boundary, report the disagreement** rather than resolving it.
5. **Merge only where two names are plainly the same category** under different labels, and say
   which two and on what basis. **Split a source's category only if a different source splits it**,
   and name that source. Do not split on your own judgement.
6. **Report what you could not reach**, and what your chosen sources systematically miss.

**OUTPUT**

**Write the candidate list to `<OUTFILE>`.** Create it, and its directory if it does not exist.

**Return to me only this:**

1. `## The question I was asked` — **`<FIELD>`** copied back exactly, character for character.
2. `## Sources used` — one line each: what it is, its URL, its date, its kind, and `FETCHED` or
   `RECALLED`.
3. `## Candidate areas` — one line per area: its name, the level you took it from, and **one clause
   of what it includes and one of what it excludes**. No counts and no scores on this line.
4. `## Disagreements` — boundaries the sources draw differently. `none found` if none.
5. `## What this run could not see` — in full, as specified below.
6. `## Written to` — the file path and the number of areas in it.

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

**Every category your sources name, with no exceptions and no selection rule of your own.** From at
least `<FLOOR>` fetched sources of at least three different kinds, having spent at least
`<SEARCH-FLOOR>` searches.

**You may not filter the list.** Not by how many sources attest a category, not by a tiebreak, not
by your sense of what belongs together, not to keep the list a readable length. **If your sources
name forty categories, report forty.** A long list with source counts is exactly what the owner
needs in order to cut it himself; a short list cut by your rule tells him nothing about what you
removed.

**Each unit carries `ATTESTED BY`** — how many of your sources name this category, and which. That
number is what he cuts on. **It is not a score and you may not order by it.**

**Say if you could not reach either floor**, and what you reached instead.

**BUDGET**

25 searches, 25 fetches, and **at least `<SEARCH-FLOOR>` searches must be spent.** Spend them on
reaching the category listings themselves rather than on reading about them.

**A page you cannot reach is not a lost source until you have searched for another route to it.**
When a fetch returns 403, redirects away, or renders without the list, **search for the same
taxonomy elsewhere** — a mirror the body itself publishes, a different page of the same site, the
listing quoted in full by the organisation that owns it. Only after that does it become a loss, and
then you report both the block and the search that failed.

**WHAT THIS RUN COULD NOT SEE**

Required, and judged as strictly as the list itself. **An honest account of what the instrument
missed is worth more than a longer list.**

- **Searches used, of 25. Fetches used, of 25. Sub-agents started (must be zero).**
- **Which sources you chose, and which you considered and rejected**, with the reason for each
  rejection.
- **Which categories rest on a `RECALLED` source** — one you did not open in this run. List them by
  name.
- **What your sources systematically miss.** Work that is not submitted, reviewed, indexed or
  advertised anywhere is invisible to every source of this kind. Say so, and say what kinds of work
  those are.
- **Language.** Which languages your sources are in, and that categories named only in other
  languages are absent.
- **Recency.** Each source's date. A category established since the newest source you read will not
  appear.
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
- **A search-result summary treated as a source.** A snippet tells you something was said. Fetch the
  page before you quote it: a source can have been revised, corrected, retracted or withdrawn since
  it was indexed. A category you did not open is marked `RECALLED` and listed as such.
- **Saying which areas are most important, most active, most promising or most worth studying.**
  Not in the list, not in the summary, not in passing. An ordering is an argument disguised as a
  report.
- **Ordering the list by anything but the alphabet.**
- **Any selection rule of your own** — a threshold, a tiebreak, a minimum source count, a judgement
  that two categories are "really" one beyond the merge rule above, or any cut made to keep the list
  short. **Report everything your sources name.** Deciding which categories survive is the owner's
  job and the single thing this run must not do for him.
- **Abandoning a blocked source without searching for another route to it.**
- **A number without what it is a ratio of**, and any share of the whole subject.
- **Resolving a disagreement between sources** by picking the one you find more convincing.
- **Splitting a source's category on your own judgement.** Only another source may split it.
- **Reading any file in this repository**, if you can see one. Open no file except the one you are
  told to write.

**PARTIAL**

If the budget runs out, report the complete units you have, the floor you reached, and the sources
you had not opened. **A short list with an honest coverage section is a complete result.**

**STOPPING RULE**

Stop when **both floors are reached** — `<FLOOR>` fetched sources and `<SEARCH-FLOOR>` searches
spent — **and** every category your sources name has `NAME`, `LEVEL`, `SOURCES`, `INCLUDES`,
`EXCLUDES` and `ATTESTED BY` filled, with the remaining fields filled or honestly marked
`none found` / `none available` — **or** when the budget is spent. **Reaching the source floor is
not a reason to stop searching**: the first two runs stopped there and lost three taxonomies between
them that a search might have reached. Do not keep searching
for a better carving: there is no better carving to find, only more sources, and the coverage section
is where that is reported.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
boundary reported as disputed costs one reading. A boundary reported as settled, wrongly, becomes a
research area and then a part of a book.

**DELEGATION: ZERO.** Do not start any sub-agent.
