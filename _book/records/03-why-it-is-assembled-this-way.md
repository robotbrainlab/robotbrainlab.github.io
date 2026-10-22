# Chapter 03-why-it-is-assembled-this-way — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale
`sha256`, or on stages out of order. Fill `sha256` LAST:
`shasum -a 256 markdown/<stem>.md`

chapter: markdown/03-why-it-is-assembled-this-way.md
sources: TOC.md rows for chs 1-5 and the Part I headings; markdown/01 and markdown/02 in full as the authority on what the reader knows; LEDGER-TAUGHT.md ch 1 and ch 2 rows plus the Claims in their corrected form table, grepped for 'Do not'; orientation concept 3, read with concepts 4 and 5 to bound the scope.
non-scope: agents and the loop (ch 4); where the effort goes (ch 5); tokens (ch 10); how a tool call is expressed (ch 23); retrieval mechanics (chs 24-29); schemas, judges, evaluation, tracing (chs 21, 30-33); fine-tuning as a procedure (ch 39); security in depth (ch 51); cost and latency measurement (chs 52-53).
begun: 2026-10-22T18:18:55+05:30
written: 2026-10-22T18:29:26+05:30
reviewed: 2026-10-22T18:53:07+05:30
absolutes: 79 on the final text. Four failed before review and were rewritten: 'none in particular' about a model's relation to the truth (false - models correlate with truth, which is why they are useful), 'Certainty, free, every time' for a rule (the banned claim from LEDGER-DEFECTS 13, written a third time), 'a part that only ever helped would be in every system already', and 'the only part that matters'. Two more failed in the fix-verification pass: 'the one gap whose cause sits outside engineering' (gaps 1 and 2 have causes outside engineering too) and 'fails in the same places' for a self-check.
new-terms: 1 - `refund(order=4471)`, an illustrative tool call reusing chapter 1's order number. Triaged: it builds on nothing the reader has not been given.
covers-misses: 0 throughout. The completeness review nonetheless found the fourth Covers item - what each part costs - unevenly delivered: retrieval's was the strongest, checks' second cost was three asserted sentences with no example, and people's four rows said the same cost twice. The strictness cost now has a worked example.
sha256: a9d914c5813f92827bc66c94f8a2f2b27d8f546abfb68aeb684be56fcd38a1f8

> **The `written` stage was skipped.** I went from writing straight to the review, as I did
> on chapter 2, and `chapter.py reviewed` accepted it because it only checked the boxes after
> the writing. The timestamp above is the first commit that carried the draft, recorded
> retrospectively rather than at the stage. `chapter.py` now refuses `reviewed` when
> `written:` is empty, so this cannot recur silently.

## Before writing

- [x] `LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before — ch 1 and ch 2 rows read in full; grep 'Do not' returned 12 rows. Chapter 2's row pins the gap-to-part pairing and its order; the chapter uses retrieval, tools, checks, people in that order and credits chapter 2 rather than presenting the mapping as new. The completeness review confirmed this independently
- [x] The chapter's `TOC.md` row read: its opening problem, its Covers list, its page estimate (an estimate, never a target — `BOOK-GUIDE.md` §11) — row for ch 3 (opening problem, 3-item Covers list, 14 pp estimate - an estimate, per BOOK-GUIDE §11), plus rows 1, 2, 4 and 5 to set the boundaries
- [x] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate — written in the field above before writing, from the TOC rows for chapters 4 and 5 and the later owners of each mechanism
- [x] Sources read **in full, immediately before writing** — named, with what was read — chapters 1 and 2 in full, the ledger rows, and orientation concepts 3 to 5, read in one pass immediately before writing
- [x] `BOOK-GUIDE.md` §6 boundary cases and `LEDGER-DEFECTS.md` to hand — §6 read; this chapter teaches no mechanism, so no boundary case applies, and the boundary gate is CLEAN. LEDGER-DEFECTS entries 2, 5, 9 and 13 used as the while-writing checks - entry 13 fired anyway

## While writing

- [x] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many — no arithmetic. The structural counts - four gaps, three questions, three reasons, two halves, one of three - were each counted against what follows them by the fix-verification pass, which found all nine correct
- [x] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed — 79; six failed across the two rounds and were rewritten, listed in the absolutes field above
- [x] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged — verify-inputs.py: 1, triaged above
- [x] Maths written as raw LaTeX spans and fences, never `$…$` — no mathematics in this chapter
- [x] The chapter holds the structure in `BOOK-GUIDE.md` §5; any lab is isolated and safe — title, intro, *The problem.* / *The question.*, four gap sections each with 'Is the gap real?' and 'What closes it, and what it costs', the Pattern, a Lab with expected results per step, Summary / Key Terms / Review Questions / Review Answers, closing 'You understand this when'
- [x] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report — one, and it was mine rather than a received one: that human review creates accountability. The chapter now argues the opposite and it is flagged in the report

## After writing

- [x] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` — all CLEAN — all three CLEAN on the final text
- [x] `verify-coverage.py` — every miss triaged **one by one**, not counted — covers-misses 0 at draft and after both rounds
- [x] `\input{chapters/03-why-it-is-assembled-this-way}` in `latex/book.tex`; `make` → 0 overfull · 0 missing glyphs · 0 undefined — present; make -> 46 pp total, the chapter is 13 printed pages, 0 overfull, 0 missing glyphs, 0 undefined
- [x] **Completeness review** launched with the `BOOK-GUIDE.md` §14 brief — brief carried the chapter, both earlier chapters, the ledger including the corrected-claims table, the plan rows, the declared non-scope, 6 named claims to verify, and an instruction to challenge the accountability and per-reader arguments hardest. Returned 19 findings
- [x] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done** — 18 accepted, 1 rejected with reason (restating 'the model proposes, your code decides' as the argument for why the gap is real, which is this chapter's property; the reviewer leaned the same way). Four applied fixes were LOST when a patch batch aborted before writing and were only found by rendering the page - LEDGER-DEFECTS entry 15, and tools/patch.py now writes after each edit
- [x] **Fix-verification pass** launched, naming every changed passage — 11 changed passages named. Returned 8 findings, all accepted. Two were the rewritten argument failing to reach the Pattern table and Review Answer 4, which both still asserted the proposition the section opens by calling false. One was my own F5 fix overreaching. One was the corrected confidence claim surviving in Review Answer 3. All four were in the back matter
- [x] `LEDGER-TAUGHT.md` row added; `LEDGER-DEFECTS.md` updated if a new defect class appeared — ch 3 row added; two rows added to Claims in their corrected form (accountability, and the self-check hedge). LEDGER-DEFECTS gained entry 15
- [x] `README.md` status updated; the part's PDF delivered — README Part I row shows 3 of 7; PDF delivered

## Reviews

completeness-review: 19 findings, 18 accepted, 1 rejected with reason. The serious one was conceptual rather than verbal: the chapter claimed that adding human review buys you 'somebody is answerable', which implies nobody was answerable before. False - the organisation deploying an automated decision is accountable whether or not anyone looked. The section was rewritten around accountability never moving. The reviewer also found the banned claim from LEDGER-DEFECTS 13 a THIRD time, in prose, with chapter 2's caveats dropped.
fix-verification: 8 findings, 0 rejected, all applied. The rewritten argument had not reached the Pattern table or Review Answer 4, both of which still asserted the proposition the section opens by calling false; the corrected confidence claim survived in Review Answer 3; and my own fix for the permanence claim overreached, since gaps 1 and 2 also have causes outside engineering. Every one of those four was in the back matter - the fourth time in three chapters.
