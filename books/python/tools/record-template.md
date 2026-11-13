# Chapter NN — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale `sha256`,
on stages out of order, and **on an `absolutes:` number that does not match what
`verify-absolutes.py` counts**. Fill `sha256` LAST — `chapter.py reviewed` writes it.

chapter: markdown/NN-slug.md
sources:
non-scope:
begun:
written:
reviewed:
absolutes:
new-terms:
covers-misses:
files-read-back:
sha256:

`absolutes:` **starts with the number** and then says what you found, like
`37 — tested; two softened, one moved to chapter 25`. The number is checked.

`files-read-back:` **names every file you edited, read in full after the last edit.**
`verify-record.py` reads `records/EDITS.log` and fails when a file `tools/patch.py` touched
while this chapter was open is missing from the list. See `../GATES.md` §8.

## Before writing

- [ ] `../LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before
- [ ] The chapter's `../TOC.md` row read: its opening problem, its Covers list, its Lab
- [ ] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate
- [ ] Sources read **in full, immediately before writing** — named, with what was read. The roadmap page is read as HTML, never as stripped text
- [ ] `../GATES.md` §2.2 (the three boundaries) and `../LEDGER-DEFECTS.md` to hand
- [ ] **If this is a Part I chapter**: every Part II term it will need is in `tools/verify-inputs.py`'s ALLOW list, with the owning chapter named (`../GATES.md` §4)

## While writing

- [ ] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many
- [ ] **Every output printed in the book was produced by running the code**, never typed — `verify-code.py` count
- [ ] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed
- [ ] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged
- [ ] The chapter holds the structure in `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §5, which decision 18 copies exactly; the lab is isolated and safe
- [ ] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report

## After writing

- [ ] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` · `verify-code.py` — all CLEAN
- [ ] `verify-coverage.py` — every miss triaged **one by one**, not counted
- [ ] `\input{chapters/NN-slug}` uncommented in `book.tex`; `make -C ../latex BOOK=python` → 0 overfull · 0 missing glyphs · 0 undefined
- [ ] **Completeness review** launched with `../docs/briefs/completeness-review.md`
- [ ] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done**
- [ ] **Fix-verification pass** launched with `../docs/briefs/fix-verification.md`, naming every changed passage
- [ ] **Every file I edited, read in full after the last edit** — named in `files-read-back:` above. A removal you did not read is a removal you cannot judge
- [ ] `../LEDGER-TAUGHT.md` row added; `../LEDGER-DEFECTS.md` updated if a new defect class appeared

## Reviews

completeness-review:
fix-verification:
