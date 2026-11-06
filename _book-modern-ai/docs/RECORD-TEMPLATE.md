# Chapter NN — record

Copy this to `records/NN-slug.md` when a chapter begins.

**Tick a box only with evidence after it** — a command result, a count, a line number. A ticked box
with nothing after it is a lie the gates can detect, and prose is what gets skipped, so this is a
checklist a script refuses rather than a habit.

**Fill `sha256` LAST.** Editing one character of the chapter afterwards makes this record stale and
fails the suite.

```
chapter:        markdown/NN-slug.md
question:       the chapter's durable question, one sentence
sources:        named, with what was read of each
non-scope:      what this chapter does NOT cover, so review has an edge
claims:         the CLAIMS.tsv ids this chapter rests on
begun:
written:
reviewed:
amended:
absolutes:      count from the absolutes gate, and what was scoped back
new-terms:      count from the inputs gate, each triaged
coverage-misses: count, each triaged one by one
operations:     the changelog operations this chapter needed, one row each, or `none`.
                GATES.md gate 10 reads these, and CHANGELOG.md is generated from them
sha256:
```

## Before writing

- [ ] `LEDGER-TAUGHT.md` read — every row above this chapter, **and every `Do not` row wherever it
      sits.** The opening paragraph claims nothing false about what came before
- [ ] `LEDGER-DEFECTS.md` read
- [ ] The chapter's row in `PLAN.md` read: its durable question, its subject, and what it must
      cover
- [ ] **Non-scope declared** in the field above. Without an edge, review never terminates
- [ ] `OWNERSHIP.tsv` checked: every concept this chapter will own is free, and every concept it
      leans on has an owner to refer to
- [ ] Sources read **in full, immediately before writing** — not earlier in the session
- [ ] `GUIDE.md` §8's mathematics test to hand, and `GATES.md` for what each gate will check

## While writing

- [ ] **Every number recomputed** against the thing it describes, in the file, before it was
      written — say how many
- [ ] **Every claim has a `CLAIMS.tsv` row**, with its source and strength, and **none is stated
      above its recorded strength**
- [ ] **Every absolute tested** against a counter-example **in this chapter**, and against any
      `Do not` row in `LEDGER-TAUGHT.md` that bears on it. **Not against the whole book** — that
      obligation grows with the book while being charged to one chapter, which is how it comes to be
      skipped
- [ ] **Every term built on** was already given to the reader
- [ ] The chapter holds the anatomy in `GUIDE.md` §5, including its durable question and its
      `Claims` section
- [ ] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged
      in the report
- [ ] A disputed subject carries `## What is disputed` in the fixed shape, including **what
      measurement would settle it**
- [ ] The lab states the hardware it needs, and gives the reduced version `GUIDE.md` §6 requires —
      or says plainly that there is none

## After writing

- [ ] Every gate `CLEAN` or `VACUOUS` on this chapter, **and every `VACUOUS` explained** — a
      chapter with no arithmetic or no absolutes gets `VACUOUS` from those gates and that is
      correct, but an unexpected `VACUOUS` means the gate found nothing to read (`GATES.md`)
- [ ] **The book builds clean** — 0 overfull lines, 0 missing glyphs, 0 undefined references. Write
      the command and its counts. **While the build toolchain is `[OPEN]` (`GUIDE.md` §10) there is
      nothing to run: write `no build yet` and move on**
- [ ] **Every command and code sample in the chapter has been run** — say how many, and that the
      output shown is what came back (`GUIDE.md` §4)
- [ ] Index entries read one by one against Key Terms **before** review
- [ ] **Pass 1, completeness review** — launched with the brief in `briefs/`
- [ ] Each finding **verified before accepting**; each fix **swept book-wide with `tools/sweep.py`,
      back matter first — paste its before and after output, not a number you typed.** Zero, or the
      fix is not done (`PROCESS.md` §2)
- [ ] **Pass 2, adversarial claims** — CLEAN
- [ ] **Pass 3, lab execution from the chapter text alone** — produced a verdict
- [ ] **Pass 4, fix verification** — launched, naming every changed passage
- [ ] `LEDGER-TAUGHT.md` row added; `LEDGER-SHORTHAND.md` updated; `OWNERSHIP.tsv` updated
- [ ] `LEDGER-DEFECTS.md` updated if a new defect class appeared
- [ ] **The `operations:` field above is filled** — every operation this chapter needed, from the
      six in `PROCESS.md` §5.2, with the kind (new / revised / overturned). `ADD`, `SPLIT`, `MERGE`
      and `RETIRE` are decided here; a `NEW QUESTION` or `RECARVE` is the owner's and its row is
      written at PLAN, so write `none` rather than leaving the field empty. `CHANGELOG.md` is
      generated from these rows, never written
- [ ] Every acceptance question in `ACCEPTANCE.md` keyed to this chapter marked `answered`,
      `answered-as-disputed` or `cannot` — and **a `cannot` reopens the chapter or moves the
      question with a reason**
- [ ] Every page looked at

## Reviews

```
pass-1-completeness:
pass-2-claims:
pass-3-lab:
pass-4-fix-verification:
```

Record for each: how many findings, how many declined and why, and how many were **false teaching**
rather than cosmetic. The stopping rule in `PROCESS.md` §6 reads these numbers, and it reads them
for what caused them rather than as a verdict on the chapter.
