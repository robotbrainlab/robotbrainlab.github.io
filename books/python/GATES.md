# Python from Zero — the gates, and what says a chapter is finished

**`[STATED 2026-11-13]` This file discharges the last live rule that stood between this book
and chapter 1.** `../future-books/README.md` listed it as *"Which of the finished book's gates
transfer unchanged, which need changing, and which do not apply."* The owner read the proposal
and ruled: *"you can go ahead with your recommendations."*

**Decision 8 has two conditions.** *"Nothing is drafted until the rules are written and the table
of contents is approved."* The contents were approved on 2026-11-12. **The rules are this file.**
Both conditions are now met.

---

## 1. How the book is checked, in one picture

Three things check a chapter, and they check different things.

| What | Reads | Answers |
|---|---|---|
| **The two review agents** | The chapter and its sources, by a human-written brief | *Is this true? Does it teach? Is it in the right place?* |
| **The gates** | The Markdown and the built PDF, by program | *Is this the right shape? Does it build? Does the code run?* |
| **The hand checks** | The printed pages | *Have I looked at every page of this?* |

**The rule that divides them, and it is not mine:** *automation may check form; it may never
judge content* (`../modern-ai/docs/briefs/README.md`). A gate that judges content is a gate that
cries wolf, and a gate nobody trusts is worse than no gate.

---

## 2. The gates, and what was decided about each

Nineteen pieces of machinery were read in full on 2026-11-13, and the finished book's suite was
run. The ruling, tool by tool.

### 2.1 Transferred with no change

| Tool | Why it needed nothing |
|---|---|
| `chapter.py` | The staged driver. Subject-free |
| `glossary.py` | Decision 18 copies the chapter shape exactly, so the `### Key Terms` tables exist to read |
| `patch.py` | Exact-match editing. Subject-free, and §8 makes it the only way to edit |
| `build-probe.sh` | *A count from a build that died means nothing.* Subject-free |

### 2.2 Transferred with a change

| Tool | What changed |
|---|---|
| `verify-boundary.py` | **A new word list and a new exemptions file.** This book's boundary is the Advanced and Mastery material — descriptors, metaclasses, variance, performance tuning, the C API — plus the two subjects it must not teach at all: the shell and Git, and building a web service |
| `verify-inputs.py` | **A new jargon list for Python**, and a rule for the double pass (§4) |
| `verify-render.py` | Its width limit read ` ```text ` blocks only. It now holds code blocks to 79 characters and exempts diagrams. §2.4 has the limits |
| `verify-voice.py` | The word list was reviewed once. It still forbids *roadmap*, *website* and the build documents, which matters more here than in the finished book, because this book is planned from the roadmap page. It does not block a book title, so the two books this one points at are safe |
| `verify-coverage.py` | It required five columns in a contents row. Part IV has four, so chapters 46 to 51 were refused |
| `cheatsheet.py` | New part numbers: 1–17, 18–28, 29–45, 46–51 |
| `citations.py` | Chapter range 1–57 becomes 1–51 |
| `verify-index.py`, `check-all.sh` | Paths point at the shared build, not at a `latex/` folder inside the book |
| `verify-record.py` | It now **enforces** the `absolutes:` coupling: it imports `verify-absolutes.count()` and fails when the record's number and the gate's count disagree. The finished book only described that check |
| `verify-absolutes.py` | It exposes `hits()` and `count()`, so the rule for what an absolute is lives in one place and `verify-record.py` can use it |
| `verify-outline.py` | **Replaced by `verify-contents.py`, and the reason is in §2.5.** It could not run here at all |
| `check.sh` | Every check kept. **The page-count window is dropped.** Decision 14 says the finished size is permission and may never be cited for including or excluding anything, and a smallest and largest page count is exactly that citation |

### 2.3 Not transferred

| Tool | Why not |
|---|---|
| `verify-arithmetic.py` | It evaluates printed sums. The finished book is full of them; this one is not. Its real equivalent is `verify-code.py` (§3.1) |
| `verify-bank.py` | It checks a record names the interview questions the bank assigns it, which needs the bank written **first**. `TOC.md` writes Appendix B **last**, from the finished chapters. Nothing for it to check while chapters are written. **Revisit when Appendix B is written**, and run it once then |
| `pages.py` | It reads each chapter's page estimate from the contents. This contents file has no page column, deliberately (decision 14) |

---

### 2.4 The width limits

| Block | Limit | Why |
|---|---|---|
| ` ```python `, ` ```bash ` and other code | **79** | PEP 8's own limit, which chapter 11 teaches. The build wraps a longer line, and a wrapped Python line loses its indentation — which in Python is the syntax |
| ` ```text `, ` ```output `, unlabelled | **64** | The page width |
| Anything holding box-drawing characters | **exempt** | The build sizes a diagram to fit |

### 2.5 There is no PDF-outline gate, and `verify-contents.py` is why

`book.out`, which the finished book's `verify-outline.py` reads, is written by hyperref
alone. The shared preamble also loads the `bookmark` package, which writes the outline
straight into the PDF and produces no `book.out`. Reading it back out of the PDF needs a
PDF library, and this machine has none.

**`verify-contents.py` checks the same tree from `book.toc`**: the Preface first, the
Index last, no chapter before a part, chapter numbers with no gap, no section before its
chapter, and the four part names in order.

**The front-matter bookmarks — Cover, Title Page, Copyright, Contents, Back Cover — reach
no gate.** They are on the hand-check list in §6.

## 3. The two gates that are new

### 3.1 `verify-code.py` — every code block runs, and prints what the book says

**The single largest risk in a Python book, and no ported gate touches it.** Code typed from
memory does not run. Output typed from memory is wrong in the last digit, and the last digit is
where a reader looks.

```python
>>> 0.1 + 0.2
0.30000000000000004     # chapter 2 prints this. A machine proves it.
```

Today this is a promise in prose — *"every command and code sample has been run"* — and a promise
is what gets skipped. §6 lists the other seven promises like it.

### 3.2 `[STATED 2026-11-13]` A gate must prove it read something

The owner approved this rule on 2026-11-13, after the evidence below.

- Every gate prints how many files it read.
- **A gate that read zero files fails.** It never prints a pass.

**Why it exists.** A gate that reads nothing reports a pass. In the finished book one gate
read zero files and printed *"0 bad index entries"* over 461 unchecked entries.

---

## 4. The double pass, and the one rule it needs

Decision 15 teaches the language twice. Part I gets the reader writing Python. Part II returns
and explains it. **This is the mechanism, not redundancy.**

`verify-inputs.py` fails a chapter that uses a term no earlier chapter gave the reader. Without a
rule, it would fail Part I for using words Part II owns, and report your own method as a defect.

**The rule:** a Part I chapter may use a term that Part II owns, if it gives the reader a plain
working sentence for it where it is first used. Part II then owns the full explanation and the
`### Key Terms` row. A term used in Part I with no working sentence is a defect, and the gate
catches it.

This is what the `ALLOW` list in `tools/verify-inputs.py` is for. **Every entry names the chapter
that owns the term**, so an early use can be read as a loan rather than a mistake.

---

## 5. The two review agents

A review agent is not a program. It is an agent plus a **brief**, and the brief is the only part
that is a file. Both briefs are in `docs/briefs/`.

| Brief | When | Reads |
|---|---|---|
| `docs/briefs/completeness-review.md` | Step 3 of the chapter loop | The chapter and its sources, side by side |
| `docs/briefs/fix-verification.md` | Step 5 | **Only the passages that changed**, listed by name |

The five-step loop, the sweep rule and the stopping rule are stated in
`../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §14 and are **not restated here**. A rule
may be cited from several files; it may be stated in only one.

## 6. The checks that are still done by hand

These have no program, and that is a choice, not an oversight — each needs judgement.

- The gate suite says `ALL GATES PASS`.
- Every page has been looked at, cover to cover.
- **The PDF outline is right**: open the PDF, open the outline pane, and check the front
  matter is there — Cover, Title Page, Copyright, Contents, Back Cover. **No gate can see
  these** (§2.5). Once per part is enough.
- Every question in Appendix B for this chapter can be answered from the chapter alone.
- Every chapter has its lab, summary, key terms, review questions and the
  *"You understand this when…"* line.
- Every chapter has been edited by hand.
- Nothing refers to a website, a roadmap, numbered steps or tracks.

**One promise left this list and became a program**: *every command and code sample has been run*
is now `verify-code.py`.

---

## 7. `[STATED 2026-11-13]` How the book gets written, and who is asked what

The owner ruled on this after reading a comparison of three ways to run the writing. **He
chose chapter by chapter.**

**The rule, in one line: one chapter at a time, finished completely, before the next one
starts.** Research, writing, both reviews, the fixes and the gates all happen inside one
chapter. Nothing is carried to a later chapter to be finished.

**He is NOT asked to approve each chapter.** The reviews, the gates and the record do that
work. `[STATED 2026-11-13]` *"I do not want to approve every chapter individually.
Internal reviews, validations, and revisions should happen automatically wherever
possible."*

**Writing starts at chapter 1.**

**Do not write two chapters in one stretch.** Writing several together is what produces
invented content: the first chapter's sources leave working context before it is finished.

**What a review of one chapter cannot see**, so that it is not a surprise later: a fault
that lives between two chapters, and a claim one notch wider than its support. Neither
chapter is wrong on its own.

---

## 8. `[STATED 2026-11-14]` How a file is edited

**Every edit goes through `tools/patch.py`.** It takes the exact text to remove and the
exact text to put there. It never takes a position.

**Never cut by offset.** If you cannot quote the text you are removing, you have not read
it, and you cannot judge what the removal leaves behind.

**After any edit that removes something, read the file — the whole file, not a grep of
it.** Then name it in the chapter record's `files-read-back:` field.

**This is enforced, not trusted.** `patch.py` appends every applied edit to
`records/EDITS.log`. `verify-record.py` fails a chapter when a file that was edited while
it was open is missing from `files-read-back:`.

**Why it exists.** On 2026-11-13 passages were removed from eight files by computing two
offsets and splicing the text between them, without reading those passages. The only check
afterwards was a grep for the words that had been removed, plus a line count and a syntax
check — all three check form, and none of them reads. Three false statements survived it in
`GATES.md` alone: two tools listed as unchanged had both been changed, and one tool was
listed as unchanged and changed at the same time. **A grep found none of them. Reading the
file found all three in one pass.**

---

## 9. One thing to ask him about, when you reach it

**Chapter 51's closing table.** Which topics go in it is decision 13 and decision 21 in
`../future-books/README.md`, and he has not ruled on either. **Put them to him when you
fill that table in, not before.**
