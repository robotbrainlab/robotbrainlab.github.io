# AI Engineer interview prep guide (3 years)

Oct 30, 2026 · @Lakshmi Deepak

## Bottom line

Prepare one production LLM project that you can defend with numbers: eval results, cost, latency and failures. That single asset answers the two things Indian interviews ask most ("explain your project", "explain RAG") and the one thing hiring managers reject for (no measurement).

**Facts (275 coded 2026 postings; India-relevant pool n=208).** Employers most often require Python (80%), agents (62%), hosted LLM APIs (62%), shipped production AI (60%), RAG (57%) and backend APIs (56%). Evals are required in 49%, and in 70% of Indian startup postings they are at least mentioned. Framework names (LangChain 36% required) and MCP (14%) matter much less than the noise suggests.

**Must-know topics, ranked**

1. RAG and retrieval quality
2. Your production project, end to end
3. Python and backend engineering
4. Agents, tool calling and context engineering
5. LLM evaluation and observability
6. LLM fundamentals and prompting
7. Production trade-offs: cost, latency, reliability, guardrails

**Rule of thumb (inference):** frameworks get you past the resume filter; measured results get you the offer.

## What the market asks for

Eight skills are required in 40% or more of India-relevant postings; Python, agents, LLM APIs, production experience, RAG and backend APIs lead, with evals just below half.

&#91;embedded content: 275 coded postings, Oct 2026 · India-relevant pool n=208 (Indian startups, GCCs/services, remote-India); US/EU benchmark n=67\]

**Reading.** The core is the same in every segment: Python, an LLM feature or agent in production, and a backend around it. Communication is also required in 70%, but it is practised, not studied. India postings name tools more often: any cloud is mentioned in 58% of India postings vs 22% of US/EU postings. US/EU postings name practices instead: evals (75%), system design (49%), TypeScript (54%), customer-facing work (61%). Segments differ too: evals are mentioned in 70% of Indian startup postings but only 41% of GCC/services postings, where a cloud is mentioned in 76%.

**Demand vs hype.** Real demand: agents, production experience and evals, which are common in both markets and even more common abroad. Weaker than the noise suggests: MCP (14% required), fine-tuning (21%, concentrated in model-heavy roles), second agent frameworks such as CrewAI or AutoGen (20% mentioned). LangChain is a resume-filter keyword in India (46% mentioned) but rare in US/EU postings (12%), and hiring managers treat a framework list without trade-offs as a red flag ([Nakrani](https://alpeshnakrani.com/blog/ai-engineer-red-flags/)).

## Must-know topics

Each topic shows why it ranks (postings n=208; "accounts" = first-hand interview accounts dated 2025–2026, n=54, of which 24 are India AI-engineer accounts), what to know, what to show, and questions that came up.

### 1. RAG and retrieval quality

**Why:** required in 57%, mentioned in 65% of postings. Asked in 14 of 24 India accounts.

- **Know:** the full pipeline (ingest → chunk → embed → index → retrieve → rerank → generate → cite); chunking strategies (fixed, recursive, semantic, structure-aware); hybrid search (BM25 keyword search + vectors); cosine vs dot product; top-k trade-offs; when not to retrieve; what RAG fixes and does not fix about hallucination.
- **Show:** one vector store (pgvector, Qdrant or FAISS), a reranker, citations, and a chunking comparison on your own data.
- **Questions:** "Explain the full RAG flow." "The answer is fluent but wrong — how do you debug it?" "How do you choose a chunk size, and how do you know it works?"

### 2. Your production project, end to end

**Why:** shipped production AI is required in 60% of postings. A project deep-dive appears in 16 of 24 India accounts. "No deployment experience" is a stated rejection reason.

- **Know:** the problem and user, the architecture, the reason for each choice, the eval method, failures, cost, latency, and what you would change.
- **Show:** a 2-minute and a 10-minute version of the story, with numbers, and a diagram that matches the code.
- **Questions:** "Walk me through your hardest GenAI project." "What broke in production?" "Why no fine-tuning or agent?"

### 3. Python and backend engineering

**Why:** Python is required in 80%, backend APIs in 56%. A coding check appears in 34 of 54 accounts; it is usually practical Python, pandas or SQL. Hard DSA (data structures and algorithms) appears mainly at Amazon-type product firms.

- **Know:** async I/O for LLM calls, batching, retries with backoff, timeouts, idempotency, streaming responses, Pydantic validation, basic SQL, easy-to-medium DSA.
- **Show:** a FastAPI service around an LLM call, with tests, secrets from environment variables, and error handling.
- **Questions:** "Batch these LLM calls under a rate limit." "pandas/SQL: group, join, deduplicate." One easy string or array problem.

### 4. Agents, tool calling and context engineering

**Why:** agents are required in 62% and mentioned in 72% (88% in US/EU postings, n=67). Asked in 8 of 54 accounts.

- **Know:** workflow vs agent, and why to start with the simpler one ([Anthropic](https://www.anthropic.com/research/building-effective-agents)); the tool-call loop; JSON schemas and structured outputs; memory; step and cost caps; human approval for irreversible actions; context engineering — deciding what enters the model's context (compaction, retrieval on demand, sub-agents) ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)); MCP at the concept level.
- **Show:** one agent built on raw API tool calling, then the same agent in LangGraph, so you can explain what the framework hides.
- **Questions:** "LLM vs AI agent — what is the difference?" "Process thousands of items a day without misses or token explosion." "An agent loops forever on some inputs — find out why."

### 5. LLM evaluation and observability

**Why:** required in 49%, mentioned in 56%; mentioned in 70% of Indian startup postings and 75% of US/EU postings. Few candidates report eval questions (5 of 54), but every hiring-side source ranks evals as the top differentiator. **Upgraded by judgement.**

- **Know:** a frozen, labelled test set; binary pass/fail checks instead of 1–5 scores; error analysis on real traces ([Husain](https://hamel.dev/blog/posts/evals-faq/)); retrieval metrics (recall@k, MRR); faithfulness; LLM-as-judge calibrated against human labels; regression gates in CI; BLEU/ROUGE and their limits.
- **Show:** an eval harness with 50+ cases, a pass rate, a threshold that can block a deploy, and traces in Langfuse or LangSmith.
- **Questions:** "How would you know it works?" "How do you evaluate retrieval separately from generation?"

### 6. LLM fundamentals and prompting

**Why:** LLM APIs are required in 62%, prompt or context engineering in 46%. Theory (transformers, LLM basics) is asked in 14 of 54 accounts, even though postings rarely list it.

- **Know:** tokens and tokenization; context windows; self-attention at whiteboard level; BERT vs GPT; temperature, top-p, top-k; embeddings; KV cache and quantization as concepts; prompting vs RAG vs fine-tuning.
- **Show:** prompts under version control with tests; a model choice backed by eval results.
- **Questions:** "Explain the transformer." "What does temperature do?" "When would you fine-tune instead of using RAG?"

### 7. Production trade-offs: cost, latency, reliability, guardrails

**Why:** moderate in postings (guardrails 34% required, cost/latency 28%, any cloud 38%), but production and system-design questions appear in 9 and 7 of 54 accounts, and hiring managers screen for cost and failure numbers. **Upgraded by judgement.**

- **Know:** cost per request and per 1,000 requests; p95 latency; exact and semantic caching; model routing; fallbacks when the API fails; rate limits; prompt-injection defence; PII redaction; Docker; deployment on one cloud.
- **Show:** a one-page cost and latency table for your project, and one incident write-up.
- **Questions:** "Cut inference cost by 50% without hurting quality." "The LLM API is down — what is your fallback?"

## Good-to-know topics

Learn these to the stated depth, and go deeper only for the employer type that asks. Percentages are "mentioned" in the India pool (n=208) unless noted.

| Topic | Frequency | When it matters | Depth that is enough |
| --- | --- | --- | --- |
| LangChain / LangGraph | 46% (36% required); GCC/services 57%; US/EU 12% | Services firms and GCCs; their interviews ask about it | Build one graph with tools and state; explain what it abstracts |
| One cloud + managed LLM platform | Any cloud 58%; GCC/services 76% | AWS in banks, Azure OpenAI in services firms | Deploy one service; call Bedrock or Azure OpenAI; IAM and secrets basics |
| Docker, CI/CD, testing | 31% / 39% / 28%; testing 39% in GCCs | GCCs and larger product firms | A Dockerfile and a GitHub Actions pipeline with unit tests and an eval gate |
| MLOps / deployment | 36%; GCC/services 46% | GCCs, platform roles | Prompt and model versioning, rollback, monitoring |
| SQL and data pipelines | 36% / 28% | Data-heavy roles, text-to-SQL agents | Joins and window functions; one ETL job that feeds a RAG index |
| Classical ML and deep-learning basics | 21% / 33%; GCC/services 30% / 45%; asked in 10 of 54 accounts | GCCs, consultancies | Overfitting, bias–variance, precision/recall, random forest, one PyTorch training loop |
| Fine-tuning concepts | 32% (21% required) | Model-heavy, voice and some GCC roles | When to fine-tune; the LoRA/QLoRA idea; data needs |
| Open-source models, self-hosting | 30% | Privacy-bound clients, inference startups | Ollama or vLLM basics; quantization trade-offs |
| MCP (Model Context Protocol) | 19% (14% required) | Agent platforms, model labs | Client/server/tool model; token and security costs; one small server |
| TypeScript | 34%; US/EU 54% | Remote and US/EU product roles | Read and change a Node/React app; call an LLM from TypeScript |
| Voice / multimodal | 23%; Indian startups 32% | Voice-agent startups (BFSI, collections) | Speech-to-text → LLM → text-to-speech pipeline and its latency budget |
| Customer-facing / FDE | 26%; US/EU 61% | Forward-deployed and Applied AI roles | A clear demo, a scoping conversation, written design notes |
| Medium DSA | Asked in 14 of 54 accounts | Product firms, big tech | LeetCode 75 level; hard DSA only for Amazon-type loops |

## Low priority for now

Skip these until the must-know topics are solid. Each is mentioned in about 20% of India postings or less, and none came up as a regular interview theme.

| Topic | Frequency (India pool, n=208) | Why it can wait |
| --- | --- | --- |
| Kubernetes | 20% mentioned, 14% required | Platform and MLOps roles only; Docker covers most AI Engineer roles |
| A second agent framework (CrewAI, AutoGen, ADK) | 20% mentioned | Learn one framework well; the patterns transfer |
| Queues at scale (Celery, Kafka) | 10% mentioned | Know asyncio basics; queue design is platform work |
| Classic NLP (NER, spaCy) | 22% mentioned | Mostly GCC model roles; LLMs now cover most of these tasks |
| Document AI / OCR | 9% mentioned | Niche; keep it as a differentiator if you already have it, but do not study it |
| Pretraining, RLHF/DPO, training at scale | Inside fine-tuning (21% required) | Not asked in any first-hand account; research-team work |
| Vector-index internals (HNSW details) | 0 of 67 accounts | Know that approximate search trades recall for speed; more detail is rarely asked |
| Master's or PhD | 4% mentioned | Not a gate at this level |

Classic NLP is slightly above 20%, but it stays here because nearly all mentions are in model-heavy GCC roles, not LLM-application roles (judgement).

## Recruiter view: strong vs average

A hiring manager expects a 3-year AI Engineer to have owned one LLM system end to end: built it, measured it, deployed it, debugged it in production, costed it, and be able to redesign it for scale (inference from the hiring-side sources below).

| Strong candidate | Average candidate |
| --- | --- |
| Asks "How will we know it works?", then describes a frozen test set and a metric | Says "we tested it" with no method |
| Separates failure causes: retrieval miss, context ignored, stale index | Blames "hallucination" and swaps the model |
| Gives cost per 1,000 requests and p95 latency | Gives no numbers, or "it was fast" |
| Tells one specific production failure and the fix that held | Has only demo or benchmark stories |
| Picks the simplest design and explains why not an agent or fine-tuning | Defaults to multi-agent or fine-tuning |
| Explains what the framework does underneath | Lists LangChain, RAG and vector DBs with no trade-offs |
| Validates structured output, with retries and graceful failure | Assumes the model always returns clean JSON |
| Uses AI coding tools, then explains every line | Cannot explain AI-written code in the take-home |
| Asks about data, latency and cost before choosing a chunk size | Picks a fixed chunk size with no reason |

One interviewer who ran about 80 GenAI interviews reports that about half of candidates defaulted to fixed-size chunks, and about 20% could not define a chunk ([Pandit](https://levelup.gitconnected.com/chunking-strategies-in-rag-systems-insights-from-80-genai-interviews-8ceb4a17701a)). Other sources: [Nakrani](https://alpeshnakrani.com/blog/hire-llm-engineer/), [KORE1](https://www.kore1.com/how-to-hire-ai-engineer-2026/), [Dover](https://www.dover.com/blog/how-to-hire-ai-engineer-startups-2025), [Canva](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews), [LeadDev](https://leaddev.com/ai/why-expect-candidates-ai-hiring-process).

**Self-test before any interview.** Can you state these for your main project without notes?

- [ ] Eval set size and pass rate
- [ ] Top 3 failure modes and how you found them
- [ ] Cost per 1,000 requests and p95 latency
- [ ] One production incident and its fix
- [ ] Why you did not use an agent or fine-tuning

**Likely gaps for a RAG / FastAPI / ETL profile (inference):** formal evals with numbers, guarded tool-calling agents, hands-on cloud deployment, and transformer theory plus easy DSA for the coding filter.

## Projects to build and show

Build one deep project, not several similar demos. A "chat with PDF" demo convinces only when it shows a named user, an eval set, failure cases and costs ([DataTalks.Club](https://datatalksclub.github.io/podwiki/wiki/ai-engineering-portfolio-projects/)).

**Project 1 — Domain RAG with an eval harness** (covers must-know topics 1, 5 and 7). Use public documents, such as court opinions or SEC filings. Never use employer data.

- A labelled set of 50–100 questions; recall@5 and MRR for retrieval; faithfulness for answers
- A table that compares 3 chunking strategies, plus hybrid search and reranking on and off
- Citations in every answer, traces in Langfuse, and an eval gate in CI
- Cost per 1,000 queries, p95 latency, and a failure-analysis write-up
- Deployed with FastAPI and Docker on one cloud; a README that states known limits

**Project 2 — Tool-calling workflow agent** (topics 3, 4 and 7), for example ticket triage that drafts a reply and updates a CRM.

- Built first with raw tool calling, then ported to LangGraph; optionally one MCP server
- Structured outputs with schema validation, step and spend caps, human approval before any write
- A task-success eval on 30+ scenarios, plus one replayed failure that you fixed

**Project 3 — Work case study** (inference: production work is stronger evidence than side projects). A 2-page sanitized write-up of your best production system: problem, architecture, eval numbers, cost, incidents, lessons. Use it in every project deep-dive.

**Do not build:** several near-identical RAG demos, LLM wrappers with no evaluation, multi-agent systems for their own sake, or fine-tuning only for show. Reviewers also check repo hygiene: API keys in commit history, invented eval numbers, and diagrams that do not match the code are red flags.

## Interview rounds and question bank

Indian loops are short and talk-based (project + RAG + theory); international loops add a take-home that must include an eval. Evidence: 67 first-hand accounts, 54 dated 2025–2026.

| Loop | Typical rounds | Evidence |
| --- | --- | --- |
| India services firms and GCCs | Online test or light coding → 1–2 technical rounds (project, RAG, LLM theory) → managerial → HR | 24 India accounts: project 16, RAG 14, any coding 14, DSA 7, production 6, transformers 5, agents 5, evals 2, take-home 0 |
| India product firms and startups | A build or system-design round, then a founder round; Amazon-type firms add hard DSA | Few accounts in the sample |
| International (US/EU, remote) | Recruiter screen → take-home (1–5 h, with an eval) → coding, LLM system design, ML basics → product or culture round | Take-home in 3 of 7 US/EU accounts; published loops at [PromptLayer](https://blog.promptlayer.com/the-agentic-system-design-interview-how-to-evaluate-ai-engineers/), [KORE1](https://www.kore1.com/how-to-hire-ai-engineer-2026/), [Dover](https://www.dover.com/blog/how-to-hire-ai-engineer-startups-2025). Some first rounds are AI-run (Mercor) |

Questions are grouped by round and ordered by how often the theme appeared in the 54 recent accounts.

**Project deep-dive (22 of 54)**

1. Walk me through your hardest GenAI project, end to end.
2. How did you measure that it works? Test set size and pass rate?
3. What failed in production, and how did you find and fix it?
4. What does one request cost? What is the p95 latency?
5. Why did you not use fine-tuning or an agent?

**RAG and retrieval (21 of 54)**

6. Explain the full RAG flow.
7. How does RAG reduce hallucination? When does it fail?
8. How do you choose a chunking strategy, and how do you know it works?
9. The answer is fluent but wrong. How do you debug it?
10. How are embeddings created? Cosine vs dot product? How do you choose a vector DB?
11. How do you evaluate retrieval separately from generation?

**Coding (practical 25, DSA 14 of 54)**

12. Batch LLM API calls with a rate limit and retries.
13. Parse and validate model JSON output; handle malformed output.
14. pandas or SQL: group, join and deduplicate.
15. One easy-to-medium DSA problem (string, array, simple DP).

**LLM theory and classical ML (theory 14, classical ML 10 of 54)**

16. Explain self-attention and the transformer. Compare BERT and GPT.
17. What is tokenization? What do temperature, top-p and top-k do?
18. Explain overfitting and random forest. What are BLEU and ROUGE, and their limits?

**Agents, production and system design (production 9, agents 8, design 7 of 54)**

19. What is the difference between an LLM and an AI agent?
20. Run an agentic pipeline over thousands of items a day without misses or token explosion.
21. An agent loops forever on some inputs. Find out why.
22. Design a support-ticket triage agent. Choose a model for each step.
23. Cut inference cost by 50% without hurting quality.
24. The LLM API fails or slows down. Design the fallback and the caching.
25. What is MCP? When would you not use it?

**Managerial / behavioural (21 of 54)**

26. A customer says the bot "feels dumb". What do you do first?

## Preparation plan

Four weeks, one concrete output set per week. Start interviewing from week 2; the project story from week 1 already covers the most-asked round.

**Week 1 — Project story and fundamentals**

- [ ] Write the 2-page work case study with numbers (eval, cost, latency, incidents)
- [ ] Rehearse 2-minute and 10-minute versions aloud
- [ ] Notes on transformers, tokenization and sampling (temperature, top-p, top-k)
- [ ] 15 easy LeetCode problems and 5 pandas/SQL drills

**Week 2 — RAG and evals (Project 1)**

- [ ] Labelled set of 50–100 questions; recall@5, MRR and faithfulness
- [ ] Chunking comparison table; hybrid search and reranking on/off
- [ ] Traces in Langfuse or LangSmith; eval gate in CI
- [ ] Answer questions 6–11 aloud

**Week 3 — Agents and production (Project 2)**

- [ ] Tool-calling agent with schema validation, caps and human approval
- [ ] Docker deployment on one cloud; cost and latency table
- [ ] Answer questions 19–25 aloud

**Week 4 — Mock interviews and segment add-ons**

- [ ] 2 mock system-design rounds and 2 mock project deep-dives
- [ ] One timed 3-hour self-set take-home with an eval
- [ ] Add-on for your target employers: LangGraph + Azure OpenAI or Bedrock (services, GCCs); TypeScript (remote, US/EU); medium DSA (product firms); classical ML basics (GCCs)

## Methodology and limitations

The sample is 275 coded postings from 199 employers, read in October 2026; percentages describe this sample, not the whole market.

| Segment | Postings | ATS pages | Aggregator copies |
| --- | --- | --- | --- |
| Indian startups and product companies | 74 | 13 | 61 |
| Indian GCCs and IT services/consulting | 74 | 25 | 49 |
| Foreign employers hiring remotely from India | 60 | 7 | 53 |
| US/UK/EU benchmark | 67 | 45 | 22 |
| **Total** | **275** | **90** | **185** |

The India-relevant pool is the first three rows: 208 postings from 151 employers. Interview evidence: 67 first-hand accounts (54 dated 2025–2026; 34 from India), mostly Glassdoor and Reddit mirrors. Hiring-side evidence: about 20 employer, recruiter and practitioner sources.

**Inclusion.** AI-application titles (AI, GenAI, LLM, Applied AI, Agentic AI, AI Product, Forward Deployed Engineer; ML Engineer only when the work is mainly LLM). An experience range that includes 3 years, or no years stated with mid-level signals. Posted or live in 2026.

**Coding.** Each full job description was read; none was coded from a search snippet. Each posting was coded on 41 skill columns: 2 = required or a stated duty, 1 = preferred, 0 = not mentioned. A Python script computed every percentage.

**Ranking rule.** Must-know = required in 40% or more of India-pool postings, or consistently tested or stressed in interviews. Good-to-know = mentioned in about 20–40%, or specific to one segment. Low priority = mentioned in under 20% and not tested. Judgement changes: evals and production trade-offs were upgraded (hiring managers stress them); LLM theory was added (interviews test it; postings rarely list it); communication (70% required) is treated as a skill to practise, not a study topic; LangChain stays good-to-know.

**Checks.** No duplicate URLs. One repeated company and title (Wipro "Gen AI Developer") has different URLs, experience and skills, so both were kept. A strict sample that drops 38 borderline rows (237 left; India 181) moves no India percentage by more than 4 points.

**Limitations**

- **Not random.** Rows depend on which pages loaded. LinkedIn, Naukri, AmbitionBox, Instahyre, Indeed India and many ATS boards were blocked; Reddit was read through mirrors. TCS, Cognizant and LTIMindtree have no rows.
- **Concentration.** JPMorgan has 13 rows, Anthropic 9, Deloitte USI 8.
- **Aggregator copies** (185 of 275) can blur required vs preferred. Unlabelled lists were coded as required, which raises "required" shares.
- **One coder per segment**, with no second-coder check.
- **Dates.** 225 rows show a 2026 date; about 17 were closed when read but still showed the full description.
- **Interview counts are lower bounds.** Short reviews omit topics, and Glassdoor rarely states years of experience.
- **Inference, not measurement:** the tiers, the recruiter table, the projects, the gap list, the plan and the question order.

## Sources

Per-posting URLs are kept in the coded dataset (five CSV files); ask if you want it as a spreadsheet.

**Posting sources:** [Wellfound India](https://wellfound.com/role/l/ai-engineer/india), [Weekday](https://jobs.weekday.works), [The Muse](https://www.themuse.com), [Himalayas India](https://himalayas.app/jobs/countries/india/ai-engineer), [Remote Rocketship](https://www.remoterocketship.com/country/india/jobs/llm-engineer), [Jobgether](https://jobgether.com/remote-jobs/india/artificial-intelligence-engineer), [Deloitte USI](https://usijobs.deloitte.com), [Citi](https://jobs.citi.com), [Sarvam](https://www.sarvam.ai/careers), Greenhouse and Ashby job boards, [Built In London](https://builtinlondon.uk), [YC jobs](https://www.ycombinator.com/jobs).

**Interview accounts (most used):** Glassdoor reviews for [Deloitte](https://www.glassdoor.co.uk/Interview/Deloitte-Interview-E2763-RVW104965530.htm), [Capgemini](https://www.glassdoor.sg/Interview/Capgemini-Interview-E3803-RVW99746333.htm), [Infosys](https://static.glassdoor.at/Interview/Infosys-Interview-Questions-E7927_P54.htm), [EPAM](https://www.glassdoor.ca/Interview/EPAM-Systems-Interview-E15544-RVW103965005.htm), [Wipro](https://static.glassdoor.com.br/Interview/Wipro-Interview-E9936-RVW103220419.htm), [PwC](https://static.glassdoor.de/Interview/PwC-Interview-E8450-RVW103066787.htm), [Accenture](https://www.glassdoor.com.ar/Entrevista/Accenture-Entrevista-E4138-RVW97080467.htm), [Scale AI](https://www.glassdoor.sg/Interview/Scale-Interview-E1656849-RVW103984515.htm); [Amazon ADCI (PracHub)](https://prachub.com/interview-experiences/software-engineer-interview-at-adci-karnataka-difficult-dsa-and-genai-49111c2d0a); [LeetCode Discuss](https://leetcode.com/discuss/post/8446005/); Reddit threads via [mirror](https://reddit.sentinel-team.org/posts/1sn7hc8/snapshots/2026-04-17T05%3A37%3A44.74927Z).

**Hiring-side and practitioner sources:** [Nakrani — hiring](https://alpeshnakrani.com/blog/hire-llm-engineer/), [Nakrani — red flags](https://alpeshnakrani.com/blog/ai-engineer-red-flags/), [KORE1](https://www.kore1.com/how-to-hire-ai-engineer-2026/), [Dover](https://www.dover.com/blog/how-to-hire-ai-engineer-startups-2025), [Recruiting From Scratch](https://www.recruitingfromscratch.com/blog/how-to-hire-a-generative-ai-engineer-at-a-startup-2026), [PromptLayer](https://blog.promptlayer.com/the-agentic-system-design-interview-how-to-evaluate-ai-engineers/), [Canva](https://canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews), [LeadDev](https://leaddev.com/ai/why-expect-candidates-ai-hiring-process), [Pandit — 80 interviews](https://levelup.gitconnected.com/chunking-strategies-in-rag-systems-insights-from-80-genai-interviews-8ceb4a17701a), [Hamel Husain — evals FAQ](https://hamel.dev/blog/posts/evals-faq/), [applied-llms.org](https://applied-llms.org/), [Anthropic — building effective agents](https://www.anthropic.com/research/building-effective-agents), [Anthropic — context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Thoughtworks — MCP](https://www.thoughtworks.com/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025), [DataTalks.Club portfolio wiki](https://datatalksclub.github.io/podwiki/wiki/ai-engineering-portfolio-projects/).
