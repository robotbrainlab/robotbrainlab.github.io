# Towards Intelligence — session instructions

## This file can be out of date. The repository cannot.

Where this file and the actual state of the repository disagree, **the repository wins**.
Check what the files and the code actually do before you act on an instruction here. Do not
change the repository to match this file. Say that this file looks out of date, and ask.

Why this rule exists: measured on 40 projects and 320 runs, coding agents followed a stale
instruction file over the existing code **90.1%** of the time. One agent reported the conflict in
79 of 80 runs and followed the file anyway; another rewrote working code to match the file, and
the project's tests then failed. One sentence giving the code precedence moved code-following
from 4.2% to 91.4% and the test pass rate from 89.4% to 100%
([arXiv 2610.30571](https://arxiv.org/abs/2610.30571), verified 2026-11-03; the study tested a
user-level file, this is a project-level one).

## First thing in every session

Before doing anything else, ask the user which kind of work this session is (use the
AskUserQuestion tool):

1. **Changing the HTML look.** This means the restyle to the reference design; content stays letter-for-letter.
2. **Working on the website.** This means content, pages, links, books, the roadmap sources, publishing.
3. **Writing the interview-prep book.** The book in `books/interview-prep/`. It has nothing to do with the
   website and governs itself — go straight to `books/interview-prep/docs/HANDOVER.md` and `books/interview-prep/docs/BOOK-GUIDE.md`
   and follow those, not this file. **That book is finished** (2026-10-31, all 57 chapters and
   Appendix B); a session here is an edit to it, not drafting.
4. **The two books that come after it** — Python, and Core Machine Learning and Deep Learning.
   **Neither is started, and neither may be started until its rules are written and its table of
   contents approved**, which is the owner's instruction. Read `books/FUTURE-BOOKS.md` first;
   it records every decision and the rules still to be settled. Nothing about the website.

Then follow the matching section of the handover: "Restyle work", "Website work", or
"The interview-prep book".
If the user's first message already makes the answer obvious, confirm it in one line instead
of asking.

**Exception: unattended restyle run.** If the first message asks you to follow
`.claude/RESTYLE-RUNBOOK.md`, don't ask anything. Go straight to the runbook; the user is away.

If the user wants to undo the redesign or part of it, follow "Rolling back the redesign" in the
handover. Those recipes were tested; confirm with the user before pushing a rollback.

## Standing rules, in every kind of session

**`[STATED 2026-11-12]` Read. Do not substitute a search, a pattern or a count for reading.** This
binds every session in this repository — the website, every book, and ordinary repository work —
not only the research work in `books/modern-ai/`. **A program may check form; it may never judge
content.** Where a search or a count is used, it is a hint about where to read and never the
finding itself.

**Why it is here and not only in the book.** The owner made it a rule for the research process, was
then asked whether it was the standing rule for everything, and said it was. On 2026-11-11 three
pattern matches were used in one day to answer questions about meaning and all three were wrong,
and **one of them was ordinary repository work**: a sweep for a phrase found six places where
reading found twenty-five.

**`books/modern-ai/docs/briefs/README.md` owns the agent-facing form of this rule** — the wording
the briefs carry, and the table of what may and may not be automated. Read it there before changing
anything about it.

## Handover

@HANDOVER.md
