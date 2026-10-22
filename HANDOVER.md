# Handover — Modern AI Engineering from Zero

Last updated: 2026-10-22.

Read this file first, then `BOOK-GUIDE.md` (the spec), then `TOC.md` (the plan).

---

## 1. What this is

One book, about 875 pages, written from zero. The reader is the owner of this repository. The
purpose is to pass **AI/LLM application engineer** interviews before **31 December 2026**.

- The owner studies about **10 to 15 hours a week**. That is about 125 hours in all.
- The book is about **modern AI engineering only**. It is not about data structures, operating
  systems, networking, databases or distributed systems. The owner decided this.
- The book is **temporary**. After the interviews the owner may study the full theory. This
  repository can be archived then.

## 2. The decisions, and why

Do not reopen these. Each one was decided with the owner.

| # | Decision | Why | What was rejected |
|---|---|---|---|
| 1 | **One book, not nine** | The nine subject areas are one system. Separate books must each stand alone, so they repeat the shared ground — about 100 pages of it. You also get nine prefaces, nine glossaries, nine cheat sheets, and the four threads split nine ways | One book per subject area |
| 2 | **Claude writes the book. The owner reads it** | The owner's decision, stated more than once. **Do not argue about this again.** Earlier in the first session Claude pushed the owner to write the books. That was wrong and it was dropped | The owner writes, Claude edits |
| 3 | **About 875 pages** | The owner reads quickly and accepts 1000+ pages. Page counts follow the material. Never pad a chapter to reach a number | A 500-page version, which Claude recommended and the owner overruled |
| 4 | **This repository sits outside the website repository** | The book is not website material. The website repository is public. This book is temporary, and the website repository's rule is "commit every file and keep it forever" | `_sources/modern-ai/` inside the website repository |
| 5 | **The book never mentions the website** | The syllabus came from the owner's own research notes. The book stands alone. No chapter may name a website, a roadmap, a learning path, numbered steps or tracks | — |
| 6 | **Four parts, plus an unnumbered pre-part** | The owner's books always have four parts. *The Complete Software Engineering Guide* already uses an unnumbered pre-part for *How Web Applications Work*, so the device is proven | A fifth part |
| 7 | **The pre-part teaches the model's mechanism** | Interviews ask how attention works, why long context costs more, why models hallucinate, and what a key--value cache is. The earlier plan treated the model as a black box. That was a real gap | Leaving the model as a black box |
| 8 | **Mathematics yes. ML and DL theory no** | The owner asked for this exactly. The line is: teach what the model computes when it answers; state how it learned and move on. `BOOK-GUIDE.md` §6 draws the line | Teaching gradients, optimisers and learning theory |
| 9 | **Chapters are numbered straight through, 1 to 51** | Appendix B keys about 100 interview answers to chapter numbers. Unnumbered chapters make that clumsy | Unnumbered pre-part chapters, as in the big book |
| 10 | **Serving, cost and security live in Part IV** | They are the answers to the four threads — Security, Speed, Cost, Failure. Part IV therefore carries 110 pages and is not a thin ending | Ordinary chapters in Part II |
| 11 | **Appendix B is an interview bank** | It is the reason the book exists. Write it last, from the finished chapters, never from memory | — |
| 12 | **Part III is one system that grows** | Lab 42 builds on labs 40 and 41. Standalone labs repeat themselves and cost about 25 more pages | Nine independent labs |
| 13 | **Statistics and ranking metrics are taught inline** | Chapter 19 teaches variance and confidence intervals. Chapter 25 teaches recall@k, MRR and nDCG. Without them the book cannot stand alone | Sending the reader to another book |
| 14 | **Each part is delivered as its own PDF** | The owner reads part 1 while part 2 is written. Writing order is the same as reading order | One delivery at the end |

## 3. State, as of 2026-10-22

**Repository:** `~/LearningLab/towards-intelligence/modern-ai-interview-prep`, branch `main`,
5 commits, nothing pushed.

| Path | What it is | State |
|---|---|---|
| `HANDOVER.md` | This file | — |
| `BOOK-GUIDE.md` | The spec. Self-contained, because a writing agent sees no other repository | Done |
| `TOC.md` | 51 chapters, 4 appendices, page budgets | **Draft. Not approved** |
| `TOC.pdf` | A review copy of `TOC.md` on A4. Generated, and in `.gitignore` | Sent to the owner |
| `README.md` | Status tracker, part by part | Done |
| `markdown/00-preface.md` | A placeholder, so the build runs | Replace before release |
| `markdown/_maths-proof.md` | Proves mathematics typesets. `convert.sh` skips it, because its name starts with `_` | Keep for regression |
| `latex/` | The O'Reilly template, with three changes (section 5) | Builds |
| `labs/` | Empty | — |

**No chapter is written.** The build makes 12 pages: front matter and five part openers.

**Checks:** `make` succeeds. `make check` reports 0 overfull boxes, 0 missing glyphs, 0 undefined
references. It fails on two points only because no content exists yet: no glossary file, and
Source Code Pro is not embedded because no code block exists.

## 4. Blocked. The owner must decide these

1. **The GitHub repository does not exist.** Create it **private**, named
   `modern-ai-interview-prep`, under the **robotbrainlab** account. The git remote is already set
   to `git@github-robotbrainlab:robotbrainlab/modern-ai-interview-prep.git`, and that SSH key
   authenticates. Then run `git push -u origin main`.
2. **The labs need a model.** Choose one:
   - install `ollama` with a small model, so every lab runs free and offline and real output goes
     in the book; or
   - write the labs against a hosted API, with the key read from an environment variable.
   Claude's recommendation is both: `ollama` for most labs, a hosted API only for strict
   structured outputs, prompt-prefix caching and reasoning modes. This blocks Part III only.
3. **`TOC.md` is not approved.** No chapter is drafted until the owner approves it.

## 5. The build, and how it differs from the other books

Markdown → pandoc (with `latex/tools/filter.lua`) → XeLaTeX → PDF. The Markdown is the only
source. Never edit `latex/chapters/*.tex`.

```bash
cd latex
make
PAGES_MIN=600 PAGES_MAX=1000 make check
```

`latex/preamble.tex` has **three changes** from the shared `book-template`. **Never copy the
template's preamble over this one.**

1. `amsmath` and `unicode-math` are loaded, with `\setmathfont{Garamond-Math.otf}`. Garamond-Math
   matches Crimson Pro, which is a Garamond face, and EB Garamond on the cover.
2. `amssymb` is removed. With `unicode-math` it fails with "Command `\eth` already defined".
   Nothing here uses an amssymb-only command.
3. `\prebookpart{<label>}{<title>}{<what to ignore>}` is added. It is an unnumbered part opener
   in the same design as `\bookpart`.

**Mathematics is written as raw LaTeX, never as `$…$`.** `tools/convert.sh` disables dollar maths
on purpose, so a price like $5 stays text. This book is full of prices.

- Inline: `` `\(O(n^2 d)\)`{=latex} ``. The delimiters go inside the span.
- Display: a fenced block opened with ```` ```{=latex} ````, holding `\[ … \]`.

## 6. Where the syllabus came from

The 83 concepts come from the owner's own research. The owner's reading copy of that research is
the Data & Intelligence guide in the website repository, under
`data-intelligence/guide/learn/<topic>/`, in nine topic pages.

**Use it only to check coverage.** Never quote it, never link it, and never let a chapter mention
it. Decision 5 above is absolute.

The nine topics and where each one now sits:

| Topic | Concepts | Chapters |
|---|---|---|
| Orientation: Contemporary AI Systems | 7 | 11 to 17 |
| Working with Models | 10 | 3, 6, 8, 18, 20, 21, 22 |
| Embeddings and Semantic Search | 6 | 23, 24 |
| Retrieval-Augmented Systems | 9 | 25 to 28 |
| Evaluating and Observing AI Applications | 9 | 29 to 31 |
| Agents, Tools and Context | 17 | 32 to 35 |
| Adapting Models in Practice | 8 | 36 |
| Securing AI Systems in Practice | 7 | 46 |
| Inference, Cost and Production | 10 | 47 to 49 |

The pre-part (chapters 1 to 10) is new. It is not in that research.

## 7. Gotchas

- **Never push as the `dlakshmizlk` account.** `gh` on this machine is logged in as that account.
  This repository pushes over the `github-robotbrainlab` SSH alias, which uses
  `~/.ssh/id_ed25519_robotbrainlab`.
- **Never re-copy `book-template/preamble.tex`** over `latex/preamble.tex`. See section 5.
- `convert.sh` skips any Markdown file whose name starts with `_`. That is how
  `_maths-proof.md` stays out of the book.
- A page holds about **240 words**, including code and tables. A 16-page chapter is about 3,800
  words.
- `TOC.pdf` is generated. Rebuild it from `TOC.md`; do not edit it.
- Keep the owner's wording. The chapter titles and opening problems in `TOC.md` were reviewed by
  the owner.

## 8. How to resume

1. Read `BOOK-GUIDE.md` in full, then `TOC.md`.
2. Check section 4 of this file. If anything there is still open, ask the owner.
3. Check `README.md` for the status of each part.
4. Write in the order `TOC.md` gives: the pre-part, then Part I, then Part II in two halves, then
   labs 37 to 42, then Part IV, then labs 43 to 45, then the appendices.
5. For each part: a writing agent drafts it, then the main session edits **every** chapter by
   hand, then build and check (`BOOK-GUIDE.md` §14 and §15).
6. Update `README.md` and this file after each part.
