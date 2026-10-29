# Handover — Modern AI Engineering from Zero

Last updated: 2026-10-28 (chapter 26 closed, sharpen pass over 8-17 applied; stopped at the reader's request).

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
| 6 | **Four parts, and one of them has two halves** | The owner's books always have four parts, and that convention held. The device for dividing a part came from the same place as everything else here: `\prebookpart` in *The Complete Software Engineering Guide*, scaled down into `\booksubpart`. See decision 7a for where the division landed | A fifth part |
| 7 | **The book teaches the model's mechanism, not just its interface** | Interviews ask how attention works, why long context costs more, why models hallucinate, and what a key--value cache is. The earlier plan treated the model as a black box. That was a real gap | Leaving the model as a black box |
| 7a | **"Inside the Model" is the second half of Part I, not a part and not an interlude** | Deepak, 22 Oct 2026: *"it is understanding right?"* He is correct, and it settles a question I had answered badly twice. By the book's own part names — Understand, Use, Apply, What Next — chapter 11 "Attention, Worked by Hand" files under Understand without hesitation. Part I therefore has two halves, both Understand: *Mental Model* (chs 1–7, the system around the model) and *Inside the Model* (chs 8–17, the model itself), divided by `\booksubpart`. The order within the part is load-bearing: four of the second half's chapters open with problems only the first half makes sensible | Making it Part II and renumbering (wrong in kind — it is not a step in the Understand→Use→Apply progression); keeping it unnumbered and relabelling it "Interlude" (Deepak rejected it, and he was right: the label marked as a detour something that is not one) |
| 8 | **Mathematics yes. ML and DL theory no** | The owner asked for this exactly. The line is: teach what the model computes when it answers; state how it learned and move on. `BOOK-GUIDE.md` §6 draws the line | Teaching gradients, optimisers and learning theory |
| 9 | **Chapters are numbered straight through, 1 to 57** | Appendix B keys 100 interview answers to chapter numbers. Unnumbered chapters make that clumsy. Part I takes 1–17 across both halves | Restarting the numbering at each half |
| 10 | **Serving, cost and security live in Part IV** | They are the answers to the four threads — Security, Speed, Cost, Failure. Part IV therefore carries 110 pages and is not a thin ending | Ordinary chapters in Part II |
| 11 | **Appendix B is an interview bank** | It is the reason the book exists. Write it last, from the finished chapters, never from memory | — |
| 12 | **Part III is one system that grows** | Lab 42 builds on labs 40 and 41. Standalone labs repeat themselves and cost about 25 more pages | Nine independent labs |
| 13 | **Statistics and ranking metrics are taught inline** | Chapter 20 teaches the bootstrap, confidence intervals and paired comparison. Chapter 26 teaches recall@k, MRR and nDCG from zero. Without them the book cannot stand alone | Sending the reader to another book | *(The chapter numbers in this row said 19 and 25 until 28 Oct 2026; the TOC shifted after it was written, and chapter 25 is now "Where Dense Search Fails", which names no measure. The decision is unchanged.)*
| 14 | **Each part is delivered as its own PDF** | The owner reads part 1 while part 2 is written. **Writing order is reading order** — the owner chose this explicitly on 2026-10-22, against a recommendation to write Part II first | One delivery at the end; writing Part II first |
| 15 | **Each concept is *owned* by one chapter** | "Appears exactly once" was already broken ten times. `TOC.md` names the owner for each. Without this, chapter 39 re-teaches chapter 14 and both overflow | The exactly-once rule, which was unenforceable |
| 16 | **The book ships its lab data** | `BOOK-GUIDE.md` demands expected results that hold for every reader, and six labs said "your own documents". Those cannot both be true. About 40 public-domain documents, 8 queries with graded labels, one awkward PDF | Each reader supplying a corpus, and hand-labelling ~360 pairs |
| 17 | **Appendix B is 100 answers at 150 to 180 words, in 45 pp** | At the old 25 pp it was 60 words per answer, including the question. Sixty seconds of speech is 150 to 180 words | 25 pp, which was wrong by a factor of 2.7 |
| 18 | **Appendix B's question list is written in week one** | It then acts as the acceptance test for each chapter as it lands. The answers are still written from the finished chapters, so decision 11 holds | Writing the whole appendix last, which left no time to drill it |
| 19 | **Four chapters were added for what interviews test and the research does not name** | Ch 19 (calling a model reliably: streaming, rate limits, retries, concurrency, multi-turn state), ch 32 (evaluating a grounded answer), ch 55 (a system designed aloud), and the split of agents into ch 37 and ch 38 | Leaving them out because they are not among the 83 concepts |
| 21 | **The chapter loop is a staged driver with evidenced records, two reviews, and a gate suite** | Imported from a finished 1,222-page book built under the same template, where every gate was paid for by a shipped defect. Its author's note on keeping the checklist as prose: *prose is what gets skipped* | A prose checklist in the guide, which is what §15 was until 22 Oct 2026 |
| 25 | **Page budgets are estimates, not limits** | The reader, 22 Oct 2026: *"the best outcome is when the content flows naturally… some of the other parts might end up needing more pages, and we shouldn't cut valuable content just to stay within the estimate."* Never pad to reach one, never cut to fit one. A large gap is a prompt to check for thin coverage, nothing more | Re-budgeting Part I after chapter 3, which is what the ledger had set as a trigger  **Reaffirmed 28 Oct 2026, and the reader noted they had said it before:** *"Never stick to the page number estimates. Content is more important than the pages, so even if it is 1500-2000, I would not mind."* This extends the decision to the WHOLE-BOOK total, which is where I broke it: I reported progress as "763 pages against the 1,040 planned" and named the gap as something for the reader to decide. There is nothing to decide. `TOC.md`'s 1,040 is a sum of estimates, never a target, and the final length is whatever the material earns. Do not project against it and do not raise it. See `BOOK-GUIDE.md` §11 point 5. |
| 23 | **The register is settled: plain, simple, genuinely from scratch** | Deepak on chapter 1, 22 Oct 2026: *"The language is really easy to understand, and I like the simplicity. It genuinely starts from scratch, which I really appreciate."* Chapter 1 is the reference for voice. Do not write up, and do not assume knowledge | — |
| 24 | **Nothing is pushed until Part I is finished** | Deepak, 22 Oct 2026: *"After Part 1, we can commit."* Keep committing locally; create the private GitHub repository and push when chapters 1 to 7 are done | Pushing as soon as the repository exists |
| 22 | **One chapter at a time, never a part at a time** | Context dilution is the main cause of invented content. Writing several chapters in one stretch makes the later ones get written from the pattern of the earlier ones rather than from their sources | A drafting agent per part, which was the plan until 22 Oct 2026 |
| 20 | **Lab 50 attacks the system before chapter 51 explains security** | Meet the failure, then learn the framework. The lab uses what chapter 36 taught. Moving it after Part IV would break Part IV's "no labs" rule | Moving the lab after chapter 51 |

## 3. State, as of 2026-10-28

**Where it lives:** `_book/` inside the website repository
(`~/LearningLab/towards-intelligence/robotbrainlab.github.io`), branch `main`, **pushed**.
It used to be its own repository; that folder was deleted on 2026-10-23 after checking every
tracked file was byte-identical here and every commit reachable. The leading `_` keeps it off
the live site — GitHub Pages never publishes a `_`-prefixed folder, and every `_book/` URL
returns 404. The website repository is public, which the owner decided deliberately. See that
repository's `.claude/HANDOVER.md`, section "The interview-prep book", for the cleanup recipe.

**Part I is complete: all 17 chapters, 197 printed pages against a 266-page estimate.**
Its first half (1 to 7) is 70 pages against 98; *Inside the Model* (8 to 17) is 127 against 168. `bash tools/check-all.sh` ends `ALL GATES PASS`.

**Part II is drafting: chapters 18 to 26 closed, 152 printed pages.** The book is
**365 printed pages** over 26 of 57 chapters. Chapter 26 is the longest at 30 pages.

**Stopped here on 28 Oct 2026, at the reader's request, with everything pushed and the PDF
delivered.** Nothing is half-finished: chapters 27 to 34 are closed and sealed, the sharpen pass
over chapters 8-17 is applied and every record amended, and `bash tools/check-all.sh` ends
`ALL GATES PASS`. **The next chapter to write is 35, Context Engineering**; read its `TOC.md` row
and every `LEDGER-TAUGHT.md` row naming it before anything else, per §14 step 1. Chapter 34 is the
one to read first: it ends by handing 35 the problem a loop has at step 13 on a fat-stepped run,
and 35's own opening problem ("works for three steps and then starts forgetting") is the same
wound.

**The evaluation chapters cost more per chapter than the mechanism ones did, and the records say
why.** Their reviews found 22, 17 and 15 findings, and in each case several of the FIRST round's
fixes were themselves wrong — 4, 11 and 7. The pattern is the same every time: a sentence written
to retire an absolute, written at the speed of a correction rather than of a claim. Entries 52 to
55 of `LEDGER-DEFECTS.md` are all from this run, and entry 54 is the one to read first.

**Three things waiting, none blocking chapter 31.** The sharpen pass should be run again over
chapters 18 to 30 once Part II is finished, and `LEDGER-DEFECTS.md` entry 44 says why later is
better than per-chapter — **it has one concrete target already**: chapter 19 line 93 says "This
is the commonest way a working script dies at scale", an empirical superlative the chapter has
no evidence for, found while sweeping the same defect out of chapter 30. And `labs/` is still
empty, which chapter 7 promises and §9 specifies; chapters 26, 27, 29 and 30 each had to print
their own data because of it. Chapters 21, 22 and 25 are the first to exceed
their estimates, each in its fix pass rather than in drafting. The reviews have changed
character across Part II: the early chapters failed on arithmetic and on invented program
output, which is gone now that every program is written and run before any sentence about it,
and the later ones fail on **claims stated one notch wider than their demonstrations support**
and on false cross-chapter citations. Chapters 23 and 25 each needed a third reading for that
reason — see `LEDGER-DEFECTS.md` entries 38 and 40.

**Measure printed pages with `python3 tools/pages.py`**, never by subtracting folios.
Three chapters were over-counted that way; `LEDGER-DEFECTS.md` entry 23 has the detail.

| Path | What it is | State |
|---|---|---|
| `markdown/01` … `markdown/07` | Part I · *Mental Model* | **Done.** Two review passes each, records sealed |
| `markdown/08` … `markdown/17` | Part I · *Inside the Model* | **Done.** Two review passes each, records sealed |
| `markdown/18` | Part II · *Use*, first chapter | **Done.** Two review passes, record sealed |
| `markdown/19` | Calling a model reliably | **Done.** Two review passes, record sealed. The first pass found that bank question 42 had never been read, so the chapter went 13 → 20 pages |
| `markdown/20` | Is the difference real? | **Done.** Two review passes, record sealed. Earned `tools/verify-index.py` and `LEDGER-DEFECTS.md` entry 34 |
| `markdown/21` | Structured output and schemas | **Done.** Two review passes, record sealed. Earned entries 35 and 36, and the index's `\raggedcolumns` fix |
| `markdown/22` | Constrained decoding and strict modes | **Done.** Two review passes, record sealed. Earned entry 37, and `check-all.sh` now checks the "0 undefined" its header always promised |
| `markdown/23` | How a tool call works | **Done.** **Three** review passes, record sealed — a section written to answer the first review had itself only been read once. Earned entry 38, and the first message list in the book that carries a tool message |
| `markdown/24` | Embeddings, and choosing one | **Done.** Two review passes, record sealed. Earned entry 39 and a real fix to `verify-arithmetic.py`, which had been reporting 540 equations checked while checking 56 |
| `markdown/19` … `markdown/57` | Chapters 19 to 57 | Not started |
| `markdown/00-preface.md` | A placeholder, so the build runs | Replace before release |
| `markdown/C-glossary.md` | Appendix C. **Generated** by `tools/glossary.py` from every chapter's Key Terms table | 115 terms, in the PDF |
| `records/` | One record per chapter, ticked with evidence, hashed last | 18 of 57 |
| `labs/` | The data every Part III lab runs on | **Empty — see section 4** |
| `LEDGER-TAUGHT.md` | What each chapter taught, with "Do not" rows | 34 rows |
| `LEDGER-DEFECTS.md` | What the gates cannot catch | 59 entries |
| `LEDGER-SHORTHAND.md` | What an interviewer calls each concept the book teaches, which chapter names the shorthand, which shorthands wait on an unwritten chapter, and which were checked and left out on purpose | Written 2026-10-29 |
| `tools/` | The driver, the gate suite, the glossary generator, the build probe | Done |
| `latex/` | The template, with five changes (section 5) | Builds clean |

**Measured, not estimated.** Chapters 1 to 17 came in at 74% of their page budget — 197
printed pages against 266 — and the per-chapter shares are 71, 56, 71, 62, 79, 92, 80, 86, 100,
80, 75, 81, 93, 59, 60, 56 and 100 per cent. Chapter 14's 59% is the largest gap in the book and both
reviewers concluded the estimate predates the decision that its biggest subjects sit outside
the boundary. Chapter 9 is the only one to land exactly on its estimate; none has yet
exceeded one. Budgets are estimates and nothing was padded (`BOOK-GUIDE.md` §11), so expect
the whole book around 700 printed pages rather than 1,040. Do not re-plan on this.

### 3.1 The schedule to 31 December

`TOC.md`'s writing-order table is the plan and has not changed. **Its order was chosen by the
owner over a review's recommendation to write Part II first** (see the review note below), so
do not reopen it. Dates, assuming the Part I rate holds:

| Stage | What | Est. pp | Target |
|---|---|---|---|
| 1 | Part I, chs 1–7 | 98 | **Done 2026-10-23** |
| 2 | *Inside the Model*, chs 8–17 | 168 | **Done 2026-10-28**, twelve days early |
| 3 | Part II, chs 18–29 | 196 | 10 Nov – 23 Nov. **18 to 24 done, 28 Oct** |
| 4 | Part II, chs 30–39 | 166 | 24 Nov – 5 Dec |
| 5 | Part III, labs 40–46 | 132 | 6 Dec – 15 Dec |
| 6 | Part III, labs 47–50 | 58 | 16 Dec – 19 Dec |
| 7 | Part IV, chs 51–57 | 136 | 20 Dec – 28 Dec |
| 8 | Appendix B's answers, and the index | 83 | 29 Dec – 31 Dec |

**This schedule has no slack, and two things about it are worth saying plainly.**

*First, the risk is concentrated at the end.* Chapter 55 (the system designed aloud) and
Appendix B (the question bank) are the two most interview-useful pieces in the book and they
land in the last ten days. If anything slips, they are what slips.

*Second, one of them no longer waits.* `TOC.md` always said **Appendix B's question list is
written in week one** — the questions only, from the contents, as the acceptance test every
chapter is then measured against. It had not happened and seven chapters had shipped without
it. **Written 2026-10-27**: 100 questions keyed to chapters, in the PDF, with the answers to
follow as the chapters do. `BOOK-GUIDE.md` §15 now makes it a condition of a chapter being
done, and eight chapters carry no question deliberately (the bank's header lists them and
says why). **Appendix A** (the cheat sheet — the numbers
worth memorising) likewise accumulates: each chapter carries an optional
`### Worth Memorising` table and `tools/cheatsheet.py` generates the appendix from them, with
a gate on freshness. **Built 2026-10-27**, so nothing in the appendices is end-loaded any
more: A and C are generated, B's questions are written and only its answers follow the
chapters, and D is the LaTeX index.

*If the schedule slips*, drop in this order: the index (Appendix D, generated), then labs 47–50
(stage 6), then depth in chapters 8–17. **Never drop chapter 55 or Appendix B.**

**An independent review of the plan ran on 2026-10-22.** It found one real defect (two stale
chapter numbers in `BOOK-GUIDE.md` §1) and six gaps now filled by decisions 15 to 20. Its
recommendation to cut to 650 pages was overruled by the owner — and the measured rate has since
arrived there anyway without cutting anything. Its recommendation to write Part II first was
**overruled by the owner, who chose reading order**; that decision stands.

## 4. Open items

1. ~~**The GitHub repository does not exist.**~~ **Resolved differently, 2026-10-23.** The
   separate repository was never created. The book moved into the public website repository as
   `_book/` instead, and is pushed. Nothing is outstanding.
2. **The labs need a model. This is the owner's decision and it is now the oldest one open.**
   Either install `ollama` with a small model, so every lab runs free and offline and real
   output goes in the book; or write the labs against a hosted API with the key in an
   environment variable. Claude's recommendation is both: `ollama` for most labs, a hosted API
   only for strict structured output, prompt-prefix caching and reasoning modes. **Due before
   chapter 40** (stage 5, early December), which is the first lab that calls a model.
3. **`labs/` is empty, and chapter 7 already promises its contents to the reader** — about
   forty short public-domain documents, eight queries with a relevance judgement each, and one
   deliberately awkward PDF with a table and a scanned page. Every Part III expected result
   depends on it (`BOOK-GUIDE.md` §9: a lab that depends on the reader's own files holds for
   nobody). Build it during stage 4, before the labs need it, not during stage 5.
4. **Chapter 6's five evidence rungs are not Key Terms.** *Announcement*, *demonstration*,
   *one study* and *settled practice* are named and defined in a table there, and chapters 20
   and 30–33 will use them, but only *practitioner report* is in Key Terms — so Appendix C
   carries one of five. Fixing it is one chapter edit and one `chapter.py reviewed` reseal.

**Nothing on this list blocks chapter 19.** Items 2 and 3 are due before chapter 40, and
items 1 and 4 are small.

## 5. The build, and how it differs from the other books

Markdown → pandoc (with `latex/tools/filter.lua`) → XeLaTeX → PDF. The Markdown is the only
source. Never edit `latex/chapters/*.tex`.

```bash
cd latex
make
PAGES_MIN=600 PAGES_MAX=1000 make check
```

`latex/preamble.tex` has **five changes** from the shared `book-template`. **Never copy the
template's preamble over this one.**

1. `amsmath` and `unicode-math` are loaded, with `\setmathfont{Garamond-Math.otf}`. Garamond-Math
   matches Crimson Pro, which is a Garamond face, and EB Garamond on the cover.
2. `amssymb` is removed. With `unicode-math` it fails with "Command `\eth` already defined".
   Nothing here uses an amssymb-only command.
3. The PDF outline covers the whole book, not only the chapters: `\pdfbookmark` entries for
   the cover, title page, copyright, contents and back cover. The nesting is controlled by
   three macros that renew `\toclevel@chapter`, `\toclevel@section` and
   `\toclevel@subsection` together with `tocdepth` — `\toplevelchapters` (front and back
   matter, chapters at the top), `\partlevels` (chapters under their part) and
   `\subpartlevels` (chapters under a sub-part). `latex/book.tex` switches between them;
   without `\toplevelchapters` before `\printindex` the back matter nests under Part IV.
   **`\usepackage{bookmark}` is deliberately not loaded**: it reimplements the outline and
   ignores `\toclevel@<type>`, which is the only hook that can put a sub-part's chapters one
   level deeper. A sub-part's contents indentation is wrapped in `\texorpdfstring` so it does
   not leak a leading space into the bookmark. `tools/verify-outline.py` reads the built PDF
   and is the only gate that checks any of this.
4. Two opener macros are added. `\booksubpart{<numeral>}{<title>}{<what to ignore>}` divides a
   numbered part into halves, in smaller type with a thinner rule and an indented contents
   entry; Part I uses it twice. `\prebookpart` is an unnumbered opener for a section before
   Part I — ported from the big book, currently **unused**, and it should stay unused unless
   something genuinely belongs before chapter 1.
5. `\indexletter`'s space is **flexible**, `9pt plus 3pt minus 3pt`, and the **first** letter
   group gets none. `book.cls`'s own `\indexspace` is `10pt plus5pt minus3pt`; this macro had
   replaced it with a rigid `\addvspace{9pt}`, so the index could not absorb being ~9pt over
   one page and the build went overfull by `9.33658pt` the moment chapter 5's two Key Terms
   opened letter group `E`. The index paginates correctly on its own — 120 injected entries
   give 3 index pages and 0 overfull — so keep the shrink. The `\newif` names carry no `@`,
   because this block sits outside `\makeatletter`. See `LEDGER-DEFECTS.md` entry 17, which
   is also where the reason to run `tools/build-probe.sh` instead of grepping `book.log` is.

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

Part I's second half, *Inside the Model* (chapters 8 to 17), is new, and so are chapters 19, 32 and 55. None of them is in
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
4. Write in the order `TOC.md` gives, which is the order the book is read: Part I's first
   half (1–7), its second half (8–17), Part II in two stretches, labs 40 to 46, labs 47 to
   50, Part IV, then the appendices. Write
   Appendix B's question list in week one and use it as the acceptance test for every chapter.
5. For each part: a writing agent drafts it, then the main session edits **every** chapter by
   hand, then build and check (`BOOK-GUIDE.md` §14 and §15).
6. Update `README.md` and this file after each part.
