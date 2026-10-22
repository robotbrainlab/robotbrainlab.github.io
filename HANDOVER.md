# Handover — Modern AI Engineering from Zero

Last updated: 2026-10-22 (revised after an independent review of the plan).

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
| 3 | **About 1,040 pages, with headroom to 1,175** | The owner reads quickly and will put in more hours if the pages buy content. **A page target that costs theory is forbidden.** Page counts follow the material. Never pad a chapter to reach a number either | A 500-page version, and later a 650-page version, both recommended to the owner and both overruled |
| 4 | **This repository sits outside the website repository** | The book is not website material. The website repository is public. This book is temporary, and the website repository's rule is "commit every file and keep it forever" | `_sources/modern-ai/` inside the website repository |
| 5 | **The book never mentions the website** | The syllabus came from the owner's own research notes. The book stands alone. No chapter may name a website, a roadmap, a learning path, numbered steps or tracks | — |
| 6 | **Four parts, plus an unnumbered pre-part** | The owner's books always have four parts. *The Complete Software Engineering Guide* already uses an unnumbered pre-part for *How Web Applications Work*, so the device is proven | A fifth part |
| 7 | **An interlude teaches the model's mechanism** | Interviews ask how attention works, why long context costs more, why models hallucinate, and what a key--value cache is. The earlier plan treated the model as a black box. That was a real gap | Leaving the model as a black box |
| 7a | **The interlude comes *after* Part I, not before it** | Four of its chapters open with problems only Part I makes sensible ("I was billed for tokens", "I set temperature to zero"). The old plan's own preface told the reader he could read Part I first and come back — if the preface must say that, the order is wrong. Putting Part I first also removes a duplication without cutting a page | The interlude first, which was the plan until 2026-10-22 |
| 8 | **Mathematics yes. ML and DL theory no** | The owner asked for this exactly. The line is: teach what the model computes when it answers; state how it learned and move on. `BOOK-GUIDE.md` §6 draws the line | Teaching gradients, optimisers and learning theory |
| 9 | **Chapters are numbered straight through, 1 to 57** | Appendix B keys 100 interview answers to chapter numbers. Unnumbered chapters make that clumsy | Unnumbered interlude chapters, as in the big book |
| 10 | **Serving, cost and security live in Part IV** | They are the answers to the four threads — Security, Speed, Cost, Failure. Part IV therefore carries 110 pages and is not a thin ending | Ordinary chapters in Part II |
| 11 | **Appendix B is an interview bank** | It is the reason the book exists. Write it last, from the finished chapters, never from memory | — |
| 12 | **Part III is one system that grows** | Lab 42 builds on labs 40 and 41. Standalone labs repeat themselves and cost about 25 more pages | Nine independent labs |
| 13 | **Statistics and ranking metrics are taught inline** | Chapter 19 teaches variance and confidence intervals. Chapter 25 teaches recall@k, MRR and nDCG. Without them the book cannot stand alone | Sending the reader to another book |
| 14 | **Each part is delivered as its own PDF** | The owner reads part 1 while part 2 is written. **Writing order is reading order** — the owner chose this explicitly on 2026-10-22, against a recommendation to write Part II first | One delivery at the end; writing Part II first |
| 15 | **Each concept is *owned* by one chapter** | "Appears exactly once" was already broken ten times. `TOC.md` names the owner for each. Without this, chapter 39 re-teaches chapter 14 and both overflow | The exactly-once rule, which was unenforceable |
| 16 | **The book ships its lab data** | `BOOK-GUIDE.md` demands expected results that hold for every reader, and six labs said "your own documents". Those cannot both be true. About 40 public-domain documents, 8 queries with graded labels, one awkward PDF | Each reader supplying a corpus, and hand-labelling ~360 pairs |
| 17 | **Appendix B is 100 answers at 150 to 180 words, in 45 pp** | At the old 25 pp it was 60 words per answer, including the question. Sixty seconds of speech is 150 to 180 words | 25 pp, which was wrong by a factor of 2.7 |
| 18 | **Appendix B's question list is written in week one** | It then acts as the acceptance test for each chapter as it lands. The answers are still written from the finished chapters, so decision 11 holds | Writing the whole appendix last, which left no time to drill it |
| 19 | **Four chapters were added for what interviews test and the research does not name** | Ch 19 (calling a model reliably: streaming, rate limits, retries, concurrency, multi-turn state), ch 32 (evaluating a grounded answer), ch 55 (a system designed aloud), and the split of agents into ch 37 and ch 38 | Leaving them out because they are not among the 83 concepts |
| 21 | **The chapter loop is a staged driver with evidenced records, two reviews, and a gate suite** | Imported from a finished 1,222-page book built under the same template, where every gate was paid for by a shipped defect. Its author's note on keeping the checklist as prose: *prose is what gets skipped* | A prose checklist in the guide, which is what §15 was until 22 Oct 2026 |
| 23 | **The register is settled: plain, simple, genuinely from scratch** | Deepak on chapter 1, 22 Oct 2026: *"The language is really easy to understand, and I like the simplicity. It genuinely starts from scratch, which I really appreciate."* Chapter 1 is the reference for voice. Do not write up, and do not assume knowledge | — |
| 24 | **Nothing is pushed until Part I is finished** | Deepak, 22 Oct 2026: *"After Part 1, we can commit."* Keep committing locally; create the private GitHub repository and push when chapters 1 to 7 are done | Pushing as soon as the repository exists |
| 22 | **One chapter at a time, never a part at a time** | Context dilution is the main cause of invented content. Writing several chapters in one stretch makes the later ones get written from the pattern of the earlier ones rather than from their sources | A drafting agent per part, which was the plan until 22 Oct 2026 |
| 20 | **Lab 50 attacks the system before chapter 51 explains security** | Meet the failure, then learn the framework. The lab uses what chapter 36 taught. Moving it after Part IV would break Part IV's "no labs" rule | Moving the lab after chapter 51 |

## 3. State, as of 2026-10-22

**Repository:** `~/LearningLab/towards-intelligence/modern-ai-interview-prep`, branch `main`,
7 commits, nothing pushed.

| Path | What it is | State |
|---|---|---|
| `HANDOVER.md` | This file | — |
| `BOOK-GUIDE.md` | The spec. Self-contained, because a writing agent sees no other repository | Done |
| `TOC.md` | 57 chapters, 4 appendices, page budgets, and the concept-ownership table | **Draft. Not approved** |
| `TOC.pdf` | A review copy of `TOC.md`, built through the book template so it has the cover, the book's page design and a contents list of all 57 chapters. Generated by `tools/make-toc-pdf.py`, and in `.gitignore` | Sent to the owner |
| `tools/make-toc-pdf.py` | Rebuilds `TOC.pdf` from `TOC.md`. Run it after any edit to the plan | Done |
| `tools/chapter.py` | The staged driver: `begin` → `written` → `reviewed`. Each stage refuses until the last is evidenced | Done |
| `tools/check-all.sh` | The gate suite. Must end `ALL GATES PASS` | Done |
| `tools/verify-*.py` | voice · boundary · render · record · coverage · absolutes · inputs. Each proved against an injected defect before wiring in | Done |
| `records/` | One record per chapter, ticked with evidence, hashed last | Empty |
| `LEDGER-TAUGHT.md` | What each chapter already taught, with "Do not" rows. The only defence against a chapter denying an earlier one | Seeded |
| `LEDGER-DEFECTS.md` | What the gates cannot catch. Ten entries inherited rather than rediscovered | Seeded |
| `README.md` | Status tracker, part by part | Done |
| `markdown/00-preface.md` | A placeholder, so the build runs | Replace before release |
| `markdown/_maths-proof.md` | Proves mathematics typesets. `convert.sh` skips it, because its name starts with `_` | Keep for regression |
| `latex/` | The O'Reilly template, with three changes (section 5) | Builds |
| `labs/` | Empty | — |

**No chapter is written.** The build makes 12 pages: front matter and five part openers.

**An independent review of the plan ran on 2026-10-22.** It found one real defect (two stale
chapter numbers in `BOOK-GUIDE.md` §1, fixed in `6f39e90`), six gaps now filled by decisions 15
to 20, and three places where the mathematics boundary could not hold, now repaired in
`BOOK-GUIDE.md` §6. Its recommendation to cut to 650 pages was overruled by the owner. Its
recommendation to write Part II first was overruled by the owner, who chose reading order. Its
recommendation to put Part I first was accepted (decision 7a).

**Checks:** `make` succeeds. `make check` reports 0 overfull boxes, 0 missing glyphs, 0 undefined
references. It fails on two points only because no content exists yet: no glossary file, and
Source Code Pro is not embedded because no code block exists.

## 4. Blocked. The owner must decide these

1. **The GitHub repository does not exist — and is deliberately not needed yet.** Decision
   24: nothing is pushed until Part I is finished. When it is, create it **private**, named
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
| Orientation: Contemporary AI Systems | 7 | 1 to 7 |
| Working with Models | 10 | 10, 13, 16, 18, 20, 21, 22, 23 |
| Embeddings and Semantic Search | 6 | 24, 25 |
| Retrieval-Augmented Systems | 9 | 26 to 29, 32 |
| Evaluating and Observing AI Applications | 9 | 30 to 33 |
| Agents, Tools and Context | 17 | 34 to 38 |
| Adapting Models in Practice | 8 | 39 |
| Securing AI Systems in Practice | 7 | 51 |
| Inference, Cost and Production | 10 | 52 to 54 |

The interlude (chapters 8 to 17) is new, and so are chapters 19, 32 and 55. None of them is in
that research; they are there because interviews test them.

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
4. Write in the order `TOC.md` gives, which is the order the book is read: Part I, the interlude,
   Part II in two halves, labs 40 to 46, labs 47 to 50, Part IV, then the appendices. Write
   Appendix B's question list in week one and use it as the acceptance test for every chapter.
5. For each part: a writing agent drafts it, then the main session edits **every** chapter by
   hand, then build and check (`BOOK-GUIDE.md` §14 and §15).
6. Update `README.md` and this file after each part.
