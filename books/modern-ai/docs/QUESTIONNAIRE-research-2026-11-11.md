# Questionnaire — every decision in the research process

**Why this exists.** 88 things govern this project that you never ruled on: 53 are my proposals, 26
are marked undecided, and 9 I acted on because you did not answer in time. This questionnaire puts
the ones that touch research in front of you, in plain words, so you decide them.

**How to answer.** Write your answer under each question. "Keep as is" is a real answer and the
fastest one. "I don't know yet" is also real — it tells me to leave the item marked undecided
instead of guessing. **Do not feel you must answer all of them in one sitting.** Part 9 is the part
that is actually broken; Parts 1–8 are mostly confirming or changing things that already work.

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

## Space for anything I did not ask

Anything you expected to see here and did not, write it below. **A gap in this questionnaire is a
gap in my understanding of what you want, and that is the thing most worth catching.**
