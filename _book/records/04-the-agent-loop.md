# Chapter 04-the-agent-loop — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale
`sha256`, or on stages out of order. Fill `sha256` LAST:
`shasum -a 256 markdown/<stem>.md`

chapter: markdown/04-the-agent-loop.md
sources: TOC.md rows for chs 1-5 plus 34, 37 and 38 to fix the ownership boundary, and the Part I headings; markdown/01 to 03 in full; LEDGER-TAUGHT.md all three per-chapter rows and the Claims in their corrected form table, grepped for 'Do not'; LEDGER-DEFECTS.md, with entries 7, 8, 9 and 16 to hand; orientation concept 4, read with concept 5 to bound the scope. The study's figures come from concept 4 and could not be checked against the paper, which is not in this repository - the chapter marks them as one study for that reason.
non-scope: the named agent patterns and when an agent is warranted (ch 34); context engineering, compaction, sub-agents, memory (ch 35); tool design and MCP (ch 36); multi-agent systems (ch 37); evaluating an agent, and pass@k / pass^k BY NAME (ch 38); where the effort goes (ch 5); tokens (ch 10); how a tool call is expressed (ch 23); security and injection (ch 51); cost and latency measurement (chs 52-53).
begun: 2026-10-22T23:06:35+05:30
written: 2026-10-22T23:28:32+05:30
reviewed: 2026-10-27T21:41:12+05:30
absolutes: 45. Four failed a counter-example before review and were rewritten: 'left your code in charge of all of them' over five parts, 'the same every run' for a path that branches on data, the compounding table presented as a law rather than a model, and 'a bill you cannot bound in advance' which contradicted the step limit taught two sections earlier.
new-terms: 3 - lookup_order(4471), refund(...), and the turn block's labels. All introduced here as illustration; none is built on without being given.
covers-misses: 0 throughout. The completeness review found two Covers items thin by reading rather than matching: 'compounding error' was taught but never named, and 'how short real deployed loops are' rested on one paragraph whose causal reading overclaimed. Both fixed.
sha256: 1055ec3ab9f4f2c6ed7a30930568bac46d7e2a6b32bc3c842b01a1638e564ce5

## Before writing

- [x] `LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before — all three rows read; grep 'Do not' returned 14. One was breached anyway - the approval thresholds repeated chapter 2's examples near-verbatim - and the completeness review caught it
- [x] The chapter's `TOC.md` row read: its opening problem, its Covers list, its page estimate (an estimate, never a target — `BOOK-GUIDE.md` §11) — row for ch 4, plus rows 34, 37 and 38 to place the boundary: ch 38 owns pass@k and pass^k by name and the 0.95-over-20 figure, so this chapter uses 0.9 and 0.99 and teaches the mechanism
- [x] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate — written in the field above before writing, from the rows for chapters 5, 34 to 38, 51 and 52-53
- [x] Sources read **in full, immediately before writing** — named, with what was read — chapters 1 to 3 in full, both ledgers, and orientation concepts 4 and 5, read in one pass immediately before writing
- [x] `BOOK-GUIDE.md` §6 boundary cases and `LEDGER-DEFECTS.md` to hand — §6 read; no mechanism is taught, and the boundary gate is CLEAN. Entries 7, 8, 9 and 16 used as the while-writing checks

## While writing

- [x] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many — thirteen figures and derived claims, every one computed in Python BEFORE it was written: six rows at 0.9, two at 0.99, the first step count below 0.5, 1/0.9^20, and 0.9^10 twice. Both reviewers recomputed all of them independently and found none wrong - the first chapter with clean arithmetic
- [x] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed — verify-absolutes.py: 45; four failed and were rewritten, listed above
- [x] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged — verify-inputs.py: 3, all triaged. Also grepped chapters 1 to 3 to confirm 'agent' is genuinely new here
- [x] Maths written as raw LaTeX spans and fences, never `$…$` — no mathematics. One ```text block, measured at 61 characters against the 64 limit after the fix - verify-render.py gained a check for that limit during this chapter
- [x] The chapter holds the structure in `BOOK-GUIDE.md` §5; any lab is isolated and safe — title, intro, *The problem.* / *The question.*, body, Lab with expected results per step, Summary / Key Terms / Review Questions / Review Answers, closing 'You understand this when'
- [x] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report — one: that an agent is a model doing the job by itself. The chapter's whole argument is that deployed agents are kept short and supervised, and that the loop is the part you add

## After writing

- [x] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` — all CLEAN — all three CLEAN on the final text
- [x] `verify-coverage.py` — every miss triaged **one by one**, not counted — covers-misses 0 at draft and after both rounds
- [x] `\input{chapters/04-the-agent-loop}` in `latex/book.tex`; `make` → 0 overfull · 0 missing glyphs · 0 undefined — present; make -> 55 pp total, 0 overfull, 0 missing glyphs, 0 undefined
- [x] **Completeness review** launched with the `BOOK-GUIDE.md` §14 brief — brief carried the chapter, chapters 1 to 3, both ledgers, the plan rows including 34, 37 and 38, the declared non-scope, 6 named claims, and an instruction to recompute every number. Returned 14 findings
- [x] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done** — 14 accepted, 0 rejected, applied as 22 edits with the back matter swept first. A book-wide grep confirmed no stale 'nothing is added', 'not repeatable' or currency amount survives in any chapter
- [x] **Fix-verification pass** launched, naming every changed passage — 14 changed passages named. Returned 5 findings plus 3 notes, all accepted: a closed count the chapter exceeded, the multiplication stated three times in eighteen lines, a glossary row covering only half the mechanism, a term bolded that chapter 2 owns, and presentation residue. It recomputed every figure again and confirmed all correct
- [x] `LEDGER-TAUGHT.md` row added; `LEDGER-DEFECTS.md` updated if a new defect class appeared — ch 4 row added. LEDGER-DEFECTS entry 15 gained a second instance: an edit batch that both inserts and removes the same sentence can delete what it just added
- [x] `README.md` status updated; the part's PDF delivered — README Part I row shows 4 of 7; PDF delivered

## Reviews

completeness-review: 14 findings, all accepted. Two serious. The headline claim 'Nothing new has been added' contradicted the chapter's own later line 'the loop is a part' and the stopping condition it says you must have; it appeared in four places including the Summary and an answer. And the two callouts under the compounding table disagreed about the same quantity - the Note said real numbers are better, the Warning said worse, and the Warning's reasons supported neither. It also found the approval thresholds repeating chapter 2 against a pinned 'Do not', and 'compounding error' never named although chapter 34 refers back to it.
fix-verification: 5 findings and 3 notes, all accepted. The count of 'two simplifications' was exceeded by the chapter itself twenty lines later; the multiplication was stated three times in eighteen lines; the Key Terms row covered the arithmetic and not the second mechanism; **context** was bolded although chapter 2 owns it. While applying them I removed the Warning's conclusion by deleting two copies of a sentence an earlier edit in the same batch had just inserted - caught by reading the passage, and recorded as a second instance of LEDGER-DEFECTS entry 15. **Reopened 2026-10-27** to add an optional `### Worth Memorising` table, which is the source `tools/cheatsheet.py` generates Appendix A from. Nothing else in the chapter changed; the table restates numbers the chapter already worked. Appendix A was the one end-loaded item in the schedule (HANDOVER §3.1) and would otherwise have been assembled from 57 finished chapters in the last three days, from memory.
