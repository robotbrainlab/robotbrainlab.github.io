# Pass 4 — fix verification

Fill in `<CHAPTER>` and `<CHANGED-PASSAGES>`.

**What this pass is for, and why it is not optional.** The recurring defect in a long document is
not writing a passage badly. **It is correcting a claim where you are looking and leaving it where
you are not.** This pass exists only to catch that, and it catches survivals in nearly every
chapter it is run on.

**Why it reads only the changed passages.** An agent told "look at the chapter" re-reads everything
and reports what pass 1 already found. The list is the brief.

---

> Copy everything below this line into the agent.

---

**YOUR JOB**

A chapter was reviewed, findings were applied, and here is every passage that changed. Read **only
these**, and answer two questions about each:

1. **Did the fix land everywhere?** The same claim may appear in several phrasings elsewhere in the
   chapter. Search for every phrasing. **Look in the summary, the key-term table, the "worth
   memorising" table and the answer key first** — those read as settled because they look like a
   glossary rather than an argument, so they are where a fix goes to not happen.
2. **Did the fix introduce a new error?** A fix round that touches more than a handful of passages
   is a drafting event, and drafting introduces errors at the usual rate. Check each changed
   passage for a new contradiction with text that did not change.

**THE CHANGED PASSAGES**

`<CHANGED-PASSAGES>`

**ALSO CHECK, for each change**

- **Arithmetic.** If a number changed, every number derived from it must have changed too. A total
  that no longer equals its parts is the commonest survival.
- **Captured program output.** If a lab's prose changed, its program and its captured output must
  have changed with it. A chapter that contradicts its own printed output on the same page is the
  single most embarrassing defect available.
- **Superlatives and quantifiers.** A fix that restores a comparison can falsify a *"the narrowest"*
  or *"in every case"* written before the restoration.
- **Cross-references.** If a passage moved, anything pointing at it is now wrong.

**OUTPUT**

```
## Survivals
The old claim still present somewhere else. Quote both the fixed passage and the
survivor, and give the survivor's location.

## New errors
Errors the fixes introduced. Quote the changed passage and what it now contradicts.

## Clean
Changed passages that are correct and complete. List them, so the count is visible.
```

**STOPPING RULE**

Finish when every listed passage has been checked. **Do not look at anything not on the list.**

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent.
