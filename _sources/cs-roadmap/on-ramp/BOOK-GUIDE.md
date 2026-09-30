# CS & Engineering On-Ramp: How to Build a Book

Everything needed to write any book in this series. A new session starts here:

1. Read this whole file.
2. Check `books/README.md` for what's done, in progress, and next.
3. Follow section 10, *Steps for a New Book*.

---

## 1. The Series

- **Towards Intelligence** is the user's own website. Its **CS & Engineering on-ramp** (`cse/on-ramp.html`) lists what an engineer needs to learn. These books **replace the courses** on that on-ramp.
- The on-ramp decides **what** to teach and how deep to go. Each book teaches exactly that, **from zero**.
- AI is out of scope. It belongs to the site's *Data & Intelligence* on-ramp.
- There are two kinds of books:
  - **The small books** teach **concepts**: *what is this thing, and how does it work?* Anything that is true for any project goes here.
  - **The big book**, *The Complete Software Engineering Guide*, teaches **process**: one project taken from an idea to production. Anything that only makes sense for one project goes there. Don't repeat it.
- `on-ramp.html` in this repository previews how the books appear on the website. The website itself lives in another repository (`/Users/lakshmideepak/LearningLab/towards-intelligence/robotbrainlab.github.io/`), which is **read-only**: never edit it.
- **Installed on this machine:** MacTeX (`latexmk`, `xelatex`), pandoc, Python 3, Git, Docker, `act`, Terraform, shellcheck, and poppler (`pdftotext`, `pdfinfo`).

---

## 2. The Books

**10 books.** Every book still to write has its table of contents in `books/<book-slug>/TOC.md`. Each book's status is tracked only in `books/README.md` (section 10). Each one opens with **the problem you hit**, which raises **the question it answers**. Use both word for word.

### Science Track

| On-ramp topic | Book | The problem you hit | The question it answers | Covers | Pages |
|---|---|---|---|---|---|
| Data Structures & Algorithms | **Data Structures and Algorithms from Zero** | My code gives the right answer, but it gets painfully slow as the data grows. | Why is one way of organising data a thousand times faster than another, and how do I choose? | Big-O, arrays and lists, hash tables, trees, heaps, graphs, sorting and searching, shortest paths, dynamic programming | 80–95 |
| Databases | **Databases from Zero** | My app forgets everything when it stops. A list in memory can't be shared between users, searched well, or trusted after a crash. | Where should my app keep information so that it survives restarts, many users can share it, and I can find exactly what I need? | Types of databases, the relational model, SQL, storage and indexes, transactions and concurrency, other stores (cache, document, search, vector), replication and backups | 95–99 |
| Distributed Systems | **Distributed Systems from Zero** | One machine can't handle the load, and any machine can die at any time. | What changes when my app runs on many machines at once? | Faults and failure models, time and clocks, replication, consistency, consensus and leaders | 65–80 |
| Operating Systems | **Operating Systems from Zero** | I start my program and it "just runs", but when it crashes, hangs, or runs out of memory, I don't know where to look. | What is the computer actually doing when my code runs? | The kernel and system calls, processes and threads, virtual memory, scheduling, file systems | 80–95 |
| Computer Networks | **Networking from Zero** | It works on `localhost`, but nobody else can reach it. | How does a request from someone's browser find my program and get an answer back? | The Internet's layers, IP and routing, TCP and UDP, sockets, DNS, HTTP, TLS, proxies and load balancers | 80–95 |

The on-ramp marks Discrete Mathematics, Programming Languages & Compilers, Theory of Computation, Parallel & Concurrent Computing, and Computer Organization & Architecture as *not necessary at this level*. They have no book.

### Engineering Track

| On-ramp topic | Book | The problem you hit | The question it answers | Covers | Pages |
|---|---|---|---|---|---|
| Software Engineering | **Linux and Git from Zero** | Every tutorial says "open the terminal", and I don't know what I'm typing. When my code breaks, I can't get the old version back. | How do I use the tools every developer uses every day, and never lose my work? | The shell, filesystem, permissions, processes and services, scripting, packages; Git: commits, branches, merging, remotes, undoing mistakes; open-source workflows | 85–95 |
| Software Engineering | **Web Applications from Zero** | I use apps every day, but I have no idea what happens after I tap a button. | What happens between tapping a button and seeing the result? | The front end and the back end, what runs in the browser and what runs on the server, how they talk, where the data lives, common stacks | 20–25 |
| Software Engineering | ***APIs to FastAPI*** (*written before this series*) | My program is useful, but other programs and people can't use it. | How does one program offer its abilities to another over the internet? | What an API is, HTTP and JSON, REST, authentication, building a real API with FastAPI | 145 |
| Software Engineering | ***The Complete Software Engineering Guide*** (*the big book, written before this series*) | I understand the pieces, but I've never taken a real application from an idea all the way to production. | How does software actually get built, from deciding what to build to a running production system? | Deciding what to build, planning, writing good code, and taking one application from a laptop to production | 1,070 |
| Infrastructure Engineering | **Infrastructure Engineering from Zero** | It works on my machine but breaks on the server, and I don't even own a server. | How does my code get from my laptop to machines that serve everyone, the same way every time? | DevOps: containers, CI/CD, infrastructure as code, deployment and rollback. Cloud: compute, storage, networking, IAM, managed services, serverless | 95–99 |

Programming is not a book: the on-ramp's programming entry links to the official [Python Tutorial](https://docs.python.org/3/tutorial/).

The on-ramp leaves Platform Engineering and the Operating topics (Reliability, Performance, Security, Observability) without an entry. They have no book.

### Suggested path and writing order

There is no required order; every book stands alone.

- **Suggested path**, for a reader who wants one: the Python Tutorial → Linux and Git → Data Structures and Algorithms → Operating Systems → Networking → Databases → Distributed Systems → Infrastructure Engineering → Web Applications → *APIs to FastAPI* → the big book.
- **Writing order:** Linux and Git, Web Applications, and Infrastructure Engineering first; then Data Structures and Algorithms → Operating Systems → Networking → Databases → Distributed Systems.

---

## 3. The Reader

- A **beginner**. Assume they know nothing about the topic. The only exception is Python basics (the level of the official Python Tutorial), which may be assumed.
- **Every book stands alone.** The reader may open this book first. When the book needs an idea from another topic, explain just enough of it to keep going. The full explanation stays in that topic's own book.
- All examples use **Python**. Shell commands are shown as the reader would type them.

---

## 4. One Problem, One Question

Every book is built around its problem and question from section 2.

> *My program is useful, but other programs and people can't use it.*
> How does one program offer its abilities to another over the internet?

- The book **opens** with that problem: the preface begins with the book's problem and question from section 2, **word for word**.
- Every **chapter** opens the same way: its own small problem (the TOC's "Opens with" line), then the question it raises. The TOC gives only the problem; the writer words the question.
- Problems and questions are **simple, vivid, and non-technical**, written the way a beginner would say them.

---

## 5. Scope

- **Cover what the book's Covers list says**, at on-ramp depth. Explain each concept clearly, not exhaustively.
- **Stay within the page target:** 50–100 pages, and never over 100. *Web Applications from Zero* is the one exception, at 20–25 pages.
- **Concepts, not a product journey.** Short labs are fine; a continuing project across chapters is not, because that is the big book's job.
- If something doesn't help answer the book's question, it belongs in another book.

---

## 6. Structure: O'Reilly Style, like *APIs to FastAPI*

Every book follows the O'Reilly style of *APIs to FastAPI*. Open `books/apis-to-fastapi/APIs to FastAPI.pdf` and match it.

### 6.1 Front matter

1. **Title page**
2. **Copyright page**, with the revision history, the tested versions, and a note that there is no warranty
3. **Contents**
4. **Preface**, with these sections:
   - Who This Book Is For
   - How This Book Is Organized
   - How to Use This Book
   - What You Need Installed
   - Conventions Used in This Book

### 6.2 Parts

| Part | Purpose | Share |
|---|---|---|
| **I · Understand** | The mental model. Opens with the book's problem. Little or no code. | ~30% |
| **II · Use** | Become a confident user of the tools for this topic. | ~30% |
| **III · Apply** | Short labs that make each concept visible. | ~25% |
| **IV · What Next** | The four threads (below), what to learn next, what to skip for now. | ~10% |
| **Appendices** | Cheat sheet and glossary, then an index. | ~5% |

Parts I–III each open with a short **"What to ignore for now"** note, as *APIs to FastAPI* does. Part IV has no note: its last chapter already says what to skip.

### 6.3 Every chapter

- A short opening paragraph that says what the chapter gives the reader.
- A small **problem**, then the **question** it raises. The one exception is *Where to Go from Here*, which needs neither. The four-threads chapter's TOC row has no problem, so the writer words one in the same style, for example: "It works now, but I don't know what could go badly wrong, slow it down, or cost me money."
- The idea explained **before** any command or code, with an everyday picture where it helps (like the restaurant picture in *APIs to FastAPI*).
- **Bold** for every new term the first time it's explained. Every bolded term also goes in the glossary.
- **Callouts:** *tip* (saves time or trouble), *note* (something to be aware of), and *warning* (can cost data, money, or security).
- A **lab**, with expected results so the reader can check their work.
- **Summary**, **Key Terms**, and **Review Questions**.
- A **"You understand this when…"** check.

The last four items apply to every chapter in Parts I–III. The Part IV chapters (the four threads, and *Where to Go from Here*) have none of them.

### 6.4 The four threads

Part IV answers the same four questions for the book's topic:

| Thread | The question |
|---|---|
| **Security** | What can go wrong here, and what limits the damage? |
| **Speed** | What makes this slow? |
| **Failure** | How does this break, and how do I diagnose it? |
| **Cost** | What does this cost me? |

---

## 7. Writing Style

- **Plain, simple, and vivid.** Short sentences. Explain things the way you would to a friend.
- **Idea first, then commands.** Never start a section with a code block.
- **Every command and code sample must work.** Run it before it goes in the book, and show real output.
- No filler, no hype, no history lessons unless they explain something.

---

## 8. Design and Build

### 8.1 Design (match *APIs to FastAPI*)

| Element | Style |
|---|---|
| Page size | 7 × 9.19 in (504 × 661.5 pt) |
| Body text | Crimson Pro |
| Headings | Source Sans 3 (semibold) |
| Code | Source Code Pro |
| Chapter opener | Small caps "CHAPTER N", then the title, right-aligned |
| Running heads | "Chapter N: Title \| page" on left pages, "Section title \| page" on right pages |
| Callouts | Tip, note, and warning, each with its own icon |
| Code blocks | No shell prompt, so commands can be pasted as they are |

### 8.2 Build pipeline

Every book is built with the shared O'Reilly-style template in `books/book-template/`: **Markdown → pandoc (with `tools/filter.lua`) → XeLaTeX → PDF**. The Markdown is the only source of truth; never edit the generated `.tex` files. `books/book-template/README.md` explains the template, and `books/book-template/sample/` shows every feature in use.

Set up the build before launching the writing agent; the editor (the main session) writes `book-meta.tex` and `book.tex`, not the agent. To set up a book's build:

```bash
cd books/<book-slug>
mkdir -p markdown latex labs
cp -R ../book-template/{Makefile,latexmkrc,preamble.tex,book.tex,book-meta.tex,tools,front,assets,.gitignore} latex/
```

Then:

1. Fill in `latex/book-meta.tex`: title, subtitles, tagline, revision date, tested versions, category, and back-cover blurb.
2. In `latex/book.tex`, declare the parts with `\bookpart{I}{Understand}{<the TOC's "What to ignore for now" text>}` (Part IV gets `{}`), list each chapter with `\input{chapters/<file-name-without-.md>}`, and the appendices after `\appendix`.
3. Build and check:

```bash
cd latex
make
PAGES_MIN=<low> PAGES_MAX=<high> make check
```

`make check` reports overfull boxes, text off any page (covers included), fonts, bold terms missing from the glossary, and the **numbered pages** compared with the book's target (section 8.4). Always pass the book's `PAGES_MIN` and `PAGES_MAX`; the defaults (50–100) would let an over-long book pass. The Makefile puts TeX on the PATH; to run `latexmk` or `xelatex` by hand, first `export PATH=/Library/TeX/texbin:$PATH`.

To change the design, change the template and copy the changed file into every book, so the series stays consistent.

Each book lives in its own folder:

```
books/<book-slug>/
  TOC.md           the approved table of contents
  markdown/        chapter files (the source of truth)
  latex/           a copy of books/book-template/: preamble, filter, convert.sh, Makefile, book.tex
  labs/            anything the labs need, tested
```

When a book is finished, copy `latex/book.pdf` to `books/<book-slug>/<Book Title>.pdf`. Every book, including the two finished ones, has its own folder in `books/`. The repository root holds only `BOOK-GUIDE.md`, `on-ramp.html`, and `books/`.

### 8.3 Markdown conventions

The build template relies on these.

- **One file per chapter:** `markdown/01-<chapter-slug>.md`, `02-…`, in TOC order. Also `00-preface.md`, one file per appendix (`A-…md`, `B-…md`), and the glossary (titled `# Glossary`) as the last appendix.
- **Parts** are declared in `latex/book.tex` with `\bookpart{I}{Understand}{<the TOC's "What to ignore for now" text>}`; Part IV gets an empty note. `books/book-template/README.md` has the full list of conventions, and `books/book-template/sample/` shows every feature.
- **Headings:** `# Chapter Title` (no "Chapter N"). The first paragraph is the intro. Then `##` sections and `###` subsections.
- **Only these files** go in `markdown/`: the preface, the chapters, and the appendices. Parts are declared in `latex/book.tex`, not in a Markdown file.
- **Opening problem and question**, right after the intro, as two short paragraphs:
  `*The problem.* <the TOC's "Opens with" line>` and `*The question.* <the question it raises>`.
- **Spelling:** British everywhere, as in *APIs to FastAPI* (colour, centre, organise), including the problems and questions. Proper names keep their own spelling ("Computer Organization & Architecture").
- **Callouts:** `> **Tip:** …`, `> **Note:** …`, `> **Warning:** …`.
- **Code blocks** always have a language tag: `bash` for commands (no `$` prompt), `text` for output, and `python`, `yaml`, `dockerfile`, `hcl`, or `html` as needed. Box-drawing diagrams go in `text` blocks, at most 64 characters wide, and every line of a box must be the same width so its right edge lines up.
- **Chapter ending** (every chapter except the last two):
  - `## Lab: <title>`: numbered steps, each with its expected result. In Part III the whole chapter is the lab: its title starts with "Lab:", its sections are `## Step 1: …`, `## Step 2: …`, and it has no separate `## Lab:` heading.
  - `## Summary, Key Terms, and Review Questions`, with `### Summary`, `### Key Terms` (a table: Term | Meaning), and `### Review Questions` (numbered, 4–6).
  - `> **You understand this when** …` (one sentence).
- **Glossary:** a table (Term | Meaning) in alphabetical order, holding every bolded term. Keep every definition to one line.
- **Bold only key concepts**, about 60–75 in a 90-page book. Command names (`chmod`, `jq`, `git revert`) go in code font, not bold, and not in the glossary. A tool that is itself a concept the book teaches (cron, Docker, Terraform) may be bolded and defined.
- **Labs are isolated and safe.** Each lab starts in its own fresh folder (such as `~/sandbox/ch3`), so it never depends on files an earlier example happened to create, and never touches the reader's real folders or settings. No lab step may risk data outside its folder.
- **Expected results must hold for every reader:** avoid quoting error text that differs between bash and zsh, or Linux and macOS; say "a Permission denied error" instead.
- **An output block holds only the output of the command shown**, not shell messages such as `[1]+ Done`.
- **Output that changes between runs** (timings, memory addresses, commit IDs, dates): show one real run, say that the reader's numbers will differ, and word expected results in relative terms ("about 100 times faster", "a new ID").
- **Labs are reproducible from the PDF alone**, because readers get only the PDF. Show every file a lab needs in full, or give a short command or script that creates it. Anything under `labs/` is also offered as a download (section 12, *Lab files*).
- **Standard library first.** Prefer Python's standard library. If a lab needs a third-party package, install it in a virtual environment, pin its version, and list it under "What You Need Installed".
- **Maths:** `$…$` is not maths in this build. Write O(n), O(n²), O(n log n), log₂ n, ≤, ≥, ×, and ≈ as plain text; they print in both fonts. The superscript ⁿ is missing from the body font, so write exponential growth in code font: `O(2^n)`.

### 8.4 Length

*APIs to FastAPI* runs about **240 words per printed page**, counting code and tables. A chapter's word budget is its pages × 240; for example, a 7-page chapter is about 1,700 words. Stay close to it: cut padding rather than adding filler.

The page count is the **numbered pages**, from Part I's opener to the end of the glossary. Part-opener pages count (one each); the front matter and the index don't. So a TOC fits its target only if its chapter pages, plus one page per part, plus the appendices, stay within it. Pages that a chapter spills only a few lines onto are the cheapest to win back. Code blocks and tables never split across pages, so cutting text earlier in a chapter often just leaves white space; to win a page, cut near the chapter's end, or stop table cells from wrapping onto a second line.

### 8.5 Before calling a book done

- `PAGES_MIN=<low> PAGES_MAX=<high> make check` passes: no text running into the margins (no overfull boxes), no text off any page (covers included), every bolded term in the glossary, and the numbered pages within the target.
- **Every page has been looked at, front cover to back cover**, not only the pages the checks cover. Render the whole PDF as contact sheets (`pdftoppm -r 40`, 20 pages to an image) and zoom in on anything odd: covers, title page, diagrams, tables, the index. `make check` can't see a badly broken title or a ragged diagram. If a title is too long for one line on the cover, set `\BookTitleLines` in `book-meta.tex` to choose where it breaks.
- Every command and code sample has been run.
- Every chapter has its lab, summary, key terms, review questions, and "You understand this when…" check.
- Every chapter has been edited by hand (section 9.2).

---

## 9. Writing with Agents

Every book is made the same way:

```text
TOC ready  ->  a writing agent drafts  ->  Claude edits every chapter  ->  build and check
```

- **The writing agent drafts.** Launch one agent per book, in the background, so several books can be drafted at once.
- **Claude edits.** The main session is the editor. It edits every chapter by hand and checks all the content itself. A draft is never the final book.
- **The agent knows only what it is given.** It hasn't seen any conversation with the user: whatever isn't in this guide, the TOC, or its brief won't reach it. When editing finds something an agent got wrong because this guide didn't say it, **add it to this guide**, so the next agent gets it right.

### 9.1 The brief to give a writing agent

Copy this and fill in the parts in angle brackets.

```text
Write the complete Markdown manuscript of "<Book Title>".

Read first:
- BOOK-GUIDE.md, all of it. Follow it exactly.
- books/<book-slug>/TOC.md. Follow its parts, chapter order, titles,
  opening problems, covers, and page budgets. Don't add or drop chapters.
- books/apis-to-fastapi/APIs to FastAPI.pdf (use pdftotext -layout)
  to absorb its voice.
- <raw material, if the TOC or section 12 names any>

Rules:
- Write only inside books/<book-slug>/ (markdown/ and labs/).
- Run every command and code sample in a scratch directory before it
  goes in the book, and paste real output.
- No accounts, logins, pushes, global config changes, or paid services.
  Clean up any containers or resources you create.
- Never touch the user's real files: run labs with HOME (and
  GIT_CONFIG_GLOBAL) pointed at the scratch directory, and never read
  or write ~/.ssh, ~/.gitconfig, the crontab, or other dotfiles.
- Follow section 8.3 (Markdown conventions) and 8.4 (length).
- Create only the preface, chapter, and appendix files (A-…md, B-…md,
  with the glossary last). Don't create parts.md or any other file;
  parts are declared in latex/book.tex by the editor.
- Use a scratch directory outside the repository, such as
  /private/tmp/claude-501/<book-slug>/.

Report when finished:
- Files with word counts, the total, and any chapter more than 15%
  off its budget.
- What couldn't be run, and how the book presents it.
- Anything in the TOC that seems wrong (report it; don't change it).
```

### 9.2 Editing every chapter

Read each chapter **in full** and check it by hand:

- It opens with the TOC's problem and question, and a beginner could follow it from start to finish.
- Ideas come before commands, and everyday pictures are used where they help.
- The voice matches *APIs to FastAPI*: plain, simple, vivid, and short sentences, with no filler or hype.
- Every fact is correct. Re-run any command whose output looks doubtful.
- It stays within the Covers list. Anything owned by another book gets only a brief explanation.
- It has its lab, summary, key terms, review questions, and "You understand this when…" check, and every bolded term is in the glossary.
- Its length is near the budget.
- Its lab is isolated and safe (section 8.3). Re-run each lab end to end in a scratch folder, with `HOME` pointed there, and check that every expected result is what really happens.
- Command names that begin a sentence are in code font, and box diagrams have straight right edges.

If a chapter isn't good enough, rewrite it rather than patching it. Then build the PDF (section 8), look at every page as section 8.5 says, compare chapter openers, code pages, and tables with the same kinds of page in *APIs to FastAPI*, and fix any gaps you found in this guide. Report to the user only what was actually checked.

---

## 10. Steps for a New Book

**Finish before starting.** If `books/README.md` shows a book in progress, finish it before starting the next one in the writing order (section 2).

**Status values** in `books/README.md`: *TOC ready* → *Drafting* → *Editing* → *Done*. Update the book's row at each step.

1. **Read** this file, the book's `books/<book-slug>/TOC.md`, and a few chapters of *APIs to FastAPI*.
2. **Review the TOC yourself**, thoroughly: coverage, order, scope, template fit, the page budget (section 8.4), and whether every lab can run on this machine and be reproduced from the PDF alone. The user is learning these topics, so checking correctness is Claude's job, not theirs.
   - You may fix the TOC's structure: move, merge, split, or retitle chapters, and change page budgets. Record the changes in the TOC.
   - The book's name, problem, and question (section 2) are the user's; ask before changing them.
3. **Set up the build** (section 8.2), including `book-meta.tex` and `book.tex`.
4. **Launch a writing agent** with the brief in section 9.1. Status: *Drafting*.
5. **Edit every chapter** as in section 9.2. Status: *Editing*.
6. **Build** the PDF, check it against section 8.5, and copy it to `books/<book-slug>/<Book Title>.pdf`. Status: *Done*.
7. **Link the book on `on-ramp.html`** (its name to its PDF) only when the user asks.

**Resuming a book in a new session.** A book marked *Drafting* has no live agent any more. If every file in its TOC exists in `markdown/`, the draft is complete: move to step 5. If some are missing, launch a writing agent with the section 9.1 brief, adding: "Some chapters already exist; keep them and write only the missing ones."

---

## 11. Working with the User

- **The user is learning.** Verify plans, TOCs, and content yourself; ask the user only about preferences and permissions, such as installing a tool.
- **Stay in this repository.** Other repositories, including the website repo, are read-only unless the user explicitly says otherwise.
- **Keep the repository tidy.** The root holds only `BOOK-GUIDE.md`, `on-ramp.html`, and `books/`, and every book has its own folder.
- **Don't add what wasn't asked for:** no extra labels, badges, page counts, or links.
- **Don't take labels literally.** Understand what a name or heading means before turning it into a book or a chapter.
- **Keep the user's wording.** Problems, questions, and names in section 2 are the user's decisions.

---

## 12. Book-Specific Notes

### Linux and Git from Zero (done)

- Built from the raw material in `books/linux-and-git/linux_unix_guide.md`, rebuilt into the template, with its OpenClaw callouts removed and its sections on containers, servers, production operations, and hardening left to other books. Git was written from zero.

### Web Applications from Zero (done)

- The one short book: two parts only (I · Understand and II · What Next), 20–25 pages, a glossary but no cheat sheet, and no `labs/` folder. Its chapters end with a short *Try It* in the reader's own browser instead of a lab.

### Infrastructure Engineering from Zero (done)

- Every lab runs on the reader's own machine, with no cloud account or bill: Docker, a local registry, GitHub Actions run with `act`, MinIO for object storage, and Terraform with its Docker provider. Steps that need a real cloud account are described in words, not as commands.
- Lab details that must stay consistent: the local registry is `registry:2` on `localhost:5001` (macOS's AirPlay Receiver holds port 5000); MinIO uses `cgr.dev/chainguard/minio` and `minio-client`; Terraform uses the `kreuzwerker/docker` provider `~> 4.6`; the example app is tinyapp (FastAPI), whose files are in `labs/tinyapp/`. `httpx2==2.13.1` in `requirements-dev.txt` is genuine: Starlette's test client imports it.
- Its cover title is too long for one line, so `book-meta.tex` sets `\BookTitleLines`.

### APIs to FastAPI and The Complete Software Engineering Guide

- Both were written before this series. Only their PDFs matter here: *APIs to FastAPI* has no source in this repository, and the big book's `LaTeX-Book/` needs a separate Markdown library that isn't in this repository, so it can't be rebuilt from here.
- *APIs to FastAPI* is the design the series template copies. The big book has its own design inside (other fonts, a larger page). The user decided to leave both as they are inside: don't restyle them.
- **Covers (2026-09-30):** both now have the series front cover (teal bands, concentric rings), so all books look like one series. The octopus on *APIs to FastAPI* and the big book's navy cover were replaced; the words are the ones already on each cover (the big book dropped "· 2026" and its four-step strip, and has no subtitle line). Each cover is built in `books/<slug>/cover/` from the template's `front/cover.tex`; `make` there swaps it in as page 1 of the PDF with `book-template/tools/swap-cover.py` (every other page stays byte for byte) and copies the PDF to `cse/books/`. The big book's `LaTeX-Book/front/cover.tex` places the same `cover.pdf`, so a rebuild keeps it.

### Lab files (downloads)

- Books with lab files offer them as a download next to the PDF on the website: `books/<book-slug>/<Book Title> Lab Files.zip`, made from the tested `labs/` folder (`zip -r -X "<Book Title> Lab Files.zip" labs -x "*.DS_Store"`), which unpacks to `labs/`. The preface names the zip and says to get it from the book's entry on the on-ramp (robotbrainlab.github.io/cse/on-ramp.html). Rebuild the zip whenever `labs/` changes. Still show short files in full in the text, so most labs work from the PDF alone.

### Programming

- There is no *Programming from Zero* book. The on-ramp's programming entry links to the official Python Tutorial. Don't add anything for it unless the user asks.
