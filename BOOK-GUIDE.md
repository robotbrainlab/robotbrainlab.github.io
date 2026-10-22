# How This Book Is Built

Everything needed to write *Modern AI Engineering from Zero*. A new session starts here, then
reads `TOC.md`.

This repository is **self-contained on purpose**. A writing agent working here has seen no
conversation and has no access to any other repository: whatever is not in this file, in `TOC.md`,
or in the agent's brief will not reach the book.

---

## 1. What this book is

One book, written from zero, for a reader preparing for **AI/LLM application engineer**
interviews inside a two-month window. It is deliberately not a thorough theoretical treatment:
it teaches what a capable AI engineer is expected to understand, use, evaluate and build today,
to the depth an interview reaches, and it says plainly where the deeper theory begins.

- **It is one book, not a series.** The nine subject areas it covers are one system, and the
  material where they meet — retrieval quality as an evaluation problem, agent safety as a
  tool-design problem, cost as a context problem — is the point. Nothing is taught twice.
- **It has nothing to do with any website.** The syllabus came from the author's own research
  notes, but no chapter may refer to a website, a roadmap, a learning path, numbered steps,
  tracks, or "the guide". The book stands alone and is the reader's only source.
- **Where a concept leans on something the reader has not studied, the book teaches it inline.**
  Two cases are load-bearing: comparing two prompts needs sampling variance and a confidence
  interval (chapter 19 teaches them from zero), and judging retrieval needs ranking metrics
  (chapter 25 teaches recall@k, MRR and nDCG from zero). Do not send the reader elsewhere.

## 2. The reader

- Knows **Python** at the level of the official Python Tutorial. Assume nothing else.
- Knows **nothing** about models, embeddings, retrieval, agents, evaluation or serving.
- Reads quickly and does not want padding. Density is a feature; filler is not.
- Is preparing for interviews, so every chapter should leave them able to *explain* the idea
  aloud, not only recognise it.

## 3. One problem, one question

The book opens with its problem and the question it raises, word for word:

> *The problem.* I keep meeting the same words — model, prompt, context, retrieval, tool, agent,
> evaluation — and I cannot say what any of them actually refer to, let alone build or judge one.
>
> *The question.* What should a capable AI engineer understand, use, evaluate and be able to
> build today?

Every chapter opens the same way: its own small problem (the `TOC.md` "Opens with" line), then
the question it raises. Problems and questions are simple, vivid and non-technical, written the
way a beginner would say them.

## 4. Scope

- Cover exactly what `TOC.md` says, at interview depth. Explain each concept clearly, not
  exhaustively.
- **Every concept is owned by one chapter.** `TOC.md` has a *Who owns what* table for the ten
  concepts more than one chapter touches. The owner teaches it. Every other chapter refers to it
  by chapter number and does not re-teach it. This is the rule that stops chapter 39 repeating
  chapter 14 and chapter 52 repeating chapter 15, and both overflowing their budgets.
- **Separate three things everywhere**, because the reader must know which is which in an
  interview:
  - the **lasting principle** — why this is done at all;
  - the **current convention** — how practitioners do it today;
  - the **details likely to change** — settings, versions, product names, prices.
  Mark the third kind plainly in the text (a `Note:` callout is the usual way) so the reader
  does not memorise a number that will be wrong by spring.
- No vendor comparisons, no product tours, no benchmark league tables. Organise by capability.

## 5. Structure

Four parts and the appendices. Parts I–III each open with a short **"What to ignore for now"**
note; Part IV has none, because its last chapter says what to skip.

| Part | Purpose | Share |
|---|---|---|
| *Before Part II · Inside the Model* | What the model computes when it answers. Notation, worked by hand. Set with `\prebookpart`, so it carries no part number and the four numbered parts stay four. It comes **after** Part I: the reader must know what a model is for before the mechanism means anything, and four of its chapters open with problems only Part I makes sensible. | ~16% |
| **I · Understand** | The system around the model. Opens with the book's problem. Little or no code. The book starts here. | ~9% |
| **II · Use** | Become a confident user of every piece of the system. | ~35% |
| **III · Apply** | Labs that build one small system, lab by lab, on data the book ships. | ~18% |
| **IV · What Next** | The four threads, one whole system designed aloud, then what to learn next and what to skip. | ~13% |
| **Appendices** | Cheat sheet, interview bank, glossary, index. | ~5% |

These shares differ from a short from-zero book on purpose: Part II carries most of the material,
and Part IV is substantial because the four threads are where serving, cost and security live.
Chapters are numbered straight through, 1--57: Part I takes 1--7, the interlude 8--17, Part II
18--39, Part III 40--50 and Part IV 51--57. Parts I--III each open with a "What to ignore for now"
note, and so does the interlude.

### Every chapter (Parts I–III)

- A short opening paragraph saying what the chapter gives the reader.
- `*The problem.*` and `*The question.*`, two short paragraphs, from `TOC.md`.
- The idea explained **before** any command or code, with an everyday picture where it helps.
- **Bold** every new term the first time it is explained. Every bolded term goes in the glossary.
- Callouts: *tip* (saves time or trouble), *note* (something to be aware of, including anything
  that will date), *warning* (can cost data, money or security).
- A **lab** with expected results, so the reader can check their work. In Part III the whole
  chapter is the lab: the title starts with "Lab:", its sections are `## Step 1: …`, and there is
  no separate `## Lab:` heading.
- `## Summary, Key Terms, and Review Questions`, with `### Summary`, `### Key Terms` (a table:
  Term | Meaning) and `### Review Questions` (numbered, 4–6).
- `> **You understand this when** …`, one sentence.

Part IV chapters have none of the last four items.

### The four threads

Part IV answers the same four questions for the whole system:

| Thread | The question |
|---|---|
| **Security** | What can go wrong here, and what limits the damage? |
| **Speed** | What makes this slow? |
| **Failure** | How does this break, and how do I diagnose it? |
| **Cost** | What does this cost me? |

### The interview appendix

Appendix B holds about 100 questions with model answers, each keyed to the chapter that teaches
it. An answer is what the reader should be able to say in about sixty seconds: the mechanism, the
trade-off, and how they would check it. This appendix is the reason the book exists; write it last,
from the finished chapters, and never from memory.

## 6. Mathematics, and the line it stops at

The reader asked for mathematics and not for machine-learning theory. That line is exact, and it
is the difference between **what the model computes when it answers** and **how it came to hold
those numbers**. Teach the first with notation. State the second and move on.

**Use notation freely for:** vectors and dimensions; matrices and matrix multiplication; the dot
product and cosine similarity; softmax, with temperature; the attention formula, worked
numerically; big-O for how cost grows; low-rank factorisation `W + BA` with real parameter
counts; key--value cache size; bits per parameter for quantisation; active versus total
parameters; cross-entropy and perplexity as definitions; logarithms and exponentials;
probability, sampling distributions and confidence intervals; ranking metrics.

**Never teach:** backpropagation derived; why gradient descent converges; optimiser design;
initialisation; numerical stability; regularisation theory; bias--variance; learning theory;
inductive biases; why depth helps in theory; convolutional or recurrent architectures; classical
machine learning; the derivation of scaling laws; representation-learning theory.

**The boundary cases, each decided. Do not widen the boundary beyond these four.**

1. **Chapter 14 states the training objective as a formula** and shows the parameter-update rule
   **once**, with a sentence of notation and no derivation, then names it as the edge of the book.
   It also states the **preference objective once as a formula**, named, not derived: a pairwise
   preference objective is an objective, not optimiser design, and interviewers ask what DPO is.
2. **Chapter 12 may give one sentence on why normalisation is there** — it stops activations
   growing through a deep stack. That is numerical stability, which this section otherwise
   forbids. One sentence, no more. "What more layers let the model do" is fair; *why depth helps*
   is not, and goes on chapter 17's list.
3. **Chapter 9 must not explain why the embedding geometry carries meaning.** That is
   representation learning. It says exactly this: the coordinates are whatever made next-token
   prediction work, nobody chose them, and no dimension means anything. The question goes on
   chapter 17's list.
4. **Chapter 16 explains intermediate reasoning with the mechanism, not with training.** The
   model's only scratchpad is its own output, so emitting intermediate tokens lets later tokens
   condition on partial work. This follows from chapter 9. Do not reach for reinforcement
   learning or serial-computation-depth arguments; both are outside the boundary.

Two more things are **inside** the boundary and must not be skipped as if they were theory. The
byte-pair merge procedure in chapter 10 is greedy corpus compression, and without it chapter 10
asserts rather than explains. The reason zero temperature is not deterministic (chapter 13) is
batching, floating-point order on a GPU, expert routing and provider-side change -- hardware and
numerics, not machine learning. Give the mechanism, not a shrug.

Chapter 17 lists everything black-boxed, so the reader knows exactly what they cannot yet explain
and what to say when an interviewer pushes.

**Every mechanism chapter carries a worked numeric example** small enough to check by hand or in
ten lines of Python with no framework: a 5-token vocabulary, 4-dimensional vectors, arithmetic
only. This is what stops an explanation from becoming a metaphor that dies on the first
follow-up question. A chapter that explains a mechanism without one is not finished.

## 7. Writing style

- Plain, simple and vivid. Short sentences. Explain things as you would to a friend.
- Idea first, then commands. Never start a section with a code block.
- Every command and code sample must work. Run it before it goes in the book, and show real
  output.
- No filler, no hype, no history lessons unless they explain something.
- British spelling everywhere (colour, centre, organise), including the problems and questions.
  Proper names keep their own spelling.

## 8. Markdown conventions

The build relies on these.

- **One file per chapter:** `markdown/01-<chapter-slug>.md`, `02-…`, in `TOC.md` order. Also
  `00-preface.md`, one file per appendix (`A-…md`, `B-…md`, `C-…md`), and the glossary (titled
  `# Glossary`) as the last appendix.
- **Parts are declared in `latex/book.tex`**, not in Markdown. Only the preface, the chapters and
  the appendices go in `markdown/`.
- **Headings:** `# Chapter Title` (no "Chapter N"). The first paragraph is the intro. Then `##`
  sections and `###` subsections.
- **Opening problem and question**, right after the intro, as two short paragraphs:
  `*The problem.* <the TOC's "Opens with" line>` and `*The question.* <the question it raises>`.
- **Callouts:** `> **Tip:** …`, `> **Note:** …`, `> **Warning:** …`.
- **Code blocks** always carry a language tag: `python`, `bash` (no `$` prompt), `text` for
  output, `json`, `yaml` as needed. Box-drawing diagrams go in `text` blocks, at most 64
  characters wide, every line the same width so the right edge lines up.
- **Glossary:** a table (Term | Meaning) in alphabetical order, holding every bolded term, each
  definition one line.
- **Bold only key concepts.** Library and command names (`httpx`, `uv`, `pytest`) go in code font,
  not bold, and not in the glossary. A tool that is itself a concept the book teaches may be
  bolded and defined.
- **Maths** is written as raw LaTeX, never as `$…$`. `tools/convert.sh` deliberately disables
  dollar maths so that a price like $5 stays text, and this book is full of prices.
  - Inline: `` `\(O(n^2 d)\)`{=latex} `` — the delimiters go *inside* the span.
  - Display: a fenced block opened with ```` ```{=latex} ```` holding `\[ … \]`.
  - Equations set in Garamond-Math (see `latex/preamble.tex`). `amsmath` is available;
    `unicode-math` supplies the symbols, so never load or rely on `amssymb`.
  - Simple inequalities and units in running prose stay as plain text: ≤, ≥, ×, ≈.

## 9. Labs

- **Labs are isolated and safe.** Each lab starts in its own fresh folder (such as
  `~/sandbox/ch12`), never touches the reader's real folders or settings, and never risks data
  outside its folder.
- **No account is required to read the book, and none is created by it.** Where a lab needs a
  model, the reader supplies it; see section 10.
- **The book ships the lab data.** `labs/corpus/` holds about 40 short public-domain documents,
  8 queries with graded (3-point) relevance labels, and one deliberately awkward PDF with a table
  and a scanned page. No lab may say "your own documents": an expected result that depends on the
  reader's files holds for nobody, and hand-labelling hundreds of query--document pairs is not a
  lab, it is a punishment.
- **Reproducible from the PDF alone.** Show every file a lab needs in full, or give a short
  command that creates it. Anything under `labs/` is also offered as a download beside the PDF.
- **Expected results must hold for every reader.** Model output is stochastic, so never promise
  exact text: say what shape the output takes, which assertion must pass, or give a range. Show
  one real run and say the reader's numbers will differ.
- **Pin versions.** A lab that needs a third-party package installs it in a virtual environment
  with a pinned version, and the package is listed in the preface's "What You Need Installed".

## 10. Which model the labs use

Decided per lab, in this order:

1. **A small local model** where the lab is about mechanics that any model shows: prompting,
   variance, embeddings, retrieval, chunking, error analysis, agent loops, injection tests.
2. **A hosted model, with the key read from an environment variable**, only where the feature
   being taught does not exist locally: strict structured outputs, prompt-prefix caching,
   reasoning modes, provider routing. These labs must degrade gracefully — state the cost in
   tokens before the reader runs them, and describe the expected result qualitatively.

No lab, and no part of the build, ever reads or writes a credential file. Keys come from the
environment and are never printed, logged or committed.

## 11. Length

The book runs about **240 words per printed page**, counting code and tables. A chapter's word
budget is its page budget × 240; a 16-page chapter is about 3,800 words. Stay close to it: cut
padding rather than adding filler.

Page counts are **numbered pages**, from Part I's opener to the end of the glossary; part-opener
pages count, the front matter and index do not. Code blocks and tables never split across pages,
so to win back a page, cut near a chapter's end.

There is **no 100-page cap** on this book. It is one long book by design.

## 12. Build

Markdown → pandoc (with `latex/tools/filter.lua`) → XeLaTeX → PDF. The Markdown is the only
source of truth; never edit the generated `latex/chapters/*.tex`.

```bash
cd latex
make                      # convert ../markdown/*.md, then typeset book.pdf
make check                # overfull boxes, text off page, fonts, glossary, page count
PAGES_MIN=600 PAGES_MAX=1000 make check
```

`make` puts TeX on the PATH. To run `latexmk` by hand first
`export PATH=/Library/TeX/texbin:$PATH`.

Design (page size 7 × 9.19 in, Crimson Pro body, Source Sans 3 headings, Source Code Pro code,
callout icons, no shell prompts in code blocks) comes from `latex/preamble.tex` and is not to be
changed.

**`latex/preamble.tex` has diverged from the shared book template in three ways**, so never
re-copy it over this one:

1. `amsmath` and `unicode-math` are loaded, with `\setmathfont{Garamond-Math.otf}`.
2. `amssymb` is removed. Loading it alongside `unicode-math` fails with
   "Command `\eth` already defined", and nothing here needs an amssymb-only command.
3. `\prebookpart{<label>}{<title>}{<what to ignore>}` is added: an unnumbered part opener in
   the same design as `\bookpart`.

`markdown/_maths-proof.md` is the proof page for all of this. Its name starts with an underscore,
so `convert.sh` skips it; to rebuild it, copy it to a name without the underscore and add its
`\input`.

## 13. Delivered part by part

The reader studies the book while it is being written, so each part is built and handed over as
its own PDF as it is finished, and the full book is assembled at the end. `latex/book.tex` lists
only the chapters that exist; add each `\input` as its chapter lands, so the build always works.

## 14. Writing with agents

```text
TOC approved  ->  a writing agent drafts a part  ->  the editor edits every chapter  ->  build and check
```

- **The agent drafts.** One agent per part, in the background, so parts can be drafted at once.
- **The editor is the main session.** It reads every chapter in full, checks every fact, re-runs
  every lab, and rewrites rather than patches anything that is not good enough. A draft is never
  the final book.
- **When editing finds something an agent got wrong because this guide did not say it, add it to
  this guide**, so the next agent gets it right.

## 15. Before calling a part done

- `PAGES_MIN=<low> PAGES_MAX=<high> make check` passes: no overfull boxes, no text off any page,
  every bolded term in the glossary, page count within the part's target.
- Every page has been looked at, cover to cover (`pdftoppm -r 40` contact sheets).
- Every command and code sample has been run.
- Every chapter has its lab, summary, key terms, review questions and "You understand this when…".
- Every chapter has been edited by hand.
- Nothing anywhere refers to a website, a roadmap, numbered steps or tracks.
