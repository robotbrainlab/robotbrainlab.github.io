# Brief — completeness review (step 3 of the chapter loop)

**Fill this in and give it to one agent. Do not rewrite it.** Replace every `<…>`.
Give the agent nothing else, and above all do not give it your own conclusion: an agent
handed a hypothesis returns it confirmed.

---

## The task

You are reviewing one chapter of *Python from Zero*, a book that teaches Python from the
first program. Read the chapter and its sources **in full**, side by side, and report what
is wrong with the chapter.

**Chapter:** `<path, e.g. books/python/markdown/04-the-four-data-structures.md>`
**Its sources, which you must read in full:**
`<every source, by path or URL, with what each one is for>`

**What I did not read closely, and you should:** `<name it, or write "nothing">`

## What this chapter does NOT cover

`<paste the chapter record's non-scope field, word for word>`

**A finding outside that is not a finding.** Say so and move on. Without this edge a
review never terminates: once a chapter seems to cover any case, "what about X?" is always
a fair question and every answer invites the next one.

## What this book does not teach at all

Three boundaries, stated in `books/python/GATES.md` §2.2:

1. **The Advanced and Mastery material** — descriptors, metaclasses, variance,
   performance tuning, the C API. Chapter 51 names them; no other chapter teaches them.
2. **The shell, the editor and Git.** Owned by *Linux and Git from Zero*. The book points
   at it and teaches none of it.
3. **Building a web service.** Owned by *APIs to FastAPI*. Part III teaches the Python a
   service needs and stops short of the service.

**A chapter that crosses one of these is a finding.** A chapter that correctly points at
the other book instead is not.

## One thing that is the method, not a defect

**The language is taught twice on purpose.** Part I (chapters 1–17) gets the reader
writing Python. Part II (18–28) returns to the same ground and explains why it behaves
that way. **Do not report the second pass as repetition.** Do report it if the second pass
contradicts the first.

## Look hardest for one mode: a claim stated wider than its support

**This is the fault that dominates.** In the book this process comes from, a pass briefed on
this one mode found **36 claims needing narrowing across ten chapters — about 3.6 each — in
chapters that had already passed two reviews and every automated check.** Of the three
chapters that ever got a third reading, it found a blocking teaching error in all three.

It does not look like an error. It looks like a clear sentence. The test is not *is this
true?* but **is this as true as the chapter says it is?**

- *Always*, *never*, *only*, *every*, *the whole difference*, *that is why* — each is a claim
  about everything, not about the example beside it.
- A claim the chapter's **own next paragraph** narrows, or its own lab refutes.
- A mechanism given as **the** reason when it is **a** reason.
- A number quoted from a rounded display, or carried from another chapter with its
  conditions dropped.

Report each one with the support it actually has, and say what the honest form would be.

## The six kinds of finding

Report only these. For each, give the line, quote the text, and say what is wrong.

1. **Omission** — the sources or the contents row promise something the chapter lacks.
2. **Alteration** — the chapter changes what a source says.
3. **False claim** — it is wrong about Python, or **true but stated wider than its support**
   (the section above). Verify it; do not recall it.
4. **Self-contradiction** — two passages of this chapter disagree. Check the summary, the
   key terms and the review answers, not only the body.
5. **Out-of-boundary** — it teaches one of the three subjects above.
6. **Cross-chapter error** — it credits a claim to a chapter that does not own it, or
   assumes something an earlier chapter never gave the reader.

## Specific claims to verify independently

`<name them: the ones that would be expensive to get wrong. Run the code.>`

## How to answer

- Order your findings by how much damage each does to a reader. Most damaging first.
- Quote the text. A finding without a quotation cannot be acted on.
- **If unsure, say so rather than asserting. A wrong finding costs more than a missed one.**
- If you think a rule above is itself wrong, say so at the end, separately.

## Stopping rule

Stop when you have read both documents in full and reported every finding of the six kinds
above. Do not read other chapters except to check a cross-chapter claim.
