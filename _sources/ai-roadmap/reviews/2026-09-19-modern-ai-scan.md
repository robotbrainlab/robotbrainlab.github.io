<div align="justify">

# 4-Week Modern AI Scan — 2026-09-19

| | |
| --- | --- |
| **Date** | 2026-09-19 (completed) |
| **Period covered** | The first scan. It covers developments since the evidence base of Baseline 2 ([landscape](../research/2026-09-17-data-intelligence-landscape.md), executed 2026-09-17, and [targeted resource research](../research/2026-09-18-targeted-resource-research.md), 2026-09-18), and it re-checks the currency of every practice the learner guide now teaches |
| **Current baseline** | Baseline 2 |
| **Trigger** | Run by explicit command during the final acceptance correction of Modern AI Engineering, before the scheduled date (2026-10-16), as [MAINTENANCE.md §1](../MAINTENANCE.md#1-normal-maintenance-command) permits |
| **Outputs** | This report; the [current-practice register](modern-practice-register.md); current-practice edits to [ROADMAP.md §7](../ROADMAP.md#7-modern-ai-engineering); the state file |

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Method](#1-method)
2. [Findings](#2-findings)
3. [Carried-Forward Watch Items](#3-carried-forward-watch-items)
4. [Changes Made](#4-changes-made)
5. [For the Next 12-Week Review](#5-for-the-next-12-week-review)
6. [Sources](#6-sources)

</details>

---

## 1. Method

**Why this scan.** The learner guide had reduced Modern AI Engineering to application stages that mostly pointed back to the Depth Track. Restoring it as substantive current engineering knowledge requires a recorded status for every practice it teaches. This scan supplies that record. It is a maintenance scan, not a landscape review: the 19-area landscape, the Universal Core, the resource-coverage research and the Depth Track were not re-examined.

**Search directions.** The directions in [MAINTENANCE.md §4](../MAINTENANCE.md#search-directions): model capability shifts; inference and serving; retrieval; agent and tool systems; context management; adaptation; evaluation; security; multimodality; standards and interoperability; engineering patterns and failure reports. An open search for agent, context and evaluation work published in July–September 2026 was run to find developments outside these directions.

**Two passes over the evidence.**

1. **Classification.** Every contemporary practice in the Baseline 2 evidence base that bears on [ROADMAP.md §7](../ROADMAP.md#7-modern-ai-engineering) — the landscape's Contemporary AI Engineering Map (§E), its subfield tables for foundation models, retrieval, compound systems, evaluation, trustworthy AI and operations (§C7, §C12, §C13, §C15–§C17), and the Modern Practice Reference Layer of the targeted research (§O) — was given a status on the [AGENTS.md lifecycle](../AGENTS.md#topic-maturity). The landscape's maturity labels were mapped as follows: *Established* → Established; *Current practice* → Current Practice; *Emerging*, *Experimental* or *Active research* with practical relevance → Watching; newly found and unassessed → Discovered.
2. **Currency check.** For each practice the guide now teaches, primary sources were re-read on 2026-09-19 where a recent change was possible: the tool-interoperability specification, observability conventions, security risk lists, agent-to-agent protocols, and the engineering guides and papers the guide cites.

**Anti-news-feed test.** Candidates were kept only if they change what engineers need to understand or build, system architecture, evaluation, reliability, security, efficiency or professional practice. Model releases, framework launches, funding news and leaderboard movement were excluded.

**Independence limitation.** The scanning agent had read and edited the curriculum in the same session. A 4-week scan requires only lightweight independence ([AGENTS.md — Proportional Independence](../AGENTS.md#proportional-independence)); the limitation is disclosed rather than hidden.

**Excluded.** Vendor announcements without technical evidence; framework and SDK releases; model releases that show no change in engineering practice; self-reported adoption counts used as sole evidence of adoption.

[⬆ Back to Contents](#contents)

---

## 2. Findings

Only meaningful findings are listed. The full status of every practice is in the [register](modern-practice-register.md).

| Finding | Evidence | Status | Why it matters | Action |
| --- | --- | --- | --- | --- |
| The Model Context Protocol's 2026-07-28 specification is current. It made the protocol core stateless, replaced server-initiated requests with multi-round-trip requests, hardened authorization, and deprecated roots, sampling, logging, dynamic client registration and the legacy HTTP+SSE transport. It treats tool descriptions as untrusted unless the server is trusted | S1; landscape E12, E13 | Current Practice | Learners connecting tools need the current specification, and need to expect deprecations | Current Practice; named in the §7 current-practice column; the specification added as a current reference |
| OpenTelemetry's generative-AI conventions are still at Development status and moved to a dedicated repository in June 2026 | S2; landscape E17 | Watching | Tracing is current practice; its standard field names are not stable | Watch. The guide teaches tracing as a practice and does not teach the conventions |
| OWASP publishes a Top 10 for Agentic Applications (2026) alongside its LLM application list; its risks include goal hijack, tool misuse, identity and privilege abuse, agentic supply chain, unexpected code execution, and memory and context poisoning | S3; landscape T21 | Current Practice | The current checklist practitioners threat-model agents against | Current Practice; added as a current reference (already a §14 Reference category) |
| Anthropic's "Writing effective tools for agents" (2025-09-11) was read directly. It recommends a few purposeful tools rather than one per endpoint, namespacing, high-signal outputs, token-efficient responses, helpful error messages and evaluation-driven tool improvement | S4 | Current Practice | Evidence update: the targeted research had verified this guide only indirectly | Evidence update |
| A2A reached a stable v1.0 in March 2026 and joined the Agentic AI Foundation in August 2026. The adoption figures found are self-reported by the project and its promoters | S5; landscape E14 | Watching | A possible second interoperability standard, but independent evidence of engineering adoption is thin | Watch |
| Recent preprints propose scoring context quality as a leading indicator of agent reliability | S6 | Discovered | Could sharpen context-engineering practice; one unreviewed preprint | Record only |
| The production-agent study behind several claims was re-read: 68% of agents execute at most 10 steps before human intervention, 70% rely on prompting off-the-shelf models, 74% depend primarily on human evaluation, and reliability is the top challenge | S7; landscape G16 | — | The guide quotes these figures | Evidence update |
| Re-read of the multi-agent failure taxonomy (MAST): 14 failure modes in three categories — system design, inter-agent misalignment, task verification — from over 1,600 annotated traces across 7 frameworks | S8; landscape E6 | Current Practice | The quantified multi-agent study the guide asks learners to consult | Evidence update |
| No change in the Baseline 2 evidence base was found for workflow patterns, context engineering, agent evaluation vocabulary, prompt caching, routing, serving mechanisms, parameter-efficient adaptation or preference tuning | S9, S10; landscape §E | Unchanged | — | None |

[⬆ Back to Contents](#contents)

---

## 3. Carried-Forward Watch Items

This is the first scan; there were no earlier watch items. The items now being watched are listed with their status in the [register](modern-practice-register.md#2-practices): observability conventions, agent-to-agent protocols, reinforcement learning from verifiable rewards as a service, model-signing tooling, agentic search loops, graph-structured retrieval, contextual chunk enrichment, agent-instruction files and skills formats, computer-use agents, and code execution against tool servers.

[⬆ Back to Contents](#contents)

---

## 4. Changes Made

- **Register created:** [reviews/modern-practice-register.md](modern-practice-register.md). It records status and evidence for 49 practices, the four current references the guide asks learners to consult, and questions for the 12-week review.
- **Current-practice column of [ROADMAP.md §7](../ROADMAP.md#7-modern-ai-engineering)** updated within the limits of [MAINTENANCE.md §4](../MAINTENANCE.md#scan-procedure). No other part of ROADMAP.md changed: not the Depth Track, not any block's capability, depth or prerequisites, not the durable-concept column, not the phases, and not the mandatory resources.

| Row | Before | After |
| --- | --- | --- |
| System architecture | Named agent patterns; quantified multi-agent studies | Named workflow patterns — prompt chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer; bounded autonomy with human intervention; quantified multi-agent studies |
| Context | "Context engineering" conventions; memory-file formats | "Context engineering" conventions — just-in-time retrieval, compaction, structured notes, sub-agents with their own context; memory kept outside the context window; memory-file formats |
| Structured generation | Provider strict modes | Provider strict modes; schema support that varies by engine |
| Tools and interoperability | Specific protocols, primitives and deprecations | Specific protocols, primitives and deprecations — currently the Model Context Protocol (2026-07-28 specification); agent-facing tool design; agent-to-agent protocols watched |
| Evaluation | Evaluation platforms and vendor vocabulary | Error analysis by open and axial coding; judges validated against labelled samples; agent evaluation over repeated trials with pass^k; evaluation platforms and vendor vocabulary |
| Inference and cost | Engine settings; format-specific guidance; provider pricing | Prompt-prefix caching layout; routing and cascades; pinned model versions; engine settings; format-specific guidance; provider pricing |
| Security | Risk lists; specific attacks; guardrail products | Risk lists — the OWASP LLM and agentic lists, MITRE ATLAS; limiting untrusted input, sensitive access and external action in one agent; specific attacks; guardrail products |

- **State file** updated: `last_modern_ai_scan` = 2026-09-19; `next_modern_ai_scan_due` = 2026-10-17 (2026-09-19 + 28 days). The baseline and the curriculum-review dates are unchanged.
- The site was regenerated.

[⬆ Back to Contents](#contents)

---

## 5. For the Next 12-Week Review

Marked *Investigate*; none is acted on here. Details are in [register §4](modern-practice-register.md#4-for-the-next-12-week-review).

- Multimodal model use, which §7 does not include in any phase.
- AI coding assistants and coding agents in an engineer's own work.
- Durable execution for long-running agents, and whether it is AI-specific.
- Whether context-engineering practice has matured enough to deepen F2.
- Whether one interoperability protocol's adoption justifies naming it in the Depth Track.

[⬆ Back to Contents](#contents)

---

## 6. Sources

Accessed 2026-09-19. Tiers follow [AGENTS.md — Research Standards](../AGENTS.md#research-standards): **P** primary (specification, paper, official documentation or first-party report); **S** secondary.

| ID | Source | Date | Tier |
| --- | --- | --- | --- |
| S1 | Model Context Protocol, "The 2026-07-28 Specification" — https://blog.modelcontextprotocol.io/posts/2026-07-28/ ; specification — https://modelcontextprotocol.io/specification/2026-07-28 | 2026-07-28 | P |
| S2 | OpenTelemetry, generative-AI semantic conventions (moved notice) — https://opentelemetry.io/docs/specs/semconv/gen-ai/ ; status summary — https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3ff6 | 2026 | P; S |
| S3 | OWASP GenAI Security Project, "OWASP Top 10 for Agentic Applications for 2026" — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | 2025-12 | P |
| S4 | Anthropic Engineering, "Writing effective tools for agents — with agents" — https://www.anthropic.com/engineering/writing-tools-for-agents | 2025-09-11 | P (vendor) |
| S5 | A2A Protocol, "A New Chapter for A2A: Joining the Agentic AI Foundation" — https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ ; adoption summary — https://agentndx.ai/blog/a2a-protocol-adoption-mid-2026/ | 2026-08-27 | P (project); S |
| S6 | "AI Agents Do Not Fail Alone: The Context Fails First", arXiv 2607.14275 — https://arxiv.org/html/2607.14275v1 | 2026-07 | P (unreviewed) |
| S7 | "Measuring Agents in Production", arXiv 2512.04123 — https://arxiv.org/abs/2512.04123 | 2025-12 (rev. 2026-06) | P |
| S8 | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657 — https://arxiv.org/abs/2503.13657 | 2025 | P |
| S9 | Anthropic Engineering, "Building effective agents" — https://www.anthropic.com/engineering/building-effective-agents ; "Effective context engineering for AI agents" — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ; "Demystifying evals for AI agents" — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2024-12 to 2026-01 | P (vendor) |
| S10 | C. Huyen, *AI Engineering*, chapter summaries — https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md | 2025 | P (book) |

[⬆ Back to Contents](#contents)

</div>
