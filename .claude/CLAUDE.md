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
AskUserQuestion tool).

**`[STATED 2026-11-12]` Use these exact labels, word for word. The owner asked for them to be
fixed so the menu reads the same every time.** The tool shows **at most four options**, which is
why there are three kinds and not six — see the note at the end of this section.

| Label, exactly | Description, exactly |
|---|---|
| `Working on the website` | Pages, links, books, the roadmap sources, publishing, and the restyle |
| `Modern AI research` | *Modern AI: Research, Science and Engineering* — choosing the areas the book covers |
| `Writing Python from Zero` | The Python book: 51 chapters approved, no chapter drafted yet |

**Then follow the matching kind below.**

1. **Working on the website.** Content, pages, links, books, the roadmap sources, publishing —
   **and the restyle**, which `[2026-11-12]` is no longer a kind of its own: the handover records
   every reachable page restyled on 2026-09-26, so a session here changes a styled page rather than
   restyling a new one. **One job is pending and the owner asked for it to come up when he opens a
   session: protect the generated guide from hand edits.** `data-and-intelligence/guide/` is 75
   pages built by `utilities/build-di-guide.py`; **not one of them says so**, and a hand edit to
   any of them is silently erased by the next build. Two fixes were agreed in principle — the
   cheap one first. See *Protecting the generated guide* in the handover's Gotchas.
2. **`[2026-11-12]` Researching *Modern AI: Research, Science and Engineering*.** The book in
   `books/modern-ai/`. **It governs itself and does not follow this file** — go straight to
   `books/modern-ai/CLAUDE.md`, which sends you to `books/modern-ai/docs/ROADMAP.md`. **Its
   section *"What is next — read this first"* names the next action**, which the owner chose on
   2026-11-12: fetch a scope statement for each of the 62 categories the consolidation could not
   judge, before any area is cut. The roadmap's second section records a question he has not
   answered, about what he expected this process to be; **it is open but it does not block the
   work.** Nothing about the website.
3. **`[2026-11-12]` Writing *Python from Zero*.** The book in `books/python/`. **It governs
   itself** — go straight to `books/python/CLAUDE.md`, which sends you to `books/python/TOC.md`.
   **It started on 2026-11-12**: 51 chapters, approved by the owner, then reviewed twice and
   corrected. **No chapter is drafted**, and the thing blocking that is **not** the contents — it
   is decision 8's other half, the rules, and for this book one is live: **which of the finished
   book's gates transfer.** Nothing about the website.

**Two things that are NOT session kinds, and why:**

- **`[STATED 2026-11-12]` *Modern AI Engineering from Zero* is finished and needs no session
  type.** It is in `books/modern-ai-engineering-from-zero/` — **renamed from `interview-prep/` on
  2026-11-12**, because the book outlived the interview deadline it was named for. A change to it
  is website or book work like any other; the book governs itself through its own `docs/`.
- **`[STATED 2026-11-12]` *Machine Learning and Deep Learning* is not started and may not be.** The
  owner ruled that the books are written **sequentially**: *"once Python book is completely done we
  will go to ML&DL book."* **So a session does not start it, offer a table of contents for it, or
  draft a chapter of it.** Its decisions are in `books/future-books/README.md`.

  **`[STATED 2026-11-12]` It takes kind 3's place when *Python from Zero* is finished**, and this
  is the trigger, because a decision with no trigger means no. **The moment is the owner declaring
  the Python book finished** — the same moment that fires `books/future-books/README.md`
  decision 22, where the CS&E on-ramp stops pointing at the roadmap page and points at the book.
  **One moment, three consequences:** that link changes, the Python on-ramp entries drop their
  *Coming soon*, and kind 3 above is replaced, label and description, by:

  | Label, exactly | Description, exactly |
  |---|---|
  | `Machine Learning and Deep Learning` | The second book: everything the AI-engineering book black-boxed, including the mathematics |

  **Until he says the Python book is finished, nothing moves.** A built PDF is not the trigger; his
  word is.

**`[2026-11-12]` There are three kinds now, not six.** The owner removed the interview-prep book.
**Folding the restyle into website work, and moving the machine-learning prohibition out of the
list, is mine** — he was shown the argument and did not rule on it. The reason is mechanical as
well as tidy: **the question tool shows at most four options, and six could not be asked.** To
restore either, put it back as its own numbered kind.

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
