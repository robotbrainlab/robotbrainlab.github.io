# Modern AI Engineering from Zero — Table of Contents

**Status: draft, awaiting approval.** Nothing is drafted until this is approved.

- **Target:** ~760 numbered pages (~182,000 words), with headroom to ~900 where a chapter earns
  it. No padding to reach a number.
- **Parts:** I · Understand (150 pp) · II · Use (300 pp) · III · Apply (155 pp) ·
  IV · What Next (110 pp) · Appendices (45 pp).
- **Coverage:** all 83 concepts of the nine subject areas, each appearing exactly once.
- Every chapter opens with its problem below, then the question it raises (the writer words the
  question). See `BOOK-GUIDE.md` §3.

---

## Part I · Understand — 10 chapters, 150 pp

*What to ignore for now:* every setting, price and product name; this part is only the shape of
the thing.

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 1 | What a Model Is, and What You Get From It | Everyone talks about "using AI" and I picture training something. I have no idea what you actually get, or how. | A model as a service you send text to and get text back from; what it knows and what it cannot know; you choose the model and what you send, not what it holds; latency as a property you feel; using versus training | 14 |
| 2 | Tokens, and Why They Set the Bill and the Wait | I was billed for "tokens". I don't know what one is, or why my short question cost more than someone else's long one. | Why text becomes tokens; input and output tokens; enough of how tokenisation works to reason about it; tokens as the unit of both cost and latency; counting before sending; why code and non-English text cost more | 16 |
| 3 | Why the Same Prompt Gives Different Answers | I ran the same thing twice and got two different answers. One was wrong. Which one do I believe? | Generation one token at a time; sampling, temperature, top-p; why even the most deterministic settings are not a guarantee; why one good output proves nothing; repeated runs as the unit of evidence | 14 |
| 4 | Thinking Before Answering | Some models "think" first and show me their reasoning. It reads convincingly, costs more, and I can't tell whether it helped. | Spending extra computation before answering; what the extra tokens buy and cost; where it pays and where it does not; why a visible reasoning trace is not a reliable account of how the answer was produced | 12 |
| 5 | The Parts Around the Model | The model is one box. Everything I read draws five more boxes around it and I can't see why any of them are there. | Context: instructions, the request, added material; retrieval; tools; checks; people; the compound system; what each part is for; the same small cast of parts in nearly every product | 18 |
| 6 | Why It Is Assembled This Way | Why not just ask the model? Why does every real system wrap it in so much machinery? | The model does not know your data, cannot act in the world, cannot reliably check itself, and is not accountable; each part answers one of those; what each part costs you in return | 14 |
| 7 | The Agent Loop, and How Much Freedom It Actually Gets | "Agent" sounds like it does the whole job by itself. That can't be how anyone ships this. | The loop: decide, call a tool, read the result, continue; where control flow moves; compounding error; how short real deployed loops are; approval points; why bounded autonomy is the norm | 16 |
| 8 | Where the Work Actually Goes | I assumed the hard part was writing the prompt. People who do this for a living say it isn't. | Choosing what information reaches the model; deciding what it may do; finding out whether the output was any good; controlling what it costs; how much of the real job is evaluation and error analysis | 14 |
| 9 | What Changes Fast, and What Changes Slowly | Half of what I read is already out of date and I can't tell which half. | Lasting principles, current conventions, and details that will date; telling which of the three a claim is; how to read a release announcement; what to memorise and what to look up | 12 |
| 10 | A Map of This Book | There's clearly a lot here. I don't know what order to learn it in, or what I can safely leave until later. | The four parts; the chapters an interview reaches first; the one small system the labs build; what this book deliberately leaves out | 10 |

## Part II · Use — 19 chapters, 300 pp

*What to ignore for now:* serving your own models, and the bill — Part IV takes both.

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 11 | The Prompt as a Specification | I keep rewriting my instructions until something works, and I couldn't tell you what I changed or why it helped. | Instructions, examples, output format and supplied information as four separable parts; changing one thing at a time; why current practice weights what the model receives over how the instruction is worded | 16 |
| 12 | Is the Difference Real? | I changed the prompt and it looks better. I have no idea whether it actually is. | Building an evaluation set; repeated runs; variance from zero; a confidence interval on a score; paired comparison; how many cases and trials are enough; treating every change as an experiment | 18 |
| 13 | Structured Output and Schemas | The model gives me a paragraph when I need a field my code can read. | Asking for a fixed format; JSON schema; validating every response; measuring how often validation fails; what to do with the failures; why a program must never trust prose | 14 |
| 14 | Constrained Decoding and Strict Modes | One provider guarantees my format and another ignores it, and on one task the strict mode made the answers worse. | How a constraint is enforced during generation; why schema support varies between engines; why very strict formats can harm reasoning on some tasks; testing the format as well as the content | 12 |
| 15 | How a Tool Call Works, and Who Decides | People say the model "called an API". Models generate text, so something here is being skipped. | Describing functions to a model; the model proposing a call with arguments; your code deciding, running and returning; validation belonging in your code; tool descriptions occupying input on every call | 16 |
| 16 | Embeddings, and Choosing One for Your Data | Two sentences that mean the same thing share no words. I don't see how any program could notice that. | What an embedding model produces; vectors and closeness; ranking by similarity; why the best model depends on your language, domain and document length; public benchmark scores as a starting point, not a verdict | 14 |
| 17 | Where Dense Search Fails | My semantic search is clever about meaning and completely useless when I search for a part number. | Names, codes and rare words lost in a vector; why similarity is not relevance; why plausible-looking results cannot be judged by eye; what you can and cannot conclude without relevance judgments | 12 |
| 18 | Lexical, Dense and Hybrid Retrieval | I have two kinds of search that each fail differently, and no way to say which is better. | Lexical retrieval and BM25; combining it with dense retrieval; two-stage reranking; relevance judgments; recall@k, MRR and nDCG from zero; measuring hybrid against dense on your own data | 20 |
| 19 | Parsing, Chunking and Indexing Your Documents | I pointed the thing at my PDFs and the answers are nonsense, even though the answer is definitely in there. | Parsing as the upstream bottleneck — tables, layouts, scanned pages; inspecting what the parser really produced; splitting into chunks; what chunk boundaries decide; indexing, and what can be retrieved at all | 16 |
| 20 | Assembling the Context: Reranking, Citations, Long Context | I found the right passages. The answer still ignored them, and I can't prove where it came from. | Fetching candidates and reranking them; placing passages with instructions; citations a reader can check; long context versus retrieval, and that neither wins in general; models using long input unevenly | 16 |
| 21 | Searching at Scale | Brute force was fine for a hundred documents. At a million it takes four seconds. | Approximate nearest-neighbour indexes; buying latency with recall; measuring what the approximation cost; in-process indexes versus a service; where the index lives as a deployment decision | 14 |
| 22 | Error Analysis: Naming the Failure Modes | My application is "sometimes bad". That's all I can say about it, so I don't know what to fix. | Reading actual outputs; writing a short note on each failure; grouping notes into a small set of named failure modes; letting the failure modes choose the metrics instead of measuring what is conventional | 14 |
| 23 | Checks and Judges, and Validating a Judge | I asked a model to score my outputs out of five. The scores look reasonable and mean nothing. | Pass/fail checks per failure mode instead of vague scores; checking with code whatever code can check; reserving model judges for judgment; a judge as a classifier; measuring agreement with your own labels on both passes and failures; position bias | 18 |
| 24 | Regression Sets, Criteria Drift and Traces | I fixed one thing and broke another, and I only found out from a user. | Keeping the cases that failed; running them on every change with repeated trials; criteria drift as you see more output; tracing every request — input, retrieval, each model and tool call, output, tokens, time; deciding what content to capture, because traces hold user data | 16 |
| 25 | Agent Patterns, and When an Agent Is Warranted | Everything is called an agent. Mine loops forever and costs a fortune, so I'd like to know when I even need one. | Prompt chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser as fixed paths your code controls; where an agent is warranted; cost and compounding error as the price; starting with the simplest design that works | 16 |
| 26 | Context Engineering | My agent works for three steps and then starts forgetting, repeating itself and going in circles. | Instructions at the right level of detail; only the tools the task needs; retrieving just in time rather than loading up front; compaction; structured notes the agent reads back; sub-agents with their own context; memory outside the context window, treated as untrusted because a model wrote it | 18 |
| 27 | Tool Design, and the Model Context Protocol | I wrapped twelve API endpoints as twelve tools and the agent picks the wrong one every time. | A few purposeful tools instead of one per endpoint; namespaced names; outputs carrying high signal in few tokens; error messages that say what to do next; descriptions written like documentation; improving tools by measuring use; MCP — clients, servers, tools, resources, prompt templates; a specification that changes; tool descriptions as untrusted input | 18 |
| 28 | Multi-Agent Systems, and Evaluating an Agent | Five agents sounded better than one. It cost six times as much and finished nothing. | Work that splits into independent parts; how multi-agent systems fail — system design, misalignment, weak verification; token multiplication; tasks, trials and graders; checking the outcome and reading the transcript; pass@k and pass^k; capability suites apart from regression suites | 18 |
| 29 | Adapting a Model: Prompt, Retrieve or Tune | People keep asking whether I fine-tuned it. I don't know how to answer, or when I should. | Retrieval supplies knowledge, tuning changes behaviour; what it costs to own a tuned model; parameter-efficient fine-tuning and LoRA; supervised fine-tuning then preference optimisation; distillation into smaller models; side effects beyond the target task; releasing only behind an evaluation gate; synthetic data added to real data, never substituted | 22 |

## Part III · Apply — 9 labs, 155 pp

*What to ignore for now:* scale and deployment. Everything here runs on one machine.

Each chapter is the whole lab: `## Step 1: …` onward, with expected results at every step. The
labs build one small system in order, each starting from the last.

| # | Lab | Opens with | Builds | pp |
|---|---|---|---|---|
| 30 | Lab: Call a Model and Measure It | I've read about tokens, cost and variance. I've never watched any of them happen. | A first call; counting tokens both ways; measuring latency; running the same prompt twenty times and looking at the spread | 16 |
| 31 | Lab: An Evaluation Set, and Two Prompts Compared Properly | I have two prompts and a feeling. I want a number with an interval around it. | Thirty labelled cases; both prompts over repeated trials; a score with a confidence interval; a verdict you could defend | 18 |
| 32 | Lab: A Schema and One Tool | I want output my code can trust, and one action the model can ask for but not take. | A JSON schema and a validation rate; one tool the model proposes; your code validating and refusing a bad call; a log of every proposal | 16 |
| 33 | Lab: Two Embedding Models, and the Query That Breaks Them | I want to see dense search fail on an exact term with my own eyes. | Embedding a small collection twice; brute-force similarity search over each; a dozen queries read by hand; one query where an exact term is lost | 16 |
| 34 | Lab: Hybrid Retrieval With a Reranker, Measured | I want to stop guessing which retrieval is better. | Lexical, dense and hybrid retrieval; a reranker; relevance judgments; recall@k and nDCG; the measured difference | 18 |
| 35 | Lab: The Pipeline End to End | I want a system that answers questions about my own documents and shows where each answer came from. | Parsing, chunking, indexing; retrieval and reranking; context assembly with citations; retrieval and generation evaluated separately; an answer traced to its passages | 20 |
| 36 | Lab: Error Analysis, and a Judge You Can Trust | I have forty real outputs and no idea how to turn them into something I can measure. | A failure taxonomy from real outputs; a pass/fail check per frequent mode; one model judge; agreement with your own labels; a regression set | 18 |
| 37 | Lab: The Same Step as a Workflow and as an Agent | Everyone has an opinion about agents. I want numbers from my own system. | One step built both ways; success, cost and time over repeated trials; one context practice applied and measured; a tool description rewritten and re-measured | 18 |
| 38 | Lab: Attack Your Own System | If a document can tell my agent what to do, I'd rather find out myself. | An injected instruction in a retrieved document, a tool output and a stored memory; what the system does; the three attacks turned into a suite that runs on every change | 15 |

## Part IV · What Next — 6 chapters, 110 pp

| # | Chapter | Opens with | Covers | pp |
|---|---|---|---|---|
| 39 | Security: What Can Go Wrong, and What Limits the Damage | Someone told me a web page could hijack my agent. I'd like to know whether that's true and what I do about it. | Why a model cannot reliably tell instructions from data; the current risk lists for agents and for applications that only generate; using a list as a checklist, not a certificate; the design rule — never combine untrusted input, sensitive access and external action in one session without approval; every channel the model reads being input, including retrieved documents, tool descriptions, tool outputs and stored memory; third-party tool servers as supply chain; why filters and guardrails are never the only defence; attack suites that run on every change | 28 |
| 40 | Speed: What Makes This Slow | My system is correct and nobody will wait for it. | Time to first token and time per token; prefill and decode; what long context and reranking cost; agent loops as latency multipliers; prompt-prefix caching and ordering your prompt for it; routing and cascades; if you serve models yourself — continuous batching, paged key–value cache, speculative decoding, quantisation; measuring on your own workload | 24 |
| 41 | Cost: What This Costs Me | The bill arrived and I cannot account for it. | Paying for tokens in and out, including reasoning tokens; features that multiply usage — reasoning modes, multi-agent designs, long contexts; budgeting them instead of switching them on; the economics of caching and cascades; cost per request as a product constraint | 20 |
| 42 | Failure: How This Breaks, and How I Diagnose It | It worked last week. Nothing in my code changed. | Attributing a failure with traces; pinned model versions and gated upgrades; a provider's update as a change that must pass your regression suite; versioning prompts, configuration, indexes and models as one artefact; gradual rollout; deciding in advance what triggers a rollback | 24 |
| 43 | What to Learn Next | I can hold a conversation about all of this now. I want to know what I actually don't know. | Where the theory begins — statistics, representation learning, retrieval and ranking, evaluation science; the three standard books by chapter; reading one complete production system end to end; how to keep up without chasing announcements | 8 |
| 44 | What to Skip for Now | Everything claims to be essential. | What an interview does not reach; what to postpone and why; the regress of prerequisites, and where to stop | 6 |

## Appendices — 45 pp

| # | Appendix | Covers | pp |
|---|---|---|---|
| A | Cheat Sheet | The numbers, defaults and formulas worth memorising: token arithmetic, latency split, retrieval metrics, judge agreement, the containment rule, the cost levers | 10 |
| B | Interview Bank | ~100 questions with model answers, keyed to chapters. Each answer is what to say in sixty seconds: the mechanism, the trade-off, how you would check it | 25 |
| C | Glossary | Every bolded term, one line each, alphabetical | 8 |
| D | Index | | 2 |

---

## Writing and delivery order

| Order | What | Pages | Why first |
|---|---|---|---|
| 1 | Part I | 150 | Nothing else can be read without it |
| 2 | Part II, chs 11–21 | 160 | Models and retrieval: the half an interview reaches first |
| 3 | Part II, chs 22–29 | 140 | Evaluation, agents, adaptation |
| 4 | Part III, labs 30–35 | 104 | Follows the chapters they rest on |
| 5 | Part IV | 110 | Security, speed, cost, failure |
| 6 | Part III, labs 36–38 | 51 | Need Part IV's material |
| 7 | Appendices A–C | 43 | Written from the finished chapters, never from memory |
