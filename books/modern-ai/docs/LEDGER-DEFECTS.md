# What the gates cannot catch

Stated plainly, because overselling the checks would defeat their purpose.

**An entry is a *class*, not an incident.** It has two parts: **what the class is, stated as the
argument for why the defect happens**, and the practice that follows. A list of mistakes is not
reusable; a class is. Where a class was earned by something that happened here, name the incident
too — but **an entry that can only be stated as "X happened once" is not yet a class.**

**Add an entry whenever a defect gets past every gate.** That is the only trigger. A defect a gate
caught does not belong here — it belongs in the gate.

**This file starts almost empty, on purpose.** An entry earned by something that happened here is
worth more than one imported from elsewhere, because an imported entry carries a story nobody in
this project paid for and invites the reaction *"that will not happen to us."*

**The eight entries below are stated as arguments**, so that each one holds because of how writing
and reviewing work rather than because of something that once happened. **`[2026-11-11]` Seven of
the eight still carry no incident, which is deliberate — no chapter has been written yet, so no
defect has got past a gate.** Entry 5 is the exception: it was earned, not by a chapter, but by the
governance prose in `docs/`, which has no gate at all (`GATES.md`, "What no gate reads").

---

**1. A rule explained in prose can vanish with no term missing.** A coverage check matches words. A
whole section of method can disappear while every keyword it used survives elsewhere in the
chapter.
*Practice:* the coverage gate is a hint, and following the hint is manual. Read the plan's promise
for the chapter and the chapter side by side, not the word lists.

**2. A chapter can be internally perfect and wrong about where it sits.** **Gate 8 reads sequence
for terms with a Key Terms row, and that is the whole of the machine coverage.** Re-explaining what
the reader already has, and claiming something false about an earlier chapter, are checked by
nothing. `LEDGER-TAUGHT.md` is their only defence, and it has to be read for its `Do not` rows as
well as its ownership rows.
*Practice:* grep the taught-ledger for `Do not` before writing the opening paragraph.

**3. Reviewers miss things and invent things.** A reviewer reads once, under a brief, with no
stake in the chapter — so it will miss things. And it is rewarded for finding things, so it will
report some that are not there.
*Practice:* verify every finding in both directions before accepting it. **A wrong finding costs
more than a missed one**, because acting on it makes the chapter worse and consumes a round.

**4. A well-sourced, correctly-bounded, badly-explained concept passes everything.** The gates can
verify that a topic is present, that its claims match their sources and that no theory strays
outside the boundary. **They cannot verify that the explanation teaches.**
*Practice:* this is what `You understand this when …` and the acceptance questions are for, and
they are judgement rather than machinery. Read the chapter as a reader, once, with nothing else
open.

**5. A fix applied where you are looking survives where you are not.** A claim in a long document
appears in several phrasings, and the writer applying a fix sees the one the finding quoted. The
defect is structural, not careless: nothing in the act of fixing one passage surfaces the others.
*Practice:* the counted sweep, which `PROCESS.md` §2 states — including which sections to sweep
first, and why those. **Searching is not enough on its own**: a phrasing you did not think of has no
string to search for, so the sweep is followed by reading the sections the sweep touched.
*Incident, 2026-11-11:* four corrections were made where a check quoted them and not where the same
claim was repeated — "five classes" fixed in `POSTMORTEM-2026-11-11.md` and left standing in
`GATES.md`; "recorded weeks ago" fixed in that document's findings table and left standing in its
own opening line; "two runs" fixed in one file and left in three; "two floors" removed from the
framing brief and left in `PROCESS.md` §4.6, the section that owns the schema. **Each was found by
opening the file, and none by a search.** `../CLAUDE.md` now states the rule as *a grep is not a
sweep*.

**5a. The stage with no brief is the stage that loses things, and it leaves no trace.**
Every bounded stage on a project can be checked against its input: it declares a total, and a total
that does not close is visible. **A stage with no brief declares nothing, so nothing it drops can
be counted.** The danger is not that such a stage is careless — it is that its output looks
complete, because the only arithmetic it offers is arithmetic over the set it chose to work on.
*Practice:* every stage that reduces its input gets a brief with an output shape, a per-item unit, a
forbidden list and an arithmetic that closes over **its input's own total**, not over the part of
the input it decided to handle.
*Incident, 2026-11-11:* the area proposal stage, invented that morning and left unbriefed because
"an agent cannot do it", cut the best-attested area in the register and removed world models,
Control methods, six AAMAS areas, expert systems and theorem proving without naming one of them. Its
arithmetic — `12 + 27 + 24 = 63` — was correct and closed over 63 when the consolidation's total was
283. **The two stages before it, both briefed, lost nothing.** `briefs/area-proposal.md` closes it.

**6. A lab's programs narrate their own output, so a claim exists in code as well as in prose.**
Printed lines state counts, comparisons and universals, and that narration is captured into the
chapter. Correcting the prose and not the program makes the chapter contradict itself on its own
page. **How many places a claim occupies is `PROCESS.md` §2's figure**; the defect here is the
category, which is that some of them are not prose at all.
*Practice:* after any lab fix, re-run the program and re-capture its output. **Never edit a captured
output block by hand** — fix the program, which is also why `GATES.md` gate 3 does not police the
width of captured output.

**7. A fix round is a drafting event, not an edit.** Writing new sentences introduces errors at
some rate. A fix round that touches many passages is writing many new sentences, so it introduces
errors at that same rate — and nobody expects it to, because it is called a fix.
*Practice:* treat a fix round as a draft — sweep it and verify it. **The rule for reading a second
round's findings is `PROCESS.md` §6's stopping rule**, which distinguishes a mis-scoped chapter from
an unswept fix round; this entry exists because the two look identical from inside the round.

**8. A gate can lie to the suite and nothing will say so.** A gate is ordinary software and fails
in ordinary ways: crashing on a renamed column, passing vacuously on an empty directory, printing a
success banner over no output. In each case it reports health and checks nothing — **worse than no
gate, because it is trusted.**
*Practice:* **`GATES.md`'s three rules about the gates themselves**, which that file owns and this
entry does not restate. The reason they belong in a defect ledger at all: a gate in this state is
invisible to every other check, so nothing but reading its output catches it.

---

## Entries earned in this project

None yet. The first will be added the first time something gets past every gate.

**Note the boundary with `GOAL.md` §11.** That section records mistakes in *how this project has
been run* — mis-read instructions, unverified claims, briefs that asked the wrong question. This
file records defects in *the book itself* that the gates cannot catch. They are different failure
surfaces and they do not share entries.
