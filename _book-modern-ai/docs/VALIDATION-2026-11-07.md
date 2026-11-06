# Validation of the research process — 2026-11-07

**What this is.** The owner asked for the research process to be *run* and its outputs *read*, so
that the decision to finalise the method rests on evidence rather than on the documents describing
it. This file records what was run, what reading each output found, and what is still untested.

**What this is not.** It is not the research. The area lists produced here are deliberately
disposable: the owner's plan is to delete `../research/` after this phase and run the method again
from scratch. **Nothing in this file is a book decision.**

**Method.** Each instrument ran as an isolated agent, because two of the briefs require a runner
that has not seen the planning documents and nobody here qualifies. **Every judgement below is from
reading the output file.** No finding rests on an agent's own summary of its work, and where a
count appears it was used to locate text that was then read. Two source pages were opened directly
to check an agent's claim against the source.

---

## What ran

| Instrument | Brief | Result |
|---|---|---|
| Framing run `e` | `briefs/TEMPLATE-area-frame.md` | `../research/frames/2026-11-07-e.md` — 104 areas, 1,235 lines, 10 sources, 12 searches, 19 fetches |
| Framing run `f` | same brief, same `<FIELD>` string | `../research/frames/2026-11-07-f.md` — 77 areas, 1,083 lines, 9 sources, 15 searches, 22 fetches |
| Consolidation | `briefs/TEMPLATE-area-consolidate.md` | see below |
| Scout | `briefs/TEMPLATE-area-research.md` | see below |
| Claim verifier | `briefs/claim-verifier.md` | see below |

Both framing runs reached both floors — five fetched sources of three kinds, ten searches — and
both reported their budgets. Neither started a sub-agent.

---

## Findings

Numbered for reference. Each says how it was established.

### V1 · The brief does not decide whether a third-party rendering of a taxonomy may be used, and the two runs split on the same URL

`TEMPLATE-area-frame.md` forbids "a curriculum, course, syllabus, roadmap, textbook contents page or
learning path" as a source of categories. Both runs found ACM's own classification pages returned
HTTP 403. Both then searched for another route, which the brief requires. They reached the same
alternative — a page on a textbook's website titled *ACM Computing Classification System* — and
**ruled on it in opposite directions.** Run `e` used it "only for ACM's category names, never as a
contents page". Run `f` rejected it as "a textbook's topic/chapter mapping, forbidden as a category
source even though it reproduces ACM CCS".

**Established by opening the page.** It reproduces the ACM 2012 artificial-intelligence subtree and
adds the textbook's chapter numbers in brackets beside each node. The category names are ACM's; the
bracketed numbers are the textbook's.

**What it cost.** The page shows *Search methodologies* and *Planning and scheduling* as children of
*Artificial intelligence*. Run `e` carries both. Run `f` carries neither, and its own coverage
section concedes it suspected they were there. **Two real categories were lost to a reading of the
brief, not to a limit of the field.**

**It also cost a resolved disagreement.** The page places *Machine learning* inside *Artificial
intelligence*; the university repository the other run used places it as a sibling. Run `e` found
the conflict and logged it unresolved, which is correct behaviour. Run `f` could not see it.

### V2 · The brief does not fix the level of reporting, so two runs of it are not comparable

The two runs overlap on seven sources and produced **104 areas against 77**. The clearest instance
is one benchmark body: run `e` took it at its suite level and reported ten areas; run `f` took the
label above and reported three. Both declared their level, which the brief requires. **The brief
asks each run to state its level and never asks two runs to use the same one**, so "run it twice and
compare" compares two different questions.

The consolidation brief is meant to resolve this, and step 4 of it does exactly that. But see V3:
resolution can only be applied to what was reported.

### V3 · Run `f` treated the same kind of object differently across two venues, and a live area disappeared

Run `f` reports four of one venue's special tracks as candidate areas, and its survey track. For a
second venue it took only the seventeen main-track submission areas and **reported neither of that
venue's two special tracks.** The word *alignment* does not occur anywhere in its 1,083 lines.

**Established by opening the second venue's own pages.** The site lists a *Special Track on AI
Alignment* and a *Special Track on AI for Social Impact* in the same navigation as the Main
Technical Track, and the areas page lists exactly the seventeen areas the run reported.

**Why it matters beyond this run.** The consolidation brief forbids adding any category no framing
run reported. So a category lost at the framing stage cannot be recovered downstream — it is absent
from the list the owner rules on, and nothing in that list shows it was ever a candidate.

### V4 · A run's own coverage report understated its weakest evidence

Run `e` reports that "36 of the 104 areas therefore say 'name only in the source'". **Reading every
record found 46.** The run counted the conference tracks and omitted ten benchmark-suite names that
are equally scopeless. So **44% of that run's records carry a name and a level and nothing else** —
no statement of what work the category includes or excludes — where its summary implies 35%.

Not a dishonest report: the sentence is about one source. But a reader of the summary gets the wrong
figure, and the figure is the one that matters, because a record with no scope cannot be judged
against any area rule.

### V5 · The isolation the framing brief requires was not delivered, and cannot be in this harness

The brief says to run "in a fresh session outside this repository, with no project file in its
context", and argues the point: "Telling an agent to ignore files already attached to it does not
work: it cannot unread them."

**Run `e` disclosed three project files injected into its context before it started** — the
website's instruction file, the website's handover, and a memory index. The memory index names a
note called *modern AI book objective*, which is about this book. The run reported all of it, as the
brief's coverage section requires, and stated it used none of it to name, shape, order or cut a
category. Run `f` reported none, so either it received none or it did not notice.

**The disclosure worked. The isolation did not.** An agent started from inside this project inherits
the project's instruction files. The brief's requirement is therefore unmet by construction, and the
only reason the leak is visible is that the brief asks for it to be declared.

### V6 · The `survey` source kind admits a document that files measurements rather than work

The brief's question is what categories the field files, reviews and presents **its own work**
under. The `survey` kind is defined as "the standing sections of a field-wide survey".

Both runs used an annual index report and took its eight chapters as candidate areas: the economy,
education, public opinion, policy and governance, research and development, responsible AI, science
and medicine, technical performance. **Those chapters file measurements of AI's effect on the world,
not submissions of AI work.** Eight of run `f`'s 77 and eight of run `e`'s 104 come from it.

The area rule drops that whole class, so the consolidator should reject all sixteen — which is the
system working. But the framing brief invited them, and a cheaper fix is to say in the `survey`
definition that the sections must be sections a body files *work* under.

### V7 · The missing role taxonomy is the source's absence, not the instrument's

Across five independent runs now, every attempt at a named job board's categories failed the same
way: the site exposes free-form tags and per-role listing pages but publishes no browse-by-category
taxonomy, so there is no level to take. Both fresh runs searched for it and said so.

**So the gap is real and not a sampling failure.** No occupational category — research engineer,
machine-learning engineer, MLOps, data engineer — appears in any list. Given that the book exists to
make the owner a strong candidate for four named roles, this is the most consequential hole in the
evidence, and no further framing run will close it.

### V8 · One standards body has defeated every run, and it holds categories nothing else carries

The international standards subcommittee for artificial intelligence returned HTTP 403 in all five
runs. Both fresh runs name it as their largest single loss, and both say what is missing with it:
conformance, certification, risk management, terminology and use-case documentation. **No source
reached by any run carries a category for any of those.**

### V9 · Nothing checks that a brief was filled in correctly

The completeness review brief takes nine filled slots, among them the ledger of what the reader has
already been taught and the field's shorthand. Its own text says that for one class of error "no
gate can catch this, so it is yours" — meaning the reviewer's, which depends entirely on those
slots being right.

**Established by reading the record template and the record gate.** The record carries one
checkbox — that the pass was "launched with the brief in `briefs/`". Neither the record nor any of
the fourteen gates records or checks what the nine slots contained. A stale ledger silently disables
the cross-chapter checks and leaves a clean verdict behind.

### V10 · The two runs read different editions of the same venues, which is the main cause of their divergence

Run `e` opened one conference's 2026 call and another's 2026 call; run `f` opened the first
conference's 2025 call and a third venue's 2025 call. Both opened the same engineering programme,
`e` the 2026 edition and `f` the 2025 one — and those two editions have different track lists, which
alone accounts for about thirty of the differing names.

The brief names no venue and no edition, and it must not: "an instrument told what to expect finds
it." **But the consequence is that two runs of it cannot be compared the way the brief intends.**
The brief says to read agreement as "no disagreement found" rather than as confirmation. The reverse
needs saying too: **disagreement between two runs may only mean they read different years.**

### V11 · Running the method again today, twice, did not reproduce what it found yesterday

The two fresh runs name 138 distinct categories between them. The four earlier runs named 251.
**158 of the earlier names appear in neither fresh run.**

Most of that gap is wording — *Computer vision* against *Computer Vision*, *Multiagent systems*
against *Multiagent Systems (MAS)* — and reading the lists side by side shows the real agreement is
much higher than a name match suggests. **But at least two families are genuine losses, and both
were checked by reading the earlier records in full:**

| Lost | What the earlier record holds | Found by |
|---|---|---|
| **AI Alignment** | A refereed special track beside a major venue's main track, with its sub-topics named: scalable oversight, mechanistic interpretability, empirical robustness evaluation, red-teaming, safe-by-design engineering | **Both** earlier runs, independently |
| **The five working groups of the international standards subcommittee** | Foundational standards · data · trustworthiness · use cases and applications · computational approaches — each with its level, its includes and its excludes | One earlier run |

**So a later run of this method is not a superset of an earlier one.** The method does not converge:
it samples, and each sample misses different things. See V12 for the other half of this picture.

### V12 · An earlier run attributed a source it had not opened

The five standards-body records in the earlier run carry `SOURCES … FETCHED`. **That run's own
coverage section says the subcommittee's page returned HTTP 403 and that the working-group titles
were reached through a general encyclopaedia.** The brief requires a source not opened in the run to
be marked `RECALLED`, and separately forbids treating a secondary summary as a source.

Those five records therefore state their evidence more strongly than the run's own account of how it
got them — and they are **the same five categories the fresh runs lost.** The earlier files are
larger; they are not uniformly sounder.

### V13 · The framing stage is the weakest link, because its losses are the only unrecoverable ones

The consolidation brief forbids adding a category no framing run reported. The owner rules on the
consolidated list. So a category lost at framing — whether by a brief ambiguity (V1), an
inconsistent level choice (V3), or simple sampling (V11) — **never reaches the decision, and nothing
in the list records that it was ever a candidate.**

Every other stage can be audited against its input. This one cannot, because its input is the
world.

### V14 · One run read its chosen level incompletely, and lost the two most distinctive categories at that source

The two runs took the same benchmark body at different levels, which V2 treats as a brief gap. **The
source itself was then opened to see whether either run had simply misread it.**

The page carries a *Benchmark Suites* section with three category labels — safety, training
algorithms, and performance — above **twelve** named suites.

| Run | Level taken | Reported | Verdict on reading the page |
|---|---|---|---|
| `f` | the three labels | all three | **Complete.** Its safety record names the safety suite as its content |
| `e` | the twelve suites | **ten** | **Incomplete.** It omitted the safety suite and the training-algorithms suite |

The ten it kept are all performance suites differing by deployment setting. **The two it dropped are
the only two that measure something else** — whether a system is safe, and whether a training
algorithm is faster. So the finer level, read incompletely, carried *less* information than the
coarser one.

This is not a brief gap. The brief's `TARGET` says "every category your sources name, with no
exceptions and no selection rule of your own." **The run failed its own instruction**, and said
nothing about it in its coverage section.

### V15 · Nothing reviews a research run. Every defect above was found by hand or not at all

This is the finding that matters most, and it is about the method rather than any run.

The project has four review passes and fourteen gates. **All of them read a chapter.** There is no
reviewer for a framing run, a consolidation run or a scout run — no second agent, no gate, no
checklist. The briefs ask each run to report its own coverage honestly, and both fresh runs did so
at length and with real candour.

**But self-reporting found none of these:**

| Finding | Could the run have reported it? |
|---|---|
| V3 · a venue's special tracks omitted while another venue's were kept | No — it did not notice |
| V4 · scopeless records undercounted by ten | No — it stated the lower figure |
| V12 · a source attributed as fetched that was not opened | No — the record and the coverage section contradict each other |
| V14 · two of twelve categories dropped at the chosen level | No — not mentioned |

Each was found by reading the output file against the brief, and three of them required **opening
the source page to check the run's claim.** That work took one person about an hour per run and it
is not in the process anywhere. **The research half of this project has no verification stage at
all**, while the writing half has four.

### V16 · One venue's area list has now defeated all six runs, and one claim about it is unverified

A fourth major venue reviews by area but publishes the list only behind its submission system. An
earlier run found a third party's repost carrying fourteen of its area names — among them two that
**no other source on any list names** — and rejected it, because the venue's own page carries no
list to check the repost against. Both fresh runs reached the same dead end independently.

**The V1 fix does not rescue this.** That fix permits a faithful reproduction of a *classifying
body's own taxonomy*; a third party's repost of a conference call is not that, and there is nothing
to verify it against. So the hole stands, and it is the second-largest after the standards body.

**One thing I could not check.** Run `f` states that this venue's main call lists no areas at all.
The page would not load for me either, so **that claim is recorded as the run's, not as verified.**

---

### V17 · The consolidator judged a fifth of the area list from category names, which its brief forbids in those words

**The run itself did well on the two rules that were hardest to keep.** It gave all 181 records
exactly one verdict with no arithmetic gap; every rejection cites a kind and **not one cites
importance**; it added no category, and where the rule implied an area neither run had reported — the
operation of a deployed system — it said so under what it could not settle instead of inventing it.
Its account of its own doubts runs to two pages and names the merges to undo first.

**It broke the other one.** Its brief says: "**Judge from the record, not from the name.**"

**Fourteen of the 69 areas carry `COVERS: name and level only in the source` and `EXCLUDES: not
stated`** — the record contains a category name, the level it sits at, and nothing else. For each,
the run wrote a `WHY` that paraphrases the name:

| Area | The `WHY` written for it | What the record held |
|---|---|---|
| Graphs | "learning on graph-structured data" | the word *Graphs* |
| Harness Engineering | "the harness a model runs inside" | the two words, restated |
| Computer Use | "models operating a computer" | the two words |
| Inference | "serving models" | the word |

The other ten are Context Engineering, Data Quality, Design Engineering, Local AI, Memory &
Continual Learning, Posttraining & Midtraining, Robotics & World Models, Sandbox & Platform
Engineering, Vision & OCR, and Voice & Realtime AI.

**The correct verdict was available and defined.** `UNCLEAR` means "the record does not settle it",
and the run used it six times — but only where a *name pointed two ways*, never where the *record
was empty*. Where the name pointed one way, it followed the name.

**The run disclosed the problem and issued the verdict anyway.** Its coverage section says: "'AREA'
on an applied track means no more than 'a track name that denotes AI engineering'." That sentence is
an accurate description of a defect, filed beside the output it describes.

**Why this one matters most.** It is where the chain converts nothing into something. A conference
publishes a track title; the framing run reports it faithfully, which is correct; the consolidator
must give it a verdict and has nothing to judge, so it judges the title; and an area enters the list
the owner rules on. **Downstream it gets worse**: each approved area becomes a scout's `<SCOPE>`,
and a scout handed "Harness Engineering" with no source scope would supply one itself.

**Fixed in `briefs/TEMPLATE-area-consolidate.md`**: a record carrying no scope from its source cannot
receive `AREA`.

---

## What held, checked the same way

An honest account has to say what the instruments got right, or the findings above read as a verdict
on the method rather than a list of repairs.

**The consolidation run was checked against seven of its brief's rules. Six held.**

| Rule | Held? | How it was checked |
|---|---|---|
| Every record gets exactly one verdict, none unaccounted for | **Yes** | The arithmetic closes twice: 104 + 77 = 181, and 116 area records + 18 + 10 + 18 + 13 + 6 = 181 |
| **Never reject for being unimportant** — only on kind | **Yes** | Every rejection in the file was read. Each names the clause of the rule it fails. **No rejection anywhere appeals to size, activity, fashion or worth** |
| A borderline rejection must reach the owner | **Yes** | The closest call — a category rejected on a one-line gloss while its near neighbour was kept — is marked **Close** in the table and carried into its own section, with the reason |
| Add no category the runs did not report | **Yes** | The rule implies an area neither run named — the operation of a deployed system. The run put it under what it could not settle and **did not add it** |
| Resolve the level, and name what sits below rather than dropping it | **Yes** | It chose one level, argued for it from what differs in the work, and listed what the choice demotes — then said which of its own choices it thinks may be wrong, and why |
| Order by nothing but the alphabet; no scores | **Yes** | Read the list |
| **Judge from the record, not from the name** | **No** | V17 |

**Both framing runs also kept the rule they were most likely to break.** Neither filtered its list,
neither invented a cutting rule, and both reported categories their own text calls audience
groupings or session formats rather than quietly dropping them — one writing, on an audience
category, "I have left it on the list rather than apply a rule of my own." **That is exactly the
defect the brief's first two runs committed yesterday** — each capped its own list and invented its
own rule for cutting it — and the fix made after them held today, twice.

**The disclosure rules worked where the isolation rules did not.** Two of the three runs named the
project files injected into their context and said what each contained. That is how V5 is known at
all.

---

## The cost inventory, for the overengineering question

Facts, counted from the files. The verdict they support is at the end of this document, after the
remaining runs.

**What the method specifies, and how much of it has ever run:**

| Part | Specified | Built | Ever run |
|---|---|---|---|
| Briefs, one per agent role | 8 | — | **2** (framing, consolidation) |
| Chapter review passes | 4 | — | **0** |
| Gates | 14, over 16 scripts | **0** | **0** |
| Roadmap steps | 11 | — | 3 closed, now on step 4 |
| Approval points per cycle | 5 | — | 0 cycles run |
| Mistake classes recorded, with instances | 13 | 10 mechanised | — |
| Decision markers in use | 5 | — | — |

**What one chapter will cost, from `PROCESS.md` §6 and `GUIDE.md` §12:** six loop steps; four
review-pass agent runs; a book-wide sweep after each pass's findings, counted before and after; all
fourteen gates `CLEAN` or `VACUOUS` with a reason; every command and code sample run; the lab run
from the chapter text alone in a fresh folder; a record whose hash is written last, so any later
edit makes it stale; four ledger and ownership files updated; and a driver program with four stages
that each refuse to advance.

**Where the verification actually sits:**

| Half of the project | Verification stages | Work done so far |
|---|---|---|
| **Writing a chapter** | 4 passes + 14 gates | **Nothing. No chapter exists** |
| **Research** | **None** | 6 framing runs, 1 consolidation, 1 scout |

**What the documents still leave open.** 22 statements marked `[OPEN]` and 50 marked
`[I RECOMMEND]`. Reading each `[OPEN]` site, they reduce to seven real decisions, and **four of the
seven cannot be taken before the research reports**: the book's structure, breadth against depth,
the mathematics boundary, and which area goes deep. Two more need cycle 1 to have happened: whether
the revision cost, the acceptance rule for contested material, and ownership moving between cycles
are solved. **The seventh is a genuine gap with nothing behind it** — `GOAL.md` records that no file
owns the reading order, and says so in those terms: "this requirement rests on nothing."

**Where the last two days went.** Of the 43 findings fixed yesterday, the file recording them says
31 were created in the preceding two days by the fix rounds themselves. **Today's 16 findings came
from running the instruments, and 3 of them could only be found by opening a source page.** That is
the measurement the overengineering question needs: the marginal return on re-reading the documents
had fallen to near nothing, and the marginal return on executing them is high.

---

## What this phase cannot test at all

- **The four chapter review passes and the fourteen gates.** All of them read a written chapter or a
  built document. No chapter exists, and none will in this phase.
- **The exclusion lists.** The scout brief requires every area's exclusions to be written for all
  areas in one sitting, "because writing them one at a time is how two areas end up both claiming a
  subject or neither claiming it". One scout runs here, so there is no sibling area to collide with,
  and the failure that rule prevents cannot occur.
- **The sixteen gate scripts.** None exists. Step 10 has not started.
