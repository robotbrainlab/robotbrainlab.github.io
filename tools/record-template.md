# Chapter NN — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale
`sha256`, or on stages out of order. Fill `sha256` LAST:
`shasum -a 256 markdown/<stem>.md`

chapter: markdown/NN-slug.md
sources:
non-scope:
begun:
written:
reviewed:
absolutes:
new-terms:
covers-misses:
sha256:

## Before writing

- [ ] `LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before
- [ ] The chapter's `TOC.md` row read: its opening problem, its Covers list, its page budget
- [ ] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate
- [ ] Sources read **in full, immediately before writing** — named, with what was read
- [ ] `BOOK-GUIDE.md` §6 boundary cases and `LEDGER-DEFECTS.md` to hand

## While writing

- [ ] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many
- [ ] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed
- [ ] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged
- [ ] Maths written as raw LaTeX spans and fences, never `$…$`
- [ ] The chapter holds the structure in `BOOK-GUIDE.md` §5; any lab is isolated and safe
- [ ] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report

## After writing

- [ ] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` — all CLEAN
- [ ] `verify-coverage.py` — every miss triaged **one by one**, not counted
- [ ] `\input{chapters/NN-slug}` in `latex/book.tex`; `make` → 0 overfull · 0 missing glyphs · 0 undefined
- [ ] **Completeness review** launched with the `BOOK-GUIDE.md` §14 brief
- [ ] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done**
- [ ] **Fix-verification pass** launched, naming every changed passage
- [ ] `LEDGER-TAUGHT.md` row added; `LEDGER-DEFECTS.md` updated if a new defect class appeared
- [ ] `README.md` status updated; the part's PDF delivered

## Reviews

completeness-review:
fix-verification:
