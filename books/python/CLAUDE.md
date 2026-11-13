# Python from Zero — session instructions

## This file can be out of date. The repository cannot.

Where this file and the actual state of the repository disagree, **the repository wins**. Check
what the files actually say before acting on an instruction here. Do not change the repository to
match this file. Say that this file looks out of date, and ask.

## What this is

A book that teaches Python from the first program, built against the **Fundamentals stage** of the
owner's own roadmap page at `../../data-and-intelligence/books/python-roadmap.html` — six phases,
49 projects, three capstones. The Advanced and Mastery stages are **not** in this book.

It is the **first** of the two books still to be written. `../future-books/README.md` holds every
decision about both, and is the authority on all of them. **This file does not restate those
decisions**; it says what a session does.

**Writing is sequential.** `[STATED 2026-11-12]` Python is finished completely before *Machine
Learning and Deep Learning* starts. Do not start the second book.

## First thing in every session

**Read `TOC.md`** — the contents, 51 chapters in four parts. It is approved and it has been
reviewed. Its last section, *What the review found*, lists fourteen faults two reviews found in it
**after** it was approved, and what was done about each. Read that section before trusting any
other summary of this book, including this file.

Then read only what the work needs:

| Read | For |
|---|---|
| `GATES.md` | **What says a chapter is finished.** Read it before writing anything |
| `../future-books/README.md` | Every decision, with its marker. **Nothing is a decision unless it is `[STATED]` or `[AGREED]`.** `[I RECOMMEND]` is a proposal the owner has not ruled on |
| `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §5 | **The chapter shape**, copied exactly (decision 18). §5 is the spec; do not reinvent it |
| `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §6, §7, §9 | The maths line, the writing style, and what a lab is |
| `../modern-ai-engineering-from-zero/docs/LEDGER-DEFECTS.md` | What the gates cannot catch. 20 entries, earned |
| `../../data-and-intelligence/books/python-roadmap.html` | The source. **Read the HTML, not a stripped copy** — the owner asked for this specifically, and reading the stripped text once hid phase 1.5's reading list |

## `[STATED 2026-11-13]` DRAFTING IS UNBLOCKED. Both of decision 8's conditions are met

Decision 8 has **two** conditions: *"Nothing is drafted until **the rules are written** and the
table of contents is approved."*

- **The contents were approved** on 2026-11-12, then reviewed twice and corrected.
- **The rules are written.** They are `GATES.md`, ruled on by the owner on 2026-11-13:
  *"you can go ahead with your recommendations."*

## `[STATED 2026-11-13]` What the next session does: WRITE CHAPTER 1

**Chapter 1 is `01-getting-python-and-running-something`.** Its line is already in `book.tex`,
commented out. Nothing else is waiting.

```bash
python3 tools/chapter.py begin 01-getting-python-and-running-something
```

**Read `GATES.md` first, in full.** §7 says how the book is written and who is asked what; the
rest says what test declares a chapter finished.

**Three rulings that decide how the next session behaves:**

- **One chapter at a time, finished completely.** Not a batch, not continuously. `GATES.md` §7
  carries the evidence that decided it.
- **The owner is NOT asked to approve each chapter.** The reviews, the gates and the record do
  that. Do not stop to ask.

**One thing to check before chapter 12 or 13, not before chapter 1:** `pytest` and `hypothesis`
are **not installed** on this machine, and `uv` is. Those two chapters teach them, so their code
samples cannot be run until they are. Chapters 1 to 11 do not need them.

**What exists now, and did not on 2026-11-12:**

| | |
|---|---|
| `GATES.md` | The ruling, tool by tool |
| `tools/` | 20 files. `bash tools/check-all.sh` runs the suite |
| `docs/briefs/` | The two review briefs, which are step 3 and step 5 of the chapter loop |
| `book.tex`, `book-meta.tex`, `markdown/` | The book builds. **All 51 chapters are listed in `book.tex` and commented out** — a chapter joins the book by being written and having its line uncommented |
| `LEDGER-TAUGHT.md`, `LEDGER-DEFECTS.md`, `records/`, `labs/` | Empty, each saying what goes in it |

**The chapter loop, which is a driver and not a habit:**

```bash
python3 tools/chapter.py begin    01-getting-python-and-running-something
python3 tools/chapter.py written  01-getting-python-and-running-something
python3 tools/chapter.py reviewed 01-getting-python-and-running-something
bash tools/check-all.sh            # must end ALL GATES PASS
```

## The book's title, and the name the on-ramps give it

**`[STATED 2026-11-12]` The book is *Python from Zero*. The on-ramps call it
*Programming Language From Zero: Python*, and that is deliberate** — the same rule the CS&E
on-ramp has used since 2026-10-29: **the topic is the language, Python is the instance.** So the
entry in `../../data-and-intelligence/on-ramp.html`, and the CS&E entry that will point here once
this book ships (`../future-books/README.md` decision 22), both carry the longer name while the
book's own cover does not. **Do not "fix" either to match the other.**

## The rules that are easy to break

- **This book points at three others rather than repeating them.** Each pointer is the owner's
  ruling, not a convenience:
  - ***Linux and Git from Zero*** (`../linux-and-git/`) — the shell, the editor and Git. **The
    book teaches none of it.** `[STATED 2026-11-12]` *"make sure you point to the Linux and Git
    Book."*
  - ***APIs to FastAPI*** (`../apis-to-fastapi/`) — building a web service. **The book teaches
    none of it.** `[STATED 2026-11-12]` *"We have the API book already, just point it out there
    just like Linux and Git Book."* Part III stops at the Python a service needs.
  - The roadmap page itself. `[STATED 2026-11-12]` **Nothing happens to the page.** But
    **`[STATED 2026-11-12, later the same day]` the CS&E on-ramp will stop pointing at it once
    this book is finished** and will point at the book instead — one `href` in
    `../../cse/index.html`, nothing else, and nothing until the book is done
    (`../future-books/README.md` decision 22). The page itself stays exactly
    as it is when this book ships. Do not repoint it, do not retire it, do not propose either.
- **Six of the 49 roadmap projects are deliberately not placed**, each with the book that owns it.
  `TOC.md`'s header lists all six. **Never silently re-add one, and never silently drop another** —
  an unnamed cut is `../modern-ai/docs/LEDGER-DEFECTS.md` entry 5a, the worst failure this project
  has recorded.
- **The language is taught twice** (decision 15). Part I gets the reader writing Python; Part II
  returns to the same ground and explains it. **This is the mechanism, not redundancy.** Do not
  merge the passes.
- **Page estimates never decide scope** (decision 14). The finished book's size is permission, not
  a target. `TOC.md` carries no page column on purpose; do not add one.
- **One chapter at a time. Never a part at a time.** Read that chapter's roadmap sources in full
  immediately before writing it.
- **Read. Do not substitute a search, a pattern or a count for reading.** `../../.claude/CLAUDE.md`
  makes this a standing rule for every session in this repository. A grep is a hint about where to
  read, never the finding. **This rule has been broken on this book already**: the first version of
  a decision about phase 1.5 was written from regular expressions over the roadmap page and dropped
  SQL; the owner caught it.
- **The owner is never handed an unrecommended list.** Propose, with a reason per item, and he
  rules. A sorted inventory is not a proposal.
- **An `[I RECOMMEND]` item is put to him before the first time it binds something real, named as
  mine, and never in a batch** (`../modern-ai/docs/GOAL.md` §0, `[STATED 2026-11-12]`). Two stand
  against this book: decision 13, the test for what is taught, and decision 21, the kinds that get
  a one-page entry instead. `TOC.md` says where each already binds.
- **The repository is public.** Scan for secrets before every commit. Push only to the
  `github-robotbrainlab` remote; never as the `dlakshmizlk` account.

## Style, in everything the owner reads

Plain, controlled English — about 80% ASD-STE100. Short sentences. Active voice. The answer first,
then what was done and decided, then the explanation. Tables where they carry the information
better than prose. **No internal codes or shorthand: name things.** He asked for this directly on
2026-11-12, including for the questions put to him.

## Where things are

| Path | What |
|---|---|
| `TOC.md` | The contents. Approved, reviewed, corrected |
| `../future-books/README.md` | Every decision about this book and the next |
| `GATES.md` | **What says a chapter is finished.** The gates, the two reviews, and the hand checks |
| `tools/` | The machinery. `check-all.sh` is the suite; `chapter.py` is the driver |
| `docs/briefs/` | `completeness-review.md` and `fix-verification.md` |
| `LEDGER-TAUGHT.md` | What the reader already knows. **Read before writing any chapter** |
| `LEDGER-DEFECTS.md` | What the gates cannot catch. Starts empty on purpose |
| `../latex/` | **The shared build, which serves every book.** Treat as frozen; a book needing its own style adds `../latex/styles/python.tex`, which is additive |
| `../README.md` | The book index |
