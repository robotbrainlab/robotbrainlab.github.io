# What the gates cannot catch

Stated plainly, because overselling the checks would defeat their purpose.

**An entry is a *class*, not an incident.** It has three parts: what the class is, the instance that
produced it, and the practice that follows. A list of mistakes is not reusable; a class is.

**Add an entry whenever a defect gets past every gate.** That is the only trigger. A defect a gate
caught does not belong here — it belongs in the gate.

**This file starts almost empty, on purpose.** An entry earned by something that happened here is
worth more than one imported from elsewhere, because an imported entry carries a story nobody in
this project paid for and invites the reaction *"that will not happen to us."*

**The eight entries below are stated as arguments, not as incidents**, so that each one holds
because of how writing and reviewing work rather than because of something that once happened. An
entry that can only be stated as *"X happened once"* is not yet a class.

---

**1. A rule explained in prose can vanish with no term missing.** A coverage check matches words. A
whole section of method can disappear while every keyword it used survives elsewhere in the
chapter.
*Practice:* the coverage gate is a hint, and following the hint is manual. Read the plan's promise
for the chapter and the chapter side by side, not the word lists.

**2. A chapter can be internally perfect and wrong about where it sits.** No gate looks at
sequence. `LEDGER-TAUGHT.md` is the only defence, and it has to be read for its `Do not` rows as
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
*Practice:* every fix is a sweep — grep the whole book for every phrasing, count before, count
after, zero or it is not done. **Sweep the back matter first**: summaries, key-term tables and
answer keys read as settled because they look like a glossary rather than an argument, so they are
where a fix goes to not happen.

**6. In a lab, one claim lives in about six places and four of them are prose.** A lab's programs
narrate their own output — printed lines stating a count, a comparison or a universal — and that
narration is captured into the chapter. So a single claim exists in the body, the program, the
captured output, the summary, a key-term row and an answer. Correcting the prose and not the
program makes the chapter contradict itself on its own page.
*Practice:* after any lab fix, re-run the program and re-capture its output. Never edit a captured
output block by hand.

**7. A fix round is a drafting event, not an edit.** Writing new sentences introduces errors at
some rate. A fix round that touches many passages is writing many new sentences, so it introduces
errors at that same rate — and nobody expects it to, because it is called a fix.
*Practice:* classify a second round's findings before concluding the chapter is mis-scoped.
Findings about the *subject* mean mis-scope. Findings that are the previous round's own unswept
fixes mean the fix round needs sweeping and verifying again.

**8. A gate can lie to the suite and nothing will say so.** A gate is ordinary software and fails
in ordinary ways: crashing on a renamed column, passing vacuously on an empty directory, printing a
success banner over no output. In each case it reports health and checks nothing — **worse than no
gate, because it is trusted.**
*Practice:* three rules. When the suite fails, find out **which** gate and why, every time. Prove a
new gate by breaking something it should catch and watching it exit non-zero. A gate that checked
nothing prints `VACUOUS`, never `CLEAN`.

---

## Entries earned in this project

None yet. The first will be added the first time something gets past every gate.

**Note the boundary with `GOAL.md` §11.** That section records mistakes in *how this project has
been run* — mis-read instructions, unverified claims, briefs that asked the wrong question. This
file records defects in *the book itself* that the gates cannot catch. They are different failure
surfaces and they do not share entries.
