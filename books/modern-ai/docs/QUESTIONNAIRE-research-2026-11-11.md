# Questionnaire — every decision in the research process

**Why this exists.** 88 things govern this project that you never ruled on: 53 are my proposals, 26
are marked undecided, and 9 I acted on because you did not answer in time. This questionnaire puts
the ones that touch research in front of you, in plain words, so you decide them.

**How to answer.** Write your answer under each question. "Keep as is" is a real answer and the
fastest one. "I don't know yet" is also real — it tells me to leave the item marked undecided
instead of guessing. **Do not feel you must answer all of them in one sitting.** Part 9 is the part
that is actually broken; Parts 1–8 are mostly confirming or changing things that already work.

**`[2026-11-12]` There are 60 questions, not 49.** Parts 1 to 8 hold 45, Part 9 holds 11 and Part
10 holds 4. **I called it 49 from the day it was written**, in the file's first commit and in every
message since, because I counted the lines matching `**N.M**` and Part 9's questions are written
`**9.1 The stage that…**` — a different shape, so the count never saw them. That is class M in
`GOAL.md` §11: a pattern match answering a question about meaning.

**`[2026-11-12]` All 60 are answered.** Parts 1 to 10 each carry an `ANSWERED` section with the
ruling and the files it changed. **What is still open is the space at the end of this file** —
anything the questionnaire did not ask.

**Words I will not use without explaining them:**

| Word | What it means here |
|---|---|
| **Framing run** | One search for how the field sorts its own work into categories |
| **Consolidation** | Merging the framing runs into one list, removing duplicates |
| **Area** | A big division of the field — "Computer vision", "Reinforcement learning" |
| **Subject** | A thing inside an area that could become one chapter |
| **Claim** | A single factual statement the book makes, with a source |
| **Gate** | A program that checks a finished chapter and refuses it if something is wrong |
| **Pass** | A review by an AI agent that reads a draft chapter |

---

# Part 1 — What the research is for

**1.1** Your stated goal is to become a strong candidate for AI Researcher, Research Engineer, AI
Engineer and Machine Learning Engineer. Everything in the research is judged against that.
**Is that still exactly right, or has it changed?**

**1.2** You said the aim is a **research-oriented engineer** — someone who understands the science,
follows the research, and can build. The research keeps an area only if it has **both live research
and live engineering**. An area with only one of the two is cut.
**Is that the right test, or should an area with only one still be covered?**

**1.3** Robotics. I cut it, then found that half of robotics hiring — perception, robot learning,
vision-language-action models — is exactly your target roles, and put it back. The other half
(mechanical, electrical, control theory, functional safety) I keep out.
**Is that split right? Or is robotics fully in, or fully out?**

**1.4** The research reports, for each area, how big it is, how concentrated, how widely adopted and
whether it is growing. It is forbidden to report "X% of AI", because nobody can define the total.
**Do you want those four measures kept, or are some of them not worth the budget they cost?**

---

## Part 1 — ANSWERED 2026-11-11

| # | Answer |
|---|---|
| 1.1 | **"AI: Research and Engineering. Simple and Clear."** The goal is stated as a field, not as four job titles |
| 1.2 | **Keep both required.** An area needs live research AND live engineering |
| 1.3 | **Split as described.** Perception, robot learning and vision-language-action in; mechanical, electrical, control theory and functional safety out |
| 1.4 | **Keep all four measures** — size, concentration, adoption, growth |

**What 1.1 changes, and it is not small.** The test was "does this serve AI Researcher, Research
Engineer, AI Engineer or Machine Learning Engineer". It is now **"is this the research of AI or the
engineering of AI"**. That is a test about the field, not about a job advertisement — and the
robotics cut I made was argued entirely from job titles, which is no longer the question being
asked. The answer to 1.3 stands on its own evidence and is unaffected.

**One thing 1.1 leaves open and 3.2 must settle:** the book is called *Research, Science and
Engineering*, and the consolidation rule keeps a category if it belongs to **any of those three**.
1.1 names two. Question 3.2 asks whether science stays as a third mode.

# Part 2 — Finding the areas (framing runs)

**2.1** You revoked the fixed source list today. Each run now finds its own sources.
**Confirm: every future research cycle starts from nothing, with no list, no routes and no earlier
findings?**

**2.2** Because runs now differ, there must be more than one, and their results are **combined, not
compared** — if one run finds a category and the other misses it, the category is kept.
**Is two runs right? Three? And is combining them correct, or should a category only count if more
than one run found it?**

**2.3** A run must use **at least 8 sources across at least 4 of 5 kinds** (conference categories,
archive classifications, meeting programmes, field surveys, industry taxonomies).
**Are those numbers right? They are mine, not measured.**

**2.4** A run must spend **at least 10 searches** looking for sources, out of a budget of 25
searches and 25 page-fetches.
**Are those numbers right?**

**2.5** A run may not use a course, syllabus, roadmap, textbook contents page or learning path as a
source of categories — only how the field files its own work.
**Keep this? It excludes some well-organised material.**

**2.6** A run must report every label it finds at the level it chose, **including ones that are
obviously not subjects** — room names, session formats, company sizes. Deciding they are not areas
happens later.
**Keep this? It makes the lists longer and noisier.**

**2.7** When a source gives only a bare name with no description, the run must say so in those
words, and may not write its own description. This is the rule that was broken when a run invented
"graph-shaped data and knowledge in AI applications" for a track called *Graphs*.
**Keep this?**

**2.8** A run must not order the list by anything but the alphabet, and must not say which areas
matter most.
**Keep this?**

**2.9** Runs happen at step 4 only, and again only if you approve a full re-carving of the areas.
They do **not** happen every cycle.
**Is that right, or should the areas be re-checked every cycle?**

---

## Part 2 — ANSWERED 2026-11-11

| # | Answer |
|---|---|
| 2.1 | **Science stays.** "You can consider AI: Research, Science and Engineering. I missed the Science part previously." The book's title and the three-mode rule both stand |
| 2.2 | **Nothing is carried between runs.** No source list, no routes, no earlier findings |
| 2.3 | **Combine: keep everything either run found.** A category one run found and the other missed is kept |
| 2.4 | **Source floor stays at 8**, "keep a buffer if it is needed" |
| 2.5 | **At least 4 of the 5 kinds**, with his reasoning: *"research without engineering at least for me is pointless, because we should know what we are up to"* |
| 2.6 | **Find a route to role and job categories.** The gap must be closed, not just recorded |

**`[STATED 2026-11-11]` The 4-of-5 rule gains a floor inside it, on evidence from the two runs.**
Both runs met 4-of-5 and both still came back reporting the **same single gap: no source that files
AI work by job or role.** Run `h` also recorded that 36 of its 172 labels came from one commercial
programme — so the engineering side of its list rested on a single source. **4-of-5 can be satisfied
while dropping the one kind that carries engineering**, which is the kind the owner says the book
exists for. So: at least 4 of 5, **and at least one of them must be `practitioner`.**

# Part 3 — Turning the runs into one list (consolidation)

**3.1** One agent reads the framing runs and gives every category one verdict: it is an area, or it
is a domain (AI applied to another field), or a format, or a product name, or unclear.
**Keep this step, or should the framing runs go to you directly?**

**3.2** The rule it applies is the book's own title: a category is an area if it belongs to **the
science of AI, the research in AI, or the engineering of AI** — and engineering includes its tools,
its measurement and its operation.
**Is that the right test?**

**3.3** This agent **may reject a category for not being an area, and may never reject one for being
unimportant.**
**Keep this split?**

**3.4** When a category has no description from its source, the agent must mark it **unclear** and
send it to you undecided, rather than guessing.
**Keep this?**

**3.5** The agent must pick one level of detail — for example, taking a conference's 12 broad topics
rather than its 37 narrow ones — and file the finer ones underneath.
**Keep this, or should every level be reported flat?**

---

## Part 3 — ANSWERED 2026-11-11

| # | Answer |
|---|---|
| 3.1 | **Sort first.** An agent gives every entry a verdict before it reaches the owner |
| 3.2 | **Settled by 2.1** — the three modes stand: science, research, engineering |
| 3.3 | **Keep the split.** The sorting agent may reject on kind, never on importance |
| 3.4 | **No description means undecided, and it is sent to him** — never thrown out, never guessed |
| 3.5 | **Take the broad level, keep the detail filed underneath** |

**All four confirm the design as written.** Nothing changes in
`briefs/TEMPLATE-area-consolidate.md` except what Part 2 already required: it now unions two or more
independent runs instead of reading one.

# Part 4 — Choosing what the book covers

**4.1** After the list exists, **I propose which areas the book covers**, with a written reason for
each one kept and each one cut. You approve, redraw or reject that proposal.
**Confirm this is what you want. You have said so; I am asking once more because I got it wrong
four times.**

**4.2** The proposal must account for **every category the consolidation produced** — not just the
areas, but the merged names, the ones filed underneath, the rejections and the undecided ones.
**Keep this? It makes the document long.**

**4.3** Every cut must name what goes with it: the finer categories underneath it, and any subject
only one source mentioned.
**Keep this?**

**4.4** Each cut gets **its own reason**. Group reasons are forbidden — the failure was ten areas cut
under one paragraph.
**Keep this?**

**4.5** The five best-attested cuts must each carry a sentence answering "why is the field's
most-filed subject not in my book?", and must be marked if the reason rests on an assumption about
your career rather than evidence.
**Keep this?**

**4.6** If you do not rule within **7 days**, I act on my own recommendation, mark it as mine, and
you can reverse it later.
**Is 7 days right? Longer? Or should nothing ever proceed without you?**

---

## Part 4 — ANSWERED 2026-11-11 (4.1 reopened)

| # | Answer |
|---|---|
| 4.2 | **Account for everything** — all ~300 entries, not only the areas |
| 4.3 | **Name what each cut takes down with it** |
| 4.4 | **One reason per cut.** Group reasons forbidden |
| 4.1 | **Not answered — he asked a better question back** (below) |

**4.1, in his words:** *"But do you recommend that it's necessary that I have to judge, because how
will I know? If I know already, why would I do research in the first place?"*

**He is right, and `GOAL.md` §3.3 already agrees with him** — it calls asking him to partition the
field circular, *"because that knowledge is what the book exists to give him."* The retraction
covered authoring the list. **It did not cover ruling on it, and the same circularity applies to
most of that ruling.**

**The distinction I had been missing.** Two different questions get bundled into "rule on the list":

| Question | Who can answer it |
|---|---|
| Is this a real division of AI? Is this boundary drawn where the field draws it? | **The sources.** He cannot know this and should not be asked |
| Does this selection serve what I want? Is robotics in my future? Would I take a job in evaluation infrastructure? | **Only him.** No source and no agent can answer it |

**So the ruling narrows.** He is not shown 60 areas to approve. He is shown **only the decisions
whose reason rests on an assumption about him** — which `briefs/area-proposal.md` already forces me
to mark, under the five-at-a-time check. On the last proposal that would have been **three rows**:
robotics, multi-agent systems, and the symbolic-AI group. Everything else was argued from
attestation and evidence, and needs nothing from him.

### `[STATED 2026-11-11]` 4.1 settled: the criterion is enough, with one rule derived from 1.3

**His question:** *"Wouldn't the role as I said before — AI: Research, Science and Engineering — be
sufficient for you to act on it? Or is there still grey area?"*

**Almost. Three things could have been grey, and two are already closed by answers he has given:**

| Could have been grey | Settled by |
|---|---|
| Is a settled, mature area still in? | **No** — 1.2, both live research and live engineering required; and `GUIDE.md` §3 `[AGREED]`, the book is about what is currently moving |
| What about things half in AI and half in another field — robotics, AI hardware, computational biology, quantum machine learning, AI for science? | **1.3 gives the rule**: keep the part that is the science, research or engineering **of AI**; exclude the part that belongs to the other field. **Generalised from robotics to every boundary case, 2026-11-11** |
| How many areas — 60 covered shallowly, or 12 covered deeply? | **Still open.** `GOAL.md` §10, `[OPEN]` Breadth against depth |

**So the criterion is sufficient to act on, and the only thing it cannot decide is how many areas.**
That is not a question about AI — it is a question about how much of his time the book is allowed to
take, and it is already marked open at step 7, where the subjects are known and the choice is
informed.

**The practical consequence: he is not asked to rule on areas at all.** The criterion decides them.
He is asked one question, later, about depth.

## Part 4 — remaining answers

| # | Answer |
|---|---|
| 4.5 | **Evidence-only cuts: just make them**, recorded with their reason, reversible |
| 4.6 | **Keep seven days** |
| 4.7 | **An independent agent always checks the proposal before he sees it** — comparing it against the full sorted list and reporting what left without being named |

# Part 5 — Researching inside an area (scouts)

**5.1** One AI agent researches each approved area and writes up to **6 subjects**. If the area holds
more, it names the ones it skipped.
**Is 6 right? It is an arbitrary starting number.**

**5.2** Each subject record has nine parts: what it is, why it matters, what it rests on, what is
being researched now, where it sits between research and practice, how it is built, what skills it
needs, what can be built to learn it, and its factual claims.
**Are any missing? Are any not worth the cost?**

**5.3** Each part has a hard word limit — 120 to 200 words. A record that exceeds one is "not
finished".
**Keep the limits? They force brevity and they also force cutting.**

**5.4** Each subject must carry **at least 2 dated items from the last twelve months** showing the
research is live, or say plainly there are none.
**Keep this?**

**5.5** Each subject must produce **3 to 6 factual claims** with sources.
**Is a floor of 3 right? It may push an agent to invent a third claim.**

**5.6** The scout's budget is 30 searches and 30 fetches, with at least 10 searches.
**Right?**

**5.7** The scout reports what it could not reach and what its sources over-represent — but **that
report currently has no permanent home** and nothing downstream reads it.
**Should that report be saved into the research file and read at the next stage?**

**5.8** If an area turns out too big for 6 subjects, the rule is to **run it again with a higher
cap**, not to raise the cap in place.
**Keep this? It costs a second full run.**

---

## Part 5 — ANSWERED 2026-11-11 (5.1 deferred, with a reason)

| # | Answer |
|---|---|
| 5.1 | **"Not sure at all on this."** Deferred — see below |
| 5.3 | **Keep the word limits, and record what was cut to meet them** |
| 5.5 | **Drop the floor of three claims.** Report however many hold up, even if that is one |
| 5.7 | **Save the coverage report into the file, and the next stage must say what it did about each point** |

**5.1, and why not knowing is the correct answer.** The cap cannot be judged in the abstract, and
it does not have to be — **5.7 is what dissolves it.** Once a run must save what it skipped, and
the next stage must act on that list, **the cap stops being a limit on coverage and becomes a batch
size.** A run that finds eleven subjects writes six and names five; the five are read, and the area
is run again if they are worth having.

So: **6 stays as a starting batch size, marked for review after the first real cycle**, on the same
basis he used for the source floor — *"keep a buffer if it is needed."* The number to watch is how
many subjects get named as skipped. If it is routinely large, 6 is too small and the evidence will
say so.

**5.5 has a consequence worth naming.** Dropping the floor removes the pressure that produced a
bundled claim — one row that carried a throughput figure and two separate speed comparisons, where
the source itself had retired part of it. **A subject with one solid claim is now a legitimate
result**, and "thin evidence here" becomes a finding rather than something to pad around.

## Part 5 — remaining answers, and what was applied

| # | Answer | Applied to the brief |
|---|---|---|
| 5.2 | **Keep all nine parts** of a subject record | no change needed |
| 5.4 | **Keep: two dated items from the last twelve months**, or say plainly there are none | no change needed |
| 5.6 | **Raise fetches to 45**, searches stay at 30 | done |
| 5.8 | **Re-run an oversized area**, never raise the cap mid-run | already stated; now owned by a stage |

**All four Part 5 decisions are in `briefs/TEMPLATE-area-research.md` as of 2026-11-11**, not held
for later: the word limits now require a `CUT TO FIT` line saying what was dropped to meet them;
the floor of three claims is gone; fetches are 45; and the coverage report is written into the
research file rather than returned in a reply and lost.

**Why fetches and not searches.** The two framing runs on 2026-11-11 used 23 and 24 of 25 fetches,
against 11 and 16 of 25 searches. **Pages opened was the binding limit, not searches made** — and
opening a page is what turns a search result into evidence.

# Part 6 — Recording what the research found

**6.1** Every claim a scout returns becomes a row in a claims file — **including claims for subjects
you later reject**, so they are not re-researched next cycle.
**Keep this?**

**6.2** Each claim records how strong its source is (peer-reviewed, preprint, vendor, blog…) and how
settled it is (established, contested, disputed…). **A claim may never be stated in the book more
strongly than its source allows.**
**Keep this?**

**6.3** Claims have a review date based on how fast they go stale — volatile ones in 3 months,
durable ones in 24.
**Are those intervals right?**

**6.4** A claim the book depends on may not stay "unverified". A separate agent re-checks it at the
original source.
**Keep this?**

**6.5** **The claims file has no column for a quotation.** The rule says the source must be quoted,
and there is nowhere to put the quote.
**Should a quote column be added?**

---

## Part 6 — ANSWERED 2026-11-11

| # | Answer | Applied |
|---|---|---|
| 6.1 | **Keep every claim**, including those of rejected subjects — he asked what I suggest, and this is it, with the reasoning below | already the rule |
| 6.2 | **Keep both ratings** — how strong the source is, and how settled the claim is | no change |
| 6.3 | **Keep 3 and 24 months** for review dates | no change |
| 6.5 | **Add a quote column** | done, four files |

**Why I suggested keeping every claim.** The cost of keeping one is a line in a text file. The cost
of dropping one is researching it again from nothing. And his own position on rejected subjects
makes the difference decisive: **rejections are re-raised next cycle.** Re-raising a rejection whose
evidence has been deleted is hollow — it asks him to reconsider something with nothing in front of
him. A claim found while researching a rejected subject also frequently supports a kept one; claims
are not owned by a single subject.

**The quote column, applied in four places** so it cannot be half-done:

| File | Change |
|---|---|
| `CLAIMS.tsv` | `source_quote` added as column 4, with a comment saying why |
| `PROCESS.md` §5.1 | Eleven columns became twelve; the new one documented in the transformation table |
| `briefs/TEMPLATE-area-research.md` | The scout must now return the quote with every claim — **"if you cannot quote a sentence that carries it, you have not established the claim"** |
| `briefs/pass-2-claims.md` | Judges the chapter's wording against the quote, not against the strength label |

**This closes one of the eleven things that were broken.** `GUIDE.md` §5 and `GOAL.md` §3.4 both
required that a source be quoted; there was nowhere to put the quotation; and the review that checks
wording against evidence was forbidden to open the page. It was checking prose against a label.

# Part 7 — Choosing which subjects become chapters

**7.1** A subject earns a full chapter when it has all three of: a mechanism worth understanding,
live research, and something you can build.
**Keep this test?**

**7.2** A subject failing on "nobody has explained it yet" or "nothing can be built" gets a **one-page
short entry** instead of nothing, if the research says a practitioner is expected to know it.
**Keep this?**

**7.3** I sort the subjects; **you rule on them**, and you get every rejection with the test it failed
and the quote behind it.
**Keep this?**

**7.4** Rejected subjects stay in a table and **I must re-raise them next cycle** to ask whether new
research changes the verdict.
**Keep this, or is a rejection final?**

---

## Part 7 — ANSWERED 2026-11-11

| # | Answer | Applied |
|---|---|---|
| 7.1 | **All three tests required** — with "buildable" clarified, see below | `GOAL.md` §10 |
| 7.2 | **Keep short entries** | no change |
| 7.3 | **The tests decide; he sees only the close calls** | `briefs/select-subjects.md` |
| 7.4 | **Record what each `must cover` cell drops** | already in `briefs/plan-chapters.md` as `NOT CARRIED` |

**7.1, and he was right to push.** His question: *"It's good to have what new research is going on,
but we will always not have something to build right?"* — frontier work nobody can reproduce.

**I had stated the test more harshly than it is.** The research brief does not ask whether the
headline result can be reproduced. It asks for **the smallest experiment that teaches the
mechanism**, as a separate thing from what reproducing the central result would cost, and it says in
its own words: *"if nothing here can be reproduced on that machine, say that — it is a true and
important finding about the area, not a failure."*

You cannot train a frontier model; you can implement attention and watch why a KV-cache matters.
You cannot run a ten-thousand-GPU job; you can run data-parallel across two processes and watch the
gradients synchronise. **Both pass.** Where there truly is no smallest experiment — emergent
behaviour only visible at unreachable scale, interpretability needing the actual weights — the
subject fails test 3 and takes the short-entry route **he kept in 7.2**. The two answers fit
together: the strict test is survivable precisely because the escape exists.

`GOAL.md` §10 now says this, because its one-line version — *"something buildable, so dimension 5 is
possible at all"* — is what I misread to him, and a later reader would misread it the same way.

**7.3 follows his 4.1 answer down one level.** He does not rule on every subject, for the same
reason he does not rule on every area: the three tests are answered by the research, not by him.
He sees the close calls and anything resting on an assumption about him.

# Part 8 — Keeping it honest over time

**8.1** Research output goes to a file, never into our conversation, because a result that lives in
a conversation is lost.
**Keep this?**

**8.2** Nothing from an earlier cycle is deleted. Superseded findings are kept and marked.
**Keep this?**

**8.3** Agents may not use a search or a word-count in place of reading. Programs may check form
(does this table have the right number of cells); they may never judge content (is this claim
overstated).
**Keep this?**

**8.4** No agent may start another agent.
**Keep this?**

---

## Part 8 — ANSWERED 2026-11-11

| # | Answer | Applied |
|---|---|---|
| 8.1 | **Everything to a file**, the agent's account of its own limits included | `briefs/TEMPLATE-area-consolidate.md`, `area-proposal.md`, `select-subjects.md`, `plan-chapters.md`, `../CLAUDE.md` |
| 8.2 | **Keep everything, but clean up periodically** — cadence left to me | `PROCESS.md` §11.1 (new), §5 `Close` row, §10 per cycle, `research/frames/README.md`, `ROADMAP.md`, `../CLAUDE.md` |
| 8.3 | **Full manual reading** | `briefs/README.md`, `../CLAUDE.md` |
| 8.4 | **He asked what I would suggest** — keep the ban, and take it out of Claude's hands | `PROCESS.md` §4.6 and §8 |

### 8.1 — four stages had no file to write to

The rule existed in the scout's brief and the framer's. **It did not exist in the consolidator's,
nor in any of the three main-session reducing stages** — the area proposal, SELECT and PLAN. Each
of those three now names its output file in its own brief, and the consolidator must put its
coverage section in the file rather than only in its reply.

**Why the gap sat exactly there.** A delegated agent hands back a reply and keeps nothing, so its
brief had to say where the work goes or there would be no work. **A main-session stage has no such
boundary** — the writing is already in the conversation, so nothing forces the file. That is the
same structural blindness as the robotics loss: the stages that run in the main session are the
ones whose rules nobody wrote.

### 8.2 — his question was the cadence, and the cadence was the wrong question

His words: *"We should do some cleanup thing may be every 3 researches or 6. I am not sure, because
we are already making the book."*

**A cadence alone cannot do this job.** Between two cleanups a superseded file sits in a live
directory, and any session that opens it reads a void document as current. That is `GOAL.md` §11
class J, which has already cost this project a re-run. **So the rule is a trigger first and a sweep
second:** a document moves to `superseded/` in the same commit that supersedes it, and a sweep at
`CLOSE` every cycle catches what the trigger missed. `PROCESS.md` §11.1 owns both, and answers
the three forms of his question in a table — why every cycle and not every third or sixth, why
`CLOSE` and not `EXPIRE`, and why it is worth the time while the book is being written.

**Nothing has been moved yet, and that is deliberate.** About a dozen files here are already
superseded — framing runs `a` to `g`, both consolidated lists, `SOURCES.md`,
`MERGED-CANDIDATES.md`, the two check files, and the withdrawn area proposal. **Question 9.11 asks
you to confirm that the old 283 categories and 63 areas are history.** Moving them before you
answer would take that decision from you, which §11.1 forbids in its own words. **The sweep runs
in the commit after 9.11 is answered**, and `ROADMAP.md` now records that debt so it cannot be
lost. **`[2026-11-12]` He answered 9.11 and the sweep has run** — fifteen files moved, nothing
deleted. See the Part 9 record below.

### 8.3 — the rule did not say what `CLAUDE.md` claimed it said

You chose reading. The rule stays. **Checking it, I found the citation did not hold.**
`../CLAUDE.md` has always said *"No agent — and not you either — substitutes a search…"* and
cited `briefs/README.md`. **The owned wording in `briefs/README.md` said only "An agent reads and
judges."** So the half of the rule that binds Claude in the main session was stated nowhere, and on
2026-11-11 Claude broke it three times in the main session. The owned wording now says it.

### 8.4 — what I suggest, and why

**Keep the ban.** Not because spawning is never useful, but because of what it would cost in
exactly the places this project keeps failing:

| | |
|---|---|
| **The budget stops being countable** | `PROCESS.md` §4.6 already says it: *"one that may start further agents has no budget at all, because each new agent brings its own."* |
| **Attribution is lost** | The robotics loss was diagnosed only because every stage's output was a file with one author. With five helpers under one agent, *"who opened the standards body's page"* has no answer |
| **The reports compound** | A parent summarising its children's summaries is `GOAL.md` class A twice over: *"having the summary is worse than having nothing, because nothing makes you look"* |

**And the coverage it would buy is already bought a safer way.** Two or more independent framing
runs per cycle, unioned, give breadth at the top level where I launch each one, count its budget,
and read its file. **Every serious failure on this project came from a stage being unbounded, not
from a stage being too small** — so spawning pushes in the direction every failure came from.

**One thing I changed on my own initiative, and you should know about it.** §8 used to read
*"Depth 0, everywhere, unless a brief states otherwise and says why."* That made the ban something
Claude could lift by editing a brief — the same file Claude edits anyway. It now says **only the
owner lifts it.** All twelve briefs already carry `DELEGATION: ZERO`; nothing else changed.

---

# Part 9 — What is still broken

**These are the real ones.** Each was found by an independent review, verified by me at source, and
is **not yet fixed**.

**9.1 The stage that turns research into claim rows has no written instructions.** It runs in the
main session, unbounded — the same condition that lost robotics.
**Should it get a brief like every other stage?**

**9.2 The trigger for re-checking a claim cannot fire.** It says "re-check claims the book will
depend on", but what the book depends on is not known until the chapter is finished, several stages
later.
**Options: re-check every claim marked weak (costs more); or move the re-check to after the chapter
is drafted (later, but it can actually run); or something else.**

**9.3 Every claim's identifier is "the area's number, a hyphen, a counter" — and no stage assigns
area numbers.**
**Who numbers the areas, and when? My suggestion would be when you approve the list, but it is your
call.**

**9.4 The research agent's instructions are written from the proposal, which does not carry what an
area covers or excludes.** That information stops at the consolidation step.
**Should the proposal carry it forward, or should whoever writes the scout's instructions read the
consolidation file?**

**9.5 Nothing in the chapter-writing process ever re-opens a source.** If a paper is corrected or
withdrawn between the research and publication, nothing notices.
**Should one of the reviews be allowed to fetch sources? It costs time and money.**

**9.6 A finished chapter can be changed later with none of the checks that applied when it was
written** — no review re-run, no sweep for the same error elsewhere.
**Should a change to a finished chapter trigger the same checks?**

**9.7 Review findings survive only as counts.** "12 findings, 3 declined" is recorded; what they
actually said is not.
**Should the findings themselves be kept?**

**9.8 Nothing requires a chapter to say what it left out.** A reader cannot tell a fully covered
subject from one that reached the book through a word limit and a 6-subject cap.
**Should chapters state their own limits?**

**9.9 Which chapter depends on which claim is recorded in three places, and only two are checked
against each other.**
**Should the third be removed?**

**9.10 One rule about how the rules themselves work has no checker**: "a rule may be stated in only
one file". An independent review found seven cases where the same rule had drifted into different
wordings.
**Accept that this rests on care, or build something that checks it?**

**9.11 The existing 283 categories and 63 areas are now void**, because they came from the source
list you revoked. Two fresh runs are going now.
**Confirm you want the old ones treated as history and not used.**

---

## Part 9 — ANSWERED 2026-11-12

**All eleven were verified at source before being put to him**, and **all eleven were answered as
recommended.**

| # | Answer | Applied |
|---|---|---|
| 9.1 | **Write CONFIRM a brief** | `briefs/confirm-claims.md` (new), `briefs/README.md`, `../CLAUDE.md`, `PROCESS.md` §8 |
| 9.2 | **Verify every provisional claim** | `PROCESS.md` §5 `Confirm` row, `briefs/confirm-claims.md` |
| 9.3 | **Areas numbered at his approval** | `ROADMAP.md` step 4 part 4, `PROCESS.md` §5.1 |
| 9.4 | **The proposal carries `COVERS` and `EXCLUDES`** | `briefs/area-proposal.md` UNIT, `ROADMAP.md` step 4 part 5 |
| 9.5 | **Re-open the load-bearing sources at CLOSE** | `PROCESS.md` §5 `Close` row, `RECORD-TEMPLATE.md` |
| 9.6 | **An amendment runs pass 4 and the sweep** | `PROCESS.md` §6.1, `GATES.md` gate 5 |
| 9.7 | **Keep the findings, not only the counts** | `RECORD-TEMPLATE.md` |
| 9.8 | **The chapter tells the reader what it left out** | `GUIDE.md` §5 part 11, `RECORD-TEMPLATE.md` |
| 9.9 | **Remove the third copy of the claim mapping** | `RECORD-TEMPLATE.md` |
| 9.10 | **The document checker checks the one-statement rule** | `briefs/document-check.md` (a fourth finding type), `../CLAUDE.md`, `PROCESS.md` §8 |
| 9.11 | **The old 283 and 63 are history** | **The first document sweep ran** — see below |

### What each answer changed

**9.1 and 9.2 go together.** CONFIRM was the last reducing stage running on prose alone. Its new
brief closes an arithmetic over the claims the research returned, refuses a row rather than
guessing a column, and **stops rather than coining an area number** — which is 9.3. The old
verification trigger said *"every provisional claim a candidate chapter would rest on"*; what a
chapter rests on is `dependents`, empty until CLOSE, so **the trigger could never fire.** It now
reads every provisional row, which is what it already meant: at CONFIRM every researched subject
is still a candidate.

**9.3 and 9.4 are both the proposal not carrying enough forward.** Nothing assigned area numbers,
so no claim id could be formed; the numbers are now fixed when you approve the list, in its order,
because a number is never renumbered and you cut and redraw when you rule. And the scout's scope
was to be written "from the approved list", which carried neither `COVERS` nor `EXCLUDES` — so the
proposal now carries both, on cuts as well as keeps, because **what an area covers is exactly what
cutting it removes.**

**9.5 found something worse than the question said.** Pass 1 does read the sources, but its brief
says *"No web searches — everything you need is in the files named."* **Nothing in the chapter
loop opens a source at all.** The chapter's `owner-verifies` ids — at most three — are now
re-opened at CLOSE through the claim verifier, before the record is hashed.

**9.6, 9.7 and 9.8 are three ways the record was thinner than it looked.** An amendment now runs
pass 4 and the book-wide sweep, and nothing else, because you declined the full re-run and said
why it would be wrong: a one-line correction costing what a chapter costs is how amending stops
happening. Findings are kept, not just counted, because `LEDGER-DEFECTS.md` is built from them.
And `non-scope` now reaches the page, as `## What this chapter does not cover`, naming for each
line which of the three it is — another chapter owns it, the research did not reach it, or it did
not fit.

**9.9 removed a field rather than adding a check.** Gate 12 already compares the chapter's
`## Claims` with `CLAIMS.tsv` `dependents` in both directions. The record's `claims:` field was a
third copy that nothing read, so it could only drift.

**9.10 could not be given to a program, by your own 8.3 answer.** Whether two paragraphs state one
rule is a question about meaning. `document-check.md` is the only instrument that reads prose, so
it gained a fourth finding type — **rules stated twice** — with the two exceptions written in:
a delegated agent's brief copies word for word, and `CLAUDE.md` may restate a rule in its
easy-to-break list **as long as the entry names its owning file.**

### 9.11 — the first document sweep, and what it corrected in its own rule

**Fifteen files moved. Nothing was deleted.** Eleven to `research/frames/superseded/` — framing
runs `a` to `g`, both consolidated lists, `MERGED-CANDIDATES.md` and `SOURCES.md` — and four to
`docs/superseded/`: the withdrawn area proposal, its ruling sheet, and the two run-`g` check files.
Each carries a dated line under its title saying what superseded it; each directory has a
`README.md` listing them.

**Three files were deliberately left in place**, and the `superseded/README.md` says so:
`FINDINGS-2026-11-07.md` and the two reorganisation files are **finished and still true**, and
§11.1 says `superseded/` means *do not read this as current*, never *this is finished*.
`VALIDATION-2026-11-07.md` stays too — the diagnosis supersedes two of its items, not the file.

**The sweep found §11.1 too broad and it was corrected.** The rule said a file may not move while
*another live document* still cites it. Doing that would have meant rewriting the paths inside
`DIAGNOSIS-2026-11-07.md`, `VALIDATION-2026-11-07.md`, `POSTMORTEM-2026-11-11.md` and this
questionnaire — **falsifying four dated records of where a file was on a date.** The clause now
binds **live governance documents only**: `CLAUDE.md`, the five specification files, the briefs and
every directory `README.md`. Those were all changed in the moving commit. **The directory
`README.md` is what carries a reader from an old path to a new one**, which is why §11.1 required
a line there from the start.

---

# Part 10 — How this project makes decisions

**10.1** Every statement in the planning documents is marked as yours, agreed, my proposal,
undecided, or acted-on-by-default. **53 are currently my proposals that you have never ruled on.**
**Do you want them all put to you, or only when one actually matters in practice?**

**10.2** When a decision has waited 7 days I act and mark it. Four things never do this: publishing,
spending your money, throwing away finished work, and anything you have reserved.
**Is that list right?**

**10.3** Independent agents review the rules. Today three of them found 36 problems; about 19 are
fixed.
**Do you want a review like that on a schedule, or only when something goes wrong?**

**10.4** I was told to read everything manually rather than searching files. That is slower and it is
how three real errors were found today.
**Keep it as the standing rule?**

---

## Part 10 — ANSWERED 2026-11-12

**All four answered as recommended. With this, every one of the 60 questions is answered.**

| # | Answer | Applied |
|---|---|---|
| 10.1 | **Each proposal comes to you when it first binds something** — never in a batch | `GOAL.md` §0 (new sub-section), `../CLAUDE.md` |
| 10.2 | **Add a fifth thing that never defaults** | `PROCESS.md` §2.1, `ROADMAP.md`, `../CLAUDE.md` |
| 10.3 | **A rules review before each of your five approval points** | `ROADMAP.md` |
| 10.4 | **The reading rule binds all work in this repository** | `../../../.claude/CLAUDE.md`, `briefs/README.md` |

**10.1 — both failures are now named, because they are opposite.** About fifty `[I RECOMMEND]`
statements stand. You declined to rule on them in a batch, and the reason is in `§3.3`'s own
history: **a rule ruled on in the abstract is approved from its wording**, which is exactly how an
inventory of 63 areas came to be put to you as a recommendation. So each one comes to you when it
first decides a concrete thing. **The opposite failure is mine and is written down beside it**:
using a recommendation at the moment it matters without saying it was never ruled on. The count is
now reported at `CLOSE`, so the pile cannot grow unseen.

**10.2 — you closed a gap I found while checking the question.** The four things that never
default are all about what an action costs: publishing, money, discarding work, and anything you
reserved. **None of them covers a rule you had already stated or agreed to** — that is only
covered if you thought to reserve it in advance, and the case where nobody thinks to is the case
that matters. The fifth row says a `[STATED]` or `[AGREED]` statement never defaults, because
changing one is not unblocking the work, it is overriding you.

**10.3 — a trigger, not a calendar.** The three reviews of 2026-11-11 found 36 problems, and they
found them **where rules had just changed.** A review runs before each of your five approvals,
reading the rules as a set — which is what found the contradictions *between* files, and is a
different instrument from `briefs/document-check.md`, which reads one document against what it
cites.

**10.4 — the rule left this book.** `../../../.claude/CLAUDE.md` now carries it for every session
in this repository, and points back to `briefs/README.md` for the wording the briefs use and the
table of what may be automated. One of the three pattern-match failures on 2026-11-11 was ordinary
repository work, not research: a sweep for a phrase found six places where reading found
twenty-five.

---

## Space for anything I did not ask

Anything you expected to see here and did not, write it below. **A gap in this questionnaire is a
gap in my understanding of what you want, and that is the thing most worth catching.**
