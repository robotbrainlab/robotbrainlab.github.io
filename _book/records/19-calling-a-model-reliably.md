# Chapter 19-calling-a-model-reliably — record

Tick a box only with **evidence** after it: a command result, a count, a line number.
`verify-record.py` fails on any `- [ ]`, on a missing review verdict, on a stale
`sha256`, or on stages out of order. Fill `sha256` LAST:
`shasum -a 256 markdown/<stem>.md`

chapter: markdown/19-calling-a-model-reliably.md
sources: TOC.md row 19 (covers list, 20pp estimate); markdown/B-interview-bank.md q39-42 - q42 was MISSED on the first pass and the chapter went to review with no answer to it; the question list must be grepped out of the bank by chapter number, never remembered as a range; LEDGER-TAUGHT.md rows 1-18 in full, every 'Do not' row; LEDGER-DEFECTS.md entries 1-28; BOOK-GUIDE.md sections 5, 6, 9, 11, 14, 15; markdown/13-from-scores-to-a-word.md, markdown/15-what-it-costs.md, markdown/16-why-it-fails.md and markdown/18-the-prompt-as-a-specification.md read in full for the cross-references; Python 3 stdlib behaviour of asyncio.Semaphore, asyncio.gather and io buffering checked by running code, not from memory
non-scope: parsing or validating what comes back (chapter 21 owns it - this chapter only says when streaming makes validation impossible); caching (later in Part II); tracing, metrics and what to log (Part III); the cost model itself (chapter 15 owns it - this chapter only compares batch against concurrent); agent loops and tool calls; provider-specific SDK code, since BOOK-GUIDE section 9 requires every lab to run for every reader with no account and no key; threads and multiprocessing, because the work here is I/O-bound and asyncio is enough
begun: 2026-10-28T05:45:38+05:30
written: 2026-10-28T06:35:08+05:30
reviewed: 2026-10-28T06:35:08+05:30
absolutes: 144 flagged by verify-absolutes.py after the fix passes (80 before them), each tested against the rest of the book. The load-bearing ones are narrowed in the text: 'you cannot stream a response you have to validate' holds because validating needs the whole answer; 'never retry a 400' is scoped to the request being malformed; 'every call needs a timeout' survives because no chapter shows a call without one. 'nobody is waiting' (batch) is a question the chapter asks the reader, not a claim it makes.
  Three absolutes were narrowed because the fix passes made them false: 'streaming bought you
  nothing' in three places (body, lab key, answer key) once the early-abort edge was added;
  'the status cannot tell them apart'; and a Warning that promised four thousand duplicate
  emails from a resume that can only produce one.
new-terms: verify-inputs.py: 100 new after the fix passes (58 before them), bare-terms 0 CLEAN. Triaged: server-sent events, delta, 429, exponential backoff, jitter, semaphore, batch endpoint and idempotent are all introduced here and all in Key Terms. 'idempotent' first failed the gate because only the whole sentence was bold; the word itself is now bold at its definition.
covers-misses: 0 (verify-coverage.py markdown/19-calling-a-model-reliably.md)
sha256: ff5cf52978789a3638457ec8cccfb98d7f28fce9cb39568b16a0d8e30916ebfa
reseal:
  Reopened 2026-10-28 for one change: a bold span that `latex/tools/filter.lua` turns into an automatic index entry began with a digit, which `tools/verify-index.py` now rejects. No text, claim or number was touched - see LEDGER-DEFECTS.md entry 33.
  Reopened again the same day for a stale cross-reference of my own making: the
  `return_exceptions=True` paragraph said the record was "the last section of this chapter",
  which stopped being true when "When the Pipeline Has Stages" was added after it during the
  same fix pass. Found by a book-wide grep while closing chapter 20.

## Before writing

- [x] `LEDGER-TAUGHT.md` consulted — what the reader already knows, and every "Do not" row read. The opening claims nothing false about what came before — read rows 1-18; the "Do not" rows that bear on this chapter are chapter 13's (do not re-derive sampling) and chapter 15's (do not re-explain prefill/decode). The chapter cites both rather than repeating them
- [x] The chapter's `TOC.md` row read: its opening problem, its Covers list, its page estimate (an estimate, never a target — `BOOK-GUIDE.md` §11) — 20pp estimate, 19 printed pages built (tools/pages.py: 19 214-232 19 20 95%). Nothing was padded to reach the estimate; the chapter went 13 -> 20 pages when the missed bank question was answered, then 20 -> 19 when two wordy paragraphs were tightened
- [x] **The chapter's non-scope declared** in the field above — what this chapter does not cover, so review has an edge and can terminate — see `non-scope:` above; seven exclusions, each with the chapter that owns it
- [x] Sources read **in full, immediately before writing** — named, with what was read — see `sources:` above
- [x] `BOOK-GUIDE.md` §6 boundary cases and `LEDGER-DEFECTS.md` to hand — verify-boundary.py CLEAN; no training, loss or architecture theory enters the chapter

## While writing

- [x] **Every number recomputed** against the thing it describes, in the file, before it was written — say how many — 9: the three programs' outputs (all three run before any sentence was written, per LEDGER-DEFECTS entry 24), the backoff ceiling table (0.5/1/2/4/8/8), 20 documents at 0.1s giving 2.0/0.5/0.1s, 120 a minute at 2s giving 4, 300 a minute at 4s giving 20, 8 hours for 10,000 at 3s each, and `max_tokens / 20 + 10` for a 1,000-token cap giving 60s against the 50s floor stated in the text
- [x] **Every absolute tested** against a counter-example *in the book*, not only in this chapter — `verify-absolutes.py` count, and what failed — see `absolutes:` above (80 flagged, each triaged)
- [x] **Every term the chapter builds on** already given to the reader — `verify-inputs.py` count, each triaged — see `new-terms:` above (58 new, bare-terms 0)
- [x] Maths written as raw LaTeX spans and fences, never `$…$` — 3 inline spans, no display fences, no `$…$`; verify-render.py CLEAN
- [x] The chapter holds the structure in `BOOK-GUIDE.md` §5; any lab is isolated and safe — problem, question, nine sections, lab, Summary/Key Terms/Worth Memorising/Review Questions/Review Answers, "You understand this when". The lab is pure stdlib: no network, no key, no account
- [x] Where a well-known explanation is wrong, the book states the correct rule — and it is flagged in the report — "stream everything, it is faster" is the common advice; the chapter states the correct rule, that you cannot stream a response you must validate, and gives the reason

## After writing

- [x] `verify-render.py` · `verify-voice.py` · `verify-boundary.py` — all CLEAN — all CLEAN (bash tools/check-all.sh). render failed first on three text-fence lines over 64 characters; shortened
- [x] `verify-coverage.py` — every miss triaged **one by one**, not counted — 0 misses, so nothing to triage
- [x] `\input{chapters/19-calling-a-model-reliably}` in `latex/book.tex`; `make` → 0 overfull · 0 missing glyphs · 0 undefined — line 71, replacing the commented placeholder. tools/build-probe.sh: exit=0 latex-errors=0 overfull=0 glyphs=0. Two build-side things were paid for on the way. The extra 19 pages pushed the last index page 0.22693pt over, which is LEDGER-DEFECTS entry 17's defect again, so the index glue's shrink went 3pt -> 4pt in `latex/preamble.tex`: 0 overfull, page count unchanged. A tolerance in the build gate was written first, which was wrong twice over - it diagnosed the box as the glossary when the log says the index, and it bought tolerance in place of a fix that was available and already documented - so it was reverted and deleted. And `latex/tools/check.sh` still carried the template's 50-100 page target, so `make check` had been printing PRE-FLIGHT FAILED on nothing else for weeks; raised to 100-1400, and it now prints PRE-FLIGHT OK
- [x] **Completeness review** launched with the `BOOK-GUIDE.md` §14 brief — 20 findings, 12 of them must-fix. Verified before accepting: the gather-discards-results claim, the flush claim under `kill -9`, the resume listing failing to run as printed, the 7.5s worst case and the missing bank question were each reproduced by running code or by grepping the bank
- [x] Each finding **verified before accepting**; each fix **grepped book-wide, count before and after — zero, or it is not done** — all 20 applied, each as an assert-once replacement with HIT/MISS printed per item (LEDGER-DEFECTS entry 28). Swept book-wide after: `nobody builds`, `Two timeouts`, `about fifteen seconds`, `thirty seconds of your pipeline`, `Five at once`, `bank-question`, `burst of slow calls`, `buys nothing`, `bought nothing` - 0 each. `Into a validator, never` survived once, in the generated cheat sheet, and went on the regeneration
- [x] **Fix-verification pass** launched, naming every changed passage — every changed passage named. It confirmed all 20 fixed or partly fixed, re-ran all five programs and all eight empirical lab steps against their keys, and found 14 new problems. The serious one was mine: `tools/overfull.py` diagnosed the overfull box as the glossary when the log says the index, and bought tolerance in place of a fix already documented in `latex/preamble.tex`. Reverted and deleted; the index glue's shrink fixed it instead. The other 13 were applied
- [x] `LEDGER-TAUGHT.md` row added; `LEDGER-DEFECTS.md` updated if a new defect class appeared — row 19 added, 23 "Do not" clauses. `LEDGER-DEFECTS.md` gained entries 29 to 32: a transformation that silently did nothing, the bank read as a remembered range, a gate that always failed, and a tolerance written in place of an available fix
- [x] `README.md` status updated; the part's PDF delivered — Part II at 2 of 22 chapters; 19 printed pages, 216 across Parts I and II

## Reviews

completeness-review: 2026-10-28. 20 findings, 12 must-fix. The real gap was bank question 42 and the TOC's 'multi-step pipeline', neither covered - a whole new section, program and review question. Four findings were things the chapter taught falsely and the reader would have said out loud: Review Answer 5 opening 'Five at once' when the answer is twenty; a margin argument that blamed slow calls when fast ones breach a rate limit; `f.flush()` described as what survives a crash when an exception loses nothing; and a read timeout described as a budget for the whole response. `resume.py` could not be run as printed. Verdict: not closeable, close - 'the rest is an afternoon'.
fix-verification: 2026-10-28. All 20 FIXED, one PARTLY (three surviving 'buys nothing' absolutes, since narrowed). It re-ran all five programs - every printed output matches a real run character for character - and all eight empirical lab steps. 14 new problems, all applied. The one that mattered was the build gate I had written: the box is the index, not the glossary; `latex/preamble.tex` already documented the same defect from entry 17; one point more shrink in the index glue removes it with no page change. It also found `make check` had been failing for weeks on the template's 50-100 page target. Verdict: closeable once those four are done, no third review needed.
