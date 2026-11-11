<div align="justify">

# Roadmap Comparison: Independent Landscape vs ROADMAP.md

**Comparison date:** 2026-09-17

**Compares:** [2026-09-17-data-intelligence-landscape.md](2026-09-17-data-intelligence-landscape.md) (independent reconstruction) against [ROADMAP.md](../ROADMAP.md) (Baseline v0)

**Status:** Gap-analysis evidence for the later curriculum-design phase. [ROADMAP.md](../ROADMAP.md) was **not modified**. This document makes **no curriculum changes**, assigns no depth levels, and does not recommend adding every discovered topic.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

- [1. Method](#1-method)
- [2. Summary of Findings](#2-summary-of-findings)
- [3. Coverage Matrix](#3-coverage-matrix)
- [4. Clearly Represented Knowledge](#4-clearly-represented-knowledge)
- [5. Partially Represented Knowledge](#5-partially-represented-knowledge)
- [6. Missing Knowledge](#6-missing-knowledge)
- [7. Possible Overemphasis](#7-possible-overemphasis)
- [8. Outdated or Unexamined Assumptions](#8-outdated-or-unexamined-assumptions)
- [9. Missing Dependencies](#9-missing-dependencies)
- [10. Boundary Problems](#10-boundary-problems)
- [11. Roadmap Content Not Reflected in the Landscape](#11-roadmap-content-not-reflected-in-the-landscape)
- [12. Areas Needing Further Research](#12-areas-needing-further-research)
- [13. Open Questions for the Curriculum-Design Phase](#13-open-questions-for-the-curriculum-design-phase)
- [14. Comparison Record](#14-comparison-record)

</details>

---

## 1. Method

1. The independent landscape report was completed first, without reading [ROADMAP.md](../ROADMAP.md) or [README.md](../README.md).
2. [ROADMAP.md](../ROADMAP.md) was then read in full.
3. Each of the landscape's 19 areas (C1–C19) and their significant subfields was checked against every place the roadmap mentions a subject:
   - Fundamentals sections 1–7;
   - Advanced / Mastery / Research descriptions;
   - Modern AI Engineering candidate lists;
   - Dynamic Topics;
   - Current Curriculum Boundary;
   - the Existing Engineering Section.
4. The independent taxonomy was **not** altered to ease comparison.

**Coverage codes**

| Code | Meaning |
| --- | --- |
| **● Explicit** | The roadmap names the subject as a section, stated purpose, or listed topic. |
| **◐ Partial** | The roadmap mentions it only in passing, only as an unapproved candidate, only at one depth description, or only implicitly through a resource title. |
| **○ Absent** | No mention found. |

> ⚠️ Resource titles are not evidence of coverage.
>
> The roadmap itself states that detailed coverage "will be audited rather than assumed from the resource title alone." Where a listed resource is *likely* to cover a subject, this report marks it **◐ (resource-implied, unverified)** rather than ●.

> ⚠️ "Missing" is descriptive, not a recommendation.
>
> Many missing items are specializations, frontier research, or boundary topics. Whether any should enter the curriculum — and at what depth — is a decision for the curriculum-design phase under the promotion criteria in [AGENTS.md](../AGENTS.md).

[⬆ Back to Contents](#contents)

---

## 2. Summary of Findings

1. **The roadmap and the landscape are different kinds of objects.** The roadmap is a resource-organized Baseline v0: Fundamentals is a sequence of books/courses, and Advanced, Mastery and Research are not yet designed. The landscape is a concept-organized field map. Much apparent "absence" reflects the roadmap's early stage, not a deliberate exclusion.
2. **Strong alignment on contemporary engineering.** The roadmap's Modern AI Engineering candidate lists name most of the durable engineering capabilities the landscape found independently: context engineering, retrieval, agentic retrieval, tool use, agent architecture, memory, interoperability protocols, model adaptation, reasoning models, evaluation, observability, AI security, inference techniques. The landscape adds evidence on maturity, durability and contested claims for each.
3. **Strong alignment on research practice.** The roadmap's Research section lists literature review, baselines, ablations, reproducibility and statistical reasoning. These match landscape area C3 closely. The landscape found these methods used broadly in everyday evaluation and engineering, not only in research (C3, C15).
4. **The largest structural gaps sit between "ML & DL" and "LLMs".** Several areas the landscape found to be distinct, and in some cases prerequisite, are not named anywhere:
   - statistics and experimentation (C2);
   - reinforcement learning and decision-making (C8);
   - generative modeling beyond language models (C6);
   - information retrieval as a discipline (C12);
   - data for AI beyond analysis — labeling, quality, provenance, curation, synthetic data (C10);
   - trustworthy AI beyond security — interpretability, robustness, fairness, privacy, alignment (C16).
5. **Evaluation is placed differently.** The roadmap treats evaluation as a Modern AI Engineering candidate and a possible dynamic topic. The landscape found evaluation to be a scientific discipline in its own right, cutting across every model and system area (C15).
6. **The modality coverage is uneven.** Language (two NLP resources plus two LLM resources) and audio are explicit. Vision, time series, tabular, graphs and documents are not named. This is a possible emphasis question, not a proven overemphasis (see **7**).
7. **Classical AI and non-LLM traditions are absent.** Knowledge representation, planning, constraint solving and theorem proving (C9) are unnamed, as are embodied AI (C14) and AI for science (C19). The landscape records the first as increasingly *integrated with* LLM systems. The latter two are mainly specializations.
8. **The boundary framework is consistent with the landscape.** The roadmap's list of boundary areas matches the landscape's boundary map closely: MLOps, LLMOps, distributed training, inference systems, GPU computing, data infrastructure. The landscape supplies evidence for how to split them (see **10**).
9. **Two landscape gaps were exposed by the roadmap.** The roadmap names *programming (Python), SQL querying and exploratory data analysis* as foundations. The landscape did not treat these as knowledge areas: it treated tools as implementations, and it did not research EDA/visualization. This is recorded in **11**.

[⬆ Back to Contents](#contents)

---

## 3. Coverage Matrix

| Landscape area | Roadmap location(s) | Coverage | Notes |
| --- | --- | --- | --- |
| **C1** Mathematical Foundations | Fundamentals §1 Mathematics (purpose names ML, DL, probabilistic reasoning, optimization) | ● Explicit (area) / ◐ (subfields) | Detailed structure explicitly "to be audited"; information theory, autodiff and numerical methods not named |
| **C2** Statistics, Causality and Experimentation | §1 purpose mentions "probabilistic reasoning"; Research lists "statistical reasoning" | ◐ Partial | No explicit statistics, uncertainty/calibration, causal inference, A/B testing, or statistics of evaluation |
| **C3** Empirical Methodology | Research section (baselines, ablations, reproducibility, statistical reasoning, peer review) | ● Explicit (at Research description only) | Validation protocols and leakage not named; landscape shows broad practical use (see **9**) |
| **C4** Statistical and Classical ML | Fundamentals §5 ML & DL via *Hands-On Machine Learning with Scikit-Learn and PyTorch* | ◐ (resource-implied, unverified) | Learning theory, probabilistic/Bayesian ML, tabular-FM developments, AutoML not named |
| **C5** Deep Learning and Representation Learning | §5 (same resource); §7.1 LLM from scratch | ◐ (resource-implied, unverified) | Architectural frontier (MoE, SSM hybrids), self-supervised learning, embeddings not named in Fundamentals (embeddings named in Modern track) |
| **C6** Generative Modeling | §7 LLMs (autoregressive LMs); §7.2 purpose mentions "generation" | ◐ Partial | Diffusion/flow matching, VAEs, GANs, world models absent |
| **C7** Foundation Models | §7.1 and §7.2; Modern track (model adaptation, reasoning models, multimodal applications) | ● Explicit (LLMs) / ◐ (lifecycle) | Pretraining science, scaling laws, post-training (RLHF, DPO, RLVR), distillation, test-time compute, CoT faithfulness, continual learning not named |
| **C8** Sequential Decision-Making and RL | Modern track "planning" | ○ Absent (◐ planning only) | No RL, bandits, off-policy evaluation, multi-agent/game theory |
| **C9** Knowledge, Reasoning and Symbolic AI | Modern track "planning"; Dynamic Topics "reasoning" | ○ Absent (◐ via "reasoning"/"planning" terms) | Knowledge graphs, logic, solvers, theorem proving, neuro-symbolic integration absent |
| **C10** Data for AI | Fundamentals §3 SQL, §4 Data Analysis (cleaning, transformation, exploration) | ◐ Partial | Labeling, data quality/label errors, provenance/licensing, pretraining curation, synthetic data, documentation absent |
| **C11** Modality and Data-Type Specializations | §6 NLP (two resources); §6.3 Audio; Modern track "multimodal applications"; Dynamic Topics "multimodality" | ◐ Partial (language/audio explicit) | Vision, time series, tabular, graphs, documents, geospatial absent by name |
| **C12** Information Retrieval, Ranking and Recommendation | Modern track: embeddings, semantic search, simple RAG, modern retrieval systems, agentic retrieval; Dynamic Topics "retrieval" | ● Explicit (retrieval as engineering) / ○ (IR science, recommender systems) | Lexical retrieval, IR evaluation, ANN indexing, recommender systems not named |
| **C13** Compound AI Systems and Agents | Modern track: model APIs, prompting, structured generation, tool/function calling, agentic workflows, context engineering, agent architecture, agent harnesses, memory, planning, interoperability protocols | ● Explicit (as candidates) | Strong alignment; multi-agent orchestration, verification loops, coding/computer-use agents, durable execution not named |
| **C14** Embodied and Interactive AI | — | ○ Absent | Mainly specialization/research per landscape |
| **C15** Evaluation Science | Modern track "evaluation"; Dynamic Topics "evaluation" | ◐ Partial | Classical validation, construct validity, contamination, statistics of evals, LLM-as-judge validity, human evaluation not named |
| **C16** Trustworthy AI | Modern track "AI security" | ◐ Partial | Interpretability, robustness, fairness, privacy, alignment/safety, provenance absent |
| **C17** AI Engineering, Serving and Operations | Modern track: observability, inference techniques; Boundary list (MLOps, LLMOps, distributed training, inference systems, GPU computing, data infrastructure); Existing Engineering Section (*Designing Machine Learning Systems*, *LLM Engineer's Handbook*) | ◐ Partial (pending reclassification) | Cost/latency engineering, compression, drift monitoring, data flywheels, ML technical debt not named |
| **C18** Human-AI Interaction, Governance and Societal Context | — | ○ Absent | Human oversight, regulation/standards, data rights, environmental accounting, AI-assisted work evidence absent |
| **C19** AI for Science and Domain Applications | — | ○ Absent | Mainly specialization per landscape |

[⬆ Back to Contents](#contents)

---

## 4. Clearly Represented Knowledge

The roadmap names these subjects explicitly, and the landscape independently confirmed them as significant.

| Subject | Roadmap location | Landscape confirmation |
| --- | --- | --- |
| Mathematics for ML (as an area) | Fundamentals §1 | C1: established, broad relevance; all examined textbooks/courses treat it as prerequisite |
| Large language models (construction and use) | Fundamentals §7 | C7: dominant substrate of contemporary AI engineering |
| Natural language processing | Fundamentals §6 | C11: established field; specific elements remain broadly useful (tokenization effects, information extraction trade-offs, MT evaluation) |
| Speech/audio (introductory) | Fundamentals §6.3 | C11: ASR/TTS current practice; role-dependent |
| Research methodology competencies | Research section | C3: established principles, unevenly practiced |
| Context engineering; tool use; structured generation; agent architecture; memory; agentic workflows | Modern AI Engineering candidates | C13: current practice; durable concepts beneath evolving implementations |
| Embeddings, semantic search, RAG, modern and agentic retrieval | Modern AI Engineering candidates | C12/C13: current practice; retrieval quality bounds system quality |
| Interoperability protocols | Modern AI Engineering candidates | C13: MCP current practice (spec evolving), A2A emerging, both under neutral governance |
| Reasoning models; model adaptation; multimodal applications | Modern AI Engineering candidates | C7: current practice with several contested sub-questions |
| Evaluation; observability; AI security; inference techniques | Modern AI Engineering candidates | C15, C17, C16: current practice; security and evaluation have large unresolved research components |
| Dynamic topic examples (retrieval, reasoning, tool use, agents, model adaptation, multimodality, evaluation) | Dynamic Topics | Landscape evidence shows each spans multiple areas and maturity levels (see landscape **D**, **F**) |
| Boundary with Computer Science & Engineering | Current Curriculum Boundary | Landscape **H** reaches a compatible boundary with topic-level placement evidence |

[⬆ Back to Contents](#contents)

---

## 5. Partially Represented Knowledge

| Landscape knowledge | What the roadmap has | What the landscape found that is not visible in the roadmap | Landscape evidence |
| --- | --- | --- | --- |
| Statistics (C2) | "probabilistic reasoning" (math purpose); "statistical reasoning" (Research) | Estimation and uncertainty, calibration, conformal prediction, statistics of evaluation (error bars, paired comparisons, power), inference with ML predictions | C2; `[M19–M22, M30]` |
| Classical ML (C4) | ML & DL via one practical resource | Generalization theory debates; probabilistic/Bayesian ML; tabular learning state (GBDT vs deep vs tabular foundation models); AutoML convergence with agents | C4; `[M8–M15, A7]` |
| Deep learning (C5) | Same resource; LLM-from-scratch book | Architecture lineage and current contested frontier (MoE, efficient attention, SSM/linear-attention hybrids); self-supervised representation learning | C5; `[D6–D10, D13]` |
| Generative modeling (C6) | Autoregressive LLMs; "generation" in §7.2 purpose | Diffusion and flow matching as the dominant non-text generative family; discrete diffusion LMs; world models | C6; `[D16–D20]` |
| Foundation-model lifecycle (C7) | LLM construction/adaptation; reasoning models and model adaptation as candidates | Scaling laws; pretraining data curation and mid-training; post-training stack (SFT → preference optimization → RLVR); distillation; test-time compute; CoT faithfulness; forgetting and emergent misalignment from fine-tuning | C7; `[D21–D38]` |
| Data for AI (C10) | SQL; data analysis (cleaning, exploration, transformation) | Annotation and LLM-assisted labeling; label-error detection; provenance and licensing; pretraining curation; synthetic data risks; dataset documentation | C10; `[A1–A4, T26, T32]` |
| Modalities (C11) | NLP; audio; "multimodal applications" | Vision (detection, segmentation, 3D, video); time series and anomaly detection; tabular; graphs/relational; document understanding | C11; `[X2–X5, X10, E32, M16–M18]` |
| Evaluation (C15) | "evaluation" as candidate and dynamic topic | Evaluation as an explicit scientific discipline (NeurIPS 2026 Evaluations & Datasets track); construct validity; contamination; LLM-as-judge validity; human evaluation; capability/agentic evaluation; production error analysis | C15; `[G8, T1–T5, E15, E16]` |
| Trustworthy AI (C16) | "AI security" | Interpretability (post-hoc, probing, mechanistic); robustness and shift; fairness; privacy (DP, memorization, unlearning); alignment and safety phenomena; provenance/watermarking | C16; `[T6–T33]` |
| Engineering and operations (C17) | Observability; inference techniques; MLOps/LLMOps resources pending reclassification; boundary list | ML technical debt; serving concepts (KV cache, batching, speculative decoding, disaggregation); compression; cost/latency engineering; drift; durable execution; data flywheels | C17; `[E17–E26, E30, E31]` |
| Planning and reasoning (C8/C9) | "planning" (Modern track); "reasoning" (Dynamic Topics) | Classical planning, search, constraint solving and theorem proving as established traditions now combined with LLMs; RL-based reasoning | C8, C9; `[X14–X17]` |
| Research methodology applied in practice (C3) | Research section competencies | Validation protocols and leakage taxonomy; evidence standards for state-of-the-art claims; these recur in everyday evaluation and model selection | C3; `[M23, M30, A3, A5]` |

[⬆ Back to Contents](#contents)

---

## 6. Missing Knowledge

Grouped by the landscape's own relevance labels so that absence is not mistaken for a recommendation.

**6.1 Absent and labeled broadly relevant (Broad) in the landscape**

| Knowledge | Landscape area | Maturity (landscape) | Why the landscape labeled it broad | Evidence |
| --- | --- | --- | --- | --- |
| Online experimentation and A/B testing | C2 | Established | Product and model decisions depend on it | `[M24]` |
| Calibration and uncertainty quantification | C2 | Established / emerging for LLMs | Abstention, risk control, judge reliability | `[M19, M20]` |
| Statistics of evaluation | C2/C15 | Emerging to current practice | Many reported differences are within noise | `[M22, M30]` |
| Validation protocols and data leakage | C3 | Established, growing importance | Leakage across hundreds of papers; contamination of pretraining data | `[M23, M18]` |
| RL concepts underlying post-training (policy gradients, KL-regularized objectives, verifiable rewards) | C7/C8 | Current practice | Reasoning models and preference tuning are built on them | `[D25–D27]` |
| Bandits and off-policy evaluation | C8 | Established / current practice | Personalization, ranking, rollout decisions | `[X18, M26]` |
| Lexical retrieval and IR evaluation | C12 | Established | Retrieval bounds RAG quality; BM25 remains competitive | `[E8, X7, X8]` |
| Hybrid retrieval and reranking | C12 | Current practice | Large measured reductions in retrieval failure | `[E8]` |
| Annotation, label quality and LLM-assisted labeling | C10 | Established / current practice | Label errors change model rankings; LLM annotators need validation | `[A3, A4]` |
| Data provenance, licensing and consent | C10/C18 | Current practice, consolidating | Legal exposure and regulatory obligations | `[T26, T32, T28]` |
| Synthetic data and model collapse debate | C7/C10 | Current practice; debate active | Widely used in training pipelines | `[D38]` |
| Distillation | C7 | Current practice | Principal route to small, cheap models | `[D29]` |
| Test-time compute and CoT faithfulness limits | C7 | Current practice / active research | Changes cost planning; CoT is not a reliable explanation | `[D30, D32]` |
| Fine-tuning side effects (forgetting, emergent misalignment) | C7/C16 | Replicated research finding | Narrow tuning can broadly change behavior | `[D35, D37]` |
| Robustness and distribution shift | C16 | Established problem | Same failure appears across overfitting, drift and benchmark invalidity | `[T14]` |
| Fairness (definitions and impossibility results) | C16 | Theory established | Metric choice is normative and must be documented | `[T25]` |
| Privacy risks (memorization, disclosure) | C16 | Established attack class | Maps to sensitive-information disclosure in security taxonomies | `[T21, T23]` |
| Prompt-injection containment by architecture (data-flow separation, capability limits) | C16 | Emerging best practice | Detection-only defenses judged insufficient | `[T15–T17]` |
| ML technical debt and drift monitoring | C17 | Established | Maps directly onto LLM systems | `[E18, E19]` |
| Cost/latency engineering (caching, routing, token economics) | C17 | Current practice | Directly determines viability of deployed systems | `[E24, E25]` |
| Human-AI interaction design and human oversight | C18 | Established guidelines / current practice | Bounded autonomy with human intervention is the production norm | `[A8, G16]` |
| Regulatory obligations affecting engineering artifacts | C18 | Current (changing) | EU AI Act GPAI/transparency obligations; state frontier AI law | `[T27, T28, T30]` |
| Tokenization effects on cost and multilinguality | C7/C11 | Current practice | Unequal cost and quality across languages | `[D24, X1]` |

**6.2 Absent and labeled role-dependent (Role) in the landscape**

- Probabilistic/Bayesian modeling `[M2, M27]`
- Causal inference beyond A/B testing `[M25, M31]`
- Tabular learning developments `[M10–M14]`
- Time-series forecasting and anomaly detection `[M16–M18, X10]`
- Vision detection/segmentation `[X2]`
- Document understanding `[E32]`
- Recommender systems `[X9]`
- ANN indexing `[E11]`
- Knowledge graphs and GraphRAG conditions `[X12, X13]`
- Classical planning and constraint solving as tools `[X14, X15]`
- Multi-agent orchestration `[E3, E5, E6]`
- Game theory for interacting agents `[X20]`
- Advanced serving architectures `[E21]`
- Distributed training concepts `[E30]`
- Model compression depth `[E31]`
- Risk management standards `[T29, G13]`
- Environmental accounting `[T31]`
- Knowledge editing `[A10]`
- AutoML `[A7]`

**6.3 Absent and labeled specialization or research (Spec/Research) in the landscape**

- Diffusion/flow depth, GANs, world models `[D16–D20]`
- SSM/hybrid architecture design `[D8–D10]`
- Mechanistic interpretability `[T7–T9]`
- Alignment research (scheming, scalable oversight) `[T11–T13]`
- Differential privacy and federated learning depth `[T23, X27]`
- Theorem proving `[X16]`
- Embodied AI and VLAs `[X21]`
- 3D vision `[X3, X4]`
- Full-duplex speech models `[X6]`
- Graph foundation models `[M28]`
- Decision-focused learning `[A6]`
- Survival analysis `[A9]`
- AI for science domains `[X22–X24]`
- TinyML `[X28]`
- Quantum ML (currently low priority) `[A12]`

> ⚠️ These lists are not a to-do list.
>
> They record knowledge the landscape found and the roadmap does not name. Promotion requires the evaluation in [AGENTS.md — Promotion Into the Permanent Curriculum](../AGENTS.md#promotion-into-the-permanent-curriculum).

[⬆ Back to Contents](#contents)

---

## 7. Possible Overemphasis

Evidence is limited because the roadmap's detailed coverage has not yet been audited. The following are **questions raised by the comparison**, not conclusions.

| Roadmap element | Possible issue | Landscape evidence | Confidence |
| --- | --- | --- | --- |
| Two NLP resources (§6.1, §6.2) plus audio (§6.3) in Fundamentals, while no other modality is named | Relative emphasis on language-specific classical NLP compared with vision, time series, tabular and documents | Landscape records standalone pipeline NLP as *narrowed* (inference, not directly measured) while tokenization, extraction trade-offs and MT evaluation remain broadly useful; other modalities are role-dependent and common in industry (C11) | Low — depends on the resources' actual coverage and on how much of their content serves transferable concepts |
| Two LLM resources (§7.1, §7.2) and a long LLM-centered Modern track candidate list, with no RL, IR science, evaluation science, or data-quality section | Possible LLM-centered imbalance relative to the areas LLM systems depend on | Landscape **I** (hidden dependencies) and **J4** (outside current attention) | Medium — the imbalance is structural, but it may resolve once Advanced and the Modern track are designed |
| "Agent harnesses" as a named candidate area | Term appears to be contemporary practitioner vocabulary; durable concept may be better captured as agent runtime/orchestration and context management | Landscape **K** (unsettled terminology), C13 | Low — naming issue rather than content issue |

No evidence was found that any **explicitly named** roadmap subject is obsolete or superseded.

[⬆ Back to Contents](#contents)

---

## 8. Outdated or Unexamined Assumptions

| Assumption visible in the roadmap | What the landscape found | Evidence |
| --- | --- | --- |
| Evaluation is primarily a modern-engineering / dynamic topic | Evaluation is also an established and fast-developing scientific discipline that underpins claims in every area; the field's main venue reframed its track around the science of evaluation in 2026 | `[G8, T1, M22]` |
| Research methodology belongs mainly to the Research stage | Validation, leakage prevention, baselines and statistical reporting are used routinely in engineering practice and model selection | `[M23, M30, E15]` |
| "Machine Learning & Deep Learning" as one bundle, followed directly by NLP and LLMs | The landscape found several distinct areas between them — statistics/experimentation, generative modeling, RL, IR, data for AI — that later LLM and agent knowledge relies on | Landscape **B**, **I** |
| LLMs organized as a subject parallel to NLP | The landscape found foundation models to be a cross-modal lifecycle (pretraining → post-training → reasoning → adaptation) whose science is not specific to language | C7; `[D21–D38, D34]` |
| Data work equals SQL plus data analysis | Data for AI includes labeling, quality, provenance/licensing, curation and synthetic data, with scientific, security and legal consequences | C10; `[A1–A3, T26, T32]` |
| AI security represents the trustworthiness dimension | Security is one of several trustworthy-AI areas; interpretability, robustness, fairness, privacy and alignment have distinct methods and maturity | C16 |
| Retrieval is an LLM-application topic (embeddings, semantic search, RAG) | Retrieval is a mature scientific field (IR) with its own evaluation methodology; lexical retrieval remains competitive | C12; `[X7, X8, E8, E10]` |
| Reasoning and planning appear as modern-LLM topics | Planning, search, constraint solving and theorem proving are established traditions, now integrated with LLMs via generate-and-verify | C8, C9; `[X14–X17]` |

These assumptions are not necessarily wrong for a Baseline v0. They are recorded because the landscape's evidence bears on them.

[⬆ Back to Contents](#contents)

---

## 9. Missing Dependencies

Knowledge the roadmap already names (or lists as candidates) whose prerequisites the landscape found are not introduced anywhere in the roadmap.

| Named roadmap subject | Prerequisite not named in roadmap | Why the dependency exists | Evidence |
| --- | --- | --- | --- |
| Reasoning models; model adaptation (Modern track); LLM adaptation (§7.1) | Reinforcement learning fundamentals (C8) | RLHF, DPO-family and RLVR post-training are RL or RL-derived | `[D25–D27]` |
| Evaluation (Modern track) | Statistics of estimation and experimentation (C2); validation and leakage (C3); IR evaluation (C12) | Evaluations are statistical estimates; retrieval evaluation has its own metrics | `[M22, M23, X8]` |
| Semantic search, simple RAG, modern and agentic retrieval (Modern track) | IR fundamentals: lexical retrieval, hybrid retrieval, reranking, IR metrics (C12) | Retrieval quality bounds system quality | `[E8, X7]` |
| Context engineering (Modern track) | Attention mechanics and long-context limitations (C5, C7) | Explains non-uniform degradation with input length | `[D11]` |
| AI security (Modern track) | Data-flow/capability reasoning; threat modeling; poisoning and supply-chain concepts (C16, boundary with cybersecurity) | Detection-only defenses fail against adaptive attacks | `[T15–T19]` |
| Inference techniques (Modern track) | KV cache, attention variants, MoE, quantization concepts (C5, C17) | Architecture determines memory, latency and cost | `[E20, E21, D6]` |
| Model adaptation (Modern track) | Forgetting, fine-tuning side effects, evaluation design (C7, C15, C16) | Narrow tuning can broadly change behavior | `[D35, D37]` |
| Multimodal applications (Modern track) | Vision and multimodal representation learning (C5, C11) | No vision or representation-learning subject is named | `[D13, D34]` |
| Observability (Modern track) | Monitoring/drift concepts and ML technical debt (C17) | Classical MLOps concepts carry over to LLM systems | `[E18, E19]` |
| Structured generation (Modern track) | Decoding and sampling from probabilistic models (C1, C6) | Constrained decoding operates on token distributions | `[E7]` |
| Research: statistical reasoning, baselines, ablations | Statistics (C2) beyond "probabilistic reasoning" in mathematics | Research methods presuppose inferential statistics | `[M22, M30]` |

> ⚠️ This table identifies prerequisite relationships only.
>
> It does not determine at which depth any prerequisite should be taught.

[⬆ Back to Contents](#contents)

---

## 10. Boundary Problems

| Boundary item | Roadmap position | Landscape evidence | Observation |
| --- | --- | --- | --- |
| MLOps / LLMOps (Existing Engineering Section) | Preserved pending reclassification | Landscape **H**: AI-specific components are ML technical debt, data/model validation, drift, evaluation in production, AI-specific observability concerns (non-determinism, token cost, content privacy); general components are pipeline infrastructure, CI/CD, orchestration | Evidence available for the planned split; no reclassification made here |
| "Software Engineering — Development / Operations" rows | Preserved with no details | Landscape found AI-assisted development evidence and ML technical debt are AI-specific; general development practice is CS&E | Content undefined in roadmap; cannot be compared in detail |
| Inference systems / GPU computing | Boundary list | Landscape **H**: serving *concepts* (KV cache, batching, speculative decoding, disaggregation, quantization) belong to D&I; engine internals and kernel implementation belong to CS&E/ML systems | Compatible with roadmap's "may appear in both roadmaps at different depths" |
| Distributed training | Boundary list | Landscape **H**: parallelism strategies and memory trade-offs as they shape model and cost decisions belong to D&I; distributed-systems theory and collective-communication implementation to CS&E | Compatible |
| Data infrastructure; database systems (CS&E list) vs SQL (Fundamentals) | SQL in D&I Fundamentals; database systems in CS&E | Landscape treats data validation, lineage, leakage-safe splits and curation logic as D&I; storage and pipeline infrastructure as CS&E; vector database implementation as CS&E beyond ANN algorithms | Consistent; vector search and ANN indexing not placed in either roadmap |
| Security | "AI security" in Modern track; no general security in CS&E list | Landscape **H**: AI-specific attacks in D&I; identity, least privilege, supply-chain security and classical threat modeling are general security | CS&E list does not name security; boundary owner for general security is unassigned |
| Interoperability protocols | Modern track | Landscape **H**: tool/context semantics in D&I; transport, OAuth, gateways in CS&E | Compatible |
| Governance, law, HCI, economics, OR, robotics, domain sciences | Not addressed | Landscape **H** places each as boundary, specialization, or outside with obligation-awareness exceptions | Roadmap boundary section covers only CS&E, not other neighboring disciplines |
| Python programming | Fundamentals §2 | Landscape did not treat programming languages as knowledge areas (tools as implementations); general software engineering is on the roadmap's CS&E list | Possible overlap between §2 Python and CS&E "general software engineering"; roadmap justifies Python by purpose (data analysis, ML, experimentation) |

[⬆ Back to Contents](#contents)

---

## 11. Roadmap Content Not Reflected in the Landscape

The comparison also tests the landscape. The following roadmap content has no corresponding landscape area or subfield.

| Roadmap content | Why the landscape lacks it | Assessment |
| --- | --- | --- |
| Python programming (§2) | The landscape recorded languages and frameworks as implementations, following the research prompt | **Landscape limitation.** Practical programming for data and ML work is a real capability dependency; the landscape does not record it explicitly. |
| SQL / relational querying (§3) | Treated implicitly as data-engineering boundary | **Landscape limitation.** Querying and manipulating relational data is not named in C10. |
| Exploratory data analysis, data cleaning and transformation (§4) | Only "feature engineering and preprocessing" and "data quality" are recorded in C10; EDA and data visualization were not researched | **Landscape gap.** Exploratory analysis and visualization are not represented as knowledge in the landscape and were not audited. |
| Projects as validation of knowledge (§2.2; AGENTS.md Projects) | Out of scope of a field map | Not a gap in the landscape; a curriculum concern. |
| Review cycles and dynamic-topic governance | Out of scope of a field map | Not a gap. |

[⬆ Back to Contents](#contents)

---

## 12. Areas Needing Further Research

**Needed before curriculum decisions can use this comparison fully**

1. **Resource coverage audit.** The Fundamentals resources' actual tables of contents should be mapped against landscape subfields. Most ◐ ratings in **3** are resource-implied and unverified:
   - *Hands-On Machine Learning with Scikit-Learn and PyTorch*
   - *Speech and Language Processing*
   - *Natural Language Processing in Action*
   - *Hugging Face Audio Course*
   - *Build a Large Language Model (From Scratch)*
   - *Hands-On Large Language Models*
   - *Designing Machine Learning Systems*
   - *LLM Engineer's Handbook*
2. **Mathematics detail.** The roadmap's mathematics structure is "to be audited". A comparison against C1 subfields and the statistics content in C2 is not yet possible.
3. **Exploratory data analysis and visualization.** Not researched in the landscape (see **11**).
4. **Practical programming and tooling for ML work.** Not represented in the landscape; boundary with CS&E needs its own evidence.

**Landscape evidence gaps carried forward** (from the landscape's Research Record):

5. Kernel methods, clustering and dimensionality reduction: current usage evidence.
6. Off-policy evaluation: recent work.
7. Independent production evidence on routing, quantization accuracy trade-offs and feature-store adoption.
8. Robotics data scarcity and VLA generalization.
9. The exact ordering of the OWASP GenAI LLM Top 10 2026 items.

**Contested areas that should be re-checked before any promotion decision** (landscape **F**):

10. RL capability expansion.
11. Hybrid/linear attention.
12. LLM-as-judge validity.
13. Tabular and time-series foundation models.
14. Multi-agent systems value.
15. AI coding productivity.

[⬆ Back to Contents](#contents)

---

## 13. Open Questions for the Curriculum-Design Phase

These questions are handed forward as evidence-backed decision points. They are phrased as questions deliberately; this comparison does not answer them.

1. Should statistics and experimentation (C2) be represented separately from mathematics, given their direct use in evaluation and product decisions?
2. Where should reinforcement-learning concepts sit relative to the LLM, reasoning-model and model-adaptation material that depends on them?
3. Should information retrieval be represented as a discipline, or only through retrieval-augmented system topics?
4. How should evaluation be split between durable evaluation science and evolving engineering practice?
5. Which parts of data for AI (labeling, quality, provenance, curation, synthetic data) are dependency-critical, and which are specialization?
6. Which trustworthy-AI areas beyond security meet the promotion criteria, and which should remain awareness-level or specialization?
7. Should the language-centered modality coverage be complemented by vision, time series, tabular or document data, and on what evidence of career relevance?
8. How should classical AI traditions (planning, constraint solving, knowledge graphs) be represented, given evidence that they are being integrated with LLM systems rather than replaced?
9. Which landscape areas marked Spec/Research (C14, C19, frontier rows in **F**) are candidates for Mastery specialization options versus watchlist only?
10. How should the Existing Engineering Section be divided, using the boundary evidence in **10**?
11. Should the landscape itself be extended to cover programming, querying and exploratory data analysis before curriculum design, given **11**?

[⬆ Back to Contents](#contents)

---

## 14. Comparison Record

| Item | Value |
| --- | --- |
| Date | 2026-09-17 |
| Landscape report | [2026-09-17-data-intelligence-landscape.md](2026-09-17-data-intelligence-landscape.md) |
| Roadmap version compared | [ROADMAP.md](../ROADMAP.md) — "Baseline v0" |
| Order of work | Landscape completed before ROADMAP.md was read; independent taxonomy not altered afterwards |
| Files modified outside `research/` | None |
| Curriculum changes made | None |
| Citation convention | Bracketed IDs refer to the source register in the landscape report, section **L** |

[⬆ Back to Contents](#contents)

</div>
