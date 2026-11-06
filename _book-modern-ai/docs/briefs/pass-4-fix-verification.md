# Pass 4 — fix verification

Fill in `<CHAPTER>`, `<ANSWERS>` and `<CHANGED-PASSAGES>`. `<ANSWERS>` is the path to
`markdown/ZZ-review-answers.md` and this chapter's section number in it — the review answers are in
the back matter, not the chapter (`../GUIDE.md` §5).

**What this pass is for, and why it is not optional.** The recurring defect in a long document is
not writing a passage badly. **It is correcting a claim where you are looking and leaving it where
you are not.** Nothing in the act of fixing one passage surfaces the others, so no amount of care
during a fix finds them — which is why this is a separate pass with a separate reader.

**Why it reads for the listed passages and not the whole chapter.** An agent told "look at the
chapter" re-reads everything and reports what the earlier passes already found, burying the
survivals in a second copy of their findings. The list is the brief.

---

> Copy everything below this line into the agent.

---

**QUESTION**

Did each fix land everywhere the claim appears, and did any fix break something that was correct?

**YOUR JOB**

A chapter was reviewed by three earlier passes, their findings were applied, and here is every
passage that changed as a result.

**What you read, precisely.** You read the listed passages **as your subject**, and you **must**
search the whole chapter for the claims those passages contain — a survival is by definition
somewhere the fix did not land, so a brief that kept you out of the rest of the chapter would
forbid the job. What you must **not** do is review unchanged text on its own merits. That was the
earlier passes' work, it is done, and repeating it hides your findings inside theirs.

**The list bounds what you are looking for, not where you may look.**

Answer two questions about each listed passage:

1. **Did the fix land everywhere?** One claim appears in several phrasings. Search for all of them.
   **Look in the summary, the key-term table, the "worth memorising" table and the review answers
   first** — those read as settled because they look like a glossary rather than an argument, so
   they are where a fix goes to not happen. **The review answers are in `<ANSWERS>`, a different
   file**, which makes them the likeliest survival of all: a fix applied to the chapter never
   touches them.
2. **Did the fix break something?** A fix round that touches many passages is writing many new
   sentences, and new sentences carry errors whether or not they are called fixes. Check each
   changed passage against text that did **not** change.

**THE CHANGED PASSAGES**

`<CHANGED-PASSAGES>`

**ALSO CHECK, for each change**

- **Arithmetic.** If a number changed, everything derived from it must have changed too. A total
  that no longer equals its parts is the commonest survival.
- **Captured program output.** If a lab's prose changed, the program and its captured output must
  have changed with it. **A captured block is never edited by hand** — if it disagrees with the
  prose, the program is what gets fixed, and that is a finding either way.
- **Superlatives and quantifiers.** A fix that restores a comparison can falsify an *"the
  narrowest"* or an *"in every case"* written before the restoration.
- **Cross-references.** If a passage moved, anything pointing at it is now wrong.

**OUTPUT**

```
## Survivals
The old claim still present somewhere else. Quote BOTH the fixed passage and the
survivor, and give the survivor's location. A survival you can only show once is
not a survival — it is a single passage, and belongs below or nowhere.

## New errors
Something now wrong that was not wrong before. Quote the changed passage, and
quote what it contradicts or what it got wrong. One location is enough here.

## Clean
Changed passages that are correct and complete, listed, so the count is visible.

## Coverage
Which listed passages you checked. Any you did not, and why.
```

**BUDGET**

One pass over the listed passages, plus a whole-chapter search for each claim they contain. **No
web searches.**

**TARGET**

No number. Every listed passage gets one of the three verdicts above.

**PARTIAL**

If you stop early, name the passages you checked and those you did not. **An unchecked passage is
where the survival will be**, so the list matters more than the findings.

**FORBIDDEN**

- **Reviewing unchanged text on its own merits.** The earlier passes did that.
- **Reporting a survival you can show in only one place.** Two locations, or it is not one.
- **Rewriting.** You report; you do not edit.

**STOPPING RULE**

Finish when every listed passage has been checked and every claim in them searched for across the
chapter. **Do not report a defect in unchanged text unless it contradicts, or duplicates, something
on the list.**

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent.
