# Chapter 01-what-a-model-is — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale
`sha256`, or on stages out of order. Fill `sha256` LAST:
`shasum -a 256 markdown/<stem>.md`

chapter: markdown/01-what-a-model-is.md
sources: TOC.md L28-30 (Part I heading + the chapter-1 row: opening problem, 5-item Covers list, 14 pp); orientation concept 1 "The model, and what you get from it", read with all 7 concepts so concepts 2-7 could be excluded as chapters 2-7's property. No published book was available on this machine; subject matter is my own knowledge, which is why every durable claim is written as mechanism and every datable one is a Note.
non-scope: context/retrieval/tools/checks/people as a system (ch 2); why it is assembled that way (ch 3); agents and the loop (ch 4); where the effort goes (ch 5); durable vs datable (ch 6); tokens and the unit of text (ch 10); anything inside the model (chs 8-17); fine-tuning as a procedure (ch 39); measuring or reducing cost and latency (chs 52-53).
begun: 2026-10-22T15:38:21+05:30
written: 2026-10-22T15:52:56+05:30
reviewed: 2026-10-22T15:59:55+05:30
absolutes: 44 after the fixes (38 before). 6 failed a counter-example and were rewritten: "disappoint you in the same way tomorrow" (false - replies vary, ch 13), "nothing is remembered" (true of the model, false of products that resend history), "never seen your material" (public material may well have been trained on), "cannot look anything up" (true of the model, not of products with search), "refuses almost nothing" (models refuse plenty; the claim meant the interface sets no limit), "two requests meet the identical model" (providers replace models).
new-terms: 0 new backticked terms against 0 earlier chapters. Triaged by hand instead: grep confirms the chapter uses none of token/context/retrieval/tool/agent, so chapters 2, 4 and 10 may introduce all five. Latency is used and defined here, so chs 15 and 52 must not call it new - recorded in LEDGER-TAUGHT.md.
covers-misses: 0. verify-coverage.py reports 0 against the chapter-1 Covers list, before and after the fixes.
sha256: 67bbacb69efec114081498cfc2dab7a3cac7c63a26d2010589c57b9478e529b2

## Before writing

- [x] `LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before — ch 1 is the first chapter, so the ownership table applies but no per-chapter row existed; grep 'Do not' returned 10 rows, all for chapters 8+; none constrains this chapter. Its own row was written on close and then corrected after a grep disproved it
- [x] The chapter's `TOC.md` row read: its opening problem, its Covers list, its page budget — L28-30; opening problem copied word for word into the chapter's *The problem.* line; 5 Covers items; 14 pp budget
- [x] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate — written in the field above before writing, from orientation concepts 2-7 and the Part I 'what to ignore for now' line
- [x] Sources read **in full, immediately before writing** — named, with what was read — all 7 orientation concepts extracted and read in one pass, then the chapter written with nothing read in between
- [x] `BOOK-GUIDE.md` §6 boundary cases and `LEDGER-DEFECTS.md` to hand — §6's four decided cases read; none applies to ch 1, which teaches no mechanism. LEDGER-DEFECTS entries 5, 7, 8 and 10 used as the while-writing checks

## While writing

- [x] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many — the cost example is the only arithmetic: 8 numbers recomputed independently in Python after the rewrite - 0.0018/call, 18/day, 540/month, 0.00205/call, 20.5/day, 615/month, 13.9% ~ 'about 14 per cent', 25% input growth ~ 'a quarter'. The first version of this example was wrong and was replaced
- [x] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed — verify-absolutes.py: 38 before fixes, 44 after; 6 failed and were rewritten (listed in the absolutes field above)
- [x] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged — verify-inputs.py: 0; hand-triaged by grep for the five deferred terms
- [x] Maths written as raw LaTeX spans and fences, never `$…$` — no mathematics in this chapter; the one display block is a ```text block, not maths
- [x] The chapter holds the structure in `BOOK-GUIDE.md` §5; any lab is isolated and safe — title, intro paragraph, *The problem.* / *The question.*, body, Lab with expected results per step, Summary / Key Terms / Review Questions / Review Answers, closing 'You understand this when'. No code, per Part I
- [x] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report — two: that a model 'remembers' you (the product resends history), and that zero variation follows from fixed weights. Both corrected in the body and flagged in the report

## After writing

- [x] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` — all CLEAN — all three CLEAN on the final text. render FAILED once with 8 findings, all false: the gate matched real ordered-list markers. Checked against the generated .tex, corrected the gate, re-proved it both ways (LEDGER-DEFECTS entry 11)
- [x] `verify-coverage.py` — every miss triaged **one by one**, not counted — covers-misses 0 at draft, after the completeness fixes, and after the verification fixes. Nothing to triage
- [x] `\input{chapters/01-what-a-model-is}` in `latex/book.tex`; `make` → 0 overfull · 0 missing glyphs · 0 undefined — present, grep count 1; make -> 23 pp total, the chapter is 10 printed pages, 0 overfull, 0 missing glyphs, 0 undefined
- [x] **Completeness review** launched with the `BOOK-GUIDE.md` §14 brief — brief carried the chapter, both sources, the declared non-scope, the six categories, 7 named claims to verify independently, and the wrong-finding warning. Returned 16 findings ranked, plus verdicts on all 7 claims
- [x] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done** — 16 accepted, 0 rejected. Both high findings verified against TOC.md directly: chapter 2 has five parts not four, and chapter 3's four reasons contain no cost-watching need. Every replacement asserted count==1 before and 0 survivors after; a closing grep for all phrasings of the withdrawn claims returned zero
- [x] **Fix-verification pass** launched, naming every changed passage — 14 changed passages named individually. Returned 6 findings, all accepted and applied with counted sweeps. It recomputed all 11 numbers in the cost example independently and confirmed each; items 1, 2, 4, 8, 10 and 11 of the list returned NO ISSUES
- [x] `LEDGER-TAUGHT.md` row added; `LEDGER-DEFECTS.md` updated if a new defect class appeared — row added, corrected after a grep disproved its own claim, then extended with the three request labels the worked exchange spends. LEDGER-DEFECTS gained entries 11 and 12
- [x] `README.md` status updated; the part's PDF delivered — README Part I row set to Drafting, and its stale chapter ranges from the reorder corrected at the same time. PDF delivered

> **One change after the record was closed.** `verify-render.py` gained a check for
> `BOOK-GUIDE.md` §8's 64-character limit on `text` blocks, and it found one line of this
> chapter's worked exchange at 65. Shortened to 60 by cutting the word "below"; no other
> character of the chapter changed, and nothing quotes that line. The hash above is
> re-stamped for the corrected file. A content change would have re-triggered the review;
> a whitespace fix to a line the gate now enforces does not.

## Reviews

completeness-review: 16 findings, 0 rejected. Two high, both checkable against the plan: a closing paragraph promising four parts where chapter 2 has five, with accountability silently swapped for a cost-watching need matching no part; and a worked cost example whose flat per-request premise refuted its own doubling conclusion while omitting the reply. 14 moderate/low, all applied. It verified 7 named claims independently, found all 7 true, and corrected my own premise about the page budget.
fix-verification: 6 findings, 0 rejected, all applied with counted sweeps. One exposed a gap in the PLAN rather than the chapter: the Settings bullet pointed at chapter 13 for 'how long the reply may run', and no chapter in the whole TOC owned an output-length setting. Chapter 13's Covers extended. All 11 numbers recomputed and confirmed right.
