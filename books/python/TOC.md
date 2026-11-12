# Python from Zero — Table of Contents

**Status: approved by the owner 2026-11-12, then reviewed and corrected. See *What the review
found* at the end.**

**`[2026-11-12]` Approving this list does NOT unblock drafting, and the first version of this line
said it did.** Decision 8 has **two** conditions — *"Nothing is drafted until **the rules are
written** and the table of contents is approved"* — and this line quoted only the second. **The
rules are still unwritten**; `../future-books/README.md` lists what is left under *The rules still
to be written*. That work stands between this list and chapter 1.

- **Scope: the Fundamentals stage of the roadmap, and nothing above it**
  (`../../data-and-intelligence/books/python-roadmap.html`, decision 10). Six phases, 49 projects,
  three capstones. The Advanced and Mastery stages are not in this book.
- **Prerequisite: *Linux and Git from Zero*** — `../linux-and-git/Linux and Git from Zero.pdf`.
  The book starts at the first Python program. **It does not teach the shell, the editor or
  version control at all, and it says so and points at that book wherever the ground would
  otherwise be covered twice.** `[STATED 2026-11-12]` The owner ruled this: the Git chapter is
  dropped, and the pointer replaces it.
- **Order is reading order.** The book is written in the order it is read.
- **No page estimates appear in this file, deliberately.** `../future-books/README.md` decision 14
  says the finished book's size is permission and never a target, and that the figure may not be
  cited for including or excluding anything. A page column would be cited.
- **Every chapter in Parts I–III has a lab with expected results** (decision 18), so the roadmap's 49 projects
  become the labs. The **Lab** column names which project feeds which chapter. Projects are cited
  as *phase.number* — `1.3 p7` is Phase 1.3's project 7.
- **43 of the 49 are placed. The other six are named, not dropped silently**, and each one went
  with a chapter the owner ruled out. **Four belong to *APIs to FastAPI***: `1.5 p4` URL
  shortener, `1.5 p5` CRUD API with auth, `1.5 p6` async endpoints, and phase 1.5's own project,
  *a service you'd actually use*. **A fifth, `1.5 p7` the OWASP audit, belongs to no book** —
  chapter 51 sends it to the OWASP page itself, because neither *APIs to FastAPI* nor this book
  teaches the top ten and pretending otherwise would be a pointer to nowhere. **One belongs to *Linux and Git from
  Zero***: `1.2 p9`, below. **Chapter 51 lists all six with the book that owns each.**
  **What this costs is stated plainly, not buried:** phase 1.5's building half leaves this book,
  and with it the stage exit criterion *"Build a tested, typed API from empty directory to running
  service in an afternoon."* **The reader still builds one** — Capstone 3 in chapter 50 is a
  backend service — but the teaching for it is in the other book, by the owner's ruling.
- **The sixth: project `1.2 p9`**, *History surgery — interactive rebase on a messy branch*, had
  the Git chapter and lost it with that chapter. **It belongs to *Linux and Git from Zero***, and
  chapter 51 points the reader there for it. **Stated at its real strength:** that book's chapter 10 covers *"rebasing in
  brief"* — which is less than the roadmap's project asks for, and the only thing in this stage
  that neither book now covers in full. It is a small, named gap and not a silent one, which is
  the failure `../modern-ai/docs/LEDGER-DEFECTS.md` entry 5a exists for.
- **The language is taught twice, on purpose** (decision 15). Part I gets you writing Python.
  Part II returns to the same ground and shows you why it behaves that way. The roadmap calls the
  second pass *"the hinge of everything here"* and makes `1.1 before 1.3` one of its only two hard
  orderings. **This is the mechanism, not a redundancy to remove.**
- **Chapter shape is copied from `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §5**, exactly, per
  decision 18. Each chapter opens with its problem below, then the question it raises.

---

## `[STATED 2026-11-12]` The four part names did not survive, and the owner ruled on it

**Decision 19 carried Understand / Use / Apply / What Next across as a default. Only *What Next*
survives here, and the reason is decision 15. The owner was shown the three options below and
chose the new names.** This discharges decision 20 **for *Python* only**; that row still
governs *Machine Learning and Deep Learning*, which gets the same four names as its default and
the same test.

The four names are a progression in what a reader can do: comprehend, then operate, then
construct, then judge. **Python's material does not arrive in that order, because the roadmap
deliberately inverts the first two steps.** Phase 1.1 has you *writing* Python before anything
explains why it behaves as it does, and phase 1.3 — the second pass — is where the understanding
lands. Naming Part I *Understand* would describe phase 1.3 and mis-describe phase 1.1.

Three ways out were considered:

| Option | Why it was not taken |
|---|---|
| Keep the names, teach 1.3 first | Breaks the roadmap's hard ordering `1.1 before 1.3`, and removes the double pass decision 15 protects |
| Keep the names, call 1.1 *Understand* | Puts the deepest material (1.3) in the middle of the book under *Use*, which is the opposite of what it is |
| **Name the parts for the stage the reader is at, and keep *What Next*** | **Taken.** The same sequencing point as `../modern-ai/docs/GOAL.md` §5.3, *structure follows the subjects* — **which is marked `[I RECOMMEND]` there, in a section headed *Structure — not yet decided*, and about a different book. It is cited as a parallel, not as authority.** What carries this row is the owner's own ruling above it |

**`[2026-11-12]` Note what this does NOT overturn.** Decision 19 still stands in full: the
interview bank, the four threads and the chapter shape all transfer, and Part IV is still called
*What Next*. **Only the division of material into the first three names changed**, which is the
one limit decision 20 reserved. ***Linux and Git from Zero* keeps all four names**, and that is
correct — its material does arrive in that order.

**The grouping follows the roadmap's own statements about its phases**, not my taste:

- **1.2 joins 1.1** because the roadmap places 1.2 early for a stated reason: *"Placed here, not
  later, so every project in 1.3–1.5 is built properly from the first commit."*
- **1.4 joins 1.5** because the roadmap says *"1.4 and 1.5 are meant to run together — build the
  API while you learn concurrency, and put the concurrency into the API."*
- **1.3 stands alone** because it is the one phase the roadmap singles out: *"If you read one
  phase on this page, make it 1.3."*

---

## Part I · Write It — phases 1.1 and 1.2

*Part I's own note:* ignore *why* Python behaves as it does. Part II is that. Here you are learning
to write it, and to write it to a standard somebody else would accept.

*What to ignore for now:* the data model, the method resolution order, and every sentence that
begins *"the reason this works is…"*. You will meet all of it in Part II, after you have written
enough Python for the explanation to land on something.

*And one thing this part does not teach at all:* **the shell, the editor and Git.** Chapters 11 to
17 assume you can already branch, commit and read a diff. **If you cannot, read *Linux and Git
from Zero* first** — `../linux-and-git/Linux and Git from Zero.pdf`. It is a prerequisite of this
book and not an optional extra, and this part says so again at the first chapter that needs it.

| # | Chapter | Opens with | Covers | Lab |
|---|---|---|---|---|
| 1 | Getting Python, and Running Something | I have Python installed three times already and I don't know which one runs when I type `python`. | The interpreter and where it lives; `uv` for a project and an environment; running a file, a module and the REPL; what a virtual environment actually isolates | Set up a project, run it three ways |
| 2 | Values, Types and Operators | I can read `x = 1`. I cannot tell you what Python did, or why `0.1 + 0.2` isn't `0.3`. | Objects and names; numbers, strings, booleans; operators and precedence; binary floating point and where it bites; `Decimal` when the cents must reconcile; **f-strings and format specifications** — width, alignment and decimal places, which project 1 needs | 1.1 p1, p2 — Unit converter, bill splitter |
| 3 | Control Flow and Functions | Loops and `if` I can manage. `match` looks like a `switch` and people tell me it isn't. | `if`/`elif`/`else`, `for`, `while`; `match` and structural patterns; defining functions; arguments, defaults and return values; what a function returns when you don't say | 1.1 p3 — Number-guessing game |
| 4 | The Four Data Structures | I use a list for everything. I suspect that's wrong and I can't say when. | `list`, `tuple`, `dict`, `set` — what each costs and what each guarantees; comprehensions; sorting with `key`; `Counter`, `defaultdict` and `deque`, and when to reach for them | 1.1 p4, p5 — Word frequency, contact book |
| 5 | Modules and Packages | My code is one long file and I know that's a problem. I don't know what the right shape is. | Modules, imports and the import path; `__name__`; packages and `__init__.py`; what `python -m` does; circular imports and why they happen | 1.1 p6 — Text-utility module |
| 6 | Files, Paths and Formats | I've been building file paths by gluing strings together with slashes. | `pathlib` instead of string paths; opening, reading and writing; `json` and `csv`; `shutil` and `zipfile`; why you close a file and what `with` is doing | 1.1 p8, p9 — File organizer, CSV→JSON |
| 7 | Text, and the Encodings Under It | I got a `UnicodeDecodeError` and solved it by copying a Stack Overflow line I don't understand. | Characters, code points and bytes; what an encoding is; `str` versus `bytes`; reading a file that isn't UTF-8; normalisation, and why two identical-looking strings compare unequal | A file that round-trips through three encodings |
| 8 | Errors and Exceptions | My scripts stop on the first bad row. I want them to keep going and tell me what went wrong. | Raising and catching; the exception hierarchy and its shape; `try`/`except`/`else`/`finally`; custom exceptions; catching too much, and why a bare `except` hides bugs; reading a traceback | Count the bad rows instead of stopping on the first |
| 9 | Classes, First Pass | I've written classes that were just dictionaries with extra steps. | Defining a class; `__init__` and instance state; methods; `__repr__` and `__len__`; `@property` and enforced invariants; when a class is the wrong answer | 1.1 p10, p11 — Deck of cards, bank account |
| 10 | The Standard Library You Will Actually Reach For | The standard library is enormous and I don't know which parts I'm supposed to already know. | A tour with a purpose: `re` and the Regex HOWTO in full; `datetime` and the aware-versus-naive distinction that causes the bugs; `argparse` for a real CLI; `subprocess`, and why `shell=True` is never the answer. **Closing with the two FAQs** — *Design & History*, then *Programming*, both in full, which is where the roadmap puts them and which answer *why is Python like this* | 1.1 p7, p12, phase project — Log parser, backup tool, Journal CLI |
| 11 | Style, and the Tool That Enforces It | Everyone's Python looks the same and mine doesn't. I can't tell if that matters. | PEP 8, PEP 20 and PEP 257; docstrings; `ruff` configured and run; fixing every finding in code you already wrote; why a formatter ends the argument rather than winning it | 1.2 p1 — Ruff everything |
| 12 | Testing: Functions, Fixtures and Parametrization | I've written tests that passed whatever the code did. | `pytest` and test discovery; assertions; fixtures and what they are for; the builtin fixtures; parametrizing instead of copying a test body; markers | 1.2 p2, p3 — Retrofit tests, parametrize |
| 13 | Testing: Strategy, Mocking and Properties | I test the happy path. I know that isn't testing. | Test strategy and what to cover; configuration and coverage; mocking, and the trap of testing the mock; debugging a failing test; advanced parametrization; property testing with Hypothesis | 1.2 p4 — Hypothesis finds a bug you'd never test for |
| 14 | Type Hints | I've seen `-> None` and `List[str]` and copied them without knowing what checks them. | Annotations, and that Python does not enforce them; the `typing` vocabulary; `mypy` and what `--strict` actually demands; `Protocol` versus a base class; `Any` as a defeat | 1.2 p5 — `mypy --strict`, zero `Any` |
| 15 | Packaging and Publishing | My project runs when I'm in its folder and nowhere else. | `pyproject.toml`; the `src` layout and why it exists; dependencies and version constraints; building a wheel; TestPyPI, then PyPI; what a stranger needs to install it | 1.2 p6, p7 — `src` layout, publish |
| 16 | Logging and Configuration | I debug with `print()` and delete them afterwards. Usually. | Why `print` is not logging; levels and what each is for; `dictConfig`; handlers and formatters; configuration layered defaults → file → environment, with `tomllib` and `os.environ` | 1.2 p8 — Replace every `print()` |
| 17 | Continuous Integration | I run the tests on my machine. I have no idea whether they pass on anyone else's. | What CI is for; a GitHub Actions workflow; a matrix across three Python versions; caching; a red build as information rather than an insult; branch protection | 1.2 p10, phase project — CI matrix, journal professional-grade |

---

## Part II · Why It Works That Way — phase 1.3

*Part II's own note:* nothing here is new syntax. Every chapter returns to something Part I had you
write, and explains it. **The roadmap calls this phase the hinge of everything, and says most
self-taught developers never arrive here — which is exactly why they plateau.** Do not rush it.

*What to ignore for now:* descriptors, metaclasses and the C API. The first two are the Advanced
stage and the C API is further out still — the roadmap puts it in Mastery and tells you to skip it
*"before Advanced is complete"*. Either way
this book stops below them. Chapter 51 says where they are.

| # | Chapter | Opens with | Covers | Lab |
|---|---|---|---|---|
| 18 | The Data Model | People say "everything in Python is an object" as if it explains something. It doesn't, yet. | What the data model is; special methods as a protocol the language calls on your behalf; why `len(x)` and `x.__len__()` are not the same thing; the one idea the rest of this part is built on | Make a plain class answer to three builtins |
| 19 | Names, Binding and Scope | I was bitten by a mutable default argument and the explanation I found made no sense. | Names as labels, not boxes; binding versus mutation; aliasing; `LEGB` scope; `global` and `nonlocal`; why the default argument is evaluated once; the prediction drill | 1.3 p1 — Predict 15 outputs in writing first |
| 20 | Objects, Copies and Identity | `a = b` sometimes copies and sometimes doesn't, and I can't predict which. | Identity, equality and `is`; shallow and deep copies; writing a deep copy by hand; reference cycles and what survives one; what `id()` tells you and what it doesn't | 1.3 p2 — Deep copy by hand, survive a cycle |
| 21 | Special Methods as Protocols | I know `__init__`. I don't know what else the language will call if I define it. | The protocols that matter: sequence, iterable, container, callable; `__repr__` that round-trips through `eval()`; operator overloading; arithmetic that refuses the wrong operand | 1.3 p3 — `Vector` |
| 22 | Hashing, Equality and Immutability | I put an object in a set twice and got two entries. | The `__hash__`/`__eq__` contract and what breaks when you violate it; why a mutable object should not be hashable; ordering with `__lt__` and `functools.total_ordering`; immutability as a design choice | 1.3 p4 — `Money`: hashable, orderable, refuses cross-currency |
| 23 | Functions Are Objects | I've passed a function as an argument. I don't understand what I handed over. | Functions as first-class objects; closures and what they capture; `functools.partial`; `lru_cache`; `singledispatch`; the functional tools and where they stop being clearer | 1.3 p7 — Memoizing decorator, written before reading `lru_cache` |
| 24 | Decorators | Decorators are the thing I copy and never write. | What `@` does, in two lines; writing one; preserving metadata with `wraps`; a decorator that takes arguments; one implementation that works bare *and* parameterized | 1.3 p6 — `@retry(times=3, backoff=2)` |
| 25 | Iterators and Generators | I know a generator saves memory. I can't tell you what it actually is. | The iterator protocol; `yield` and what suspends; generator expressions; a pipeline of generators; `itertools`, and the recipes at the bottom of its page that are the real payload | 1.3 p8 — Rewrite the CSV converter, measure with `tracemalloc` |
| 26 | Context Managers | `with open(...)` is the only `with` I've ever written. | What `with` guarantees; `__enter__` and `__exit__`; `@contextmanager`; `ExitStack` and `suppress`; a writer that leaves the original file intact when it fails | 1.3 p9 — Atomic file writer |
| 27 | Modern Class Design | My classes have six lines of boilerplate before anything happens. | `dataclasses`; `enum`; `Protocol` versus ABC, and structural typing; `collections.abc` and what inheriting from it gives you; composition over inheritance, with a refactor | 1.3 p5, p10 — Custom mapping; refactor to composition |
| 28 | Inheritance, `super()` and the MRO | I use `super().__init__()` because the tutorial told me to. | What `super()` actually does; the method resolution order and how it is computed; why it is not "the parent class"; cooperative multiple inheritance, and when to refuse it | 1.3 phase project — Journal on the data model |

---

## Part III · Build With It — phases 1.4 and 1.5

*Part III's own note:* the roadmap calls phase 1.5 *"the only phase that isn't Python"* and *"a
vehicle, not a subject"*. **One part of it is treated as a subject here, on your ruling: SQL and
databases** (decision 17). **Building an API is not**, and this part stops short of it.

*And one thing this part does not teach at all:* **how to build a web service.** `[STATED
2026-11-12]` The owner ruled it out — *"We have the API book already, just point it out there just
like Linux and Git Book."* **Read `../apis-to-fastapi/APIs to FastAPI.pdf`** for it. That book's
Part III is eight chapters on exactly this, and the roadmap already names it inside phase 1.5.
This part teaches the Python that a service needs — storage, validation, and calling other
services — and sends you there for the service itself. **This is decision 16 obeyed**, whose
rejected column reads *"Teaching web frameworks and APIs again in the book's own words, which
rewrites eight chapters of a published book."*

*What to ignore for now:* deployment. Docker and hosting are outside the roadmap and outside this
book. Chapter 51 says so and says where to go.

| # | Chapter | Opens with | Covers | Lab |
|---|---|---|---|---|
| 29 | I/O-Bound, CPU-Bound, and the GIL | I've read that Python can't do threads properly. I've also read that's a myth. | What makes a program wait versus what makes it work; the global interpreter lock, what it actually locks, and what it does not; why threads help one kind of program and not the other; measuring which kind you have | Time the same job both ways |
| 30 | Threads and Queues | I started a thread, it printed nothing, and the program exited. | Starting and joining; why shared mutable state goes wrong; a queue as the way threads talk; a worker pool; clean shutdown and the sentinel | 1.4 p1 — Threaded downloader |
| 31 | One Interface, Two Executors | There appear to be four ways to do this and I don't know which to pick. | `concurrent.futures`; `ThreadPoolExecutor` and `ProcessPoolExecutor` behind one interface; futures, results and exceptions; `map` versus `submit`; the difference between the two executors as the whole lesson; measuring the speedup and explaining the gap between it and the number of cores | 1.4 p2 — Parallel file processor |
| 32 | Processes, Underneath | I used `ProcessPoolExecutor` and it worked. I don't know what it did. | What the executor was hiding: process creation, start methods, and what has to be pickled to cross the boundary; `multiprocessing` pools directly; why an object that works in a thread fails in a process | Send an unpicklable object across, and fix it |
| 33 | `asyncio` | `async def` and `await` look like syntax I can paste. I'd rather understand them. | The event loop; coroutines as suspendable functions; `await` as a yield point; why one blocking call stalls everything; `asyncio.run`; debug mode | 1.4 p3 — Async fetcher, semaphore-bounded |
| 34 | Tasks, Cancellation and `TaskGroup` | I cancelled a task and something leaked. | Tasks versus coroutines; `TaskGroup`; `CancelledError` and why you must not swallow it; `timeout()` and `shield()`; **cancellation is the part everyone gets wrong** | 1.4 p4 — A task cancelled cleanly mid-flight |
| 35 | Choosing a Model | I now know three ways to do this and still can't choose. | The decision in one sentence; the same job written three ways and measured; what each costs in complexity; when the answer is "none of them, make it faster instead" | 1.4 p5, phase project — Three ways measured; concurrent tool |
| 36 | Storing Data: SQLite and SQL | I've only ever stored data in JSON files and I know that stops working. | Why a database; `sqlite3` with zero setup; tables, types and constraints; `SELECT`, `INSERT`, `UPDATE`, `DELETE`; parameterized queries, and SQL injection as the reason | 1.5 p1 — Task manager on SQLite |
| 37 | Joins | I can query one table. The moment there are two I write a loop in Python. | Primary and foreign keys; inner, left and the others, with the same small data each time; why a loop in Python is the wrong answer; `GROUP BY` and aggregates; the join that silently multiplies your rows | Build the same report three ways, one correct |
| 38 | Indexes, and Why Your Query Is Slow | A query got slow and nothing errored. I had no idea where to look. | What an index is and what it costs; which column to index; why an index on the wrong column does nothing; `LIKE '%x'` and the leading wildcard; composite indexes and column order | *Use the Index, Luke!* ch. 1–5, against your own schema |
| 39 | Transactions | Two things had to both happen. One did. | Atomicity, and what a transaction guarantees; `COMMIT` and `ROLLBACK`; isolation levels in plain terms; what a deadlock is; why autocommit surprised you | A transfer that must not half-happen |
| 40 | Reading a Query Plan | I know the query is slow. I don't know why. | `EXPLAIN` and `EXPLAIN QUERY PLAN`; scan versus seek; what the planner is estimating and how it gets it wrong; confirming a fix rather than hoping | Make one query fast, prove it |
| 41 | An ORM, and What It Hides | An ORM made my queries slower and I couldn't see them. | SQLAlchemy 2.0: the core and the session; mapping classes to tables; relationships; **the N+1 query, found by logging the SQL**; when to drop to raw SQL | Find and fix an N+1 |
| 42 | Migrations | I changed a column by hand on my own machine and broke everything else. | Why a schema needs version control; Alembic; autogenerate and why you read what it wrote; a data migration; the migration that cannot be undone | 1.5 p2 — Three migrations, one of them data |
| 43 | Moving to Postgres | SQLite is fine. I'm told it won't be. | What changes and what doesn't; `psycopg` 3; types SQLite was lax about; connection pools; **why a hosted service cannot keep SQLite on an ephemeral filesystem** | Move one project across |
| 44 | Validating What Comes In | I check incoming data with a pile of `if` statements. | Pydantic v2 models; validators; parsing versus validating; how it builds on Part II's dataclasses; errors a caller can act on | Reject six malformed payloads, each for a stated reason |
| 45 | Calling Other Services | My script hung for eleven minutes because a server never answered. | **Assumes `../apis-to-fastapi/APIs to FastAPI.pdf` ch. 1–8** for what an API is, HTTP, REST, auth, pagination, rate limits, retries and idempotency — **this chapter does not re-teach any of them.** Here only the Python: `httpx`; **a timeout on every outbound call, unprompted**, which is a stage exit criterion; `tenacity` for the retry policy; reading a paginated response into an iterator | 1.5 p3 — API client |

---

## Part IV · What Next

*No "What to ignore for now" note*, because this part's last chapter says what to skip —
the same rule `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §5 states.

**The four threads transfer** (decision 19), asked of Python's own subject rather than of a model.
Per §5, Part IV chapters carry **none of its last four items**: no callouts, no lab, no
`## Summary, Key Terms, and Review Questions` block, and no `> **You understand this when** …`
line. `[2026-11-12]` The first version of this sentence named three of the four and left out the
callouts and the closing line, which is the sentence a writer would have worked from.

| # | Chapter | Opens with | Covers |
|---|---|---|---|
| 46 | Thread · Security | I've fixed the holes I was told about. I don't know how to look for the rest. | Untrusted input as the single idea, in the Python the book has taught: `subprocess` and `shell=True`, which phase 1.1 names and tells you to read twice; `pickle` as remote code execution, which is what phase 1.4's *"how data crosses the boundary"* is really about; secrets that end up in git; what `pip install` actually runs. **`[2026-11-12]` The roadmap marks *security hygiene* as not covered by it**, so this chapter is the thread asking its question of this book's own material, and does not become a security course. **API security belongs to `../apis-to-fastapi/`, and the OWASP API Security Top 10 to the OWASP page**, which chapter 51 names — no book here teaches it |
| 47 | Thread · Speed | My program is slow and my instinct is to rewrite it in something else. | **Finding** the slow thing, not tuning it: measure before you change anything; `timeit`, `cProfile`, `tracemalloc`; algorithmic cost before micro-optimisation; the cost of the wrong data structure. **`[2026-11-12]` The boundary is explicit and chapter 51 repeats it** — the roadmap puts *performance* in the Advanced stage, so this chapter teaches you to locate a bottleneck and stops there |
| 48 | Thread · Failure | It worked for a month and then it didn't, and the logs said nothing. | Reading a traceback to the cause; logging that is useful at three in the morning; what fails when a dependency is slow rather than down; retries that make an outage worse; the failure that only appears under concurrency |
| 49 | Thread · Cost | Nobody told me a program could cost money by being badly written. | What a query costs, what a retry storm costs; the N+1 as a bill; bounded memory as a cost control; when to stop optimising. **`[2026-11-12]` Containers were cut from this row**: the roadmap marks Docker and deployment *"No — and deliberately not required by any capstone"*, and chapter 51 lists them as not taught, so pricing them here contradicted both |
| 50 | The Three Capstones | I've finished the book. I don't know whether I can actually do any of this. | **Set, not taught** (decision 16) — a capstone you read is not a capstone. The three, with the roadmap's two options each and its must-have list for each; what each one proves; how to get it reviewed by somebody who is not you; the real test: read an unfamiliar module from `Lib/` and explain every line |
| 51 | What This Book Does Not Teach | I need to know what I still don't know, by name. | **The closing table you approved** — four columns: *what this book does not teach* · *where you met it* · *what it actually is* · *where to read it*. **Three rows carry a book of the owner's own in the fourth column, and they are the point of this chapter**: **building a web service** — FastAPI, routing, request and response models, dependency injection and API auth — → ***APIs to FastAPI***, whose Part III is eight chapters on it; **the OWASP API Security Top 10** — → **the OWASP page itself**, `https://owasp.org/API-Security/`, and **not** to a book, because **no book of the owner's teaches it**: *APIs to FastAPI* names OWASP once, in passing, and the roadmap marks security hygiene as not covered. **`[2026-11-12]` This row exists because the owner asked for it.** An earlier version folded OWASP into the row above and sent the reader to a book that does not teach it, which is worse than naming it as a gap. **What it is, in one line:** the ten most common ways an API is broken, of which the first — reading another user's record by changing a number in the URL — causes more real breaches than the other nine. **Project `1.5 p7` is the audit**, one evening against a running API; **the shell, the editor and Git**, including the interactive rebase project `1.2 p9` asks for → ***Linux and Git from Zero***; and **the six roadmap projects this book does not set** — `1.2 p9`, `1.5 p4`–`p7` and phase 1.5's own project — each listed with the book that owns it. Then the rest: descriptors, metaclasses, variance, performance tuning and architecture (the Advanced stage); CPython internals and the C API (Mastery); Django and Flask; writing a pytest plugin; deployment, Docker and hosting; data science, scraping and the other domains. **The second column is the point: you met it, so the book did not hide it** |

---

## Appendices

| | Appendix | What it is |
|---|---|---|
| A | Cheat Sheet | Generated from every chapter's optional `### Worth Memorising` table. Numbers, defaults and formulas only |
| B | Interview Bank | About 100 questions with model answers, each keyed to the chapter that teaches it. An answer is what you should be able to say in about sixty seconds: the mechanism, the trade-off, and how you would check it. **Written last, from the finished chapters, never from memory** (decision 19) |
| C | Glossary | Generated from every chapter's `### Key Terms` table |
| D | Index | |

---

## What is settled, and what is not

**Settled by `../future-books/README.md`, and reflected above:** the scope (decision 10), the
double pass (15), the capstones as set work and 1.5 split (16), SQL taught properly (17), the
chapter shape (18), and that the interview bank and the four threads transfer (19). **The part
names are the exception and are NOT reflected above** — decision 19 carried them as a default and
the owner then ruled they do not survive here, which the section above records.

**`[STATED 2026-11-12]` Settled by the owner on this list, in one sitting:**

| Asked | He ruled |
|---|---|
| Do the four part names survive? | **No.** The new names stand. Decision 20 is discharged for *Python*, and still governs the second book |
| Should the book have a Git chapter? | **No.** It is dropped, and the book points at *Linux and Git from Zero* instead |
| What happens to the roadmap page on the website? | **Literally nothing.** It stays exactly as it is, and the book does not change it. This closes the open rule *"What happens to the roadmap page once Python exists"* |
| Should the four API chapters stay? | **No.** *"We have the API book already, just point it out there just like Linux and Git Book."* Chapters on building an API, dependency injection, API auth and the OWASP top ten are cut, and Part III stops at the Python a service needs |

**Still open, and not needed to approve this list:**

| Open | Where it bites |
|---|---|
| **Decision 13** — *core* is a dependency test | When chapter 51's table is filled, and when any topic above is moved out of a chapter into it |
| **Decision 21** — the five kinds of short entry | Same moment as 13; it is 13's output. **`[2026-11-12]` It already binds, and this is said rather than hidden:** chapter 51's list and Part II's *what to ignore* note are decision 21's sort, published while the rule behind it is unruled. If the owner redraws the rule, both lists are redrawn with it |

**What this list still does not do**, named here rather than left silent:

1. **No cross-book ledger entries are written yet.** Sequential writing makes this cheap — the
   machine-learning book is written against a finished Python book — but the terms this book owns
   should be recorded as it goes, not afterwards. **No ruling needed; it happens while writing.**
2. **The roadmap's own Git reading is now unowned.** Phase 1.2 lists *Pro Git* ch. 2, 3, 6 and
   §7.6. With the Git chapter dropped, this book covers none of it and *Linux and Git from Zero*
   covers most of it. **The remainder is §7.6, rewriting history**, which that book treats in
   brief — the same gap project `1.2 p9` leaves, recorded once at the top of this file and once
   here because it is the only hole in the stage.

**`[2026-11-12]` Two items that were on this list are now closed**, by the owner's rulings above:
the Git chapter is dropped, and the roadmap page is left exactly as it is.

---

## `[2026-11-12]` What the review found

**Two independent reviews read this list against its two sources** — one against the roadmap page,
one against `../future-books/README.md` and `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §5. Neither was
told what the answer was expected to be. **Every finding below was then checked against the files
by hand before it was acted on**, which is the rule at the top of `../../.claude/CLAUDE.md`.

**They found fourteen faults. The list had been approved before they ran.** That is the point of
recording this: an approved document is not a checked one.

| What was wrong | What was done |
|---|---|
| **Four chapters rewrote *APIs to FastAPI*** — decision 16's rejected column names that exact act, and Part III's note claimed the book did not do it | Cut, on the owner's ruling. Part III now stops at the Python a service needs |
| **The Python FAQs had no chapter.** The roadmap says *"Both in full"* | Added to chapter 10, where the roadmap puts them |
| **Format specifications had no chapter**, and project `1.1 p1` exercises them | Added to chapter 2, which now carries that project |
| **Cursor pagination had no chapter**, and project `1.5 p5` requires it | Goes with the cut chapters to *APIs to FastAPI*; named in chapter 51 |
| **Project `1.5 p3` was cited as a lab twice** | Chapter 44 now has a lab of its own |
| **Phase 1.4 ran in the wrong order.** The roadmap reads `concurrent.futures` before `multiprocessing`; the book had it reversed | Chapters 31 and 32 swapped. Project `1.4 p2` is `ProcessPoolExecutor`, so it moved with the executors |
| **Five labs sat ahead of the chapter teaching them** | `1.1 p7` and `1.1 p12` moved to chapter 10, which owns `re` and `datetime`. The rest resolved with the cuts |
| **Decision 8 was quoted as its own superseded predecessor**, dropping the condition that is still unmet | Both conditions now quoted. **Approving this list does not unblock drafting; the rules are still unwritten** |
| **`GOAL.md` §5.3 was cited as a rule.** It is `[I RECOMMEND]`, in a section headed *not yet decided*, about a different book | Recited as a parallel. The owner's own ruling carries the row |
| **Decision 20 was called closed.** It still governs the second book | Now *discharged for *Python*** |
| **"The part names transfer" was listed as settled and reflected above.** The owner had ruled the opposite | Corrected, with the exception named |
| **The header claimed every chapter has a lab.** Part IV has none | Scoped to Parts I–III |
| **Chapter 47 taught performance and chapter 49 priced containers**, while chapter 51 said the book taught neither | 47 scoped to finding a bottleneck, not tuning. Containers cut from 49 |
| **The C API was filed under the Advanced stage.** The roadmap puts it in Mastery | Corrected in both places |

**What the reviews did not find**, which is worth recording too: the chapter numbering, every
cross-reference, every relative path, every other decision citation, and the mapping of every
remaining project to its chapter were all sound.

**One finding was rejected rather than fixed.** A reviewer read the drafting of this list as
breaking the `[STATED]` deferral *"we can discuss the Table of Contents later, but not right
now."* **The owner lifted that himself** — *"After that we will start with the Python book"* —
and this file records the rulings he then made on it. The deferral paragraph in
`../future-books/README.md` should say so, and does not yet.

**`[2026-11-12]` One more fault, found by the owner after the reviews had run.** Chapter 51 sent
the reader to *APIs to FastAPI* for the OWASP API Security Top 10. **That book names OWASP once,
in passing** — checked in its text, not assumed — so the pointer went somewhere that does not
teach it. **A pointer to nowhere is worse than naming a gap**, because it looks closed. OWASP now
has its own row with the source itself as its fourth column, and project `1.5 p7` is named there
rather than counted among the five that went to *APIs to FastAPI*. **Neither review caught this.**
Both checked that the file was faithful to its sources; neither checked that a book being pointed
at actually covers what it is pointed at for.
