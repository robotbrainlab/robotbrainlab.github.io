# Area framing brief

**The framing run.** It proposes the area list that step 4 rules on. **It decides nothing**, and it
does not look for subjects — one scout per approved area does that afterwards
(`TEMPLATE-area-research.md`).

**Why it exists.** A brief that says "research modern AI" measures the search index rather than the
field (`../GOAL.md` §3.3). The areas are a coverage device that forces attention somewhere the index
does not point. **This run gets that device from the categories the field already files its own work
under**, so the boundaries come from evidence with a source rather than from anybody here.

## How to fill this in

Replace `<OUTFILE>`, `<CAP>` and `<RUN-ID>`. **Change nothing else, and add no examples.** If a
change is needed, change this file and say in the commit what it fixes.

- **`<OUTFILE>`** is `../../research/YYYY-MM-DD-frame-<RUN-ID>.md`, relative to `docs/briefs/`.
- **`<RUN-ID>`** is `a` for the first run of a cycle, `b` for the second. **Run this brief twice,
  independently, with no agent seeing the other's output.** Two runs that produce different carvings
  mean the carving is an artefact of what each one happened to read — which is a finding about the
  frame, and the owner needs it before he rules.
- **`<CAP>`** is the maximum number of candidate areas to report. **It bounds the report, not the
  field**, so it cannot be calibrated by the run it bounds. The run must say whether it hit the cap.

**This brief names no area, no subject, no venue, no index and no expected outcome, and it must stay
that way.** An instrument told what to expect finds it.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Under what categories does this field currently file, review and present its own work — and what
does each category include and exclude?

You are describing how the field is already organised. **You are not proposing how it should be
organised, and you are not saying which parts matter.**

**WHAT TO DO**

1. **Find the places where the field sorts its own work into named categories.** Submission or
   review categories, programme or session groupings, index or archive subject classes, the standing
   sections of a field-wide survey. **You choose which of these to consult** — nobody here has
   chosen them for you, and which ones you chose is part of what you report.
2. **Take the category names from those sources.** Not from your own sense of how the field divides,
   and not from any teaching sequence, course, roadmap or curriculum.
3. **Where sources disagree about a boundary, report the disagreement** rather than resolving it.
   Two sources splitting one area differently is evidence the owner needs, not noise to tidy.
4. **Merge only where two names are plainly the same category** under different labels, and say
   which two and on what basis.
5. **Report what you could not reach**, and what your chosen sources systematically miss.

**OUTPUT**

**Write the candidate list to `<OUTFILE>`.** Create it.

**Return to me only this:**

1. `## Sources used` — one line each: what it is, why you chose it, and its date.
2. `## Candidate areas` — one line per area: its name and the number of sources that carry it.
3. `## Disagreements` — boundaries the sources draw differently.
4. `## What this run could not see` — in full, as specified below.
5. `## Written to` — the file path and the number of areas in it.

**UNIT — one candidate area, every field filled**

```
NAME            the category name, as the sources call it. Not a name you coined
SOURCES         every source that carries this category: what it is, and its date.
                A category with no source is not reportable — drop it
ALSO CALLED     other names the same category appears under, with their sources
INCLUDES        what work is filed here, in the sources' own terms
EXCLUDES        what is filed elsewhere, naming the category it goes to instead
OVERLAPS        any other candidate area whose INCLUDES overlap this one, and how
SIZE SIGNAL     an absolute count with its source, or a ratio against a denominator
                the source itself defines. NEVER a share of "the field" or "all of AI":
                nobody can define that denominator, so nobody can check it.
                Write "none available" rather than estimating
SOURCE DISAGREES  where a source splits, merges or omits this category differently
```

**TARGET**

At most `<CAP>` candidate areas. **A cap, not a goal.** Report fewer complete units rather than more
incomplete ones. **Say whether you hit the cap**, and if so, which categories you left out and on
what basis — that is a finding about the cap, not a tidy-up.

**BUDGET**

25 searches, 20 fetches. Spend them on reaching the category listings themselves rather than on
reading about them.

**WHAT THIS RUN COULD NOT SEE**

Required, and judged as strictly as the list itself. **An honest account of what the instrument
missed is worth more than a longer list.**

- **Which sources you chose, and which you considered and rejected** — with the reason for each
  rejection.
- **What your sources systematically miss.** Work that is not submitted, reviewed or indexed
  anywhere is invisible to every source of this kind. Say so, and say what kinds of work those are.
- **Language.** Say which languages your sources are in, and that categories named only in other
  languages are absent.
- **Recency.** Each source's date. A category established since the newest source you read will not
  appear.
- **Anything you could not fetch**, and what you lost by it.

**FORBIDDEN**

- **Proposing a category no source carries.** If you think the field is missing one, say so under
  `What this run could not see` — never as a candidate area.
- **Using a curriculum, course, syllabus, roadmap, textbook contents page or learning path** as a
  source of categories. Those are teaching orders built for somebody else's purpose.
- **Saying which areas are most important, most active, most promising or most worth studying.**
  Not in the list, not in the headline, not in passing. That judgement is not this run's, and an
  ordering is an argument disguised as a report.
- **Ordering the list by anything but the alphabet.** A ranked list is a recommendation.
- **A number without what it is a ratio of**, and any share of "the field".
- **Resolving a disagreement between sources** by picking the one you find more convincing.
- **Reading any file in this repository.** It holds the planning documents for the book this feeds,
  and reading them would tell you what is expected rather than what is true. Project instruction
  files may be attached to your context automatically — **ignore them, and open no file except the
  one you are told to write.**

**PARTIAL**

If the budget runs out, report the complete units you have and name the sources you had not reached.
**A short sourced list with an honest coverage section is a complete result.**

**STOPPING RULE**

Stop when every candidate area has every `UNIT` field filled from a named source, **or** when the
budget is spent. Do not keep searching for a better carving — there is no better carving to find,
only more sources, and the coverage section is where that is reported.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** A
boundary you reported as disputed costs one reading. A boundary you reported as settled, wrongly,
becomes a research area and then a part of the book.

**DELEGATION: ZERO.** Do not start any sub-agent.
