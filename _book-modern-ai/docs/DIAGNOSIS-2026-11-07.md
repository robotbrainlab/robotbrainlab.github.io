# Why the second pair of framing runs looked worse, and what changes

**Supersedes `VALIDATION-2026-11-07.md` V8 and V11.** Both were wrong. This file says how.

**Method.** Every number below comes from opening the six framing files, the merged list and the
consolidated list and reading them. Where a count appears it was used to find text that was then
read. Two claims — that a standards body was unreachable, and that a refereed alignment track was
lost — were checked by opening the records that carry them.

---

## 1. The answer

**The second pair was not worse. The comparison was invalid.** It put 254 against 69, and those two
numbers count different things:

| | What it counts |
|---|---|
| **254** | Every distinct category name across **four** runs, **before any rejection**. `MERGED-CANDIDATES.md` says so in its own first line: "not a proposal", every name any source carried — application domains, session formats, audiences and product names included |
| **69** | The categories from **two** runs that **survived a rejection rule on kind** and were then merged. The consolidator gave all 181 records a verdict: 69 `AREA`, 18 `DOMAIN`, 10 `RECORD`, 18 `FORMAT`, 13 `PRODUCT`, the rest merged or `UNCLEAR` |

**The rejection rule never ran on the 254.** Had it run, roughly a third of that list would have gone
the same way — it contains the same domains, formats and product names, because the brief requires a
run to report them.

**So three of the four differences are arithmetic, not quality:** two runs instead of four, 19
source-reads instead of 41, and a filter applied to one list and not the other.

**Two losses are real**, and neither is explained by the above. Section 3 gives the cause of each.

## 2. Why no comparison between runs was ever possible

Per-source output, which is the only normalisation available:

| Run | Sources opened | Records reported | Records per source |
|---|---|---|---|
| `c` | 12 | 86 | 7.2 |
| `d` | 15 | 209 | 13.9 |
| `e` | 10 | 104 | 10.4 |
| `f` | 9 | 77 | 8.6 |

**The two runs of the first pair differ from each other by more than the pairs differ.** Run `d`
reported nearly twice as much per source as run `c`, and both ran the same brief on the same day.
`MERGED-CANDIDATES.md` already knew why: "`c` took mostly top-level categories, `d` went a level
deeper on several sources — **so these two differ in resolution, not in content**."

**That is the finding.** Three things set a run's total — how many sources it opened, which editions
it opened, and how deep a level it took — and **the brief fixed none of them.** A difference between
two runs could therefore never be attributed to anything. **Including an improvement.** Two days of
brief work could not be measured, because there was nothing holding still to measure it against.

Part of the second pair's output was also junk by the brief's own new rule: both runs read an annual
impact report as a `survey` source, and **10 of the 181 records came from its chapters and were
rejected as `RECORD`.** The brief fix of 2026-11-07 excludes that source. So the second pair's real
yield is better than its raw count, not worse.

## 3. The two real losses, and the one cause behind both

| Lost | Where it was | Why the second pair missed it |
|---|---|---|
| **AI Alignment** — a refereed track with eleven named subjects | Runs `c` and `d`, both from the AAAI **main technical track call**, which names the special tracks beside the main track | Runs `e` and `f` read a **different page of the same venue** — a later cycle's "areas and topics", which lists main-track areas only and carries no special tracks |
| **Five standards working groups** — foundational standards, data, trustworthiness, use cases, computational approaches, each with its own includes and excludes | Run `d` only, via a Wikipedia page quoting the subcommittee's own titles, after the body's own site returned 403 | Runs `e` and `f` hit the same 403. **Run `e` searched once, gave up, and wrote that this was "the single biggest hole" in its list** |

**Read that last cell again.** The route had been found the day before and written down in the same
directory. Run `e` could not know, and was right not to: the brief forbids it from reading project
files, so isolation is real. **The defect is that nothing carried the discovery across.** The same
thing happened three times over with the ACM classification — runs `c`, `e` and `f` each hit the same
blocked page and each spent searches hunting its own route.

**The cause is one sentence in the framing brief:**

> **You choose which sources to consult. That choice shapes the answer, so it is part of what you
> report.**

and the rule that backed it: *"This brief names no area, no subject, no venue, no index, no vendor and
no expected outcome … An instrument told what to expect finds it."*

**The reasoning is right about categories and wrong about sources.** A source is a place to look, not
an answer. Naming the arXiv taxonomy tells a run where to read and nothing about what it will find
there, because the page decides that. **The brief conflated "do not tell it the answer" with "do not
tell it where to look"** — and so every run re-drew its own input. **Only two sources were opened by
all six runs.** Four venues were read at different editions.

**Every improvement went into the reporting rules. None could reach the input.** That is the whole
answer to "why did better instructions not produce better results".

## 4. Two findings of mine that were wrong

**V8 said the standards body's 403 was a permanent limit of the world.** It is not. Run `d` reached
that content through Wikipedia, and its five records are in this repository with full includes and
excludes. **I recorded a limit as permanent while a run in the same directory had already got past
it.** This is the worse of the two errors, because it told the owner to accept a gap that was closed.

**V11 said the method does not converge, and that framing runs must therefore be unioned across
cycles forever.** Non-convergence is not a property of the method. It is the symptom of an
unspecified input, and it goes away when the input is fixed. **I stated a law where there was a bug**,
and the cost of believing it would have been a permanent union of every run ever made.

Both are withdrawn in `ROADMAP.md`. The dated files stay, as evidence of what a source carried on a
date — not because the method cannot settle.

## 5. The changes

**Four. Three of them delete work.** Nothing here adds a brief, an agent, a gate or a script.

1. **A source register — `research/frames/SOURCES.md`.** Every filing system any run has opened, with
   its URL, its kind, **the level to take**, what it was already found to carry, and the route round
   it where it blocks. **Built from the six runs; no new research.** The brief now pastes it in whole,
   the way the consolidator brief pastes in the area rule, and says: open every one of these. A run
   may spend four searches finding sources the register lacks and **reports at most two for addition**
   — the owner adds them, not the run. So discovery survives, and it accumulates.
2. **A regression floor, for free — and the run is not shown it.** The register records what each
   page was already found to carry, in a `CARRIES` column that is **deleted when the register is
   pasted into the brief.** The run gets the URL, the kind, the level and the route round a block; the
   owner keeps what the page was found to hold. **A run shown the answer can report it back without
   establishing it, and the check would then compare the run's output against text the run was
   handed.** So: a run that opens a registered page and reports less than the withheld floor has
   failed, visibly, without anybody opening the page. **This is the first check the research half has
   ever had**, and it closes the open decision from V15 without the verification stage I was going to
   propose.

   **This is also where the register could have gone wrong, and nearly did.** The brief's oldest rule
   is that an instrument told what to expect finds it. **A URL and a level are not an answer** — "open
   this taxonomy at the category level" says where to read, and the page decides what is there. **A
   list of expected categories is an answer.** That line is what makes a source register compatible
   with the rule it sits under, and the first draft of this change crossed it.
3. **One framing run per cycle, not a pair.** The pair existed for exactly one reason, stated in
   `research/frames/README.md`: to show when a division was "an artefact of whichever sources one run
   opened". **With a register there is no source choice, so there is no such artefact.** What the pair
   was really detecting was the brief's missing input — and it detected it by producing two
   incomparable lists instead of naming the cause. **Half the cost of step 4, every cycle.**
4. **The briefs are frozen.** No further edit to any brief without a run that failed and shows the
   defect. Measured reason: **31 of the 43 findings of 2026-11-06 were created by the fix rounds
   themselves**, and the seven fixes of 2026-11-07 are themselves untested. The register is the last
   change made without a failing run, and it is justified by one: run `e`'s.

**Unchanged, deliberately.** The gates recommendation stands as written — build five before chapter
one, defer nine. The consolidator, the scout and the claim verifier are not touched: the claim
verifier caught a real error on its first run, and the consolidator's one real defect was fixed in
its brief this morning.

## 6. How to know whether this worked

**One run, and a test with a known answer** — which has never existed on this project before.

| Check | Pass |
|---|---|
| **Coverage** | Every source in the register opened or accounted for by name |
| **Regression** | Nothing reported thinner than the register's `CARRIES` floor without a stated reason |
| **The two known losses** | **AI Alignment and the five standards working groups are both back.** The run is told to open the pages that carry them and is **not** told that they are there, so recovering them is evidence and missing them is a failure of reading rather than of sampling |
| **Comparability** | The run's level per source matches the register's, so its totals mean something against the next cycle's |

**Cost: one framing run, and about an hour of reading to check it.** If the two known losses come
back and the coverage is complete, the input problem is closed and step 4 can proceed to the owner's
ruling. **If they do not come back, the fault is in the run's reading**, which is a different and much
narrower problem than the one diagnosed here.

**What this does not test.** The writing half — the chapter loop, the four review passes, the fourteen
gates — remains untested and cannot be tested without a chapter.

---

## 7. The test was run, and it passed

**Run `g`, 2026-11-07.** One framing run, over the register, in an isolated agent with the register's
`CARRIES` column removed from its copy. The pass conditions were written down **before its output
existed** and are in `CHECK-run-g-2026-11-07.md`. Output: `research/frames/2026-11-07-g.md`, 283
categories, 3,211 lines. **Every judgement below is from reading that file**, and the two pages the
whole test turns on were opened by hand in the browser before the run finished.

### The result against each condition

| Condition | Result |
|---|---|
| **All 19 registered sources opened** | **Pass.** All nineteen, each named in its coverage section. This is the **first run of six to open every source** — the previous best was 15 of a self-chosen set |
| **The alignment track recovered** | **Pass.** Reported with the page's own words, and with the page's own Summary counting *"Three technical tracks (Main Track; AI for Social Impact; AI Alignment)"* — which is exactly what I read at the source myself. The run was not told it was there |
| **The standards working groups recovered** | **Pass, and better than the floor. Eight, not five.** It found the three joint working groups — testing of AI-based systems, AI enabled health informatics, functional safety and AI systems — that run `d` missed on the page it alone had reached |
| **Nothing below a floor without a reason** | **Pass.** Every floor met or exceeded |
| **Nothing from "do not read"** | **Pass.** No trace of the excluded report or the textbook-site mirror anywhere in the file |
| **No searches on the unreachable sources** | **Pass.** 4 searches of 25, all four on discovery |
| **No filtering** | **Pass.** No threshold, no tiebreak, no cap, alphabetical only |
| **Discovery reported, not added** | **Pass.** Two sources reported for the owner — a model hub's task vocabulary, and the European standards committee writing the AI Act's standards. **Neither appears in the candidate list** |

### What it recovered that nobody had asked it to

**Four nodes of the ACM classification that runs `c`, `e` and `f` all lost** — distributed computing
methodologies, symbolic and algebraic manipulation, planning and scheduling, and search
methodologies. One registered route renders that scheme only partially; the register names a second
route, and the run used it. **Those four were lost three times before by runs that had no second
route to use.**

### Two of my own floors were wrong, and the run was right

1. **I had the benchmark-rules source at 10 Areas. It holds 7.** My floor added the two tables' rows
   and double-counted the three Areas that appear in both. I read all seven records to establish
   this; the run states which table each Area sits in, and the arithmetic comes out 6 + 4 with 3
   shared.
2. **I expected 8 units from the archive taxonomy and got 7.** The run merged two categories that
   carry the *same name* at that source, named both with their own descriptions, and recorded the
   split as a disagreement citing the rule that only another source may split a category. **A
   documented, reversible merge, not a loss.**

**This is the check working on me as well as on the run.** A floor I wrote from an earlier run's
report was wrong in one place and over-strict in another, and reading found both.

### The one finding against the run

**It moved 32 labels into appendices instead of reporting them as units.** Room names, stages, days,
an audience, a session format and a few placeholders — all at the registered level, all listed in
full with reasons, none hidden. **But deciding that a label is a format rather than an area is the
consolidator's verdict**, and that run has six verdicts for exactly this. Doing it a stage early
routes those labels around the stage the owner reverses decisions at. **Mild, visible, reversible —
and fixed in the brief**, which now says every label at the registered level goes in the main list
with its nature stated, and that an appendix is not an option.

### Three corrections the run made to the register, all applied

1. One route's URL resolves to a different node than the register intended; the register now names
   both nodes it means. The run reported the under-specification rather than guessing.
2. One URL form of that route returns 403 where the other works. Recorded, so no run loses a fetch
   to it again.
3. One programme source has rolled to the next event year and now needs two fetches, so the two
   programme entries are two editions rather than two views of one.

### Verdict

**The input problem is closed.** The register did what it was built to do: coverage was complete,
both known losses came back, four further losses came back unasked, and the two things that went
wrong were a floor of mine and a decision taken one stage early. **The method now accumulates** —
every floor in the register is higher tonight than it was this morning, and floors never fall.

**What this still does not test.** The writing half — the chapter loop, the four review passes, the
fourteen gates — remains untested and cannot be tested without a chapter. **And one caution about
this result**: a single run passing is evidence that the register works, not proof that every future
run will read every page properly. The check is cheap and should be run every cycle.
