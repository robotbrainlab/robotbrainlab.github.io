# Chapter 02-the-parts-around-the-model — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale
`sha256`, or on stages out of order. Fill `sha256` LAST:
`shasum -a 256 markdown/<stem>.md`

chapter: markdown/02-the-parts-around-the-model.md
sources: TOC.md rows for chs 1-4 and the Part I heading; markdown/01-what-a-model-is.md in full, as the authority on what the reader already knows; LEDGER-TAUGHT.md chapter-1 row, grepped for 'Do not'; orientation concepts 2-5, concept 2 being this chapter's and 3-5 bounding it.
non-scope: why the model cannot do each job and what each part costs (ch 3); agents and the loop (ch 4); where the effort goes (ch 5); tokens (ch 10); how a tool call is expressed (ch 23); retrieval mechanics (chs 24-29); schemas, judges, evaluation, tracing (chs 21, 30-33); MCP (ch 36); injection and security (ch 51); cost and latency measurement (chs 52-53).
begun: 2026-10-22T17:29:04+05:30
written: 2026-10-22T17:48:38+05:30
reviewed: 2026-10-22T17:49:43+05:30
absolutes: 54. Six failed a counter-example and were rewritten before review: 'the model can only ASK for tools you described' (it can ask for anything; it cannot have one run), instructions written 'once' (they can be per user), retrieval's shape 'always the same' (some systems retrieve after a first model call), 'only ever changes what the model knows' (a retrieved example changes how it writes), 'the model never reaches out' (scoped to the model, as ch 1 does), and 'a rule is right every time' (deterministic is not correct). The last of those was fixed in the body and SURVIVED in Review Answer 3 until the completeness review found it - see the fix-verification note.
new-terms: 2, both triaged: the order line reused verbatim from chapter 1's worked exchange, and `refund` as an example tool name introduced here. Neither is built on without being given.
covers-misses: 0 at draft and after both rounds of fixes. The completeness review nonetheless found four Covers items thin by reading them rather than matching words - context's 'what it is for', the five-part cast delivered at four, people, and the compound system. All four addressed.
amended:
  - 2026-10-29T03:43:50+05:30: Name the interview shorthand: retrieval-augmented generation and RAG, named where the chapter gives retrieval's five steps
  - 2026-10-29T04:03:08+05:30: The index carried only the long form of each interview shorthand, so a reader looking up the abbreviation they will actually hear found nothing. Added an index entry for the abbreviation beside its naming sentence; no visible text changed.
sha256: 267485394109f8781eab981ebeb721ffe8f83cab4eaeb0b4f79842ded9c3f862

## Before writing

- [x] `LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before — chapter-1 row read in full; grep 'Do not' returned its list. One violation shipped into the draft anyway - the cost lesson re-taught as new - and was caught by the completeness review, not by me
- [x] The chapter's `TOC.md` row read: its opening problem, its Covers list, its page budget — row for ch 2 (opening problem, 8-item Covers list, 18 pp estimate), plus rows 1, 3 and 4 to fix the boundaries
- [x] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate — written in the field above before writing, from the TOC rows for chapters 3, 4 and 5 and the later owners of each mechanism
- [x] Sources read **in full, immediately before writing** — named, with what was read — chapter 1 in full, the ledger row, and orientation concepts 2-5 read in one pass immediately before writing; nothing read in between
- [x] `BOOK-GUIDE.md` §6 boundary cases and `LEDGER-DEFECTS.md` to hand — §6 read; no mechanism is taught in this chapter so no boundary case applies. LEDGER-DEFECTS entries 2, 5, 8 and 10 used as the while-writing checks

## While writing

- [x] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many — no arithmetic in this chapter. The only counts are structural - five parts and four gaps - and the completeness review found the chapter asserting five while operating on four in six places. Counted and fixed
- [x] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed — verify-absolutes.py: 54; six failed and were rewritten, listed in the absolutes field above
- [x] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged — verify-inputs.py: 2, both triaged above. Also grepped for the five words chapter 1 deliberately left unspent - token, context, retrieval, tool, agent - and confirmed this chapter is the first to use four of them
- [x] Maths written as raw LaTeX spans and fences, never `$…$` — no mathematics. The one display block is a ```text diagram, measured at 57 characters wide against the 64 limit, with every box line equal
- [x] The chapter holds the structure in `BOOK-GUIDE.md` §5; any lab is isolated and safe — title, intro, *The problem.* / *The question.*, body, Lab with expected results per step, Summary / Key Terms / Review Questions / Review Answers, closing 'You understand this when'. No code, per Part I
- [x] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report — two: that the model 'calls' an API itself, and that a person in the loop is a temporary stage better models will remove. Both corrected and flagged

## After writing

- [x] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` — all CLEAN — all three CLEAN on the final text. verify-voice FAILED once on the ordinary English word 'handover' (gate wrong, fixed case-sensitively, re-proved). verify-render gained a seventh check during this chapter, for a blockquote starting mid-sentence under ordinary text - the defect it was written for is in this chapter's history
- [x] `verify-coverage.py` — every miss triaged **one by one**, not counted — covers-misses 0 throughout. The reviewer found four thin Covers items by reading rather than matching, which is the limit of this gate stated in LEDGER-DEFECTS entry 1
- [x] `\input{chapters/02-the-parts-around-the-model}` in `latex/book.tex`; `make` → 0 overfull · 0 missing glyphs · 0 undefined — present, grep count 1; make -> 35 pp total, the chapter is 12 printed pages, 0 overfull, 0 missing glyphs, 0 undefined
- [x] **Completeness review** launched with the `BOOK-GUIDE.md` §14 brief — brief carried the chapter, chapter 1 as the authority on what the reader knows, the ledger row, the plan rows for chs 1-4, the declared non-scope, 7 named claims, and an instruction to hunt cross-chapter errors hardest. Returned 21 findings
- [x] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done** — 20 accepted, 1 rejected with reason (the check-ordering rule said to belong to ch 31; it is two sentences under 'what each part is for' and ch 31 is already pointed at beside it). Every replacement asserted count==1 before and 0 after
- [x] **Fix-verification pass** launched, naming every changed passage — 14 changed passages named. Returned 6 findings, all accepted: a lead-in saying 'two consequences' above three; a replaced callout that left its '>' markers and split a sentence; a person still defined as the far end of checking in the Summary AND Key Terms after the table row was removed; a new paragraph contradicting the table cell above it; 'the fifth part' announced twice; and a dangling 'By shape'. It confirmed the four-gaps-to-four-parts mapping against both authorities and verified the diagram character by character
- [x] `LEDGER-TAUGHT.md` row added; `LEDGER-DEFECTS.md` updated if a new defect class appeared — chapter-2 row added. LEDGER-DEFECTS entry 11 gained its second and third instances the same day - verify-voice on 'handover', verify-record reading the next line into an empty field
- [x] `README.md` status updated; the part's PDF delivered — README Part I row shows 2/7; PDF delivered with the chapter at pp 18-29

## Reviews

completeness-review: 21 findings, 20 accepted, 1 rejected with reason. Three structural: the chapter declared five parts and operated on four in six places, including a review question whose answer was wrong against its own diagram; the tools table denied the chapter's own slogan ten lines under it, and was false besides; and a person was both the top rung of the checks table and the fifth part, which is what produced the first problem. It also found chapter 1's cost lesson re-taught as new against an explicit 'Do not' row, and a survivor of my own earlier sweep sitting in Review Answer 3.
fix-verification: 6 findings, 0 rejected, all applied with counted sweeps. The worst was structural and invisible in the markdown: a replaced callout left two '>' prefixes behind, so a sentence ended mid-clause and the rest rendered as a blockquote. verify-render.py now has a seventh check for it, proved against an injected case and against a correct callout. The pass also found the person-as-check framing surviving in the Summary and in the Key Terms definition after the table row was removed - the third time in two chapters that a sweep has missed the back matter.
