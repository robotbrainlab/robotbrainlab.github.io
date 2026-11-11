# Area proposal brief

**The stage that proposes which of the candidate areas the book covers.** It runs **after**
`TEMPLATE-area-consolidate.md` and **before** the owner rules (`../ROADMAP.md` step 4 part 3,
`../GOAL.md` §3.3 `[AGREED 2026-11-11]`).

**Claude runs this in the main session. It is not delegated** — the criteria are the owner's own
words about his career, and no agent can judge those in a way he can check. **That is an argument
against delegating the judgement, not against bounding it.** This brief bounds it.

## Why this brief exists

**`[2026-11-11]` The first run of this stage had no brief, and it lost things silently.** An
independent review traced them. The stage cut `Intelligent Robotics` — attested by **10 of 19
sources, more than any other area in the register** — and took with it, unnamed:

| Lost with the cut | Why it mattered |
|---|---|
| **world models** | The consolidation run wrote: *"the only subject no other source names"*, and *"if the owner wants world models as its own area, that is the split to make"*. The proposal does not contain the phrase |
| **Control methods** | ACM CCS's own child node, filed `BELOW` robotics |
| **Six AAMAS areas** + `Distributed artificial intelligence` | Filed `BELOW` Multiagent Systems, which was cut in the same sentence |
| **expert systems, theorem proving** | Named only under `cs.AI` and `KRR`. Both cut |
| **The five `UNCLEAR`** | `TEMPLATE-area-consolidate.md` **required** this stage to say what it did with each. It said nothing |

**The arithmetic looked complete and was complete over the wrong set.** `12 + 27 + 24 = 63` is
correct and hides the problem: the consolidation's own total is `63 + 47 + 123 + 36 + 9 + 5 = 283`,
and the five `UNCLEAR` were never in the 63 to begin with.

**Nothing this stage dropped left a trace.** Both stages before it are checkable against their
input. This one reported and filtered in one pass, which `README.md` says cannot be checked.

---

> Copy everything below this line into the run — or, when running it yourself, work to it clause by
> clause and produce every required section before writing a word of recommendation.

---

**QUESTION**

Of the candidate areas the consolidation run produced, which does this book cover, and what does
each exclusion cost?

**THE CRITERIA, AND THEY ARE NOT YOURS TO WRITE**

`../GOAL.md` §1.1 `[STATED]` — the career goal, in the owner's words — and §3.1 `[STATED]` — the
five questions every area must answer. **Quote both before applying them.** `../GOAL.md` §3.3 says
the argument comes from the purpose: *"an argument needs a purpose and reasons; it does not need a
particular author."*

**You may not invent a test.** The first run wrote its own operative test, in the same document, in
the same sitting, and that self-authored test is what removed robotics. **If the criteria need a
test the owner has not written, say so under `What this stage could not settle` and stop — do not
apply it.**

**WHAT TO DO**

1. **Read the consolidation output in full**, including its `What this run could not settle`
   section. That section is an input, not an appendix.
2. **Account for the whole of it, not just the areas.** Your arithmetic closes over every verdict
   the consolidation issued — areas, merges, `BELOW`, rejections and `UNCLEAR` — or it does not
   close.
3. **Decide each area on its own**, against the criteria, and record the decision as a row.
4. **Before cutting anything, open its `BELOW` and its `MERGED FROM`** and list what goes with it.
5. **Write the coverage sections.** They are not optional and the proposal is not finished without
   them.

**UNIT — one decision, one row, whether keep, fold or cut**

```
NAME            as the consolidation named it. Not a name you coined
DECISION        KEEP | FOLD INTO <area> | CUT
ATTESTED BY     carried forward from the consolidation, not recomputed
WHY             the clause of §1.1 or §3.1 it serves or fails, in one sentence
ABSORBS         for a FOLD: every name and subject this takes in
CARRIES FORWARD for a FOLD: what of the absorbed area survives under the new name
LOSES           what this decision removes: its BELOW children by name, any subject
                attested by only one source, anything the consolidation flagged about it.
                "nothing" is an answer only after you have opened both fields
```

**`[STATED 2026-11-11]` Write every section below to `../PROPOSAL-areas-YYYY-MM-DD.md` before any
of it is put to the owner.** A stage that runs in the main session has no agent boundary to force
the write, so the rule has to be stated here. A result that lives in a conversation cannot be read
next cycle, cannot be cited, and cannot be checked against what it claimed — and the stage that
lost robotics was a main-session stage whose working was never written down.

**OUTPUT — every section, in this order**

```
## Criteria            §1.1 and §3.1 quoted, before any decision
## Proposed areas      one row per KEEP
## Folds               one row per FOLD, with ABSORBS, CARRIES FORWARD and LOSES
## Cuts                one row per CUT, with ATTESTED BY and LOSES
## What each cut takes with it   every BELOW child and single-source subject, by name
## The five-at-a-time check      see below
## Disposition of every UNCLEAR  one line each. Required by the consolidation brief
## Borderlines inherited          the consolidation's own flagged rejections and thin merges,
                                  each with what this stage did about it
## Arithmetic          EVERY verdict the consolidation issued, each on its own line,
                      summing to its stated total. Areas + names merged into an area +
                      categories filed BELOW an area + each rejection verdict + UNCLEAR.
                      `keeps + folds + cuts + unclear` is NOT this sum: it covers the
                      area list only, which is what the first run closed over while
                      losing 215 of 283 categories from view
## What this stage could not settle
```

**THE FIVE-AT-A-TIME CHECK**

**Before the proposal is finished, take the five best-attested areas you cut and write, for each,
the sentence you would say to the owner if he asked "why is the field's own most-filed subject not
in my book?"** If that sentence rests on an assumption about his career rather than on evidence,
**mark it as such in the row.** The first run cut the single best-attested area in the register and
the reason was one unexamined assumption.

**TARGET**

**There is no number.** Not ten, not twelve, not sixty-three. The number is what the criteria yield.
**A count in your head is a selection rule you did not declare.**

**FORBIDDEN**

- **Cutting an area for being unimportant, small, quiet, unfashionable or not worth covering.**
  This is the rule that binds both earlier stages and it binds this one. An area is cut because it
  fails a stated criterion, never because of a sense about it.
- **A reason shared between areas.** One area, one reason. The first run put ten areas and roughly a
  hundred named sub-topics under a single paragraph, and a group reason tells the owner nothing he
  can reverse.
- **An empirical claim as a reason, without its source.** *"The research here is largely mature"*
  was the whole justification for the biggest cut in the first run, and it carried no source.
  `../GOAL.md` §3.4 `[AGREED]`: *"A claim may not be stated above the strength of its source, and
  the source is quoted."*
- **Folding on a judgement that two things are similar.** A fold needs what a merge needed at the
  previous stage: the same sources, a reciprocal `ALSO CALLED`, or matching `INCLUDES`. **Two names
  you merely think belong together stay apart.**
- **A fold that does not say what it loses.** A fold whose absorbed content is not carried forward
  is a cut wearing another word. The first run folded `Model` and lost federated learning, model
  formats and model marketplaces; it folded `Audio and Speech Processing` into a *generative* area
  and subsumed speech recognition under generation.
- **Renaming an area.** Keep the name the consolidation kept, which is the name a source used. The
  first run renamed four of twelve; `Natural Language Processing`, attested by 8 sources, became
  *Language models*, and the next stage writes scout scopes from that name.
- **Inventing a category.** Unchanged from every stage before this one.
- **Substituting a search, a pattern or a count for reading.** You read and you judge. A pattern
  match tells you where a string is; it cannot tell you what a cut costs.

**BUDGET**

No searches and no fetches. **You add no evidence.** Everything is in the consolidation output. A
question you cannot answer from it goes under `What this stage could not settle`.

**WHAT THIS STAGE COULD NOT SETTLE**

- **Every cut you were unsure about**, and what would settle it.
- **Every assumption about the owner's career** that any decision rests on, named as an assumption.
- **Every subject attested by one source only** that leaves the pipeline, by name.
- **Every `UNCLEAR` you could not dispose of.**
- **Anything the consolidation flagged** that you did not act on.

**STOPPING RULE**

Stop when every verdict the consolidation issued is accounted for in a row, every cut names what it
takes with it, every `UNCLEAR` has a disposition, and the arithmetic closes over the consolidation's
total rather than over its area list. **There is nothing to search for, so there is no reason to
continue past that point.**

**PARTIAL**

If you cannot finish, publish the rows you have and name every area still undecided. **An area you
did not reach is not a cut.**

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.** An area
wrongly kept costs the owner one reading. An area wrongly cut disappears from the book, and takes
its `BELOW` children with it, and he never learns their names.

**DELEGATION: ZERO.** This stage is not delegated at all — see the head of this file.
