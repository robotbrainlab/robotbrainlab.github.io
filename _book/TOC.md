# Modern AI Engineering from Zero — Table of Contents

**Status: draft, awaiting approval.** Nothing is drafted until this is approved.

- **Target:** about **1,040 numbered pages** (~250,000 words). **Every page number below is an
  estimate for planning, not a limit.** No chapter is capped at the cost of its content, and
  nothing is padded to reach a number. Chapters that need more take more; chapters that need
  less are not padded. See `BOOK-GUIDE.md` §11.
- **Structure: four parts.** I · Understand (266 pp, in two halves — *Mental Model*,
  chapters 1–7, and *Inside the Model*, chapters 8–17) · II · Use (362 pp) · III · Apply
  (190 pp) · IV · What Next (136 pp) · Appendices (83 pp), plus the part and sub-part
  opener pages.
- **Order is reading order.** The book is written in the order it is read, and each part is
  delivered as its own PDF as it is finished.
- **Chapters are numbered straight through, 1–57.** Part I takes 1–17 across both of its
  halves; the halves divide the part, they do not restart the numbering.
- **Coverage:** all 83 concepts of the nine subject areas, each **owned** by one chapter (see
  *Who owns what*), plus the model's own mechanism, plus the material an interview tests that the
  nine subject areas do not name.
- **Mathematics is used where it is the clearest statement.** Machine-learning and deep-learning
  theory is not taught (`BOOK-GUIDE.md` §6 draws the line).
- Every chapter opens with its problem below, then the question it raises (the writer words the
  question). See `BOOK-GUIDE.md` §3.

---

## Part I · Mental Model — chapters 1–7, 98 pp

**Part I has two halves, and both of them are *Understand*.** The first is the system
around the model; the second is the model itself. Neither is a part of its own, because
both answer the same question — *what is this thing and how does it work* — but the ground
changes at chapter 8 and the reader is told so, with a sub-part opener (`\booksubpart`).

*Part I's own note:* ignore every setting, price and product name. This part is what the
thing is, not how you drive it.

*What to ignore for now, in this half:* what is inside the model — the second half opens it.

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 1 | What a Model Is, and What You Get From It | Everyone talks about "using AI" and I picture training something. I have no idea what you actually get, or how. | A model as a service you send text to and get text back from; what it knows and what it cannot know; you choose the model and what you send, not what it holds; latency and price as properties you feel; using versus training | 14 |
| 2 | The Parts Around the Model | The model is one box. Everything I read draws five more boxes around it and I can't see why any of them are there. | Context: instructions, the request, added material; retrieval; tools; checks; people; the compound system; what each part is for; the same small cast of parts in nearly every product | 18 |
| 3 | Why It Is Assembled This Way | Why not just ask the model? Why does every real system wrap it in so much machinery? | The model does not know your data, cannot act in the world, cannot reliably check itself, and is not accountable; each part answers one of those; what each part costs you in return | 14 |
| 4 | The Agent Loop, and How Much Freedom It Actually Gets | "Agent" sounds like it does the whole job by itself. That can't be how anyone ships this. | The loop: decide, call a tool, read the result, continue; where control flow moves; compounding error; how short real deployed loops are; approval points; why bounded autonomy is the norm | 16 |
| 5 | Where the Work Actually Goes | I assumed the hard part was writing the prompt. People who do this for a living say it isn't. | Choosing what information reaches the model; deciding what it may do; finding out whether the output was any good; controlling what it costs; how much of the real job is evaluation and error analysis | 14 |
| 6 | What Changes Fast, and What Changes Slowly | Half of what I read is already out of date and I can't tell which half. | Lasting principles, current conventions, and details that will date; telling which of the three a claim is; **how strong the evidence is** — one study, a survey, or settled practice — and how to say so out loud; how to read a release announcement; what to memorise and what to look up | 12 |
| 7 | A Map of This Book | There's clearly a lot here. I don't know what order to learn it in, or what I can safely leave until later. | The four parts, and Part I's two halves; the chapters an interview reaches first; the one small system the labs build; what this book deliberately leaves out | 10 |

## Part I · Inside the Model — chapters 8–17, 168 pp

The second half of Part I, set with `\booksubpart`. The first half said what the model is
for; this says what it *does* when it answers, with real notation. Both halves are
*Understand*, which is why neither is a part of its own. It does **not** teach
machine-learning or deep-learning theory: `BOOK-GUIDE.md` §6 draws the line.

*What to ignore for now:* how the model was trained, beyond the shape of the loop.

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 8 | The Maths This Book Uses | I can follow an argument in words, but the moment someone writes a formula I stop reading. | Vectors and what a dimension is; matrices and matrix multiplication; the dot product, and why it measures agreement; cosine similarity; sums and products in notation; exponentials and logarithms; softmax read as a formula; big-O as a way to say how cost grows. Worked with small numbers throughout | 14 |
| 9 | What the Model Is Made Of | I know text goes in and text comes out. I don't know what is in between, or what shape it has. | Tokens in, a probability distribution over the vocabulary out; the embedding table as coordinates **nobody chose** — they are whatever made next-token prediction work, and no dimension means anything; a stack of identical layers; parameters as the numbers that were fitted; one forward pass producing exactly one next-token distribution | 12 |
| 10 | Tokens | I was billed for "tokens". I don't know what one is, or why my short question cost more than someone else's long one. | Why text becomes tokens; subword vocabularies; **the merge procedure run by hand on a toy corpus**, so the rest is explained and not asserted; input and output tokens; tokens as the unit of both cost and latency; counting before sending; why code and non-English text cost more; why a model miscounts the letters in a word | 20 |
| 11 | Attention, Worked by Hand | Every explanation says the model "pays attention to the relevant words". I want to know what is actually computed. | Queries, keys and values; the dot product as a score; scaling by the square root of the key dimension; softmax over the scores; the weighted blend of values; the full formula worked numerically on a 5-token sentence with 4-dimensional vectors; multiple heads; masking in a decoder; **how position reaches the model**, because the formula on its own is indifferent to the order of its inputs; why every pair is compared, and the O(n² d) cost that follows | 24 |
| 12 | The Stack: Layers and the Residual Stream | One attention step is clear enough. A model has ninety-six of them and I don't know what that accumulates. | The residual stream as a running representation each layer edits; attention blocks and feed-forward blocks; normalisation, and the one honest sentence about why it is there; what more layers let the model do, and what nobody can tell you about why; why "where is the fact stored" has no clean answer; parameter counts, and where the numbers actually sit | 16 |
| 13 | From Scores to a Word | I set temperature to zero and still got two different answers. | Logits as raw scores; softmax turning them into probabilities; temperature dividing the logits, and what that does to the distribution; top-k and top-p; **how long a reply may run, and what a stop condition is**; greedy decoding; **why zero temperature is still not a guarantee** — batching, floating-point order on a GPU, expert routing and provider-side changes; why one good output proves nothing (chapter 20 shows what to do about it) | 14 |
| 14 | How It Learned to Do This | Somebody trained this on "the internet". That sentence explains nothing. | Next-token prediction as the objective, written as a formula; cross-entropy and perplexity as definitions; the training loop's shape from outside, with the update rule stated once and not derived; pretraining, supervised fine-tuning and preference optimisation as three stages with different data; **the preference objective stated once as a formula**, named, not derived; what each stage changes and what it cannot | 22 |
| 15 | What It Costs From the Inside | My first token takes two seconds and the rest arrive in a stream. Nobody has told me why. | Prefill and decode as two different computations; the key--value cache, and the size calculation that predicts your memory bill; why the first token is slow and later ones are fast; why doubling the prompt more than doubles the work; **batching, and why your request is run together with other people's**; quantisation as bits per parameter, with the arithmetic; mixture-of-experts, and why a very large model can be cheap per token | 20 |
| 16 | Why It Fails the Way It Does | It invents citations with a straight face, and I'd like to know whether that is a bug or the design. | Plausible continuation with no truth oracle; why hallucination is the default behaviour rather than a defect; tokenisation artefacts — counting, spelling, arithmetic; the context window and what falls out of it; uneven use of long inputs; why intermediate reasoning buys accuracy — **the model's only scratchpad is its own output**, so later tokens can condition on partial work — what it costs, and why the visible trace is not a reliable account of how the answer was produced | 18 |
| 17 | Where the Theory You're Skipping Begins | I can explain the computation now. I want to know exactly what I still cannot explain. | An explicit list of what this book black-boxed — why gradient descent converges, backpropagation, optimiser design, initialisation, regularisation, inductive bias, numerical stability, generalisation theory, why models got better at producing useful intermediate steps, scaling-law derivations, **why the embedding geometry carries meaning**, **why the preference objective is the right thing to minimise**, and **why depth helps**; what to say when an interviewer pushes past the boundary | 8 |

## Part II · Use — 22 chapters, 362 pp

*What to ignore for now:* serving your own models, and the bill — Part IV takes both.

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 18 | The Prompt as a Specification | I keep rewriting my instructions until something works, and I couldn't tell you what I changed or why it helped. | Instructions, examples, output format and supplied information as four separable parts; the system, user, assistant and tool message list; **multi-turn conversation state**, and truncating a history that will not fit; changing one thing at a time; why current practice weights what the model receives over how the instruction is worded | 16 |
| 19 | Calling a Model Reliably | My script works for ten documents. For ten thousand it dies on a 429, and I can't tell how far it got. | **Streaming** — server-sent events, token deltas, why you cannot stream a response you must validate, and cancellation; rate limits and 429s; retries with exponential backoff and jitter; timeouts; concurrency with `asyncio`, taught from zero, and a semaphore to bound it; batch endpoints; idempotency; partial failure in a multi-step pipeline, and how to resume it | 20 |
| 20 | Is the Difference Real? | I changed the prompt and it looks better. I have no idea whether it actually is. | Building an evaluation set; repeated runs; variance from zero; **the bootstrap**, in three lines of Python, instead of a distribution the book cannot justify; a confidence interval on a score; paired comparison; how many cases and trials are enough; treating every change as an experiment | 18 |
| 21 | Structured Output and Schemas | The model gives me a paragraph when I need a field my code can read. | Asking for a fixed format; JSON schema; validating every response; measuring how often validation fails; what to do with the failures; why a program must never trust prose | 14 |
| 22 | Constrained Decoding and Strict Modes | One provider guarantees my format and another ignores it, and on one task the strict mode made the answers worse. | How a constraint is enforced during generation; why schema support varies between engines; why very strict formats can harm reasoning on some tasks; testing the format as well as the content | 12 |
| 23 | How a Tool Call Works, and Who Decides | People say the model "called an API". Models generate text, so something here is being skipped. | Describing functions to a model; the model proposing a call with arguments; your code deciding, running and returning; validation belonging in your code; tool descriptions occupying input on every call | 16 |
| 24 | Embeddings, and Choosing One for Your Data | Two sentences that mean the same thing share no words. I don't see how any program could notice that. | What an embedding model produces; vectors and closeness; ranking by similarity; why the best model depends on your language, domain and document length; public benchmark scores as a starting point, not a verdict | 14 |
| 25 | Where Dense Search Fails | My semantic search is clever about meaning and completely useless when I search for a part number. | Names, codes and rare words lost in a vector; why similarity is not relevance; why plausible-looking results cannot be judged by eye; what you can and cannot conclude without relevance judgments | 12 |
| 26 | Lexical, Dense and Hybrid Retrieval | I have two kinds of search that each fail differently, and no way to say which is better. | Lexical retrieval and BM25 with its formula; **bi-encoder against cross-encoder**, named; two-stage reranking; **reciprocal rank fusion** as the standard way to combine rankings; relevance judgments, including graded ones; **recall@k, MRR and nDCG from zero**, with DCG, the log discount and the ideal ranking worked in a table; measuring hybrid against dense on your own data | 28 |
| 27 | Parsing, Chunking and Indexing Your Documents | I pointed the thing at my PDFs and the answers are nonsense, even though the answer is definitely in there. | Parsing as the upstream bottleneck — tables, layouts, scanned pages; inspecting what the parser really produced; splitting into chunks; what chunk boundaries decide; indexing, and what can be retrieved at all | 16 |
| 28 | Assembling the Context: Reranking, Citations, Long Context | I found the right passages. The answer still ignored them, and I can't prove where it came from. | Fetching candidates and reranking them; placing passages with instructions; citations a reader can check; long context versus retrieval, and that neither wins in general; models using long input unevenly | 16 |
| 29 | Searching at Scale | Brute force was fine for a hundred documents. At a million it takes four seconds. | Approximate nearest-neighbour indexes; buying latency with recall; measuring what the approximation cost; in-process indexes versus a service; where the index lives as a deployment decision; **metadata filtering**, and multi-tenant retrieval where a user may see only his own documents | 14 |
| 30 | Error Analysis: Naming the Failure Modes | My application is "sometimes bad". That's all I can say about it, so I don't know what to fix. | Reading actual outputs; writing a short note on each failure; grouping notes into a small set of named failure modes; letting the failure modes choose the metrics instead of measuring what is conventional | 14 |
| 31 | Checks and Judges, and Validating a Judge | I asked a model to score my outputs out of five. The scores look reasonable and mean nothing. | Pass/fail checks per failure mode instead of vague scores; checking with code whatever code can check; reserving model judges for judgment; a judge as a classifier; measuring agreement with your own labels on both passes and failures; position bias | 18 |
| 32 | Evaluating a Grounded Answer | The passages were right and the answer was still wrong. I don't know which half to fix. | Measuring retrieval and generation **separately**, and why only that tells you which stage failed; groundedness and faithfulness; answer relevance; the claim-level check — decompose the answer into claims and test each against the retrieved passages — worked on one example; what a citation must support; **generating an evaluation set from your own documents**, which is where your forty labelled cases come from | 16 |
| 33 | Regression Sets, Criteria Drift and Traces | I fixed one thing and broke another, and I only found out from a user. | Keeping the cases that failed; running them on every change with repeated trials; criteria drift as you see more output; tracing every request — input, retrieval, each model and tool call, output, tokens, time; deciding what content to capture, because traces hold user data | 16 |
| 34 | Agent Patterns, and When an Agent Is Warranted | Everything is called an agent. Mine loops forever and costs a fortune, so I'd like to know when I even need one. | Prompt chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser as fixed paths your code controls; where an agent is warranted; cost and compounding error as the price; starting with the simplest design that works | 16 |
| 35 | Context Engineering | My agent works for three steps and then starts forgetting, repeating itself and going in circles. | Instructions at the right level of detail; only the tools the task needs; retrieving just in time rather than loading up front; compaction — what to summarise, what must never be dropped, when to trigger it, and how to prove nothing was lost, with one before and after; structured notes the agent reads back; sub-agents with their own context; memory outside the context window, treated as untrusted because a model wrote it | 22 |
| 36 | Tool Design, and the Model Context Protocol | I wrapped twelve API endpoints as twelve tools and the agent picks the wrong one every time. | A few purposeful tools instead of one per endpoint; namespaced names; outputs carrying high signal in few tokens; error messages that say what to do next; descriptions written like documentation; improving tools by measuring use; MCP — clients, servers, tools, resources, prompt templates; a specification that changes; tool descriptions as untrusted input | 18 |
| 37 | Multi-Agent Systems | Five agents sounded better than one. It cost six times as much and finished nothing. | Work that splits into independent parts; how multi-agent systems fail — system design, misalignment between agents, weak verification; token multiplication; tightly coupled tasks as the wrong shape; what the evidence actually is, and how strong it is | 10 |
| 38 | Evaluating an Agent | My agent succeeded four times out of five. I don't know whether that is good. | A task, a trial and a grader; grading with code first, then models, then people; checking the final state and reading the transcript; pass@k against pass^k, with the arithmetic worked — 0.95 a step over 20 steps is 0.36; capability suites kept apart from regression suites that must stay near 100% | 14 |
| 39 | Adapting a Model: Prompt, Retrieve or Tune | People keep asking whether I fine-tuned it. I don't know how to answer, or when I should. | Retrieval supplies knowledge, tuning changes behaviour; what it costs to own a tuned model; parameter-efficient fine-tuning and LoRA, with the parameter arithmetic; when *you* would do each stage and what it costs you (chapter 14 owns what the stages do); distillation into smaller models; side effects beyond the target task; releasing only behind an evaluation gate; synthetic data added to real data, never substituted | 22 |

## Part III · Apply — 11 labs, 190 pp

*What to ignore for now:* scale and deployment. Everything here runs on one machine.

Each chapter is the whole lab: `## Step 1: …` onward, with expected results at every step. The
labs build one small system in order, each starting where the last stopped. **The book ships the
data**: about 40 short public-domain documents, 8 queries with graded relevance labels, and one
deliberately awkward PDF with a table and a scanned page, all under `labs/`. Without shipped data
no expected result holds for every reader.

| # | Lab | Opens with | Builds | pp |
|---|---|---|---|---|
| 40 | Lab: Call a Model and Measure It | I've read about tokens, cost and variance. I've never watched any of them happen. | A virtual environment, a pinned client and a key read from the environment; a first call; counting tokens both ways; measuring latency; the same prompt twenty times, and the spread | 20 |
| 41 | Lab: An Evaluation Set, and Two Prompts Compared Properly | I have two prompts and a feeling. I want a number with an interval around it. | Thirty labelled cases on a task with an **exact-match grader**, so no judge is needed yet; both prompts over repeated trials; a bootstrap interval; a verdict you could defend | 18 |
| 42 | Lab: A Schema and One Tool | I want output my code can trust, and one action the model can ask for but not take. | A JSON schema and a validation rate; one tool the model proposes; your code validating and refusing a bad call; a log of every proposal | 16 |
| 43 | Lab: Two Embedding Models, and the Query That Breaks Them | I want to see dense search fail on an exact term with my own eyes. | The shipped corpus embedded twice; brute-force search over each; a dozen queries read by hand; one query where an exact term is lost | 16 |
| 44 | Lab: Hybrid Retrieval With a Reranker, Measured | I want to stop guessing which retrieval is better. | BM25, dense and fused retrieval; a cross-encoder reranker; the shipped graded labels; recall@k and nDCG computed over 8 queries; the measured difference | 22 |
| 45 | Lab: The Pipeline End to End | I want a system that answers questions about my own documents and shows where each answer came from. | Parsing the awkward PDF, chunking, indexing; retrieval and reranking; context assembly with citations; retrieval and generation measured separately; an answer traced to its passages; **cost and latency per request recorded from the trace**, as the baseline Part IV points back to | 22 |
| 46 | Lab: Error Analysis, and a Judge You Can Trust | I have forty real outputs and no idea how to turn them into something I can measure. | A failure taxonomy from real outputs; a pass/fail check per frequent mode; one model judge; agreement with your own labels; a regression set | 18 |
| 47 | Lab: Workflow Against Agent | Everyone has an opinion about agents. I want numbers from my own system. | One step built both ways; success, cost and time over repeated trials; a table and a reading you could defend | 12 |
| 48 | Lab: Context and Tools, Measured | My agent forgets things, and I rewrote a tool description on a hunch. | A structured-notes memory store the agent reads back; compaction applied and measured; one tool's name, description and errors rewritten, and the change measured | 12 |
| 49 | Lab: Measure and Reduce Cost and Latency | I know what the levers are. I have never pulled one and watched the number move. | Time to first token and time per token measured; the prompt reordered so the stable part comes first, and prefix caching measured; a cheap model routed to the easy cases, with quality checked; a cost per request before and after | 16 |
| 50 | Lab: Attack Your Own System | If a document can tell my agent what to do, I'd rather find out myself. | An injected instruction in a retrieved document, a tool output and the memory store from lab 48; what the system does; the three attacks turned into a suite; **one `pytest` command that runs the regression set and the attack suite and prints the counts** | 18 |

> **Note.** Lab 50 attacks the system with what Part II taught (chapter 36: tool descriptions and
> every channel the model reads are untrusted input). Chapter 51 then gives the framework. This
> order is deliberate — meet the failure, then learn the system for it. Do not "fix" it by moving
> the lab after Part IV.

## Part IV · What Next — 7 chapters, 136 pp

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 51 | Security: What Can Go Wrong, and What Limits the Damage | Someone told me a web page could hijack my agent. I'd like to know whether that's true and what I do about it. | Why a model cannot reliably tell instructions from data; the current risk lists for agents and for applications that only generate, in tables; using a list as a checklist, not a certificate; the design rule — never combine untrusted input, sensitive access and external action in one session without approval; every channel the model reads being input; **insecure output handling**, where model output reaches HTML, SQL or a shell; **per-user tool authorisation**, so a tool acts with the caller's rights and not the service's; **sandboxing generated code**; third-party tool servers as supply chain; why filters and guardrails are never the only defence; **secrets and credentials** — where a key lives, why never in the repository, and what a leaked one reaches; attack suites that run on every change | 36 |
| 52 | Speed: What Makes This Slow | My system is correct and nobody will wait for it. | What you measure and which lever you pull (chapter 15 owns why, from the inside): time to first token and time per token in production; what long context, reranking and agent loops add; prompt-prefix caching and ordering your prompt for it; routing and cascades; application-level response caching, which is not the provider's; if you serve models yourself — continuous batching, paged key--value cache, speculative decoding, quantisation; measuring on your own workload | 24 |
| 53 | Cost: What This Costs Me | The bill arrived and I cannot account for it. | Paying for tokens in and out, including reasoning tokens; features that multiply usage — reasoning modes, multi-agent designs, long contexts; budgeting them instead of switching them on; the economics of caching and cascades; cost per request as a product constraint, measured against lab 49's baseline | 20 |
| 54 | Failure: How This Breaks, and How I Diagnose It | It worked last week. Nothing in my code changed. | Attributing a failure with traces; pinned model versions and gated upgrades; a provider's update as a change that must pass your regression suite; versioning prompts, configuration, indexes and models as one artefact; **re-embedding and index migration when the embedding model changes**; provider data retention, and where your customers' text goes; gradual rollout; deciding in advance what triggers a rollback | 26 |
| 55 | A System Designed Aloud | They will give me forty-five minutes and a whiteboard and say "design this". I have never had to say any of it out loud. | One whole system designed from a vague requirement, in the order an interview expects it: what to clarify first; the retrieval choice and why; the evaluation plan before the build; cost per request estimated on the back of an envelope; the failure modes named; what you would measure in week one; what you would not build yet. Reasoning spoken, not diagrammed | 16 |
| 56 | What to Learn Next | I can hold a conversation about all of this now. I want to know what I actually don't know. | Where the theory begins — statistics, representation learning, retrieval and ranking, evaluation science; the standard books by chapter; reading one complete production system end to end; how to keep up without chasing announcements | 8 |
| 57 | What to Skip for Now | Everything claims to be essential. | What an interview does not reach; what to postpone and why; the regress of prerequisites, and where to stop | 6 |

## Appendices — 83 pp

| # | Appendix | Covers | pp |
|---|---|---|---|
| A | Cheat Sheet | The numbers, defaults and formulas worth memorising: token arithmetic, the latency split, the key--value cache size, retrieval metrics, judge agreement, pass^k, the containment rule, the cost levers | 10 |
| B | Interview Bank | 100 questions with model answers, keyed to chapters. Each answer is **150 to 180 words** — what sixty seconds of speech actually holds: the mechanism, the trade-off, and how you would check it | 45 |
| C | Glossary | Every bolded term, one line each, alphabetical. Budgeted for 300+ terms, because `make check` fails the build on any bolded term that is missing | 16 |
| D | Index | Generated from the LaTeX | 12 |

---

## Who owns what

`BOOK-GUIDE.md` §4 says each concept appears exactly once. Eleven concepts are naturally touched by
more than one chapter. Each is **owned** by the chapter below; every other chapter refers to it by
number and does not re-teach it.

| Concept | Owner | Refers to it |
|---|---|---|
| Softmax | 8 (as a formula) | 11, 13 |
| Prefill and decode | 15 | 52 |
| Quantisation | 15 | 52 |
| Supervised fine-tuning, preference optimisation: *what each stage does* | 14 | 39 |
| Fine-tuning: *when you would do it and what it costs you* | 39 | — |
| Sub-agents | 35 | 37 |
| Tool descriptions as untrusted input | 36 | 50, 51 |
| Prompt-prefix caching | 52 | 18, 53 |
| Routing and cascades | 52 | 53 |
| Batching, and why your request runs with others | 15 | 13, 19, 52 |
| Tracing a request | 33 | 45, 54 |
| Citation and attribution | 28 | 32, 33 |

## Writing and delivery order

Writing order **is** reading order. Each part is built and handed over as its own PDF when it is
finished, so reading starts in week one.

| Order | What | Pages | Why here |
|---|---|---|---|
| 1 | Part I, chs 1–7 | 98 | Short, and it makes every later chapter's opening problem make sense |
| 2 | *Inside the Model*, chs 8–17 | 168 | Chapter 11 (attention) is the hardest in the book and is written while the material is freshest |
| 3 | Part II, chs 18–29 | 196 | Calling a model, and retrieval: the half an interview reaches first |
| 4 | Part II, chs 30–39 | 166 | Evaluation, agents, adaptation |
| 5 | Part III, labs 40–46 | 132 | Follow the chapters they rest on |
| 6 | Part III, labs 47–50 | 58 | Need the agent and security material |
| 7 | Part IV, chs 51–57 | 136 | Security, speed, cost, failure, and the system designed aloud |
| 8 | Appendices A–D | 83 | Written from the finished chapters, never from memory |

**Appendix B's question list is written in week one**, from this table of contents — one page, the
questions only. It is then the acceptance test for every chapter as it lands: a chapter is not
finished until its questions can be answered from it. The answers themselves are written from the
finished chapters, so nothing is written from memory and nothing waits for the last week.
