<div align="justify">

# Modern AI Engineering — Current-Practice Register

| | |
| --- | --- |
| **Role** | Maintenance record: the status of every contemporary practice considered for Modern AI Engineering, and what the learner guide may teach |
| **Last updated** | 2026-09-19, by the [4-week Modern AI Scan of 2026-09-19](2026-09-19-modern-ai-scan.md) |
| **Governed by** | [AGENTS.md — Topic Maturity](../AGENTS.md#topic-maturity) and [MAINTENANCE.md — 4-Week Modern AI Scan](../MAINTENANCE.md#4-4-week-modern-ai-scan) |
| **Curriculum** | [ROADMAP.md §7](../ROADMAP.md#7-modern-ai-engineering) defines the track; this register records the current state of its practices |

This register is how the project decides which contemporary practices are taught in [Modern AI Engineering](../LEARNING-GUIDE.md#modern-ai-engineering). It records evidence and status. It does not change the permanent curriculum.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [How to Read This Register](#1-how-to-read-this-register)
2. [Practices](#2-practices)
3. [Current References](#3-current-references)
4. [For the Next 12-Week Review](#4-for-the-next-12-week-review)

</details>

---

## 1. How to Read This Register

**Status** uses the lifecycle in [AGENTS.md](../AGENTS.md#topic-maturity): `Discovered` · `Watching` · `Current Practice` · `Established` · `Superseded` · `Declined` · `Archived`. Status describes evidence and adoption, not difficulty.

**Taught in** names the Modern AI Engineering topic that teaches the practice. Only `Current Practice` and `Established` practices may be taught. `Watching` and `Discovered` practices are recorded here and are not taught; `—` means the practice is not taught. The site build enforces both rules.

**Evidence** names source IDs in the linked reports. Evidence and adoption are separate signals ([AGENTS.md — Evidence Versus Adoption](../AGENTS.md#evidence-versus-adoption)); a vendor source alone is not treated as proof of adoption.

> ⚠️ Nothing in this register enters the Depth Track automatically.
>
> A practice that looks ready for permanent curriculum is listed in [4](#4-for-the-next-12-week-review) and decided through the [Curriculum Change Rule](../AGENTS.md#curriculum-change-rule).

[⬆ Back to Contents](#contents)

---

## 2. Practices

| ID | Practice | Capability | Status | Evidence | Taught in |
| --- | --- | --- | --- | --- | --- |
| MP-01 | Contemporary AI systems combine models with retrieval, tools, checks and people; in production, autonomy is usually bounded by human intervention | System architecture | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) G16, E1 | Orientation: Contemporary AI Systems |
| MP-02 | Using pretrained models through provider interfaces, with cost and latency counted in tokens | Model use | Established | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) G14, G16 | Working with Models |
| MP-03 | Prompting as an empirical activity: prompts treated as tested specifications, with relatively more effort on the context and tools a model receives than on phrasing | Model use | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E2, G14, G16 | Working with Models |
| MP-04 | Reasoning models that spend extra inference computation before answering; whether it pays depends on problem difficulty | Model use | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D30, D31, G12 | Working with Models |
| MP-05 | Structured output through schema-constrained decoding and provider strict modes; schema support varies, and strict formats can harm reasoning | Structured generation | Established | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E7 | Working with Models |
| MP-06 | Function-style tool calling: the model proposes a call, application code decides and executes it | Tools | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E1, E4 | Working with Models |
| MP-07 | Embedding models, often built on language-model backbones, and semantic search over them | Retrieval | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D15, X7 | Embeddings and Semantic Search |
| MP-08 | Hybrid lexical and dense retrieval with reranking as the default for retrieval-augmented systems; naive top-k dense retrieval declining as a default | Retrieval | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E8, X7 | Retrieval-Augmented Systems |
| MP-09 | Choosing between long context and retrieval by measurement; neither wins in general | Retrieval | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E9, D11 | Retrieval-Augmented Systems |
| MP-10 | Document parsing quality treated as an upstream bottleneck for retrieval | Retrieval | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E32 | Retrieval-Augmented Systems |
| MP-11 | Error analysis by open and axial coding into a failure taxonomy, with pass/fail checks per failure mode | Evaluation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E15, G16 · [Targeted research](../research/2026-09-18-targeted-resource-research.md) V10 | Evaluating and Observing AI Applications |
| MP-12 | Model-based judges validated against human labels before use; consistency does not imply validity | Evaluation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T4, E16 · [Targeted research](../research/2026-09-18-targeted-resource-research.md) V9, V10, V15 | Evaluating and Observing AI Applications |
| MP-13 | Regression sets of past failures, run with repeated trials on every change | Evaluation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E15 | Evaluating and Observing AI Applications |
| MP-14 | Per-request tracing of model, retrieval and tool calls, with deliberate capture of user content | Observability | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E17 | Evaluating and Observing AI Applications |
| MP-15 | OpenTelemetry semantic conventions for generative AI | Observability | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E17 · [Scan](2026-09-19-modern-ai-scan.md) S2 | — |
| MP-16 | Workflow patterns — prompt chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer — preferred to agents unless measurement shows autonomy pays | System architecture | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E1, G16 | Agents, Tools and Context |
| MP-17 | Context engineering: just-in-time retrieval, compaction, structured notes and sub-agents with their own context | Context | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E2, D11 | Agents, Tools and Context |
| MP-18 | Agent memory kept outside the context window as notes, summaries and retrievable history | Memory | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E3, E26 | Agents, Tools and Context |
| MP-19 | Agent-facing tool design: few purposeful tools, namespacing, high-signal outputs, helpful errors, tools improved by evaluation | Tools | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E1, E4 · [Scan](2026-09-19-modern-ai-scan.md) S4 | Agents, Tools and Context |
| MP-20 | The Model Context Protocol, specification 2026-07-28 | Interoperability | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E12, E13 · [Scan](2026-09-19-modern-ai-scan.md) S1 | Agents, Tools and Context |
| MP-21 | Agent-to-agent protocols (A2A) | Interoperability | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E14 · [Scan](2026-09-19-modern-ai-scan.md) S5 | — |
| MP-22 | Narrow multi-agent patterns, such as parallel sub-agents with separate context, and the evidence that multiple agents are not a default | System architecture | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E3, E5, E6 | Agents, Tools and Context |
| MP-23 | Agent evaluation with tasks, trials, code, model and human graders, transcripts versus outcomes, pass@k and pass^k, and separate capability and regression suites | Evaluation | Current Practice | [Targeted research](../research/2026-09-18-targeted-resource-research.md) V11 · [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E15 | Agents, Tools and Context |
| MP-24 | Parameter-efficient fine-tuning (LoRA) with current libraries | Adaptation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D35 | Adapting Models in Practice |
| MP-25 | Supervised fine-tuning followed by preference optimization such as DPO | Adaptation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D25, D12 | Adapting Models in Practice |
| MP-26 | Prompting off-the-shelf models first; fine-tuning for narrow, high-volume tasks | Adaptation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) G16, D35 | Adapting Models in Practice |
| MP-27 | Distillation into smaller models | Adaptation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D29 | Adapting Models in Practice |
| MP-28 | Evaluation-gated data flywheels from production traces and feedback; synthetic data accumulated with real data rather than replacing it | Adaptation | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) G14, E18, D38 | Adapting Models in Practice |
| MP-29 | Reinforcement learning from verifiable rewards offered as a fine-tuning service | Adaptation | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D26, D27 | — |
| MP-30 | Limiting any one agent session from combining untrusted input, access to sensitive data or systems, and external action, with human approval where it must | Security | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T16, T17, T21 | Securing AI Systems in Practice |
| MP-31 | OWASP Top 10 lists for LLM and agentic applications, and MITRE ATLAS, as threat-modelling checklists | Security | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T21, T22 · [Scan](2026-09-19-modern-ai-scan.md) S3 | Securing AI Systems in Practice |
| MP-32 | Guardrail and detection products, which adaptive attacks bypass, so they are never the only defence | Security | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T15, T16 | Securing AI Systems in Practice |
| MP-33 | Model-signing and AI supply-chain integrity tooling | Security | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T19 | — |
| MP-34 | Prompt-prefix caching: stable content first, changing content last | Cost | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E24 | Inference, Cost and Production |
| MP-35 | Routing and cascades between models of different cost | Cost | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E25 | Inference, Cost and Production |
| MP-36 | Serving engines with continuous batching and paged KV-cache memory | Inference | Established | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E20 | Inference, Cost and Production |
| MP-37 | Prefill and decode separated onto different machines, for serving at scale | Inference | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E21, E22 | Inference, Cost and Production |
| MP-38 | Speculative decoding and quantization chosen by measurement on the workload | Inference | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E23, E31 | Inference, Cost and Production |
| MP-39 | Pinned model versions, provider model updates gated on the regression suite, and prompts, configuration, indexes and models versioned together | Operations | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E18, E19 | Inference, Cost and Production |
| MP-40 | Durable execution — checkpoint and resume — for long-running agents | Operations | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E3, E26 | — |
| MP-41 | Using multimodal models — images, documents and audio as inputs | Model use | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) D34 | — |
| MP-42 | AI coding assistants and coding agents in an engineer's own work, with mixed measured productivity | Professional practice | Current Practice | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E27, E28 | — |
| MP-43 | Agentic, tool-based search loops in place of vector retrieval | Retrieval | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E10, X7 | — |
| MP-44 | Graph-structured retrieval (GraphRAG) | Retrieval | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) X13 | — |
| MP-45 | Contextual enrichment of chunks before indexing | Retrieval | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E8 | — |
| MP-46 | Repository agent-instruction files and skills formats | Context | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E13 | — |
| MP-47 | Computer-use agents operating graphical interfaces | Agents | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E29 | — |
| MP-48 | Code execution against tool servers to reduce context load | Tools | Watching | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E4 | — |
| MP-49 | Scored context-quality criteria as a leading indicator of agent reliability | Context | Discovered | [Scan](2026-09-19-modern-ai-scan.md) S6 | — |

[⬆ Back to Contents](#contents)

---

## 3. Current References

Contemporary sources a Modern AI Engineering topic asks the learner to **consult**. Each fills a gap no assigned resource covers, and each belongs to a category that [ROADMAP.md §14](../ROADMAP.md#14-resource-map) already lists as not counted as mandatory. They change quickly and are re-checked at every scan.

| Reference | Link | §14 category | Gap it fills | Evidence | Used in |
| --- | --- | --- | --- | --- | --- |
| Model Context Protocol specification, 2026-07-28 | https://modelcontextprotocol.io/specification/2026-07-28 | Modern Practice: interoperability specifications | No assigned resource teaches an interoperability specification ([targeted research §E](../research/2026-09-18-targeted-resource-research.md#e-r3-compound-ai-systems): no book covers standard interfaces; the coverage audit found none in *Hands-On Large Language Models* or *LLM Engineer's Handbook*) | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E12 · [Scan](2026-09-19-modern-ai-scan.md) S1 | Agents, Tools and Context |
| "Why Do Multi-Agent LLM Systems Fail?" (Cemri et al.) | https://arxiv.org/abs/2503.13657 | Modern Practice: quantified multi-agent studies | The assigned guides and papers argue against multi-agent defaults but none catalogues how multi-agent systems fail | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) E6 | Agents, Tools and Context |
| OWASP Top 10 for Agentic Applications | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | Reference: OWASP LLM and Agentic lists | The assigned security sources teach durable principles and attacks; the current risk list that practitioners threat-model against is not assigned | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T21 · [Scan](2026-09-19-modern-ai-scan.md) S3 | Securing AI Systems in Practice |
| OWASP Top 10 for LLM Applications | https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ | Reference: OWASP LLM and Agentic lists | As above, for applications that are not agents | [Landscape](../research/2026-09-17-data-intelligence-landscape.md) T21 | Securing AI Systems in Practice |

[⬆ Back to Contents](#contents)

---

## 4. For the Next 12-Week Review

Practices that may deserve a permanent-curriculum decision. None is promoted by this register.

| Practice | Question for the review |
| --- | --- |
| MP-41 Multimodal model use | [ROADMAP.md §7](../ROADMAP.md#7-modern-ai-engineering) lists no multimodal practice in any phase, although [AGENTS.md](../AGENTS.md#modern-ai-engineering) names multimodal engineering as Modern scope. Should a phase include it? |
| MP-42 AI coding assistants and agents | Is using them well part of a Data & Intelligence engineer's capability, given mixed measured productivity? |
| MP-40 Durable execution | Is checkpoint-and-resume for long-running agents AI-specific enough to teach, or a Computer Science & Engineering concern? |
| MP-17 Context engineering | The concept is taught in the Depth Track (F2). Has the practice stabilized enough that more of it belongs there? |
| MP-20 Model Context Protocol | Does one protocol's adoption justify naming it in the Depth Track, or should F2 keep only the concept of standard interfaces? |

[⬆ Back to Contents](#contents)

</div>
