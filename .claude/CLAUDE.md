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
   **`[2026-11-12]` One job is pending and the owner asked for it to come up when he opens a
   session: protect the generated guide from hand edits.** `data-and-intelligence/guide/` is 75
   pages built by `utilities/build-di-guide.py`; **not one of them says so**, and a hand edit to
   any of them is silently erased by the next build. Two fixes were agreed in principle — the
   cheap one first. See *Protecting the generated guide* in the handover's Gotchas.
3. **Writing the interview-prep book.** The book in `books/interview-prep/`. It has nothing to do with the
   website and governs itself — go straight to `books/interview-prep/docs/HANDOVER.md` and `books/interview-prep/docs/BOOK-GUIDE.md`
   and follow those, not this file. **That book is finished** (2026-10-31, all 57 chapters and
   Appendix B); a session here is an edit to it, not drafting.
4. **`[2026-11-12]` Researching *Modern AI: Research, Science and Engineering*.** The book in
   `books/modern-ai/`. **It governs itself and does not follow this file** — go straight to
   `books/modern-ai/CLAUDE.md`, which sends you to `books/modern-ai/docs/ROADMAP.md`. **Its
   section *"What is next — read this first"* names the next action**, which the owner chose on
   2026-11-12: fetch a scope statement for each of the 62 categories the consolidation could not
   judge, before any area is cut. The roadmap's opening section records a question he has not
   answered, about what he expected this process to be; `[2026-11-12]` **it is open but it does not
   block the work** — this entry used to say nothing proceeds until he answers it, and he has since
   ruled four times and named the next action.
   `books/modern-ai/docs/HOW-IT-WORKS.md` is the plain-language map of the whole process, written
   for him. Nothing about the website. **This option was missing from this list for six days while
   it was the only work happening.**
5. **`[2026-11-12]` Writing *Python from Zero*.** The book in `books/python/`. **It governs
   itself** — go straight to `books/python/CLAUDE.md`, which sends you to `books/python/TOC.md`.
   **It started on 2026-11-12**: 51 chapters, approved by the owner, then reviewed twice and
   corrected. **No chapter is drafted**, and the thing blocking that is **not** the contents — it
   is decision 8's other half, the rules, and for this book one is live: **which of the finished
   book's gates transfer.** `books/python/CLAUDE.md` says so where a session reads it first.
   Nothing about the website.
6. **`[2026-11-12]` *Machine Learning and Deep Learning*, which is NOT started and may not be.**
   The owner ruled on 2026-11-12 that the books are written **sequentially**: *"once Python book
   is completely done we will go to ML&DL book."* **So a session does not start it, offer a table
   of contents for it, or draft a chapter of it.** Its decisions are in
   `books/future-books/README.md`, which records every one with its marker.
   **`[2026-11-12]` The parallel-writing section in that file no longer describes the plan.** It
   is kept because the ruling is reversible and the five shared things are still real. Read it
   only if two books are ever genuinely in flight at once.
   `[2026-11-12]` This entry said *"this said `books/FUTURE-BOOKS.md`, which has never existed"*;
   the path has been right since then.

Then follow the matching section of the handover: "Restyle work", "Website work", or
"The interview-prep book". **Kinds 4, 5 and 6 have no handover section and need none** — each
book's own files govern it. `[2026-11-12]` There are six kinds now, not five: the two unwritten
books were one entry while neither had started, and *Python* has.
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
