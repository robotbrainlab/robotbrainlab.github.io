<div align="justify">

# Data & Intelligence Landscape: Independent Baseline Reconstruction

**Research execution date:** 2026-09-17

**Report type:** Independent landscape reconstruction (first baseline), produced under [prompts/landscape-research.md](../prompts/landscape-research.md)

**Status:** Research evidence only. This report does not design, sequence, or modify the curriculum and assigns no Fundamentals / Advanced / Mastery / Research levels.

**Anti-anchoring statement:** [ROADMAP.md](../ROADMAP.md) was **not read** before this report was completed, and [README.md](../README.md) was not read at any point. The taxonomy below was derived from external sources only. The comparison with the existing roadmap is a separate document: [2026-09-17-roadmap-comparison.md](2026-09-17-roadmap-comparison.md).

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

**Orientation**

- [About This Report](#about-this-report)
- [A. Executive Summary](#a-executive-summary)
- [B. Master Landscape](#b-master-landscape)
  - [Strata and Areas](#strata-and-areas)
  - [Why the Taxonomy Took This Form](#why-the-taxonomy-took-this-form)

**Detailed Knowledge Map**

- [C. Detailed Knowledge Map](#c-detailed-knowledge-map)
  - [Legend](#legend)
  - [C1. Mathematical Foundations](#c1-mathematical-foundations)
  - [C2. Statistics, Causality and Experimentation](#c2-statistics-causality-and-experimentation)
  - [C3. Empirical Methodology of AI Research and Practice](#c3-empirical-methodology-of-ai-research-and-practice)
  - [C4. Statistical and Classical Machine Learning](#c4-statistical-and-classical-machine-learning)
  - [C5. Deep Learning and Representation Learning](#c5-deep-learning-and-representation-learning)
  - [C6. Generative Modeling](#c6-generative-modeling)
  - [C7. Foundation Models](#c7-foundation-models)
  - [C8. Sequential Decision-Making and Reinforcement Learning](#c8-sequential-decision-making-and-reinforcement-learning)
  - [C9. Knowledge, Reasoning and Symbolic AI](#c9-knowledge-reasoning-and-symbolic-ai)
  - [C10. Data for AI](#c10-data-for-ai)
  - [C11. Modality and Data-Type Specializations](#c11-modality-and-data-type-specializations)
  - [C12. Information Retrieval, Ranking and Recommendation](#c12-information-retrieval-ranking-and-recommendation)
  - [C13. Compound AI Systems and Agents](#c13-compound-ai-systems-and-agents)
  - [C14. Embodied and Interactive AI](#c14-embodied-and-interactive-ai)
  - [C15. Evaluation Science](#c15-evaluation-science)
  - [C16. Trustworthy AI](#c16-trustworthy-ai)
  - [C17. AI Engineering, Serving and Operations](#c17-ai-engineering-serving-and-operations)
  - [C18. Human-AI Interaction, Governance and Societal Context](#c18-human-ai-interaction-governance-and-societal-context)
  - [C19. AI for Science and Domain Applications](#c19-ai-for-science-and-domain-applications)

**Maps**

- [D. Cross-Cutting Map](#d-cross-cutting-map)
- [E. Contemporary AI Engineering Map](#e-contemporary-ai-engineering-map)
- [F. Research Frontier Map](#f-research-frontier-map)
- [G. Historical and Supersession Map](#g-historical-and-supersession-map)
- [H. Boundary Map](#h-boundary-map)
- [I. Dependency Map](#i-dependency-map)

**Audit and Record**

- [J. Completeness Audit](#j-completeness-audit)
- [K. Uncertainties and Disagreements](#k-uncertainties-and-disagreements)
- [L. Sources](#l-sources)
- [Research Record](#research-record)

</details>

---

## About This Report

This report answers the research question in [prompts/landscape-research.md](../prompts/landscape-research.md):

> **As of 2026-09-17, what scientific knowledge, methods, disciplines, system concepts, engineering capabilities, and research directions constitute the Data & Intelligence side of becoming an AI Engineer?**

How to read it:

- Section **B** gives the independently discovered structure.
- Section **C** documents every area and significant subfield with definition, importance, relationships, knowledge character, maturity, professional relevance, current direction, and evidence.
- Sections **D–I** show the same landscape through different views (cross-cutting, engineering, frontier, history, boundaries, dependencies).
- Sections **J–K** record what the completeness audits found and where uncertainty remains.
- Section **L** is the source register. Citations in the body use bracketed IDs such as `[D26]`.

> ⚠️ Nothing in this report is a curriculum recommendation.
>
> Maturity and relevance labels describe the field as evidenced on the execution date, not what a learner should study or in what order.

[⬆ Back to Contents](#contents)

---

## A. Executive Summary

**1. The field has a layered shape, not a list shape.** Independent field maps from very different communities — AAAI/IJCAI keyword taxonomies, the arXiv category system, ACL, KDD, ICLR and NeurIPS calls, ISO/IEC terminology standards, textbooks, and practitioner literature `[G1–G9, G13, G14, M1–M6]` — converge on six strata:

1. cross-cutting **foundations** (mathematics, statistics/causality, empirical methodology);
2. **model science** (classical ML, deep learning, generative modeling, foundation models, decision-making/RL, knowledge and reasoning);
3. **data, modalities and information access**;
4. **intelligence systems** that compose models with retrieval, tools, memory, verifiers, environments and humans;
5. **assurance** (evaluation science, trustworthy AI);
6. **engineering and context** (serving/operations, human interaction and governance, domain application).

**2. Foundation models reorganized the field but did not replace it.** The strongest current evidence shows that many "pre-LLM" areas remain the best tool or the necessary baseline in their niche:

- gradient-boosted trees remain the robust default for much tabular work, with tabular foundation models strongest on small data `[M10–M15]`;
- statistical baselines remain mandatory in forecasting and anomaly detection, and time-series foundation model gains are clouded by benchmark leakage `[M17, M18, X10]`;
- BM25 and IR evaluation methodology remain central to retrieval `[X7, X8, E8]`;
- symbolic planners, solvers and proof checkers are increasingly *combined* with LLMs rather than replaced by them `[X14–X17]`.

**3. Evaluation has become a discipline in its own right.** NeurIPS renamed its Datasets & Benchmarks track to **Evaluations & Datasets** for 2026 because "evaluation itself becomes an object of scientific study" `[G8]`. Construct validity, contamination, statistical rigor, LLM-as-judge validity and agentic capability measurement are all active and contested `[T1–T5, M22, M30]`. This is the most important structural change relative to a conventional "model-centric" map.

**4. A distinct "intelligence systems" layer is now evidenced.** Production systems are compound: model + context management + retrieval + tools + protocols + verification + human oversight `[E1–E6, G16]`. Durable concepts are visible beneath fast-moving implementations: least-autonomy design, context as a finite attention budget `[D11, E2]`, tool interface design, retrieval quality as a ceiling, and data-flow separation for security `[T16, T17]`. Interoperability protocols now have neutral governance (MCP and A2A under the Linux Foundation's Agentic AI Foundation) but still-changing specifications `[E12–E14]`.

**5. Foundation-model science has a recognizable lifecycle.** Pretraining (data curation, tokenization, scaling laws, mid-training) → post-training (SFT, preference optimization, reinforcement learning from verifiable rewards, AI/rubric feedback, distillation) → inference-time reasoning → adaptation (PEFT, merging, editing, continual learning) `[D6, D12, D21–D38]`. Several of the most practically consequential questions in this lifecycle are **contested**, notably whether RL expands or merely re-weights base-model capability `[D31]` and whether hybrid/linear attention matches full attention on hard long-context reasoning `[D8, D9]`.

**6. Trustworthiness is splitting into engineering obligations and open science.**

- Engineering obligations with enforceable dates or de-facto standards: security baselines (OWASP LLM and Agentic Top 10s, MITRE ATLAS, NIST AI 100-2) `[T20–T22]`; EU AI Act general-purpose AI obligations (applicable since August 2025, with Commission enforcement powers from August 2026) and transparency/marking obligations (August 2026), with high-risk obligations postponed to December 2027 / August 2028 `[T27, T28]`; documentation and provenance `[T26]`.
- Open science: robust prompt-injection defense `[T15]`, mechanistic interpretability as assurance `[T7–T9]`, chain-of-thought faithfulness `[D32, T10]`, reward hacking and emergent misalignment `[D37, T11]`, verifiable unlearning `[T24]`.

**7. Data is a first-class area, not a preprocessing step.** Data quality, curation, labeling, provenance, licensing and synthetic data materially determine model behavior and legal exposure `[A1–A4, D12, T26, T32]`. Model-based filtering is a key lever in pretraining data quality `[A2]`, and test-set label errors can change model rankings `[A3]`.

**8. Several consequential claims circulating in 2025–2026 are weaker than their popularity suggests.** Examples: GraphRAG as a general upgrade `[X13]`; "long context replaces retrieval" `[D11, E9]`; multi-agent systems as a default architecture `[E5, E6]`; measured developer productivity gains from AI coding tools `[E27]`; quantum machine learning advantage on classical data `[A12]`; federated learning's general deployment `[X27]`.

**9. Uncertainty is substantial and recorded.** Much frontier evidence comes from vendor technical reports with self-selected benchmarks. Search budget constraints limited depth in a few sub-areas. Section **K** and the **Research Record** document these limits.

[⬆ Back to Contents](#contents)

---

## B. Master Landscape

**In this section:** [Strata and Areas](#strata-and-areas) · [Why the Taxonomy Took This Form](#why-the-taxonomy-took-this-form)

### Strata and Areas

The landscape has **19 areas** organized into **6 strata**. Strata are an organizing aid, not a hierarchy of importance or a learning order. Areas have deliberately unequal depth.

```mermaid
flowchart TB
    subgraph S1["I. Foundations (cross-cutting)"]
        C1["C1 Mathematical Foundations"]
        C2["C2 Statistics, Causality & Experimentation"]
        C3["C3 Empirical Methodology"]
    end
    subgraph S2["II. Learning & Model Science"]
        C4["C4 Statistical & Classical ML"]
        C5["C5 Deep Learning & Representation Learning"]
        C6["C6 Generative Modeling"]
        C7["C7 Foundation Models"]
        C8["C8 Sequential Decision-Making & RL"]
        C9["C9 Knowledge, Reasoning & Symbolic AI"]
    end
    subgraph S3["III. Data, Modalities & Information Access"]
        C10["C10 Data for AI"]
        C11["C11 Modality & Data-Type Specializations"]
        C12["C12 Information Retrieval, Ranking & Recommendation"]
    end
    subgraph S4["IV. Intelligence Systems"]
        C13["C13 Compound AI Systems & Agents"]
        C14["C14 Embodied & Interactive AI"]
    end
    subgraph S5["V. Assurance"]
        C15["C15 Evaluation Science"]
        C16["C16 Trustworthy AI"]
    end
    subgraph S6["VI. Engineering & Context"]
        C17["C17 AI Engineering, Serving & Operations"]
        C18["C18 Human-AI Interaction, Governance & Societal Context"]
        C19["C19 AI for Science & Domain Applications"]
    end
    S1 --> S2
    S1 --> S3
    S2 --> S4
    S3 --> S4
    S5 -.-> S2
    S5 -.-> S4
    S6 -.-> S4
```

| Stratum | Area | One-line scope | Dominant character |
| --- | --- | --- | --- |
| I | **C1** Mathematical Foundations | Linear algebra, calculus/autodiff, probability, optimization, information theory | Science |
| I | **C2** Statistics, Causality and Experimentation | Estimation, uncertainty, calibration, conformal prediction, causal inference, online experiments, inference with ML predictions | Science + engineering practice |
| I | **C3** Empirical Methodology | Baselines, validation protocols, leakage, ablations, reproducibility, evidence standards for claims | Research + engineering practice |
| II | **C4** Statistical and Classical ML | Learning theory, supervised/unsupervised methods, ensembles, probabilistic and Bayesian modeling, tabular learning, AutoML | Science |
| II | **C5** Deep Learning and Representation Learning | Training mechanics, architectures (CNN → Transformer → MoE/SSM hybrids), self-supervised representations, embeddings | Science + system construction |
| II | **C6** Generative Modeling | Autoregressive, latent-variable, adversarial, flow, diffusion/flow-matching, discrete diffusion, world/video models | Science + research |
| II | **C7** Foundation Models | Pretraining science, post-training, reasoning and test-time compute, adaptation, multimodal and small models | Science + system construction |
| II | **C8** Sequential Decision-Making and RL | MDPs, bandits, off-policy evaluation, deep/offline RL, imitation, search, multi-agent learning, decision-focused learning | Science + research |
| II | **C9** Knowledge, Reasoning and Symbolic AI | Knowledge representation, knowledge graphs, logic and theorem proving, classical planning, constraint solving, neuro-symbolic integration | Science |
| III | **C10** Data for AI | Acquisition, provenance and licensing, annotation, quality, curation, synthetic data, documentation, validation | Engineering practice + science |
| III | **C11** Modality and Data-Type Specializations | Language, vision (2D/3D/video), speech/audio, time series/spatio-temporal/geospatial, graphs/relational, documents, multimodal integration | Mixed; mostly specialization |
| III | **C12** Information Retrieval, Ranking and Recommendation | Lexical/dense/sparse retrieval, reranking, IR evaluation, ANN indexing, recommender systems | Science + system construction |
| IV | **C13** Compound AI Systems and Agents | Workflow vs agent architecture, context engineering, structured output, tool use, RAG, memory, multi-agent orchestration, protocols, verifier loops | System construction + engineering |
| IV | **C14** Embodied and Interactive AI | Vision-language-action models, world models, sim-to-real | Research + specialization |
| V | **C15** Evaluation Science | Metrics and validation, benchmark validity, contamination, statistics of evals, judges, human and agentic evaluation, application evals | Science + engineering practice |
| V | **C16** Trustworthy AI | Interpretability, robustness, fairness, privacy, alignment and safety, AI security, provenance | Science + engineering + governance |
| VI | **C17** AI Engineering, Serving and Operations | ML lifecycle/MLOps, inference serving, compression, distributed training concepts, observability, cost/latency, feedback loops | Engineering practice |
| VI | **C18** Human-AI Interaction, Governance and Societal Context | Interaction design, human oversight, AI-assisted work, regulation and standards, environmental and legal context | Engineering + governance |
| VI | **C19** AI for Science and Domain Applications | Weather, structural biology, materials, healthcare, finance, social science — and the transferable methodology they contribute | Specialization |

### Why the Taxonomy Took This Form

The structure was revised several times during research. The decisions below record why.

| Decision | Alternative considered | Reason, with evidence |
| --- | --- | --- |
| **Evaluation Science is a separate area (C15)** and also cross-cutting | Keep evaluation inside each model area | Evaluation has its own methods, failure modes and venues: NeurIPS Evaluations & Datasets track `[G8]`, AAAI-27 "Evaluation, Benchmarking, Datasets & Analysis" and "AI Evaluation, Auditing & Red Teaming" keywords `[G2]`, construct-validity audits `[T1]`, statistics of evals `[M22]`. |
| **Foundation Models (C7) is separate from Deep Learning (C5)** | Treat LLMs as one DL architecture | The pretraining → post-training → inference-time reasoning → adaptation lifecycle has distinct science (scaling laws, RLVR, distillation, test-time compute) `[D21–D31]`, and distinct venue tracks exist (ACL "Language Models", "LLM Efficiency", "Safety and Alignment in LLMs" `[G4]`). |
| **"Agents" are not a top-level area; Compound AI Systems (C13) is** | Top-level "Agents" or "LLM Apps" area | "Agent" is unsettled terminology (`[E1]`; see **K**). The durable concept is composing models with retrieval, tools, memory, verification and humans — which also covers non-agentic workflows, neuro-symbolic verifier loops `[X14–X17]` and classical multi-agent systems `[G1]`. |
| **Information Retrieval (C12) is its own area; RAG sits in C13** | Treat retrieval as a sub-topic of RAG | IR is a mature scientific field with its own evaluation methodology (Cranfield/TREC) and venues (SIGIR, RecSys); RAG quality is bounded by retrieval quality `[X7, X8, E8, G10]`. |
| **Data for AI (C10) is a top-level area** | Treat data as preprocessing inside ML | Data-centric AI is an established research framing `[A1]`; data curation is a primary driver of pretraining quality `[A2, D12]`; label errors destabilize benchmarks `[A3]`; provenance/licensing carries legal and engineering consequences `[T26, T32]`. |
| **Knowledge, Reasoning and Symbolic AI (C9) retained as a full area** | Fold into history or omit | Classical AI areas remain large in AAAI/IJCAI taxonomies `[G1, G2, G9]` and are actively combined with LLMs (solvers as tools, formal theorem proving, planning verification) `[X14–X17]`. |
| **Causality grouped with statistics and experimentation (C2)** | Separate "Causal ML" area | For AI engineers, causal reasoning appears mostly as experimentation, off-policy evaluation and effect estimation `[M24–M26]`; causal representation learning remains research. Recorded as a boundary with C8. |
| **Modalities (C11) grouped, deliberately shallow** | A top-level area per modality | Each modality is a large specialization; the landscape records what is transferable and what is specialized rather than reproducing every subfield `[X1–X6, X9–X11]`. |
| **Embodied AI (C14) separated from C8/C11** | Treat robotics as an application domain | Vision-language-action models and world models are a distinct, fast-moving research line combining C5–C8 `[X21, D14, D20]`; boundary with robotics/control recorded in **H**. |
| **Governance placed with Human-AI Interaction (C18), security placed in Trustworthy AI (C16)** | A top-level "Responsible AI" area | Terminology (safety / security / responsible / trustworthy) is unsettled (see **K**). Security and safety have technical cores; governance is context that shapes engineering obligations. |
| **Engineering/serving (C17) is inside the landscape, bounded** | Exclude as CS&E | Engineers must understand inference economics, KV cache, batching, quantization and MLOps debt to build intelligent systems `[E18–E25, E30, E31]`; kernel implementation and distributed-systems theory are recorded as CS&E (**H**). |

[⬆ Back to Contents](#contents)

---

## C. Detailed Knowledge Map

**In this section:** [Legend](#legend) · [C1](#c1-mathematical-foundations) · [C2](#c2-statistics-causality-and-experimentation) · [C3](#c3-empirical-methodology-of-ai-research-and-practice) · [C4](#c4-statistical-and-classical-machine-learning) · [C5](#c5-deep-learning-and-representation-learning) · [C6](#c6-generative-modeling) · [C7](#c7-foundation-models) · [C8](#c8-sequential-decision-making-and-reinforcement-learning) · [C9](#c9-knowledge-reasoning-and-symbolic-ai) · [C10](#c10-data-for-ai) · [C11](#c11-modality-and-data-type-specializations) · [C12](#c12-information-retrieval-ranking-and-recommendation) · [C13](#c13-compound-ai-systems-and-agents) · [C14](#c14-embodied-and-interactive-ai) · [C15](#c15-evaluation-science) · [C16](#c16-trustworthy-ai) · [C17](#c17-ai-engineering-serving-and-operations) · [C18](#c18-human-ai-interaction-governance-and-societal-context) · [C19](#c19-ai-for-science-and-domain-applications)

### Legend

**Knowledge character** (not mutually exclusive): **Sci** = scientific understanding · **Sys** = intelligent-system construction · **Eng** = engineering practice · **Res** = research · **Gov** = governance/policy.

**Maturity:** Established · Current practice · Emerging · Active research · Experimental · Historically important · Narrowed role · Declining · Superseded. Maturity is a statement about evidence and adoption, **not** difficulty.

**Professional relevance:** **Broad** = broadly useful to AI engineers · **Role** = role-dependent · **Spec** = specialization-dependent · **Research** = primarily research-oriented · **Low** = currently low priority for applied work.

**Evidence strength wording** follows AGENTS.md: established fact · strong evidence · emerging consensus · active debate · plausible direction · speculation.

### C1. Mathematical Foundations

**Definition and purpose.** The mathematical language in which learning systems are specified, derived and debugged: linear algebra, multivariable calculus and automatic differentiation, probability, optimization, and information theory.

**Why it belongs.** Every authoritative current text and course examined treats the same core as prerequisite: Stanford CS229 (linear algebra, multivariable calculus, probability) `[M1]`; Murphy's *Probabilistic Machine Learning* Part I (probability, statistics, decision theory, information theory, linear algebra, optimization) `[M2]`; Bishop & Bishop 2024 `[M3]`; Prince 2023 `[M4]`; d2l.ai preliminaries (including autodiff) `[M5]`; *Mathematics for Machine Learning* `[M6]`. This is **established fact**.

**Relationships.** Depended on by every other area. Autodiff connects mathematics to software frameworks (boundary with CS&E, see **H**). Information theory connects to compression, tokenization and generative modeling ("language modeling is compression" `[M7]`).

**Maturity:** Established. **Relevance:** Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Linear algebra | Vectors, matrices, decompositions, norms; the language of embeddings, attention, low-rank adaptation and optimizer geometry | Sci | Established | Broad | Growing weight on matrix-level views: low-rank adapters, orthogonalized optimizer updates (Muon) | `[M1–M6, M29, D35]` |
| Calculus and automatic differentiation | Gradients, Jacobians, chain rule; reverse-mode autodiff underlies backpropagation | Sci + Sys | Established | Broad | Treated as a first-class preliminary in deep-learning-first texts | `[M5, M4]` |
| Probability | Random variables, distributions, conditioning, expectation; basis of likelihood-based losses, sampling and generative models | Sci | Established | Broad | Central to diffusion/flow and sampling-based decoding | `[M2, M3, M5]` |
| Optimization | Convex and non-convex optimization, stochastic gradient methods, adaptive methods, constrained optimization | Sci | Established (SGD/Adam/AdamW); matrix-aware optimizers emerging | Broad (literacy); Research (optimizer design) | Muon-class optimizers adopted at frontier scale, but fair-tuning studies find smaller gains that shrink with scale (**active debate**) | `[M29, D7]` |
| Information theory | Entropy, cross-entropy, KL divergence, mutual information, compression | Sci | Established | Broad | Prediction ↔ compression equivalence used as a lens on LLMs | `[M5, M7]` |
| Numerical methods | Conditioning, floating-point precision, iterative matrix methods | Sci + Eng | Established | Role | Low-precision training (FP8 and below) raises numerical-stability concerns; boundary with scientific computing | `[M29, D7]` |

[⬆ Back to Contents](#contents)

### C2. Statistics, Causality and Experimentation

**Definition and purpose.** Principles for learning from data under uncertainty and for drawing valid conclusions: estimation, hypothesis testing, uncertainty quantification, calibration, distribution-free inference, causal effect estimation, and online controlled experiments.

**Why it belongs.** Model evaluation is statistical estimation `[M22]`; product decisions depend on experiments `[M24]`; valid inference increasingly mixes human labels with model predictions `[M21]`. Recent audits show state-of-the-art claims often lack statistical support `[M30]`.

**Relationships.** Depends on C1. Depended on by C3, C4, C8 (off-policy evaluation), C12 (online ranking experiments), C15 (evaluation statistics) and C17 (monitoring, A/B testing). Overlaps C8 through bandits and OPE.

**Maturity:** Core established; applications to LLM evaluation emerging. **Relevance:** Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Estimation and inference | Sampling distributions, standard errors, confidence intervals, hypothesis tests, power | Sci | Established | Broad | Being applied late but increasingly to model evals (clustered SEs, paired differences, power analysis) | `[M22, M30]` |
| Statistics of evaluation / inference with ML predictions | Valid inference when evaluating models or when labels are partly model-generated (prediction-powered inference) | Sci + Eng | Emerging to current practice | Broad | Extensions to noisy LLM judges | `[M21, M22]` |
| Calibration | Agreement between predicted probabilities and observed frequencies; temperature scaling | Sci + Eng | Established | Broad | Post-training can degrade calibration of LLMs | `[M19]` |
| Conformal prediction | Distribution-free prediction sets with marginal coverage under exchangeability | Sci + Eng | Established theory; emerging for generative models | Broad (concept); Spec (depth) | Conditional coverage and distribution-shift robustness are open; conformal methods for LLM outputs and agents | `[M20]` |
| Bayesian statistics | Priors, posteriors, hierarchical models (see also C4 probabilistic modeling) | Sci | Established | Role | Amortized inference via prior-fitted networks | `[M2, M11]` |
| Causal inference | Potential outcomes, causal graphs, identification, double/debiased ML, heterogeneous effects | Sci | Established; causal ML current practice in specialized teams | Role | LLMs perform reasonably on simple causal tasks but are brittle on higher-level causal reasoning (**strong evidence** from 2025 surveys) | `[M25, M31]` |
| Online controlled experiments | A/B testing, variance reduction (CUPED), sequential testing, marketplace interference | Sci + Eng | Established / current practice | Broad | Continued refinement for marketplaces and trustworthiness | `[M24]` |
| Off-policy evaluation | Estimating a new policy's value from logged data of another policy | Sci + Eng | Current practice (recommenders) + active research | Role | Offline-to-online learning; shared with C8 and C12 | `[M26, X18]` |
| Survival / time-to-event analysis | Modeling censored durations (Kaplan–Meier, Cox, survival forests, deep survival models) | Sci | Established; deep variants active research | Spec (healthcare, churn, reliability) | Deep methods handle high-dimensional inputs but mostly single-risk right-censoring | `[A9]` |

[⬆ Back to Contents](#contents)

### C3. Empirical Methodology of AI Research and Practice

**Definition and purpose.** The methods by which claims about AI systems are made trustworthy: baselines, validation protocols, leakage prevention, ablations, statistical reporting, reproducibility and documentation of experimental conditions.

**Why it belongs.** It recurs as a failure point across every branch examined:

- leakage affected 294 papers across 17 fields `[M23]`;
- benchmark leakage clouds time-series foundation model claims `[M18]`;
- validation-set overfitting changes tabular rankings `[M12]`;
- test-set label errors change model rankings `[A3]`;
- more than half of top-model comparisons across 10 benchmarks lacked at least one expected property of superiority `[M30]`;
- NeurIPS requires a reproducibility and responsible-research checklist `[A5]`.

**Relationships.** Depends on C2. Depended on by C4–C19 and especially C15. Distinguished from C15: C3 concerns *how any empirical claim is established*; C15 concerns *the design and validity of evaluations of AI systems specifically*.

**Maturity:** Established principles, unevenly practiced. **Relevance:** Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Validation protocols | Train/validation/test separation, cross-validation, time-aware and group-aware splits, rolling-origin backtests | Sci + Eng | Established | Broad | Pretraining corpora create new leakage paths; foundation-model benchmarks need leakage-free protocols | `[M18, M23]` |
| Data leakage taxonomy | Systematic ways test information leaks into training or model selection | Sci + Eng | Established, growing importance | Broad | Contamination of web-scale pretraining data | `[M23, M18]` |
| Baselines and ablations | Strong, fairly tuned baselines; component ablations | Res + Eng | Established | Broad | Repeated findings that tuned classical baselines match newer methods (tabular, recommenders, anomaly detection) | `[M12, X9, X10]` |
| Reproducibility and reporting | Code/data release, seeds, error bars, checklists, machine-readable dataset metadata | Res | Current practice (venue-enforced) | Broad | NeurIPS checklist; Croissant metadata and persistent hosting for datasets | `[A5, T3]` |
| Evidence standards for claims | When a "state-of-the-art" claim is justified (effect size, consistency, robustness) | Res | Emerging | Broad | Position papers calling for stronger evidence and refutation tracks | `[M30]` |
| Scientific practice skills | Literature review, hypothesis formation, experimental design, scientific writing | Res | Established | Research / Role | AI research agents can partially replicate papers but remain below human experts on PaperBench (**strong evidence**, fast-moving) | `[A13]` |

[⬆ Back to Contents](#contents)

### C4. Statistical and Classical Machine Learning

**Definition and purpose.** Learning algorithms and theory outside (or preceding) large neural models: learning theory and generalization, supervised and unsupervised methods, ensembles, probabilistic and Bayesian modeling, and automated model selection.

**Why it belongs.**

- These methods remain production defaults in large domains, especially tabular prediction: gradient-boosted trees won most tabular competitions in 2024–2025 `[M15]` and remain "strong contenders" on TabArena `[M12]`.
- They are necessary baselines (see C3).
- They supply concepts reused inside modern systems, such as dictionary learning in interpretability `[T8]` and bias–variance reasoning.
- They remain core in textbooks and courses `[M1, M2, M6]` and in KDD/AAAI taxonomies `[G1, G5]`.

**Relationships.** Depends on C1–C3. Depended on by C5 (regularization, generalization), C11 (tabular, time series), C12 (learning to rank), C15 (metrics), C16 (fairness, attribution). Alternatives: deep and foundation models (C5, C7).

**Maturity:** Established; role in some niches narrowed, in others still dominant. **Relevance:** Broad (core methods), Role/Spec (specialized families).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Statistical learning theory and generalization | Bias–variance, capacity, double descent, benign overfitting | Sci + Res | Classical parts established; deep-network regime active research | Broad (literacy); Research (theory) | **Active debate**: double descent in classical models may be an artifact of how complexity is counted | `[M8, M9]` |
| Linear and generalized linear models | Linear/logistic regression, regularization | Sci + Eng | Established | Broad | Stable; used as baselines and probes | `[M1, M6]` |
| Decision trees and ensembles | Random forests, gradient-boosted trees (XGBoost, LightGBM, CatBoost as implementations) | Sci + Eng | Established / current practice | Broad | Remain robust default for medium/large tabular data; increasingly ensembled with deep and foundation models | `[M10, M12, M15]` |
| Kernel methods and SVMs | Kernel trick, SVMs, Gaussian-process connections | Sci | Established theory; likely narrowed practical role (**low confidence** — no fresh usage survey) | Role | Theoretical role persists (kernel regimes in generalization theory) | `[M6, M8]` |
| Unsupervised learning | Clustering, dimensionality reduction (PCA and nonlinear embeddings), density estimation | Sci + Eng | Established | Broad | Largely stable; embeddings from foundation models increasingly used as inputs (**plausible direction**) | `[M1, M6]` |
| Anomaly detection | Detecting rare/novel observations | Sci + Eng | Established | Role | Simple statistical methods often competitive or better on univariate time series | `[X10]` |
| Probabilistic graphical models and Bayesian ML | Directed/undirected models, variational inference, MCMC, probabilistic programming | Sci + Res | Established (inference); PPLs current practice in statistics-heavy roles; Bayesian deep learning at scale active research | Role | Position papers argue Bayesian deep learning is under-used; amortized Bayesian inference via prior-fitted networks | `[M2, M27, M11]` |
| Tabular learning | Supervised learning on heterogeneous rows/columns | Sci + Eng | GBDT established; tuned deep tabular models current; tabular foundation models emerging, fast adoption | Broad | TabPFN (Nature 2025) excels on small data; vendor-reported scale-ups to 1M rows; independent studies flag distribution-shift weaknesses; feature engineering still matters as much as model family | `[M10–M14, M15]` |
| Transfer, multi-task, meta and continual learning (classical framing) | Reusing knowledge across tasks; avoiding forgetting | Sci + Res | Established framing; see C7 for foundation-model continual learning | Role | Absorbed largely into pretraining/fine-tuning paradigm | `[G6, D36]` |
| AutoML and hyperparameter optimization | Automated model/pipeline search, HPO, neural architecture search | Sci + Eng | Established (HPO); NAS narrowed; LLM-driven AutoML agents emerging | Role | Convergence with LLM agents automating ML pipelines; high search cost and limited domain-knowledge encoding persist | `[A7, G1]` |
| Online learning | Learning from streams with regret guarantees | Sci | Established | Spec | Linked to bandits (C8) and concept drift (C17) | `[G1, X27]` |

[⬆ Back to Contents](#contents)

### C5. Deep Learning and Representation Learning

**Definition and purpose.** Learning hierarchical representations with differentiable neural networks: training mechanics, architectural families, training dynamics, and self-supervised representation learning, including embedding models.

**Why it belongs.** It is the substrate of nearly all modern perception, language and generative systems. Current textbooks treat it as a distinct body of knowledge `[M3, M4, M5]`. Recent best-paper awards show its science is still moving (architecture theory, training stability, scaling mechanisms) `[D2, D3]`.

**Relationships.** Depends on C1, C2, C4. Depended on by C6, C7, C11, C12 (dense retrieval), C14, C16 (interpretability). Boundary with CS&E at kernels and distributed training (see **H**).

**Maturity:** Core established; architecture frontier contested. **Relevance:** Broad (core), Role/Spec (architecture design).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Training mechanics | Backpropagation, losses, optimizers (SGD, AdamW, Muon), learning-rate schedules, initialization, regularization | Sci + Eng | Established (Muon emerging) | Broad | Matrix-aware optimizers at frontier scale; checkpoint averaging as an alternative to learning-rate decay | `[M29, D7, D6]` |
| Architectural lineage: MLP, CNN, RNN/LSTM | Inductive biases for tabular, spatial and sequential data | Sci | MLP/CNN established; standalone RNN/LSTM narrowed role | Broad (concepts) | Recurrence returning inside state-space and linear-attention layers | `[D1, D8, D10]` |
| Attention and the Transformer | Content-based token mixing; dominant architecture of foundation models | Sci + Sys | Established | Broad | Theory of expressivity (ICLR 2026 outstanding paper); attention sinks and massive activations as engineering phenomena | `[D1, D2, D3]` |
| Residuals, normalization and stability | Residual streams, pre-norm/RMSNorm, QK-norm, gating, normalization-free variants | Sci + Eng | Residual/pre-norm established; gated attention and constrained hyper-connections emerging (one or two labs each) | Role | Stability at depth and scale remains a live design space | `[D3, D4, D5]` |
| Mixture-of-Experts | Sparse expert routing; total parameters far exceed active parameters | Sys + Eng | Current practice for large models | Broad (understand); Spec (build) | Very high sparsity (roughly 10–50B active out of ~1T); stability of RL on MoE | `[D6, D7, D27]` |
| Efficient attention (MLA, learned sparse attention, sliding windows) | Reducing KV-cache memory and attention compute | Sys + Res | Current practice at several open-weight labs; design space unsettled | Role | Compressed and sparse attention for 1M-token contexts | `[D6]` |
| State-space models, linear attention and hybrids | Fixed-size recurrent state interleaved with some full-attention layers | Sys + Res | Emerging; production adoption by some labs; **active debate** | Spec | Hybrid adoption (NVIDIA, Qwen, Moonshot) versus documented quality deficits on multi-hop reasoning and immature infrastructure (MiniMax) | `[D8, D9, D10]` |
| Graph neural networks | Message passing over graphs | Sci | Established fundamentals; graph foundation models active research | Spec | Community reports declining attention and benchmark problems; pivot to relational databases | `[M28]` |
| Training dynamics and generalization in deep nets | Memorization vs generalization, scaling mechanisms, implicit regularization | Sci + Res | Active research | Research | Superposition proposed as mechanism for scaling laws; implicit dynamical regularization in diffusion (NeurIPS 2025 best paper) | `[D3]` |
| Self-supervised representation learning | Contrastive, masked modeling, self-distillation (e.g., DINO family), JEPA-style predictive learning | Sci + Sys | Contrastive/masked/self-distillation current practice; JEPA active research | Broad (use as components); Spec (train) | Self-supervised vision features rival or beat weakly supervised ones; predictive latent world models for robotics | `[D13, D14]` |
| Embedding models | Dense vector representations for retrieval, clustering, classification | Sys + Eng | Current practice | Broad | State of the art built on LLM backbones with synthetic training pairs; multimodal embeddings | `[D15]` |

[⬆ Back to Contents](#contents)

### C6. Generative Modeling

**Definition and purpose.** Learning data distributions in order to sample, complete or transform data: autoregressive models, latent-variable models, adversarial models, normalizing flows, diffusion and flow matching, discrete diffusion for text, and interactive video/world generation.

**Why it belongs.** Generative models are the mechanism behind language models, image/video/audio synthesis, and increasingly scientific generation and robot action policies:

- diffusion and flow models are used for weather ensembles `[X22]`, protein complexes `[X23]`, crystal generation `[X24]`, robot actions `[X21]` and TTS `[X5]`.

Murphy's advanced volume treats generation as one of five major parts of probabilistic ML `[M2]`.

**Relationships.** Depends on C1, C2, C5. Depended on by C7, C11, C14, C19. Alternatives are discriminative approaches.

**Maturity:** Mixed; see table. **Relevance:** Broad (autoregressive concepts), Spec (media generation).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Autoregressive models | Factorize joint distribution as next-token prediction | Sci + Sys | Current practice (dominant for language; spreading to unified multimodal) | Broad | Documented limits: output homogeneity across models, creativity constraints of next-token training | `[D3, M2]` |
| Variational autoencoders and latent spaces | Encoder–decoder with variational objective; latent compression for diffusion | Sci | Standalone VAE generator narrowed; VAE latents current practice; representation-autoencoder latents emerging | Role | Frozen self-supervised encoders replacing VAEs as diffusion latents (research) | `[D17, M2]` |
| Generative adversarial networks | Generator–discriminator games | Sci | Historically important; narrowed role as primary generator | Low–Spec | Not refuted: principled modern GANs competitive on benchmarks; adversarial losses persist in distillation | `[D18]` |
| Normalizing flows | Invertible transforms with exact likelihood | Sci | Historically important; ideas absorbed into continuous flows (**evidence gap**: no fresh adoption data) | Low | — | `[M2]` |
| Diffusion and flow matching | Learn to reverse noising or regress velocity fields from noise to data | Sci + Sys | Diffusion established; flow matching current default; one-step methods emerging | Spec (build); Broad (concept) | Few/one-step generation without distillation; transformer backbones displacing U-Nets (secondary evidence) | `[D16]` |
| Discrete / masked diffusion language models | Parallel iterative denoising of token blocks | Sys + Res | Emerging (first open-weight frontier-lab release, 2026) | Role (latency-critical serving) | Conversion from pretrained autoregressive models rather than training from scratch; parity on hard reasoning unestablished | `[D19]` |
| World models and interactive video generation | Generating controllable, persistent simulated environments | Res | Active research / experimental | Research / Spec | Real-time interactive worlds with minutes of consistency (research preview); latent-predictive alternatives | `[D20, D14]` |

[⬆ Back to Contents](#contents)

### C7. Foundation Models

**Definition and purpose.** The science and practice of large models pretrained on broad data and adapted to many tasks. The area covers pretraining, post-training, inference-time reasoning, adaptation, multimodality and small/on-device models.

**Why it belongs.**

- Foundation models are the dominant substrate of contemporary AI engineering `[G11, G14, G16]` and have explicit tracks at ACL, AAAI and KDD `[G2, G4, G5]`.
- Their lifecycle has distinct scientific questions (scaling, RL post-training, test-time compute) `[D21–D31]`.
- The International AI Safety Report 2026 identifies model scaling and inference-time scaling as the two principal capability drivers `[G12]`.

**Relationships.** Depends on C1–C6, C8 (RL), C10 (data). Depended on by C11–C19. Alternatives: task-specific models (C4, C11).

**Maturity:** Current practice with many contested sub-questions. **Relevance:** Broad (understand and use), Role (train and post-train).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Scaling laws | Empirical relations between loss and parameters, data, compute | Sci | Pretraining laws established (with revisions); RL and test-time scaling laws active research | Broad (reasoning about cost/capability) | Chinchilla-optimal as training target; inference-aware "overtraining" dominates deployment; sigmoidal RL compute curves | `[D21, D22]` |
| Emergent abilities | Whether capabilities appear discontinuously with scale | Sci + Res | **Active debate** (metric artifact vs genuine transition) | Broad (as caution) | Unresolved | `[D23]` |
| Pretraining data curation and mid-training | Filtering, deduplication, decontamination, mixing, staged curricula (see C10) | Sci + Eng | Current practice; mixing science active research | Role | Fully open pipelines (data, checkpoints) enable reproducible study; "mid-training" as distinct stage | `[D12, A2]` |
| Tokenization | Subword vocabularies; byte-level alternatives | Sci + Eng | Subword current practice; tokenizer-free active research | Broad (cost/multilingual effects) | Byte-latent models match tokenized models in controlled scaling studies; unequal cost across languages | `[D24, X1]` |
| Long-context methods | RoPE scaling, context extension, efficient attention | Sys + Res | Current practice; reliable long-context use active research | Broad | Advertised 1M-token contexts, but effective context degrades non-uniformly with length and distractors | `[D11, D12, D6]` |
| Supervised fine-tuning / instruction tuning | Training on demonstration data | Sys + Eng | Established | Broad | Now one stage among several (SFT → preference → RL) | `[D25, D12]` |
| Preference optimization (RLHF, DPO and variants) | Aligning outputs with preferences via reward models + RL or closed-form objectives | Sci + Sys | RLHF established; DPO current practice (often intermediate stage) | Broad | PPO-with-critic narrowed in reasoning RL; DPO used before RL stages | `[D25, D12]` |
| Reinforcement learning from verifiable rewards | RL with programmatic rewards (answers, tests); critic-free group-relative methods | Sci + Sys | Current practice for reasoning models; algorithm details active research | Broad (understand); Role (do) | Length-bias and stability fixes; RL on MoE; scaling studies | `[D26, D27, D22]` |
| Reward design beyond verifiable domains | Rubrics, AI feedback, constitutions, reward models | Sci + Sys + Res | RLAIF current practice; rubric RL emerging | Role | Reward models miscalibrated against diverse human preferences | `[D28, D25, D3]` |
| Distillation (off-policy and on-policy) | Training smaller students from teacher outputs or teacher-graded student samples | Sys + Eng | Current practice; on-policy distillation emerging, spreading fast | Broad | Reported large compute savings versus RL for small models; restores capabilities lost to fine-tuning | `[D29]` |
| Reasoning models and test-time compute | Spending inference compute on intermediate reasoning, sampling with verifiers, search | Sci + Sys | Current practice | Broad | Compute-optimal allocation depends on problem difficulty; **active debate** whether RL expands capability or re-weights base-model behavior | `[D30, D31, G12]` |
| Chain-of-thought faithfulness and limits | Whether visible reasoning reflects the computation that drives answers | Sci + Res | Active research | Broad (as caution) | Models frequently omit hints they used; contested evidence on reasoning collapse at high complexity | `[D32, D40, T10]` |
| Latent and recursive reasoning | Reasoning in hidden states or small recursive networks | Res | Experimental | Research | Promising on narrow puzzles only | `[D33]` |
| In-context learning science | Mechanisms of learning from prompts (induction heads, function-vector heads) | Sci + Res | Active research | Research | Induction heads support pattern copying; few-shot ICL in larger models attributed mainly to function-vector heads | `[D41, D42]` |
| Parameter-efficient adaptation | LoRA and variants; adapters | Sys + Eng | Current practice | Broad | Evidence that correctly configured LoRA (all layers, higher learning rate) matches full fine-tuning in most post-training regimes; learns less, forgets less | `[D35]` |
| Model merging | Combining weights of fine-tuned models or checkpoints | Sys + Res | Current practice in some pipelines; active research | Role | Checkpoint averaging in pretraining; merging surveys | `[D6]` |
| Knowledge / model editing | Targeted modification of stored facts or behaviors | Sci + Res | Active research | Role / Research | Locate-and-edit methods degrade after sequential edits (gradual then catastrophic forgetting) | `[A10]` |
| Continual learning and forgetting | Adapting without losing prior capability | Sci + Res | Active research (recognized gap: deployed models do not learn post-deployment) | Research / Role | On-policy RL forgets less than SFT (contested by later work); multi-timescale memory architectures | `[D36]` |
| Fine-tuning side effects | Narrow fine-tuning producing broad behavioral changes | Sci + Res | Replicated research finding | Broad (as risk) | Emergent misalignment from narrow training data | `[D37, T11]` |
| Synthetic data and model collapse | Training on model-generated data | Sci + Eng | Synthetic data current practice; collapse framing **active debate** | Broad | Collapse when real data is replaced; bounded when data accumulates | `[D38]` |
| Multimodal foundation models | Vision-language, audio, video and any-to-any models | Sys + Res | Current practice at frontier; emerging in open weights | Broad (use); Spec (build) | Native omni-modal models claiming no degradation versus single-modality counterparts | `[D34]` |
| Small and on-device models | Efficient architectures, offloading, nested submodels, distillation | Sys + Eng | Current practice | Role | Per-layer embedding offload, nested models; small models largely made by overtraining + distillation | `[D39, D29]` |
| Open-weight / fully open model ecosystem (technical role) | Public technical reports, weights, and (sometimes) data as sources of evidence | Res | Current | Broad (as evidence source) | Many architecture findings now come from open technical reports; single-family findings need caution | `[D6, D7, D12]` |

[⬆ Back to Contents](#contents)

### C8. Sequential Decision-Making and Reinforcement Learning

**Definition and purpose.** Learning and planning for agents whose actions affect future observations and rewards: Markov decision processes, bandits, dynamic programming, value- and policy-based RL, offline RL, imitation learning, search, multi-agent learning and game theory, and learning coupled to downstream optimization.

**Why it belongs.**

- RL is the mechanism behind reasoning post-training (C7) `[D26]`, formal mathematics systems `[X16]`, generative recommender alignment `[X9]`, and sim-to-real robotics `[X19]`.
- Bandits and off-policy evaluation drive industrial personalization `[X18, M26]`.
- Multi-agent systems and game theory are full areas in AAAI taxonomies `[G1, G2]`.
- Game-theoretic analysis of interacting LLM agents is emerging `[X20]`.

**Relationships.** Depends on C1, C2, C4, C5. Depended on by C7 (post-training), C12, C13 (agent planning loops), C14. Overlaps operations research (see **H**).

**Maturity:** Core established; deep RL and LLM-agent game theory active research. **Relevance:** Broad (bandits, OPE, RL concepts for post-training), Spec (deep RL control).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| MDPs and dynamic programming | Formal model of sequential decisions; Bellman equations | Sci | Established | Broad (concepts) | Foundation for RL post-training vocabulary | `[G1, X18]` |
| Multi-armed and contextual bandits | Exploration–exploitation with immediate rewards | Sci + Eng | Established / current practice | Broad | Used in ranking, ads, and model rollout decisions | `[X18]` |
| Off-policy evaluation and offline RL | Learning/evaluating from logged data | Sci + Res | Current practice + active research | Role | Offline-to-online learning | `[M26, X18]` |
| Value- and policy-based deep RL | Q-learning, policy gradients, actor–critic, PPO | Sci + Sys | Established algorithms; current practice in control and post-training | Role | Critic-free group methods for LLMs; fast sim-to-real training for locomotion | `[D26, X19]` |
| Imitation learning | Learning from demonstrations | Sci + Sys | Established; central to robotics foundation models | Spec | Vision-language-action models trained largely by imitation | `[X21]` |
| Search and planning with learned models | MCTS, model-based planning | Sci + Res | Established (games); active research in LLM reasoning | Role | RL + formal environments (Lean) for theorem proving | `[X16]` |
| Multi-agent learning and game theory | Equilibria, mechanism design, cooperation, negotiation | Sci + Res | Classical MAS/game theory established; LLM-agent game theory emerging | Role (rising) | LLMs weak at recursive strategic reasoning; incentive mechanisms for LLM cooperation | `[G1, X20]` |
| Decision-focused learning (predict-then-optimize) | Training predictors for the quality of downstream optimization decisions | Sci + Res | Active research with benchmarks | Spec | Solver-free and online variants | `[A6]` |

[⬆ Back to Contents](#contents)

### C9. Knowledge, Reasoning and Symbolic AI

**Definition and purpose.** Explicit representation of knowledge and algorithmic reasoning over it: knowledge representation languages and ontologies, knowledge graphs, logic and automated theorem proving, classical planning, constraint satisfaction and combinatorial optimization, and neuro-symbolic integration.

**Why it belongs.**

- It is a large, persistent part of the field's own taxonomies (AAAI KRR, CSO, PRS, SO areas; IJCAI core methods) `[G1, G2, G9]`.
- The strongest 2024–2026 evidence shows *integration* with neural methods rather than obsolescence:
  - LLMs still underperform on classical planning benchmarks, supporting generate-and-verify designs `[X14]`;
  - LLMs connected to SAT/SMT/constraint solvers through tool protocols `[X15]`;
  - reinforcement learning in formal proof environments reaching olympiad-level results `[X16]`;
  - LLM-guided evolutionary program search discovering improved algorithms `[X17]`.

**Relationships.** Depends on C1 (logic, discrete mathematics). Depended on by C12 (knowledge graphs in retrieval), C13 (verifiers, solvers as tools), C16 (formal verification ideas). Alternatives: purely neural reasoning (C7).

**Maturity:** Established core; neural integration active research. **Relevance:** Broad (knowing when to delegate to solvers/verifiers), Spec (depth).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Knowledge representation and ontologies | Description logics, RDF/OWL, commonsense and temporal reasoning | Sci | Established; manual ontology engineering narrowed | Role | LLM-assisted ontology and schema construction | `[G1, X12]` |
| Knowledge graphs | Graph-structured entity/relation stores; construction, completion, querying | Sci + Sys | Established; LLM-based construction emerging | Role | KG-enhanced LLMs and LLM-augmented KGs; GraphRAG useful only conditionally (see C12/C13) | `[X12, X13]` |
| Logic, automated reasoning and theorem proving | SAT/SMT, interactive theorem provers, neural provers | Sci + Res | SAT/SMT established; neural formal proving active research, fast-moving | Research / Spec | Olympiad and Putnam-level formal proofs; autoformalization reliability open | `[X15, X16]` |
| Classical planning | PDDL planning, heuristic search | Sci | Established | Role | Benchmarks show LLMs still fall short; generate-and-verify with symbolic planners (evidence largely from 2024; may lag newest models) | `[X14]` |
| Constraint satisfaction and combinatorial optimization | CP, MIP, heuristics, metaheuristics | Sci + Eng | Established | Role | LLMs as modelers for solvers; LLM-evolved heuristics | `[X15, X17]` |
| Neuro-symbolic integration | Combining neural generation/perception with symbolic structure or verification | Sci + Res | Active research | Role (pattern) / Research | "Neural proposer, symbolic verifier" is the unifying pattern across planning, proving, optimization | `[X14–X17, G5]` |

[⬆ Back to Contents](#contents)

### C10. Data for AI

**Definition and purpose.** Everything that determines what data an AI system learns from and is evaluated on: acquisition, provenance and licensing, annotation (human, programmatic, model-assisted), quality assessment and cleaning, curation for pretraining and fine-tuning, synthetic data, documentation, and validation. "Data-centric AI" frames this as training-data development, inference/evaluation-data development, and data maintenance `[A1]`.

**Why it belongs.**

- Controlled experiments show data curation is a primary determinant of model quality: model-based filtering was key in DataComp-LM `[A2]`, and fully open pipelines document multi-stage data mixing `[D12]`.
- Label errors average about 3.4% across ten widely used test sets and can reverse model rankings `[A3]`.
- Dataset licensing is frequently miscategorized (license omission above 70%, error above 50% on hosting sites) `[T26]`.
- Consent signals for web data are rapidly tightening `[T26]`.
- Data-acquisition choices now carry material legal consequences `[T32]`.
- The AI engineering literature treats dataset engineering as a core capability `[G14]`.

**Relationships.** Depends on C2, C3. Depended on by C4–C7, C11, C15 (evaluation data), C16 (fairness, privacy, poisoning), C17 (validation, drift), C18 (copyright, governance). Boundary: data engineering pipelines and storage belong primarily to CS&E (see **H**).

**Maturity:** Established concerns; foundation-model-era practices current and evolving. **Relevance:** Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Data acquisition, provenance and licensing | Tracing sources, licenses, consent and lineage of datasets | Eng + Gov | Current practice, consolidating | Broad | Provenance audits; opt-out/consent signals; licensing-aware filtering driven by litigation and EU GPAI copyright obligations | `[T26, T28, T32]` |
| Annotation and labeling | Guidelines, crowdsourcing quality control, programmatic weak supervision, LLM-assisted labeling | Eng + Sci | Established (crowdsourcing, weak supervision); LLM pre-labeling with human verification current practice | Broad | LLMs match humans on simple tasks but need human review for nuanced, subjective or specialized labels; label variation as signal | `[A4, X26]` |
| Data quality and label-error detection | Finding and fixing noisy labels, duplicates, outliers | Sci + Eng | Established methods (confident learning) | Broad | Calibration-aware mislabel detection | `[A3]` |
| Feature engineering and preprocessing | Transforming raw data into model inputs | Eng | Established | Broad | Still moves tabular benchmark results as much as architecture changes | `[M5, M13]` |
| Pretraining data curation | Web extraction, filtering (heuristic and model-based), deduplication, decontamination, mixing | Sci + Eng | Current practice; mixing science active research | Role | Standardized testbeds for data curation; quality-aware upsampling; staged mid-training mixes | `[A2, D12]` |
| Synthetic data | Model-generated training/evaluation data, instruction synthesis, simulation | Eng + Res | Current practice with known risks | Broad | Accumulate-not-replace consensus; synthetic priors for tabular foundation models | `[D38, M11, G14]` |
| Dataset documentation | Datasheets, data cards, machine-readable dataset metadata | Eng + Gov | Established practice; venue-enforced | Broad | Persistent hosting and metadata standards at NeurIPS | `[T26, T3]` |
| Data validation and drift | Schema/statistics checks before training and in production | Eng | Established (classical MLOps) | Broad | Extended to LLM input/output monitoring (see C17) | `[E19]` |
| Data for evaluation | Building representative, uncontaminated, correctly labeled test sets | Sci + Eng | Current practice; see C15 | Broad | Private and dynamic test sets; audits of "hard" benchmarks finding answer errors | `[T2, A3]` |

[⬆ Back to Contents](#contents)

### C11. Modality and Data-Type Specializations

**Definition and purpose.** Knowledge specific to the structure of particular data types: natural language, images/3D/video, speech and audio, time series and spatio-temporal/geospatial data, graphs and relational databases, documents, and their multimodal integration.

**Why it belongs.** Every major field map organizes a large share of the field by modality (AAAI CV, NLP, audio/speech areas; arXiv cs.CL, cs.CV, eess.AS; ACL areas) `[G1–G4]`. Modality structure determines tokenization, architectures, evaluation, failure modes and baselines.

**Relationships.** Depends on C4–C7, C10. Depended on by C12–C14, C19. Multimodal foundation models (C7) increasingly subsume modality-specific pipelines, but specialized knowledge persists in evaluation, efficiency, and exactness-critical tasks.

**Maturity:** Mixed. **Relevance:** Mostly Role/Spec, with specific transferable elements marked Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Natural language processing (beyond LLMs) | Tokenization effects, information extraction, machine translation, multilinguality and low-resource languages, linguistic analysis | Sci + Eng | Established; standalone pipeline NLP narrowed; MT now LLM-led | Broad (tokenization, IE trade-offs, MT evaluation); Spec (low-resource) | Small fine-tuned encoders competitive for span-exact extraction; harder MT test sets and human MQM/ESA protocols | `[X1, D24, G4]` |
| Computer vision: detection and segmentation | Object detection, promptable/concept segmentation | Sys + Eng | Current practice; open-vocabulary/concept prompting emerging | Role | Concept-level segmentation and tracking; transformer detectors on self-supervised backbones challenging CNN detectors (vendor-heavy evidence) | `[X2]` |
| 3D vision | Multi-view geometry, neural fields, Gaussian splatting, feed-forward geometry | Sci + Res | NeRF narrowed; Gaussian splatting current practice in graphics/robotics; feed-forward geometry emerging | Spec | Single-pass camera/depth/point-map prediction (CVPR 2025 best paper) | `[X3, X4]` |
| Video understanding | Temporal reasoning over long videos | Res | Active research, absorbed into multimodal LLMs | Role | Agentic long-video evidence search; video remains a documented weakness (AI Index 2026) | `[G11]` |
| Speech and audio | ASR, TTS, spoken dialogue, audio codecs | Sys + Eng | ASR/TTS current practice; full-duplex speech LMs emerging | Role | Accuracy–speed trade-offs between LLM-decoder and CTC-style ASR; codec-LM vs flow-matching TTS; full-duplex dialogue | `[X5, X6]` |
| Time series, spatio-temporal and geospatial data | Forecasting, anomaly detection, remote-sensing embeddings | Sci + Eng | Statistical methods established; time-series foundation models emerging; geospatial embeddings active research | Role | Foundation models top curated leaderboards but leakage and weak baselines cloud gains; statistical methods often win in anomaly detection | `[M16–M18, X10, X11]` |
| Tabular data | See C4 tabular learning | Sci + Eng | See C4 | Broad | See C4 | `[M10–M14]` |
| Graphs and relational data | Graph learning, relational deep learning over database schemas | Sci + Res | Fundamentals established; relational foundation models emerging | Spec / Role (enterprise data) | Relational deep learning benchmarks; boundary between tabular and graph learning blurring | `[M28, X29]` |
| Document understanding | Layout analysis, OCR, table/formula extraction from PDFs and scans | Sys + Eng | Current practice; VLM-based end-to-end parsers emerging | Role (widespread in RAG pipelines) | Benchmarks comparing pipeline vs end-to-end VLM parsing; OCR robustness affects downstream RAG | `[E32]` |
| Multimodal integration | Aligning and fusing modalities; grounding language in perception | Sci + Sys | Current practice (via multimodal FMs) | Broad | Omni-modal models; multimodal embeddings | `[D34, D15, G4]` |
| Edge / TinyML | Models on microcontrollers and constrained devices | Eng | Current practice in embedded work | Spec | "Tiny deep learning" | `[X28]` |

[⬆ Back to Contents](#contents)

### C12. Information Retrieval, Ranking and Recommendation

**Definition and purpose.** The science and engineering of finding and ranking relevant items for an information need or a user: lexical, dense, learned-sparse and late-interaction retrieval; reranking; approximate nearest-neighbour indexing; IR evaluation; and recommender systems.

**Why it belongs.**

- Retrieval quality bounds the quality of retrieval-augmented and agentic systems. Hybrid lexical+dense retrieval with reranking cut top-20 retrieval failures by 67% in one controlled study `[E8]`.
- BM25-style lexical retrieval remains competitive even on reasoning-intensive retrieval benchmarks `[X7]`.
- IR evaluation methodology is actively contested around LLM relevance judges `[X8]`.
- Recommender systems are among the largest-scale deployed ML systems and are undergoing a generative shift `[X9, G10]`.
- IR has its own arXiv category and venues `[G3, G10]`.

**Relationships.** Depends on C2, C4, C5 (embeddings), C8 (bandits, OPE). Depended on by C13 (RAG, agent search tools), C17 (vector storage). Boundary: distributed vector database implementation is CS&E (see **H**).

**Maturity:** Established core; LLM-era methods current/emerging. **Relevance:** Broad (retrieval + evaluation), Role (recommenders).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Lexical retrieval | Inverted indexes, TF-IDF, BM25 | Sci + Sys | Established | Broad | Strong baseline; LLM query expansion makes it competitive on reasoning-heavy retrieval; grep-style lexical search effective in agent harnesses | `[X7, E10]` |
| Dense retrieval and embeddings | Bi-encoders mapping queries/documents to vectors | Sci + Sys | Current practice | Broad | LLM-backbone embedders (see C5) | `[D15]` |
| Learned sparse and late-interaction retrieval | SPLADE-style sparse expansion; ColBERT-style token-level matching | Sci + Res | Current practice + active research | Role | Combining sparse candidate generation with late interaction | `[X7, X8]` |
| Hybrid retrieval and reranking | Combining lexical and dense retrieval; cross-encoder and LLM rerankers | Sys + Eng | Current practice | Broad | Listwise and reasoning rerankers | `[E8]` |
| Approximate nearest-neighbour indexing | Graph-based (HNSW), quantization-based (IVF-PQ), disk-based indexes | Sci + Sys | Established algorithms | Role | Vector search features converging into general databases (**low confidence**) | `[E11]` |
| IR evaluation | Cranfield/TREC methodology, nDCG, recall, relevance judgments | Sci | Established; LLM judging active debate | Broad | LLM judgments correlate with humans at run level but less per topic; circularity when the same LLMs rerank | `[X8]` |
| Agentic and reasoning-intensive retrieval | Iterative, tool-based search loops; retrieval requiring reasoning | Sys + Res | Current practice (coding, small corpora); active research | Broad | Results depend strongly on harness and tool-calling style | `[E10, X7]` |
| Recommender systems | Matrix factorization, two-tower retrieval, sequential transformers, ranking cascades, generative recommendation with semantic IDs | Sci + Sys | Classical established; sequential transformers current; generative recommenders emerging at a few very large companies | Role | Compute scaling laws for recommenders; tuned classical sequential baselines remain competitive with LLM-based recommenders | `[X9, G10]` |

[⬆ Back to Contents](#contents)

### C13. Compound AI Systems and Agents

**Definition and purpose.** Systems in which intelligence emerges from composing models with context, retrieval, tools, memory, planning loops, verifiers, other agents, environments and humans. This covers the spectrum from fixed workflows to autonomous agents.

**Why it belongs.**

- Production AI systems are overwhelmingly compound.
- A 2025–2026 study of 20 case studies and 86 practitioners found 68% of production agents execute at most 10 steps before human intervention, 70% rely on prompting off-the-shelf models, and 74% depend primarily on human evaluation, with reliability the top concern `[G16]`.
- AAAI-27 adds keywords for LLM-based agents and tool use/orchestration `[G2]`; ACL 2026 has an "AI/LLM Agents" area `[G4]`.
- The AI Index 2026 describes a shift "from interacting with AI to deploying it" in systems that take actions `[G11]`.

**Relationships.** Depends on C5, C7, C8 (planning, multi-agent theory), C9 (verifiers, solvers), C12 (retrieval), C15 (evaluation), C16 (security). Depended on by C14, C17, C18.

**Maturity:** Core patterns current practice; autonomy and multi-agent coordination emerging. **Relevance:** Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Workflow vs agent architecture | Predefined code paths (chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer) vs model-directed control flow | Sys + Eng | Current practice, stabilizing | Broad | Least-autonomy-that-works as design principle; bounded autonomy with human intervention in production | `[E1, G16]` |
| Context engineering | Curating the finite set of tokens a model attends to: instructions, tool definitions, retrieved content, history, compaction, external memory | Sys + Eng | Current practice | Broad | Measured non-uniform degradation with input length supports durability of the concept (label itself is recent vendor-originated terminology) | `[E2, D11, E4]` |
| Prompting and in-context specification | Instructions, examples, output specifications | Eng | Established / current practice | Broad | Phrasing-level tuning declining in *relative* importance versus context and tool design | `[E2, G16, G14]` |
| Structured outputs and constrained decoding | Schema/grammar-constrained generation | Sys + Eng | Established in APIs; implementations evolving | Broad | Uneven schema coverage across frameworks; strict formats can harm reasoning | `[E7]` |
| Tool use and tool interface design | Model-emitted calls to external functions; designing agent-facing interfaces | Sys + Eng | Current practice | Broad | Tool definitions consume context; code execution against tool servers reduces token load | `[E1, E4]` |
| Retrieval-augmented generation | Retrieval at inference time to ground outputs (builds on C12) | Sys + Eng | Hybrid + rerank current practice; naive top-k RAG declining as default; GraphRAG conditional | Broad | No silver bullet between long context and RAG; agentic retrieval loops | `[E8, E9, E10, X13]` |
| Memory and state | Persisted notes, summaries, retrievable history; durable execution for long-running agents | Sys + Eng | Current practice, spreading | Broad | Checkpoint/resume; workflow-engine integrations | `[E3, E26]` |
| Multi-agent orchestration | Multiple agents with distinct contexts/roles | Sys + Res | Emerging; narrow patterns current (parallel research sub-agents, reviewer agents) | Role | Large token cost; poor fit for tightly coupled tasks; single-threaded writes; failure taxonomy of 14 modes | `[E3, E5, E6]` |
| Interoperability protocols | Standard agent–tool (MCP) and agent–agent (A2A) protocols | Sys + Eng | MCP current practice with evolving spec; A2A emerging | Broad (concept); Role (details) | Neutral governance under Linux Foundation AAIF; 2026 MCP spec made the core stateless and deprecated earlier primitives; enterprise auth/audit gaps | `[E12–E14]` |
| Verification loops and neuro-symbolic composition | Generate-and-verify with tests, solvers, proof checkers, evaluators | Sys + Res | Current practice (code/tests); active research elsewhere | Broad | Automated evaluators inside evolutionary search; symbolic verifiers for plans and proofs | `[X14–X17]` |
| Coding agents | Agents editing repositories and running tools under supervision | Sys + Eng | Current practice | Broad | Very high adoption of AI coding assistance (agent use markedly lower) with mixed measured productivity; repository-level agent instruction files as emerging convention | `[E27, E28, E13]` |
| Computer-use agents | Agents operating GUIs | Res + Sys | Experimental to emerging | Role | Long-horizon workflows mostly fail; step inefficiency and latency block practical use | `[E29]` |
| AI research / ML engineering agents | Agents replicating papers or running ML pipelines | Res | Emerging | Research | Below human experts on paper replication | `[A13, A7]` |

[⬆ Back to Contents](#contents)

### C14. Embodied and Interactive AI

**Definition and purpose.** AI that perceives and acts in physical or simulated environments: vision-language-action (VLA) models, world models for planning and simulation, sim-to-real transfer, and learned locomotion/manipulation.

**Why it belongs.** It is a distinct and fast-moving research line in AAAI/IJCAI robotics areas `[G1, G9]`. It combines C5–C8 in ways not covered elsewhere `[X21, X19, D14, D20]`.

**Relationships.** Depends on C5 (self-supervised vision), C6 (flow-matching actions, world models), C7 (VLMs), C8 (RL, imitation). Boundary with robotics and control engineering (see **H**).

**Maturity:** Emerging / experimental. **Relevance:** Spec / Research.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Vision-language-action models | Policies mapping perception + language to actions | Res + Sys | Emerging (narrow deployment) | Spec | Action representations: discrete tokens vs continuous flow; small CPU-capable variants | `[X21]` |
| World models | Learned environment simulators (pixel-generative or latent-predictive) | Res | Experimental / active research | Research | Interactive generated worlds; latent world models enabling zero-shot robot planning | `[D20, D14]` |
| Sim-to-real reinforcement learning | Training in simulation with domain randomization and transferring to hardware | Sci + Eng | Current practice (locomotion) | Spec | Very fast single-GPU humanoid training | `[X19]` |

[⬆ Back to Contents](#contents)

### C15. Evaluation Science

**Definition and purpose.** The design, execution and interpretation of evaluations of AI systems: classical metrics and validation, benchmark design and construct validity, contamination and saturation, statistical rigor, automated (LLM) judges, human evaluation, capability and agentic evaluation, and application-level evaluation in production.

**Why it belongs.**

- It is now an explicit scientific object: NeurIPS 2026 "Evaluations & Datasets" `[G8]`; AAAI-27 evaluation and auditing keywords `[G2]`.
- A review of 445 LLM benchmarks found nearly all had weaknesses in at least one area of construct validity `[T1]`.
- The International AI Safety Report 2026 states that pre-deployment test performance does not reliably predict real-world utility or risk `[G12]`.
- Practitioners report evaluation and error analysis as a dominant share of AI application development effort `[E15]`.

**Relationships.** Depends on C2, C3, C10. Depended on by every model and system area (C4–C14), C16, C17, C18. Overlaps human-computer interaction (human evaluation) and qualitative research methods (error-analysis coding) `[E15]`.

**Maturity:** Classical methods established; foundation-model evaluation science emerging and contested. **Relevance:** Broad.

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Metrics and classical validation | Task metrics, proper scoring rules, cross-validation, calibration, slice-based error analysis | Sci + Eng | Established | Broad | Being absorbed into LLM evaluation practice | `[M19, M23]` |
| Benchmark design and construct validity | Whether a benchmark measures what it claims | Sci + Res | Emerging, consolidating | Broad | Validity checklists; audits and negative results welcomed at NeurIPS | `[T1, G8]` |
| Contamination and saturation | Test leakage into training; ceiling effects | Sci + Eng | Problem well recognized; detection active research | Broad | "Hard" benchmarks have own label-error problems; coding benchmarks retired for contamination and flawed tests | `[T2, E15, M18]` |
| Statistical rigor in evaluation | Error bars, clustered standard errors, paired comparisons, power | Sci + Eng | Current practice (late adoption) | Broad | Tooling and reporting guidance emerging | `[M22, M30]` |
| LLM-as-judge | Using models to score outputs; validating against humans | Eng + Res | Widely used; validity **active debate** | Broad | High test–retest reliability with severe position bias and unstable rankings ("reliability without validity"); criteria drift in human graders | `[T4, E16]` |
| Human evaluation | Expert and crowd judgments, annotation protocols (e.g., MQM/ESA for MT) | Sci + Eng | Established | Broad | Human judgment as calibration target for automated judges | `[X1, E15]` |
| Capability and agentic evaluation | Long-horizon task suites, time-horizon metrics, real-world task success | Sci + Res | Emerging | Role | Capability-trend metrics nearing saturation of their own task suites; evaluation awareness in models undermines behavioral tests | `[T5, G12]` |
| Application evaluation in production | Error analysis, failure taxonomies, curated regression sets, online monitoring, human review | Eng | Current practice, professionalizing | Broad | Binary pass/fail criteria per failure mode; judges validated on labeled splits | `[E15, G16]` |
| Evaluation of retrieval and ranking | See C12 IR evaluation | Sci | Established | Broad | — | `[X8]` |

[⬆ Back to Contents](#contents)

### C16. Trustworthy AI

**Definition and purpose.** Knowledge needed to make AI systems understandable, robust, fair, private, aligned with intended behavior, and secure against adversaries, together with provenance and accountability mechanisms.

**Why it belongs.**

- It appears across every taxonomy examined: AAAI ML ethics/privacy/interpretability keywords and a dedicated AI Alignment track `[G1]`; KDD "Trustworthy and Responsible Data Science" pillar `[G5]`; ACL "Safety and Alignment in LLMs" and interpretability areas `[G4]`.
- Government and standards bodies have produced technical taxonomies and guidance: NIST AI 100-2 adversarial ML taxonomy `[T20]`, NIST SP 800-226 on differential privacy `[T23]`.
- Security frameworks now exist for LLM and agentic applications `[T21, T22]`.

**Relationships.** Depends on C1–C5, C7, C15. Depended on by C13, C17, C18. Neighbors: cybersecurity, law and policy, HCI (see **H**).

**Maturity:** Heterogeneous — from established theory (differential privacy, fairness impossibility results) to active research (mechanistic interpretability, scheming). **Relevance:** Broad (security, privacy, robustness awareness), Spec/Research (interpretability, alignment research).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Post-hoc explainability | Feature attribution (SHAP, integrated gradients), saliency | Sci + Eng | Established tooling with known faithfulness problems | Broad (tabular/classical ML) | Sanity-check critiques remain relevant | `[T6]` |
| Probing | Classifiers over internal activations | Sci + Res | Current practice (research and monitoring) | Role | Linear probes outperform sparse autoencoders for detecting harmful intent out of distribution | `[T7]` |
| Mechanistic interpretability | Reverse-engineering internal computations: circuits, sparse autoencoders, transcoders, attribution graphs | Sci + Res | Active research; parts contested | Research / Spec | Attribution graphs tested by perturbation; some labs deprioritized SAE research after negative downstream results; "inner workings remain poorly understood" | `[T7–T9, G12]` |
| Chain-of-thought monitorability | Whether reasoning traces can be monitored for misbehavior | Sci + Res | Emerging; validity contested | Broad (caution) | Cross-lab position paper calls it a fragile opportunity | `[T10, D32]` |
| Robustness and distribution shift | Performance under shift; out-of-distribution detection; adversarial examples | Sci + Eng | Established problems; certified robustness research-oriented | Broad (shift awareness); Spec (adversarial training) | Attention shifted from pixel perturbations to jailbreaks and prompt injection | `[T14, T20]` |
| Fairness | Group fairness definitions, impossibility results, measurement and mitigation | Sci + Gov | Theory established; generative-AI measurement active research | Broad | Metric choice is normative and must be documented; regulatory permissions for bias detection data | `[T25, T28]` |
| Privacy | Differential privacy, federated learning, memorization and extraction, machine unlearning | Sci + Eng | DP theory established; DP LLM training emerging with large utility cost; unlearning active research and contested as compliance | Broad (memorization/disclosure risk); Spec (DP, FL) | Evaluation guidelines for DP; DP scaling laws; unlearning "not a general-purpose solution" | `[T23, T24, X27]` |
| Alignment and safety | Reward hacking, specification gaming, emergent misalignment, scheming/evaluation awareness, scalable oversight, frontier safety frameworks | Sci + Res + Gov | Reward hacking established phenomenon; others active research / experimental | Research / Role (frontier labs); Broad (fine-tuning side effects) | Reward hacking in production RL generalizing to broader misalignment; anti-scheming training reduces covert actions but increases evaluation awareness; frontier safety frameworks revised and increasingly legally required | `[T11–T13, D37, G12]` |
| AI security: prompt injection and jailbreaks | Untrusted content interpreted as instructions | Sci + Eng | Unsolved engineering problem; architectural defenses emerging best practice | Broad | Adaptive attacks bypass most published defenses; capability/data-flow separation; limiting combinations of untrusted input, sensitive access and external action | `[T15–T17, T21]` |
| AI security: poisoning, supply chain, extraction | Training-data and model poisoning; model signing; model stealing | Sci + Eng | Active research (poisoning); current practice being adopted (signing) | Broad | A near-constant number of poisoned documents can backdoor models across sizes; model-signing specification | `[T18, T19, T20]` |
| Security taxonomies and threat modeling | OWASP LLM and Agentic Top 10s, MITRE ATLAS, NIST AML taxonomy | Eng | Current practice | Broad | Incident-weighted rankings (OWASP 2026); frequent ATLAS updates; agent runtime control standards (experimental) | `[T20–T22]` |
| Provenance and content authenticity | Signed metadata (C2PA), watermarking (e.g., SynthID), model/data documentation | Eng + Gov | Current practice; robustness to removal active research | Role (Broad under EU transparency duties) | EU code of practice on marking and labeling AI-generated content | `[T26, T27, T33]` |

[⬆ Back to Contents](#contents)

### C17. AI Engineering, Serving and Operations

**Definition and purpose.** Engineering knowledge needed to make AI capabilities run reliably, efficiently and maintainably: the ML lifecycle and MLOps, inference serving and optimization, model compression, distributed training concepts, observability, cost/latency engineering, and production feedback loops.

**Why it belongs.**

- ML-specific technical debt (entanglement, hidden feedback loops, undeclared consumers, data dependencies) was documented as distinct from general software debt `[E18]` and maps directly onto LLM systems.
- Serving foundation models introduced AI-specific systems concepts that AI engineers must reason about: KV-cache paging `[E20]`, prefill/decode disaggregation `[E21]`, speculative decoding `[E23]`, prompt caching economics `[E24]`, routing `[E25]`.
- Inference optimization is a core chapter of the AI engineering literature `[G14]`.
- Job-market analyses consistently emphasize deployment and production reliability (secondary evidence, low weight) `[G15]`.

**Relationships.** Depends on C5, C7, C10, C13, C15. Depended on by C18. Boundary: CS&E owns kernels, distributed-systems theory, general DevOps (see **H**).

**Maturity:** Classical MLOps established; LLM-serving techniques current practice; standards emerging. **Relevance:** Broad (concepts), Role (implementation depth).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ML lifecycle and MLOps | Pipelines, experiment tracking, model registry, CI/CD for ML, data/model validation, maturity levels | Eng | Established | Broad | Adapted rather than superseded for LLM applications; feature stores less central for API-based LLM apps (**inference, no fresh adoption data**) | `[E19]` |
| ML technical debt | Entanglement, feedback loops, configuration debt, external-world change | Eng + Sci | Established | Broad | Prompts/configs as entangled configuration; provider model updates as external change | `[E18]` |
| Inference serving fundamentals | Batching, KV-cache memory management, prefix caching, throughput/latency trade-offs | Sys + Eng | Established / current practice | Broad (understand); Role (operate) | Cache-aware routing on Kubernetes-native stacks | `[E20, E22, E24]` |
| Advanced serving architectures | Prefill/decode disaggregation; expert parallelism for MoE | Sys | Current practice at scale | Role | Disaggregation described as default playbook in major stacks; attention–FFN disaggregation next frontier | `[E21]` |
| Speculative decoding | Draft-and-verify token generation | Sys + Eng | Current practice | Role | Successive draft-model variants with incremental gains | `[E23]` |
| Model compression | Quantization, pruning, distillation for efficiency | Sci + Eng | Current practice; compression ordering and joint evaluation active research | Broad (use); Role (depth) | Unified evaluation of pruning/quantization/distillation | `[E31, D29]` |
| Distributed training concepts | Data, tensor, pipeline, sequence/context and expert parallelism; memory sharding (ZeRO); activation recomputation | Sys + Eng | Established | Role | Large-scale empirical playbooks for multi-GPU training | `[E30]` |
| Cost and latency engineering | Token economics, caching, routing/cascades, model selection by cost | Eng | Current practice | Broad | Prompt layout as cost lever; routers reduce cost while preserving quality; multi-agent runs multiply token usage | `[E24, E25, E3]` |
| Observability and tracing | Traces/metrics for model calls, tools, retrieval, agent runs | Eng | Current practice; standard conventions emerging (not yet stable) | Broad | OpenTelemetry GenAI semantic conventions in development status; opt-in content capture for privacy | `[E17]` |
| Monitoring and drift | Detecting data/concept drift and quality regressions | Eng + Sci | Established | Broad | Extended to LLM outputs; unified with continual learning research | `[E19, X27]` |
| Durable execution for long-running AI workflows | Checkpoint/replay, deployment strategies for stateful agents | Eng | Current practice, spreading | Role | Workflow-engine integrations with agent SDKs | `[E3, E26]` |
| Production feedback loops and data flywheels | Harvesting traces and user feedback for evaluation and adaptation | Eng + Sys | Current practice | Broad | Eval-gated adaptation; risk of hidden feedback loops and synthetic-data collapse | `[G14, E18, D38]` |
| Adaptation in practice | When to prompt, retrieve, or fine-tune | Eng | Current practice | Broad | Most production agents rely on prompting; fine-tuning for narrow high-volume tasks | `[G16, D35]` |

[⬆ Back to Contents](#contents)

### C18. Human-AI Interaction, Governance and Societal Context

**Definition and purpose.** How AI systems relate to the people who use, oversee and are affected by them, and to the institutional frame they operate in: interaction design, human oversight, effects on work, standards and regulation, legal constraints on data, and environmental accounting.

**Why it belongs.**

- AAAI "Humans and AI" and "Philosophy and Ethics of AI" areas `[G1, G2]`; IJCAI Human-Centred AI track `[G9]`.
- Established human-AI interaction design guidelines, validated with practitioners `[A8]`.
- Regulatory obligations with 2025–2028 effective dates that directly determine engineering artifacts `[T27–T30]`.
- ISO/IEC terminology and lifecycle standards `[G13]`.
- Rigorous measurements show perceived and measured productivity effects of AI tools can diverge `[E27]`.

**Relationships.** Depends on C13, C15, C16. Depended on by C17 (compliance artifacts, telemetry privacy). Neighbors: HCI, law, economics, social science (see **H**).

**Maturity:** HCI guidance established; governance rapidly changing. **Relevance:** Broad (obligations and oversight), Spec (policy depth).

| Subfield | What it is and why it matters | Character | Maturity | Relevance | Current direction | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Human-AI interaction design | Setting expectations, handling errors, explanation, user control, feedback | Eng + Sci | Established guidelines | Broad | User control and human-centered evaluation emphasized in recommender and HCI communities | `[A8, G10]` |
| Human oversight and human-in-the-loop operation | Approval gates, escalation, intervention budgets | Eng + Gov | Current practice | Broad | Bounded-step agents with human intervention; human approval when risky capability combinations present | `[G16, T17]` |
| AI-assisted work and productivity evidence | Measuring effects of AI tools on professional work | Sci | Active research; mixed evidence | Broad | High adoption with low trust; randomized studies show slowdowns or null effects with wide intervals | `[E27, E28]` |
| AI regulation | EU AI Act (GPAI, transparency, high-risk), US state laws, other jurisdictions | Gov | Current / changing | Broad (obligation awareness); Spec (interpretation) | EU high-risk obligations postponed to 2027/2028; transparency and GPAI enforcement from August 2026; California frontier AI transparency law in force 2026 | `[T27, T28, T30]` |
| Risk management frameworks and standards | NIST AI RMF and generative AI profile, ISO/IEC 42001 and related standards, ISO/IEC 22989 terminology | Gov + Eng | Current practice | Role | Cyber and critical-infrastructure profiles in development | `[T29, G13]` |
| Data rights and copyright | Training-data acquisition, fair use, opt-outs | Gov | Unsettled law; engineering practice consolidating | Broad | Acquisition method (e.g., pirated sources) is a material liability distinct from training itself; EU copyright obligations for GPAI | `[T32, T28]` |
| Environmental and compute accounting | Energy, carbon and water per training run or inference | Sci + Gov | Emerging (no standard boundaries) | Role | Measurement boundary changes results by more than 2×; AI data-center capacity growth documented | `[T31, G11]` |
| Societal impact | Labor, misinformation, over-reliance, systemic risk | Gov + Sci | Active research | Awareness | Systemic risks recognized in the International AI Safety Report | `[G12, G11]` |

[⬆ Back to Contents](#contents)

### C19. AI for Science and Domain Applications

**Definition and purpose.** Application of AI in scientific and professional domains, recorded for the **transferable methodology** these domains contribute, not as a catalogue of applications.

**Why it belongs.**

- AI for Science is a named area in AAAI-27 and a KDD 2026 track `[G2, G5]`.
- The AI Index 2026 reports growing AI publications in the natural sciences `[G11]`.
- Several domains show operational deployment: ECMWF's machine-learning forecast system operational since February 2025 `[X22]`; FDA-authorized AI devices concentrated in radiology `[X25]`.

**Relationships.** Depends on C4–C7, C10, C15. Contributes back methodology to C2, C3, C15, C16.

**Maturity:** Heterogeneous. **Relevance:** Spec, with transferable lessons marked below.

| Subfield | Transferable lesson | Maturity | Relevance | Evidence |
| --- | --- | --- | --- | --- |
| Weather and climate | Probabilistic generative forecasting evaluated against strong physics baselines; ML deployed *alongside* incumbent systems | Current practice (operational) | Spec | `[X22]` |
| Structural biology | Diffusion-based structure generation; licensing constraints on scientific models; open reproductions | Current practice | Spec | `[X23]` |
| Materials and chemistry | Novelty and leakage auditing when generative models claim discovery | Emerging, contested | Spec | `[X24]` |
| Healthcare | Regulation-shaped deployment; real-patient-data evaluation gaps | Current practice (imaging); many studies lack real patient data | Spec | `[X25, G11]` |
| Mathematics and algorithm discovery | Neural generation + formal verification or automated evaluation | Active research | Research | `[X16, X17]` |
| Social science and LLM-simulated participants | Validity limits of substituting model outputs for human subjects | Active debate | Spec | `[A11]` |
| Quantum machine learning | No demonstrated advantage on classical real-world data; plausible advantage only for quantum-structured problems | Experimental / speculative | Low | `[A12]` |

[⬆ Back to Contents](#contents)

---

## D. Cross-Cutting Map

Some knowledge does not belong to one branch. Rather than duplicating it, this map records concepts that recur across areas and where they recur.

```mermaid
flowchart LR
    OPT["Optimization & gradients"] --- C4b["C4"] & C5b["C5"] & C7b["C7"] & C8b["C8"]
    EVAL["Evaluation validity & statistics"] --- C3b["C3"] & C12b["C12"] & C15b["C15"] & C19b["C19"]
    DATA["Data quality, provenance & leakage"] --- C10b["C10"] & C15c["C15"] & C16b["C16"] & C18b["C18"]
    GV["Generate-and-verify"] --- C7c["C7"] & C9b["C9"] & C13b["C13"] & C19c["C19"]
    FB["Feedback & reward"] --- C7d["C7"] & C8c["C8"] & C12c["C12"] & C17b["C17"]
```

| Cross-cutting concept | Appears in | Why it is cross-cutting | Evidence |
| --- | --- | --- | --- |
| **Optimization and gradient-based learning** | C1, C4, C5, C7, C8, C17 | Same mathematics governs classical training, deep networks, post-training RL and distillation; optimizer choice interacts with scale and precision | `[M29, D7, D27]` |
| **Probabilistic modeling and sampling** | C2, C4, C6, C7, C19 | Likelihood-based losses, generative sampling, decoding, ensemble weather forecasts, uncertainty | `[M2, D16, X22]` |
| **Representations and embeddings** | C5, C11, C12, C13, C16 | Shared vector representations power retrieval, multimodal alignment, recommendation, interpretability | `[D13, D15, X9, T8]` |
| **Generalization, distribution shift and drift** | C3, C4, C15, C16, C17, C19 | The same failure (train/deploy mismatch) appears as overfitting, benchmark invalidity, robustness failure, production drift, climate extremes | `[M8, T14, X22, E19]` |
| **Evaluation validity and statistical rigor** | C2, C3, C12, C15, C19, all model areas | Every claim about any model depends on it; recurring debates about human vs automated judges appear in MT, IR, and LLM evaluation | `[M22, X1, X8, T4]` |
| **Data quality, provenance, leakage and contamination** | C3, C7, C10, C15, C16, C18 | Label errors, contamination, poisoning and licensing are one family of data-integrity problems with scientific, security and legal faces | `[A3, M18, T18, T26]` |
| **Uncertainty and calibration** | C2, C7, C15, C16, C19 | Needed for abstention, risk control, forecasts, judge reliability | `[M19, M20, X22]` |
| **Search, planning and verification** | C7 (test-time compute), C8, C9, C13, C19 | Inference-time search, generate-and-verify loops, solvers and proof checkers as tools | `[D30, X14–X17]` |
| **Feedback, reward and preference** | C7, C8, C10, C12, C17, C18 | Human/AI preference data, verifiable rewards, bandit feedback, production data flywheels; shared risk of reward hacking and feedback loops | `[D25, D26, X18, E18, T11]` |
| **Human judgment and annotation** | C10, C15, C7, C18 | Human labels calibrate models, judges and evaluations; LLM annotators need validation against humans | `[A4, E15, E16]` |
| **Efficiency and compute scaling** | C5, C7, C17, C18 | Architectural efficiency, scaling laws, serving economics and environmental accounting are linked by compute | `[D21, E21, T31]` |
| **Context and memory** | C5 (attention), C7 (long context), C12, C13 | Finite effective attention constrains architecture, retrieval and agent design alike | `[D11, E2, E9]` |
| **Adversaries and security** | C10 (poisoning), C13 (agents), C16, C17 (supply chain) | Instruction/data channel confusion and statistical attacks cross system layers | `[T15, T18, T19]` |
| **Causality** | C2, C8, C12, C16 | Experiments, off-policy evaluation, recommender feedback loops, fairness reasoning | `[M24, M26, T25]` |
| **Discrete latent codes / vector quantization** | C6, C11 (audio codecs), C12 (semantic IDs), C7 (tokenization) | Similar quantization ideas convert continuous signals or item catalogs into token-like sequences | `[X6, X9, D24]` |
| **Diffusion / flow as general-purpose structured sampler** | C6, C11 (TTS), C14 (actions), C19 (weather, proteins, crystals) | One generative family reused across media, science and robotics | `[D16, X22–X24, X21]` |

[⬆ Back to Contents](#contents)

---

## E. Contemporary AI Engineering Map

This map extracts the engineering capabilities discovered independently (primarily from C13, C15, C16, C17) and separates **durable concepts** from **evolving practice** and **implementations**. Implementations are examples of adoption, never categories.

| Capability | Durable concept | Current but evolving | Implementation examples (not categories) | Maturity | Durability |
| --- | --- | --- | --- | --- | --- |
| System architecture | Least autonomy that solves the task; workflow vs agent | Named agent patterns | Agent SDKs and graph-orchestration libraries | Current practice | Durable |
| Context management | Finite, non-uniform attention budget; just-in-time retrieval; compaction | "Context engineering" label; memory-file conventions | Agent memory files, skills formats | Current practice | Durable concept, transient conventions |
| Structured generation | Grammar/schema-constrained decoding | Provider strict modes | Constrained-decoding libraries | Established | Durable |
| Tool use | Interface design for model callers; least privilege | Tool definitions as context cost; code-execution tool access | Individual tool servers | Current practice | Durable |
| Interoperability | Standard agent–tool and agent–agent interfaces | MCP primitives/transports (2026 deprecations); A2A v1.0 | MCP servers/gateways; A2A agent cards | Current (MCP) / emerging (A2A) | Concept durable; specs evolving |
| Retrieval | Lexical + dense retrieval, reranking, recall-oriented evaluation | Agentic search loops; contextual chunk enrichment; conditional graph retrieval | Search engines, vector indexes, reranking services | Established core; evolving practice | Durable |
| Evaluation | Error analysis, failure taxonomies, human-validated judges, regression sets, statistical reporting | LLM-as-judge methods | Evaluation platforms | Current practice | Durable |
| Observability | Distributed tracing of model, tool and retrieval calls | OpenTelemetry GenAI conventions (development status) | Tracing vendors/SDKs | Current practice | Durable concept, unstable names |
| Reliability of long-running work | Checkpoint/replay, idempotency, deployment strategies for stateful processes | Agent–workflow-engine integrations | Workflow engines | Current practice | Durable |
| Inference efficiency | Batching, KV-cache memory management, speculative execution, cache locality, prefill/decode separation, quantization | Cache-aware cluster routing | Serving engines, kernel libraries | Current practice | Durable concepts, transient engines |
| Cost governance | Token economics, caching layout, routing/cascades | Pricing structures | Provider-specific caching/pricing | Current practice | Durable concept |
| Adaptation | Prompt vs retrieve vs fine-tune trade-offs; eval-gated data flywheel; parameter-efficient tuning | LoRA configuration recipes; RL fine-tuning services | Provider fine-tuning APIs | Current practice | Durable |
| Security | Least privilege, data-flow separation, human approval, threat modeling, supply-chain integrity | OWASP LLM/Agentic lists; agent control standards | Guardrail products, model-signing tools | Current practice (architecture emerging) | Durable principles; transient products |
| Data engineering for AI | Data validation, lineage, provenance, dataset versioning, document parsing | Licensing-aware filtering; VLM document parsers | Data tooling, OCR/parsing systems | Current practice | Durable |
| MLOps | ML technical debt, training–serving skew, drift monitoring, registries, CI/CD for ML | LLMOps adaptations | Registries, feature stores | Established | Durable |
| Human oversight | Intervention budgets, approval gates, escalation | Risk-combination rules for agents | — | Current practice | Durable |
| Compliance artifacts | Documentation, transparency marking, incident reporting | EU AI Act and state-law timelines | Model/system cards | Current (changing) | Concept durable; dates transient |

**Engineering concerns that academic maps tend to miss** (from C13/C17 evidence):

1. token economics and prompt-cache layout `[E24]`;
2. deploying and resuming stateful, long-running agents `[E3]`;
3. gateways, load balancing and web application firewalls in front of tool protocols `[E12]`;
4. enterprise identity, SSO and audit for agent tooling `[E12]`;
5. specification churn and deprecation management `[E12, E17]`;
6. harness sensitivity of retrieval results `[E10]`;
7. annotation operations and ownership of quality judgments `[E15]`;
8. benchmark contamination undermining model selection `[E15, T2]`;
9. perceived vs measured productivity `[E27]`;
10. telemetry privacy `[E17]`;
11. latency making otherwise-capable agents impractical `[E29]`;
12. document parsing quality as an upstream bottleneck for retrieval `[E32]`.

> ⚠️ Engineering importance does not imply foundational scientific importance.
>
> Several capabilities above (observability conventions, protocol specifications, serving engines) are high-adoption engineering practice with limited scientific novelty, and are recorded as such.

[⬆ Back to Contents](#contents)

---

## F. Research Frontier Map

**Status wording:** *Substantial evidence* = multiple independent results point the same way; *Contested* = credible evidence on more than one side; *Speculative* = important but thin empirical base.

> ⚠️ Frontier topics below are not established knowledge.

| Frontier question | Why it remains unresolved | Status | Evidence |
| --- | --- | --- | --- |
| Does RL post-training expand reasoning capability or mainly re-weight base-model behavior? | Results differ by base model, RL duration, curriculum, contamination | Contested | `[D31, D27]` |
| Do hybrid/linear/sparse attention architectures match full attention on hard long-context reasoning at frontier scale? | Saturated benchmarks hide deficits; infrastructure immature; labs diverge | Contested | `[D8, D9, D6, D10]` |
| Why does effective context lag advertised context, and how can it be closed? | Non-uniform degradation with length, distractors, multi-turn interaction | Substantial evidence of problem; solutions open | `[D11, D2]` |
| What theory explains generalization and scaling in deep networks? | Classical theory covers linear/kernel regimes; mechanisms for deep nets partial | Active research | `[M8, M9, D3]` |
| Are emergent abilities real transitions or metric artifacts? | Depends on metric choice | Contested | `[D23]` |
| Can chain-of-thought be made faithful and monitorable? | Models omit influences; training pressure and latent reasoning could remove monitorability | Substantial evidence of problem; solutions contested | `[D32, T10]` |
| Can mechanistic interpretability provide assurance? | Negative downstream results for some tools; scalability of analyses | Contested | `[T7–T9]` |
| Can prompt injection be solved rather than contained? | Instruction and data share one channel; adaptive attacks defeat published defenses | Substantial evidence that detection alone fails; architectural approaches emerging | `[T15, T16, T17]` |
| Do alignment training results reflect alignment or evaluation awareness? | Models increasingly detect evaluation settings | Contested | `[T12, G12]` |
| How can continual learning after deployment be achieved without forgetting? | Conflicting results on RL vs SFT forgetting; editing degrades at scale | Active research | `[D36, A10]` |
| Can evaluations of long-horizon agents remain valid as capabilities grow? | Task suites saturate; confidence intervals widen; construct validity weak | Active research | `[T5, T1]` |
| Can LLM judges validly replace human judgment in evaluation (IR, MT, general)? | Reliability without validity; circularity; topic-level disagreement | Contested | `[T4, X8, X1]` |
| Do tabular and time-series foundation models robustly beat tuned classical methods? | Vendor-heavy evidence; leakage; distribution shift weaknesses | Contested | `[M11–M14, M18]` |
| Can verifiable unlearning satisfy legal erasure requirements? | Parameter removal vs output suppression differ | Contested (leaning negative) | `[T24]` |
| How far can neural theorem proving and automated algorithm discovery go beyond competitions? | Autoformalization reliability; research-level mathematics | Active research | `[X16, X17]` |
| Will world models and VLAs generalize across embodiments and tasks? | Robot data scarcity; short consistency horizons | Speculative / active research | `[X21, D20, D14]` |
| Will discrete diffusion language models reach autoregressive quality on hard reasoning? | First major releases only in 2025–2026 | Speculative | `[D19]` |
| Will latent/recursive reasoning generalize beyond puzzles? | Evidence limited to narrow tasks | Speculative | `[D33]` |
| Can AI systems conduct reliable ML research? | Replication scores below human experts | Active research | `[A13]` |
| Is there practical quantum ML advantage on classical data? | No demonstrated advantage surviving fair comparison | Speculative (currently negative) | `[A12]` |

[⬆ Back to Contents](#contents)

---

## G. Historical and Supersession Map

**Lineage chains where history explains the present** (earlier approach → limitation → improvement → modern approach → remaining problem):

| Domain | Lineage | Remaining problem | Evidence |
| --- | --- | --- | --- |
| Sequence modeling | RNN/LSTM (sequential, vanishing gradients, fixed state) → attention in encoder–decoders → Transformer (parallel, but quadratic cost and growing KV cache) → KV compression, sparse attention, SSM/linear-attention hybrids | Long-context reasoning quality; infrastructure maturity | `[D1, D6, D8, D9, D11]` |
| Generative modeling | GANs (unstable, mode collapse) → diffusion (stable, many steps) → flow matching / rectified flow (straighter paths) → one-step flows, semantic latents | Long-horizon consistency; memorization theory | `[D18, D16, D17, D3]` |
| Preference and reasoning post-training | RLHF with PPO (complex, reward hacking) → DPO (simple, offline) → RL from verifiable rewards (critic-free) → stabilized, scaled RL; rubric rewards; on-policy distillation | Capability expansion vs re-weighting; reward misspecification | `[D25–D29, D31]` |
| Scaling | Parameter-favoring laws → compute-optimal balanced scaling → inference-aware overtraining → RL and test-time compute scaling | Data limits; synthetic data effects | `[D21, D22, D30]` |
| Model generalization theory | U-shaped bias–variance → interpolating overparameterized models → double descent and benign overfitting → complexity-measure critique | Deep-network theory | `[M8, M9]` |
| Tabular learning | Linear models → trees → GBDT ensembles → tuned deep tabular models → in-context tabular foundation models | Shift robustness; independent validation | `[M10–M14]` |
| Forecasting | Per-series statistical models → global ML models (M5 competition) → deep global models → zero-shot time-series foundation models | Leakage; baseline strength | `[M16–M18]` |
| Uncertainty | Bayesian posterior predictive → scalable approximations → post-hoc calibration → conformal guarantees → conformal methods for generative models | Conditional coverage; post-training miscalibration | `[M19, M20, M27]` |
| Retrieval | TF-IDF → BM25 → dense bi-encoders → learned sparse / late interaction → LLM rerankers → agentic, reasoning-intensive retrieval | LLM-judge validity; reasoning retrieval | `[X7, X8, E10]` |
| Recommendation | Matrix factorization → two-tower → sequential transformers → semantic IDs → generative recommenders | Cold start; item churn; generality beyond a few companies | `[X9]` |
| 3D vision | Structure-from-motion → neural radiance fields → Gaussian splatting → feed-forward geometry | Generalization and editing | `[X3, X4]` |
| Explainability to interpretability | Saliency / attribution → probing → circuits → sparse autoencoders → transcoders / attribution graphs → partial retreat to probes for monitoring | Assurance value | `[T6–T9]` |
| Robustness to agent security | Adversarial examples → adversarial training → jailbreaks → prompt injection → indirect injection in agents → architectural containment | Solving vs containing injection | `[T14–T17]` |
| Evaluation | Static benchmarks → leaderboards and saturation → contamination-resistant and private sets → construct-validity and statistics critiques → capability-trend metrics → evaluation as a scientific track | Validity for agents | `[T1–T5, G8]` |
| Prompting to context | Prompt wording optimization → retrieval augmentation → tool definitions and memory → context as managed resource | Stable terminology | `[E1, E2, E8]` |

**Superseded, declining, or narrowed — qualified claims**

> ⚠️ None of the items below is "dead". Each claim is qualified by the evidence found.

| Knowledge | Claimed change | Qualification | Evidence |
| --- | --- | --- | --- |
| GANs as primary image/video generator | Narrowed role | Principled GANs remain competitive; adversarial losses persist in distillation | `[D18]` |
| Standalone RNN/LSTM | Narrowed role | Recurrence resurgent in SSM/linear-attention hybrids; essential conceptual lineage | `[D8, D10]` |
| Normalizing flows (discrete-layer) | Historically important | Ideas absorbed into continuous flows; no fresh adoption data (evidence gap) | `[M2]` |
| PPO with learned critic in reasoning RL | Narrowed | Still used for RLHF alignment | `[D26, D27]` |
| DPO as final alignment stage | Moved to intermediate stage | Still widely used | `[D12]` |
| Chinchilla-optimal as deployment target | Effectively superseded by overtraining | Still valid for training-compute-optimal loss | `[D21]` |
| VAE latents for diffusion | Challenged | Representation-encoder latents still research; VAEs still ship | `[D17]` |
| Naive one-shot top-k vector RAG as default | Declining | Vector retrieval still valuable for conceptual queries and large corpora | `[E8, E10]` |
| "Long context replaces retrieval" | Not supported as blanket strategy | Depends on model, task, retrieval quality | `[D11, E9]` |
| GraphRAG as general upgrade | Not supported | Helpful for specific global/multi-hop queries | `[X13]` |
| Phrasing-level prompt tuning as main lever | Declining in relative importance | Prompting remains dominant production approach | `[E2, G16]` |
| MCP stateful sessions, HTTP+SSE transport and some primitives | Formally deprecated (2026 spec) | Deprecation windows apply | `[E12]` |
| Colocated prefill/decode at large scale | Superseded in major stacks | Fine at small scale | `[E21]` |
| Detection-only guardrails for prompt injection | Judged insufficient | Still useful as one layer | `[T15, T17]` |
| NeRF for real-time rendering | Narrowed | Still used as helper and for geometry comparisons | `[X4]` |
| Standalone syntactic parsing / pipeline NLP as product components | Narrowed (inference; no direct measurement found) | Span-exact extraction with small encoders retains role | `[X1]` |
| Manual ontology engineering | Narrowing toward LLM-assisted construction | Validation and rigor open | `[X12]` |
| Kernel methods/SVMs as front-line predictors | Likely narrowed (low confidence) | Theoretical role persists | `[M6, M15]` |
| Neural architecture search as standalone field | Narrowed; converging with LLM-driven AutoML | HPO remains established | `[A7]` |
| GBDT "universal dominance" on tabular data | Narrowed, not superseded | Still robust default at scale and under shift | `[M12, M13, M15]` |
| Per-series statistical forecasting as state of the art | Narrowed | Mandatory baseline; sometimes competitive after leakage control | `[M16, M18]` |
| Physics-only weather forecasting | Not superseded | ML systems run alongside and depend on physics-based analyses | `[X22]` |
| Federated learning as broadly deployed | Contested | Established in narrow cross-device settings | `[X27]` |
| SWE-bench Verified as frontier coding signal | Retired by a major lab (secondary report) | Illustrates benchmark lifecycle | `[E15]` |

[⬆ Back to Contents](#contents)

---

## H. Boundary Map

Boundary question applied: *Is this knowledge primarily needed to understand, develop, evaluate, or build intelligent/data-driven systems, or primarily to build general computing systems?*

| Topic | Data & Intelligence side | Neighboring side | Placement |
| --- | --- | --- | --- |
| Automatic differentiation | Chain rule, reverse mode, gradient semantics | Computation graphs, compilers, kernels | Boundary — concept here, implementation CS&E |
| Attention efficiency (FlashAttention-style, sparse kernels) | Why IO-aware and sparse attention reduce cost | Writing GPU kernels | Boundary — reason here, kernels CS&E / ML systems specialization |
| Distributed training | Parallelism strategies and memory trade-offs as they shape model and cost decisions `[E30]` | Distributed-systems theory, collective communication implementation | Boundary |
| Inference serving | KV cache, batching, speculative decoding, disaggregation concepts and trade-offs `[E20–E23]` | Engine internals, schedulers, cluster orchestration | Boundary |
| Vector search | ANN algorithm families and recall/latency trade-offs `[E11]` | Implementing distributed vector databases | Mostly CS&E beyond algorithms |
| Data pipelines | Data validation, lineage, leakage-safe splits, curation logic `[E19, M23]` | Pipeline infrastructure, storage, orchestration | Boundary |
| Durable execution and observability | AI-specific concerns: non-determinism, token cost, content privacy `[E3, E17]` | Workflow engines, tracing infrastructure | Mostly CS&E, AI-specific layer here |
| Protocols (MCP, A2A) | Tool/context semantics for model-driven systems `[E12]` | Transport, auth (OAuth), gateways | Boundary |
| AI security | Prompt injection, poisoning, extraction, adversarial ML `[T15–T20]` | Identity, least privilege, supply-chain security, classical threat modeling | Boundary — AI-specific attacks here |
| Differential privacy | Privacy-utility trade-offs in learning `[T23]` | Theoretical CS/cryptography | Boundary |
| Information-flow control for agents | Applying to model-driven systems `[T16]` | Programming-language security theory | Boundary |
| Operations research | Decision-focused learning, learned heuristics, bandits `[A6, X17, X18]` | MIP/CP modeling theory, approximate dynamic programming | Boundary |
| Robotics and control | Learned perception, policies, world models `[X21]` | Dynamics, actuation, state estimation, safety-critical control | Boundary — specialization |
| Signal processing | Audio/image representations used by models `[X5]` | Signal theory | Boundary |
| Human-computer interaction | Human-AI interaction design, human evaluation, annotation `[A8, E15]` | General interaction design | Boundary |
| Law and policy | Obligations, dates, required artifacts `[T27–T30]` | Legal interpretation | Outside, except obligation awareness |
| Economics and game theory | Mechanism design for interacting agents, recommender economics `[X20, G10]` | Economic theory | Boundary |
| Cognitive science and linguistics | Tokenization, psycholinguistic evaluation, cognitive modeling `[G1, G4]` | Theory of mind and language | Mostly outside; specialization |
| Domain sciences | ML methodology for weather, biology, materials `[X22–X24]` | Domain validation and experiments | Specialization |
| Software engineering | AI-assisted development evidence, ML technical debt `[E18, E27]` | General software practice | Boundary |
| Quantum computing | Awareness of QML claims `[A12]` | Quantum algorithms | Outside (currently low priority) |

> ⚠️ No ambiguous area was resolved by omission; each is recorded above with its boundary.

[⬆ Back to Contents](#contents)

---

## I. Dependency Map

Major prerequisite relationships between areas (arrows point from prerequisite to dependent area). Only strong dependencies are drawn.

```mermaid
flowchart TD
    C1["C1 Math"] --> C2["C2 Statistics & Causality"]
    C1 --> C4["C4 Classical ML"]
    C2 --> C3["C3 Empirical Methodology"]
    C2 --> C4
    C4 --> C5["C5 Deep Learning"]
    C5 --> C6["C6 Generative Modeling"]
    C5 --> C7["C7 Foundation Models"]
    C6 --> C7
    C8["C8 Decision-Making & RL"] --> C7
    C10["C10 Data for AI"] --> C7
    C5 --> C11["C11 Modalities"]
    C5 --> C12["C12 Retrieval & Recommendation"]
    C2 --> C12
    C7 --> C13["C13 Compound AI Systems"]
    C12 --> C13
    C9["C9 Knowledge & Reasoning"] --> C13
    C8 --> C14["C14 Embodied AI"]
    C7 --> C14
    C3 --> C15["C15 Evaluation Science"]
    C10 --> C15
    C15 --> C16["C16 Trustworthy AI"]
    C7 --> C16
    C13 --> C17["C17 Engineering & Operations"]
    C15 --> C17
    C16 --> C18["C18 HAI & Governance"]
    C13 --> C18
    C15 --> C19["C19 AI for Science"]
    C7 --> C19
```

**Dependencies that are easy to miss** (found during the dependency audit, **J5**):

| Dependent knowledge | Hidden prerequisite | Why | Evidence |
| --- | --- | --- | --- |
| Post-training (RLHF, RLVR) | RL fundamentals: policy gradients, KL-regularized objectives, credit assignment (C8) | Post-training algorithms are RL algorithms | `[D25–D27]` |
| LLM evaluation and A/B decisions | Sampling statistics and power analysis (C2) | Many reported differences are within noise | `[M22, M30]` |
| RAG and agent search | IR fundamentals and evaluation (C12) | Retrieval bounds answer quality | `[E8, X8]` |
| Context engineering | Attention mechanics and long-context limits (C5, C7) | Explains why more context can hurt | `[D11]` |
| Prompt-injection defense | Data-flow/capability reasoning and security basics (C16, H) | Detection alone fails | `[T15, T16]` |
| Serving cost reasoning | KV cache, attention variants, MoE (C5, C17) | Architecture determines memory and latency | `[E20, D6]` |
| Fine-tuning decisions | Forgetting, emergent side effects, evaluation (C7, C15, C16) | Narrow tuning can broadly change behavior | `[D35, D37]` |
| Diffusion/flow models | Probability, ODE/SDE intuition (C1, C2) | Sampling formulations rely on them | `[D16, M2]` |
| Conformal/calibrated LLM systems | Exchangeability and coverage concepts (C2) | Guarantees are marginal and assumption-dependent | `[M20]` |
| Using LLM judges or annotators | Measurement validity and agreement statistics (C2, C15) | Judges require validation against human labels | `[T4, A4]` |
| Tabular/time-series foundation models | Classical baselines and leakage-safe validation (C3, C4) | Claimed gains depend on them | `[M12, M18]` |
| Data licensing decisions | Governance context (C18) | Legal exposure depends on acquisition method | `[T32]` |

[⬆ Back to Contents](#contents)

---

## J. Completeness Audit

Each audit was performed after an initial taxonomy existed, using **new searches** outside that taxonomy where possible.

| # | Audit | What it looked for | What it discovered | What changed | Remaining uncertainty |
| --- | --- | --- | --- | --- | --- |
| J1 | Structural blind spots | Kinds of areas a model-and-LLM-centered taxonomy would omit: data work, methodology, human factors, decision-making coupled to optimization, document inputs | Data-centric AI as established framing `[A1, A2]`; pervasive label errors `[A3]`; reproducibility checklists `[A5]`; document parsing as a RAG bottleneck `[E32]`; decision-focused learning `[A6]` | **C10 Data for AI** promoted to top-level; **C3 Empirical Methodology** created; document understanding added to C11; decision-focused learning added to C8 | Depth of data-engineering boundary coverage |
| J2 | Researcher perspective | What researchers from statistics, classical AI, IR, RL, theory, CV/speech communities would find missing or mis-grouped | Classical AI areas remain large in AAAI/IJCAI `[G1, G2, G9]`; learning theory debates `[M8, M9]`; model editing `[A10]`; AutoML convergence `[A7]`; survival analysis `[A9]`; IR evaluation disputes `[X8]` | **C9** retained as full area; IR separated as **C12**; editing added to C7; AutoML to C4; survival analysis to C2 | Coverage of evolutionary computation, cognitive architectures, argumentation (recorded as specialization, not researched in depth) |
| J3 | Engineering perspective | Real production concerns that academic maps miss | Production agent statistics `[G16]`; ML technical debt `[E18]`; serving economics `[E20–E25]`; observability standards `[E17]`; durable execution `[E26]`; distributed training playbooks `[E30]`; compression `[E31]`; human–AI interaction guidelines `[A8]` | Engineering concerns list added to **E**; distributed training and compression added to **C17**; HAI design added to **C18** | Independent production data on routing, quantization accuracy trade-offs, feature-store adoption in LLM-era teams |
| J4 | Outside current attention | Important areas neglected because attention is concentrated on LLMs/agents | Tabular learning and GBDT persistence `[M12, M15]`; forecasting/anomaly detection with statistical baselines `[M18, X10]`; recommender systems' generative shift `[X9]`; operational AI weather forecasting `[X22]`; formal theorem proving `[X16]`; causal inference and experimentation `[M24, M31]`; survival analysis `[A9]`; LLM-simulated study participants' validity limits `[A11]`; QML reality check `[A12]` | These areas kept at full or explicit depth rather than folded into "LLM applications"; C19 records transferable methodology | Limited fresh evidence for clustering, dimensionality reduction, kernel methods usage |
| J5 | Dependency analysis | Areas relying on knowledge the landscape never introduced | Post-training depends on RL; LLM evaluation depends on sampling statistics; RAG depends on IR evaluation; injection defense depends on data-flow reasoning; diffusion depends on ODE/SDE intuition | Dependency map **I** with hidden-dependency table; numerical methods row added to C1; statistics of evaluation row added to C2 | Depth required for each prerequisite is a curriculum question, deliberately not answered |
| J6 | Neighboring fields | Contributions from OR, HCI, law, economics, cognitive science, linguistics, signal processing, robotics, cybersecurity, software engineering, domain sciences | Each contributes specific concepts (see **H**) | Boundary map **H** created with explicit placement per topic | Placement of cognitive science and linguistics recorded as mostly outside; could be contested |
| J7 | Emerging future | Technically credible developments that could change the landscape | Discrete diffusion LMs `[D19]`; world models `[D20, D14]`; continual/nested learning `[D36]`; latent reasoning `[D33]`; AI research agents `[A13]`; agent interoperability governance `[E13, E14]`; relational foundation models `[X29]`; byte-level models `[D24]`; quantum ML (negative so far) `[A12]` | Recorded in **F** with emerging / frontier / speculative status; none promoted to established knowledge | Future significance intrinsically uncertain |
| J8 | Taxonomy stress test | Categories based on terminology or fashion; frameworks posing as concepts; frontier mistaken for foundations; hidden relationships | See **B — Why the Taxonomy Took This Form** | "Agents" demoted to subfield of Compound AI Systems; "context engineering" recorded as current term for a durable concept; vendor names removed from categories; evaluation made a separate area and cross-cutting; cross-cutting graph (**D**) added to expose relationships hidden by hierarchy; C7 checked for fashion-driven over-detail (retained because subfields are distinct scientific questions, but maturity labels flag contested items) | C7 and C13 are the most detailed areas partly because evidence volume is highest there; possible residual recency bias |

**Stress-test questions and answers (J8 detail):**

| Question | Answer |
| --- | --- |
| Are categories based on genuine intellectual structure or current terminology? | Mostly structure; C13's name ("compound AI systems") is itself contemporary terminology and could be renamed without changing content. |
| Are some branches disproportionately detailed because they are fashionable? | C7 and C13 are the most detailed. Justified partly by distinct open questions, but volume of 2025–2026 publications likely inflates detail. Flagged. |
| Are established fields underrepresented because they generate less news? | Partially mitigated by J4; clustering, kernels, graphical models, evolutionary computation still thinner than their historical importance. |
| Are engineering practices being confused with scientific disciplines? | Separated via knowledge-character labels and **E**'s durability column. |
| Are research frontiers mistaken for foundations? | Frontier items carry Active research / Contested / Speculative labels and are collected in **F**. |
| Are frameworks masquerading as concepts? | No framework or vendor names are categories; they appear only as evidence or examples. |
| Are vendor terms treated as universal terminology? | "Context engineering", "reasoning model", "thinking mode" are flagged as vendor-originated or product terms in **K**. |
| Are historical categories retained after usefulness disappeared? | Historical items retained only where lineage or current use justifies it (see **G**). |
| Would a graph represent some areas better? | Yes — **D** and **I** are graphs; strata in **B** are explicitly not a hierarchy. |

[⬆ Back to Contents](#contents)

---

## K. Uncertainties and Disagreements

**Unsettled terminology**

| Term(s) | Issue |
| --- | --- |
| Agent / agentic / workflow / compound AI system | Definitions vary by organization; used here as a spectrum `[E1]`. |
| Context engineering vs prompt engineering | Recent vendor-originated term; underlying constraint is measured `[E2, D11]`. |
| Reasoning model / thinking mode / test-time scaling | Product terms more than technical categories `[D30]`. |
| AI safety vs AI security vs responsible AI vs trustworthy AI | Used inconsistently across governments, labs and standards bodies; the UK institute's rename from "Safety" to "Security" illustrates the shift `[T20, G12]`. |
| Linear attention vs SSM vs recurrent vs hybrid | Mathematically related families grouped differently by sources `[D8, D10]`. |
| Sparse attention | Fixed patterns, learned token selection, and block selection all called "sparse" `[D6]`. |
| Model collapse | Used inconsistently; replace vs accumulate settings differ `[D38]`. |
| Emergence | Used for scale jumps and for training-time behaviors `[D23, D27]`. |
| World model | Pixel generators, latent predictors, and LLM internal models are not comparable `[D20, D14]`. |
| Open model | Open-weight vs fully open (data, code, checkpoints) `[D12]`. |
| Scheming / alignment faking / sandbagging / evaluation awareness | Overlapping, defined per paper `[T12]`. |
| Watermarking / marking / labeling / provenance | Differ between EU code, C2PA, and watermarking research `[T27, T33]`. |

**Conflicting evidence** — see **F** (Contested rows): RL capability expansion, hybrid attention, LLM judges, emergent abilities, interpretability tools, tabular/time-series foundation models, unlearning, alignment vs evaluation awareness, multi-agent value `[E3, E6]`, AI coding productivity `[E27, E28]`.

**Maturity uncertain**

- MCP and A2A specifications (breaking changes in 2026) `[E12, E14]`
- OpenTelemetry GenAI conventions (not stable) `[E17]`
- Muon-class optimizers at larger scale `[M29]`
- Discrete diffusion LMs `[D19]`
- Relational foundation models `[X29]`
- Generative recommenders beyond a few companies `[X9]`

**Adoption unclear**

- A2A production deployments are claimed but not named `[E14]`.
- Protocol download counts are self-reported `[E12]`.
- Enterprise agent value is disputed; widely circulated failure statistics lacked traceable primary sources and were excluded `[E33]`.
- Federated learning deployment beyond narrow settings `[X27]`.
- Feature-store relevance to LLM applications (no fresh data).

**Boundaries disputed**

- ML systems vs CS&E (serving, distributed training)
- Robotics vs embodied AI
- Cognitive science and linguistics placement
- Governance depth required of engineers

**Future significance hard to assess**

- World models
- Continual learning architectures
- Latent reasoning
- AI research automation
- Quantum ML

**Evidence-quality caveats**

1. Much architecture and post-training evidence comes from vendor technical reports with self-selected benchmarks.
2. Some RL findings are specific to one model family `[D31]`.
3. Several 2026 arXiv items are recent preprints without peer review.
4. Some regulatory details (e.g., the Official Journal citation of the EU "Digital Omnibus" amendment) were reported only by secondary sources.
5. Some model and benchmark numbers from secondary sources could not be traced to primary sources and were not relied on.

[⬆ Back to Contents](#contents)

---

## L. Sources

**Access codes:** **O** = opened/fetched directly during this research run · **A** = assessed via abstract or search-result summary of the named source · **K** = well-known primary source cited by standard identifier and not re-opened during this run. **Type:** P = primary (paper, official report, specification, official documentation, conference call) · S = secondary.

Dates are publication or last-revision dates as reported by the source; arXiv identifiers encode year and month (YYMM).

### G — Field maps and cross-field evidence

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| G1 | AAAI-26 Keywords — https://aaai.org/conference/aaai/aaai-26/keywords/ | 2025 | P | O |
| G2 | AAAI-27 Areas and Topics — https://aaai.org/conference/aaai/aaai-27/areas-and-topics/ | 2026 | P | O |
| G3 | arXiv Category Taxonomy — https://arxiv.org/category_taxonomy | current | P | O |
| G4 | ACL 2026 Call for Main Conference Papers — https://2026.aclweb.org/calls/main_conference_papers/ | 2025–26 | P | O |
| G5 | KDD 2026 Research Track Call for Papers — https://kdd2026.kdd.org/research-track-call-for-papers/ | 2025–26 | P | O |
| G6 | ICLR 2026 Call for Papers — https://iclr.cc/Conferences/2026/CallForPapers | 2025 | P | A |
| G7 | NeurIPS 2026 Call for Papers — https://neurips.cc/Conferences/2026/CallForPapers ; Evaluations & Datasets call — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets | 2026 | P | A |
| G8 | NeurIPS Blog, "Introducing the Evaluations & Datasets Track at NeurIPS 2026" — https://blog.neurips.cc/2026/03/23/introducing-the-evaluations-datasets-track-at-neurips-2026/ | 2026-03-23 | P | O |
| G9 | IJCAI-ECAI 2026 Call for Papers (Main Track) — https://2026.ijcai.org/ijcai-ecai-2026-call-for-papers-main-track/ | 2025–26 | P | A |
| G10 | ACM RecSys 2026 Call for Papers — https://recsys.acm.org/recsys26/call/ | 2026 | P | O |
| G11 | Stanford HAI, "Inside the AI Index: 12 Takeaways from the 2026 Report" — https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report ; report — https://hai.stanford.edu/ai-index/2026-ai-index-report | 2026 | P | O |
| G12 | International AI Safety Report 2026, Executive Summary — https://internationalaisafetyreport.org/publication/2026-report-executive-summary | 2026-02-03 | P | O |
| G13 | ISO/IEC 22989:2022 AI concepts and terminology — https://www.iso.org/standard/74296.html ; IEC blog on ISO/IEC 22989 and 23053 — https://www.iec.ch/blog/two-new-foundational-standards-artificial-intelligence | 2022 | P | A |
| G14 | C. Huyen, *AI Engineering* (O'Reilly, 2025), chapter summaries — https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md | 2025 | P (book) | O |
| G15 | Job-description analyses (low evidential weight) — https://aishippinglabs.com/blog/what-is-an-ai-engineer-based-on-job-descriptions ; https://axialsearch.com/insights/ai-engineering-jobs | 2026 | S | A |
| G16 | "Measuring Agents in Production", arXiv 2512.04123 — https://arxiv.org/abs/2512.04123 | 2025-12 (rev. 2026-06) | P | O |

### M — Foundations, statistics, classical ML

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| M1 | Stanford CS229 course page — https://cs229.stanford.edu/ | 2026 | P | O |
| M2 | K. Murphy, *Probabilistic Machine Learning* (Intro and Advanced Topics) — https://probml.github.io/pml-book/book1.html ; https://probml.github.io/pml-book/book2.html | 2022 / 2023 (draft rev. 2025) | P | O |
| M3 | C. Bishop & H. Bishop, *Deep Learning: Foundations and Concepts* — https://www.bishopbook.com/ | 2024 | P | O |
| M4 | S. Prince, *Understanding Deep Learning* — https://mitpress.mit.edu/9780262048644/understanding-deep-learning/ | 2023 | P | O |
| M5 | *Dive into Deep Learning*, Preliminaries — https://d2l.ai/chapter_preliminaries/index.html | current | P | O |
| M6 | Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* — https://mml-book.github.io/ | 2020 | P | O |
| M7 | Delétang et al., "Language Modeling Is Compression", arXiv 2309.10668 — https://arxiv.org/abs/2309.10668 | 2023 (ICLR 2024) | P | O |
| M8 | Belkin et al., "Reconciling modern machine-learning practice and the classical bias–variance trade-off", PNAS — https://www.pnas.org/doi/10.1073/pnas.1903070116 | 2019 | P | O |
| M9 | Curth, Jeffares, van der Schaar, "A U-turn on Double Descent", arXiv 2310.18988 — https://arxiv.org/abs/2310.18988 | 2023 (NeurIPS) | P | O |
| M10 | Grinsztajn, Oyallon, Varoquaux, "Why do tree-based models still outperform deep learning on tabular data?", arXiv 2207.08815 — https://arxiv.org/abs/2207.08815 | 2022 | P | O |
| M11 | Hollmann et al., "Accurate predictions on small data with a tabular foundation model", Nature — https://www.nature.com/articles/s41586-024-08328-6 | 2025-01 | P | A |
| M12 | TabArena, arXiv 2506.16791 — https://arxiv.org/abs/2506.16791 | 2025 (NeurIPS D&B) | P | O |
| M13 | "Realistic Evaluation of TabPFN v2 in Open Environments", arXiv 2505.16226 — https://arxiv.org/abs/2505.16226 ; TabPrep, arXiv 2606.02384 — https://arxiv.org/abs/2606.02384 | 2025 / 2026 | P | O |
| M14 | TabPFN-2.5, arXiv 2511.08667 — https://arxiv.org/abs/2511.08667 ; TabPFN-3, arXiv 2605.13986 — https://arxiv.org/abs/2605.13986 (vendor reports) | 2025 / 2026 | P (vendor) | O |
| M15 | ML Contests, "State of Machine Learning Competitions 2025" — https://mlcontests.com/state-of-machine-learning-competitions-2025/ | 2026 | S | O |
| M16 | Makridakis et al., M5 Accuracy Competition, International Journal of Forecasting — https://www.sciencedirect.com/science/article/pii/S0169207021001874 | 2022 | P | O |
| M17 | GIFT-Eval, arXiv 2410.10393 — https://arxiv.org/abs/2410.10393 ; fev-bench, arXiv 2509.26468 — https://arxiv.org/abs/2509.26468 ; Chronos-2, arXiv 2510.15821 — https://arxiv.org/abs/2510.15821 | 2024–2025 | P | O |
| M18 | Meyer et al., leakage in time-series foundation model benchmarks, arXiv 2510.13654 — https://arxiv.org/abs/2510.13654 ; R. Hyndman, "Foundation models" — https://robjhyndman.com/hyndsight/foundation_models.html | 2025–26 / 2026-08 | P / S | O |
| M19 | Guo et al., "On Calibration of Modern Neural Networks", arXiv 1706.04599 — https://arxiv.org/abs/1706.04599 | 2017 | P | K |
| M20 | Angelopoulos, Barber, Bates, "Theoretical Foundations of Conformal Prediction", arXiv 2411.11824 — https://arxiv.org/abs/2411.11824 | 2024 (rev. 2026) | P | O |
| M21 | Angelopoulos et al., "Prediction-Powered Inference", Science / arXiv 2301.09633 — https://arxiv.org/abs/2301.09633 | 2023 | P | O |
| M22 | E. Miller, "Adding Error Bars to Evals", arXiv 2411.00640 — https://arxiv.org/abs/2411.00640 | 2024-11 | P | O |
| M23 | Kapoor & Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science", Patterns — https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9 | 2023 | P | O |
| M24 | Deng et al., CUPED, WSDM — https://dl.acm.org/doi/abs/10.1145/2433396.2433413 | 2013 | P | O |
| M25 | PyWhy (DoWhy, EconML) documentation — https://www.pywhy.org/ | current | P (docs) | O |
| M26 | Saito et al., Open Bandit Dataset and Pipeline, arXiv 2008.07146 — https://arxiv.org/abs/2008.07146 | 2020 (NeurIPS 2021 D&B) | P | O |
| M27 | Papamarkou et al., "Position: Bayesian Deep Learning is Needed in the Age of Large-Scale AI", arXiv 2402.00809 — https://arxiv.org/abs/2402.00809 | 2024 (ICML) | P | O |
| M28 | Bechler-Speicher et al., graph learning position paper, arXiv 2502.14546 — https://arxiv.org/abs/2502.14546 ; RelBench, arXiv 2407.20060 — https://arxiv.org/abs/2407.20060 | 2025 / 2024 | P | O |
| M29 | K. Jordan, "Muon" — https://kellerjordan.github.io/posts/muon/ ; Liu et al., "Muon is Scalable for LLM Training", arXiv 2502.16982 — https://arxiv.org/abs/2502.16982 ; Wen et al., "Fantastic Pretraining Optimizers and Where to Find Them", arXiv 2509.02046 — https://arxiv.org/abs/2509.02046 | 2024–2025 | P / S | O |
| M30 | "Position: State-of-the-Art Claims Require State-of-the-Art Evidence", arXiv 2605.17273 — https://arxiv.org/abs/2605.17273 | 2026-05 | P | O |
| M31 | Survey of LLMs and causal reasoning, NAACL Findings 2025 — https://aclanthology.org/2025.findings-naacl.327/ | 2025 | P | A |

### D — Deep learning, generative modeling, foundation models

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| D1 | Vaswani et al., "Attention Is All You Need", arXiv 1706.03762 — https://arxiv.org/abs/1706.03762 | 2017 | P | K |
| D2 | ICLR 2026 Outstanding Papers announcement — https://blog.iclr.cc/2026/04/23/announcing-the-iclr-2026-outstanding-papers/ | 2026-04-23 | P | O |
| D3 | NeurIPS 2025 Best Paper Awards announcement — https://blog.neurips.cc/2025/11/26/announcing-the-neurips-2025-best-paper-awards/ | 2025-11-26 | P | O |
| D4 | Zhu et al., "Transformers without Normalization", CVPR 2025 — https://openaccess.thecvf.com/content/CVPR2025/html/Zhu_Transformers_without_Normalization_CVPR_2025_paper.html | 2025 | P | O |
| D5 | Manifold-constrained hyper-connections (mHC), arXiv 2512.24880 — https://arxiv.org/abs/2512.24880 | 2025-12 | P | O |
| D6 | DeepSeek-V3, arXiv 2412.19437 — https://arxiv.org/abs/2412.19437 ; DeepSeek-V3.2, arXiv 2512.02556 — https://arxiv.org/abs/2512.02556 ; DeepSeek-V4, arXiv 2606.19348 — https://arxiv.org/abs/2606.19348 | 2024–2026 | P (vendor) | O |
| D7 | Kimi K2 technical report, arXiv 2507.20534 — https://arxiv.org/abs/2507.20534 | 2025-07 | P (vendor) | O |
| D8 | Nemotron-H, arXiv 2504.03624 — https://arxiv.org/abs/2504.03624 | 2025-04 | P (vendor) | O |
| D9 | MiniMax, "Why did M2 end up as a full attention model?" — https://www.minimax.io/news/why-did-m2-end-up-as-a-full-attention-model | 2025-10-29 | P (vendor) | O |
| D10 | Mamba-3, arXiv 2603.15569 — https://arxiv.org/abs/2603.15569 ; Mamba, arXiv 2312.00752 — https://arxiv.org/abs/2312.00752 | 2026-03 / 2023 | P | O / K |
| D11 | Chroma, "Context Rot" — https://www.trychroma.com/research/context-rot | 2025-07-14 | P (technical report) | O |
| D12 | Olmo 3, arXiv 2512.13961 — https://arxiv.org/abs/2512.13961 | 2025-12 | P | O |
| D13 | DINOv3, arXiv 2508.10104 — https://arxiv.org/abs/2508.10104 | 2025-08 | P | O |
| D14 | V-JEPA 2, arXiv 2506.09985 — https://arxiv.org/abs/2506.09985 | 2025-06 | P | O |
| D15 | Qwen3 Embedding, arXiv 2506.05176 — https://arxiv.org/abs/2506.05176 | 2025-06 | P | O |
| D16 | Lipman et al., "Flow Matching for Generative Modeling", arXiv 2210.02747 — https://arxiv.org/abs/2210.02747 ; Esser et al. (SD3), arXiv 2403.03206 — https://arxiv.org/abs/2403.03206 ; MeanFlow, arXiv 2505.13447 — https://arxiv.org/abs/2505.13447 | 2022–2025 | P | K / K / O |
| D17 | Representation Autoencoders (RAE), arXiv 2510.11690 — https://arxiv.org/abs/2510.11690 | 2025-10 | P | O |
| D18 | R3GAN, arXiv 2501.05441 — https://arxiv.org/abs/2501.05441 | 2025-01 (NeurIPS 2024) | P | O |
| D19 | DiffusionGemma, arXiv 2608.00146 — https://arxiv.org/abs/2608.00146 ; discrete diffusion LM survey, arXiv 2506.13759 — https://arxiv.org/abs/2506.13759 | 2026-07 / 2025-06 | P | O / A |
| D20 | Google DeepMind, "Genie 3: A new frontier for world models" — https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/ | 2025-08 | P (vendor) | A |
| D21 | Kaplan et al., arXiv 2001.08361 — https://arxiv.org/abs/2001.08361 ; Hoffmann et al. (Chinchilla), arXiv 2203.15556 — https://arxiv.org/abs/2203.15556 ; "Beyond Chinchilla-Optimal", arXiv 2401.00448 — https://arxiv.org/abs/2401.00448 ; Epoch AI, Chinchilla replication — https://epoch.ai/publications/chinchilla-scaling-a-replication-attempt | 2020–2024 | P | K / K / O / A |
| D22 | ScaleRL, "The Art of Scaling Reinforcement Learning Compute for LLMs", arXiv 2510.13786 — https://arxiv.org/abs/2510.13786 | 2025-10 | P | O |
| D23 | Wei et al., "Emergent Abilities of LLMs", arXiv 2206.07682 — https://arxiv.org/abs/2206.07682 ; Schaeffer et al., "Are Emergent Abilities a Mirage?", arXiv 2304.15004 — https://arxiv.org/abs/2304.15004 | 2022 / 2023 | P | K / O |
| D24 | Byte Latent Transformer, arXiv 2412.09871 — https://arxiv.org/abs/2412.09871 | 2024-12 (ACL 2025) | P | O |
| D25 | Ouyang et al. (InstructGPT), arXiv 2203.02155 — https://arxiv.org/abs/2203.02155 ; Rafailov et al. (DPO), arXiv 2305.18290 — https://arxiv.org/abs/2305.18290 ; Bai et al. (Constitutional AI), arXiv 2212.08073 — https://arxiv.org/abs/2212.08073 | 2022–2023 | P | K |
| D26 | DeepSeek-R1, Nature — https://www.nature.com/articles/s41586-025-09422-z ; arXiv 2501.12948 — https://arxiv.org/abs/2501.12948 | 2025-01 / 2025-09 | P | A |
| D27 | Dr. GRPO ("Understanding R1-Zero-Like Training"), arXiv 2503.20783 — https://arxiv.org/abs/2503.20783 ; GSPO, arXiv 2507.18071 — https://arxiv.org/abs/2507.18071 | 2025 | P | O |
| D28 | "Rubrics as Rewards", arXiv 2507.17746 — https://arxiv.org/abs/2507.17746 | 2025-07 | P | O |
| D29 | Thinking Machines Lab, "On-Policy Distillation" — https://thinkingmachines.ai/blog/on-policy-distillation/ ; Qwen3 Technical Report, arXiv 2505.09388 — https://arxiv.org/abs/2505.09388 | 2025 | P | O |
| D30 | Snell et al., "Scaling LLM Test-Time Compute Optimally…", arXiv 2408.03314 — https://arxiv.org/abs/2408.03314 | 2024-08 | P | O |
| D31 | Yue et al., "Does RL Really Incentivize Reasoning Capacity…?", arXiv 2504.13837 — https://arxiv.org/abs/2504.13837 ; ProRL, arXiv 2505.24864 — https://arxiv.org/abs/2505.24864 ; "Spurious Rewards", arXiv 2506.10947 — https://arxiv.org/abs/2506.10947 | 2025 | P | O / O / A |
| D32 | Anthropic, "Reasoning Models Don't Always Say What They Think", arXiv 2505.05410 — https://arxiv.org/abs/2505.05410 | 2025-05 | P | O |
| D33 | Coconut, arXiv 2412.06769 — https://arxiv.org/abs/2412.06769 ; Tiny Recursive Model, arXiv 2510.04871 — https://arxiv.org/abs/2510.04871 | 2024 / 2025 | P | O |
| D34 | Qwen3-Omni, arXiv 2509.17765 — https://arxiv.org/abs/2509.17765 | 2025-09 | P (vendor) | O |
| D35 | Thinking Machines Lab, "LoRA Without Regret" — https://thinkingmachines.ai/blog/lora/ ; Biderman et al., "LoRA Learns Less and Forgets Less", arXiv 2405.09673 — https://arxiv.org/abs/2405.09673 | 2025-09 / 2024 | P | O |
| D36 | "RL's Razor", arXiv 2509.04259 — https://arxiv.org/abs/2509.04259 ; Google Research, "Introducing Nested Learning" — https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/ | 2025 | P | A |
| D37 | Betley et al., "Emergent Misalignment", arXiv 2502.17424 — https://arxiv.org/abs/2502.17424 | 2025-02 (ICML 2025; Nature 2026) | P | O |
| D38 | Shumailov et al., Nature — https://www.nature.com/articles/s41586-024-07566-y ; Gerstgrasser et al., arXiv 2410.16713 — https://arxiv.org/abs/2410.16713 ; model collapse position paper, arXiv 2503.03150 — https://arxiv.org/abs/2503.03150 | 2024–2025 | P | K / A / A |
| D39 | Google Developers Blog, "Introducing Gemma 3n" — https://developers.googleblog.com/en/introducing-gemma-3n-developer-guide/ | 2025 | P (vendor) | A |
| D40 | Apple Machine Learning Research, "The Illusion of Thinking" — https://machinelearning.apple.com/research/illusion-of-thinking | 2025-06 | P | A |
| D41 | Induction heads and abstract pattern ICL, NAACL Findings 2025 — https://aclanthology.org/2025.findings-naacl.283/ | 2025 | P | A |
| D42 | Function-vector heads and few-shot ICL, ICML 2025 (OpenReview) — https://openreview.net/forum?id=C7XmEByCFv | 2025 | P | A |

### X — Modalities, retrieval, decision-making, classical AI, domains

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| X1 | WMT25 General MT Findings — https://aclanthology.org/2025.wmt-1.22/ | 2025 | P | A |
| X2 | SAM 3, arXiv 2511.16719 — https://arxiv.org/abs/2511.16719 | 2025-11 | P (vendor) | A |
| X3 | CVPR 2025 Best Papers (VGGT) — https://cvpr.thecvf.com/Conferences/2025/BestPapersDemos | 2025 | P | A |
| X4 | 3D Gaussian Splatting survey, arXiv 2401.03890 — https://arxiv.org/abs/2401.03890 | 2024 (rev. 2025) | P | A |
| X5 | Hugging Face, Open ASR Leaderboard post — https://huggingface.co/blog/open-asr-leaderboard | 2025-11-21 | P | O |
| X6 | Moshi, arXiv 2410.00037 — https://arxiv.org/abs/2410.00037 | 2024-10 | P | A |
| X7 | BRIGHT reasoning-intensive retrieval benchmark — https://github.com/xlang-ai/BRIGHT | 2024 (ICLR 2025) | P | A |
| X8 | UMBRELA / TREC RAG LLM judging, arXiv 2411.08275 — https://arxiv.org/abs/2411.08275 ; Clarke & Dietz, "LLM-based relevance assessment still can't replace human relevance assessment", arXiv 2412.17156 — https://arxiv.org/abs/2412.17156 | 2024 (rev. 2026) | P | A / O |
| X9 | HSTU ("Actions Speak Louder than Words"), arXiv 2402.17152 — https://arxiv.org/abs/2402.17152 ; Spotify Research, semantic IDs — https://research.atspotify.com/2025/9/semantic-ids-for-generative-search-and-recommendation ; sequential-recommendation baselines, arXiv 2507.05733 — https://arxiv.org/abs/2507.05733 | 2024–2025 | P | A |
| X10 | TSB-AD time-series anomaly detection benchmark, NeurIPS 2024 D&B — https://neurips.cc/virtual/2024/poster/97690 | 2024 | P | A |
| X11 | AlphaEarth Foundations, arXiv 2507.22291 — https://arxiv.org/abs/2507.22291 | 2025-07 | P (vendor) | A |
| X12 | LLM-empowered knowledge graph construction survey, arXiv 2510.20345 — https://arxiv.org/abs/2510.20345 | 2025-10 | P | A |
| X13 | "RAG vs GraphRAG", arXiv 2502.11371 — https://arxiv.org/abs/2502.11371 ; GraphRAG-Bench, arXiv 2506.02404 / 2506.05690 — https://github.com/GraphRAG-Bench/GraphRAG-Benchmark | 2025 (ICLR 2026) | P | A |
| X14 | Valmeekam et al., PlanBench with o1, arXiv 2409.13373 — https://arxiv.org/abs/2409.13373 ; Kambhampati et al., LLM-Modulo, arXiv 2402.01817 — https://arxiv.org/abs/2402.01817 | 2024 | P | A |
| X15 | MCP-Solver, SAT 2025 (LIPIcs) — https://drops.dagstuhl.de/storage/00lipics/lipics-vol341-sat2025/LIPIcs.SAT.2025.30/LIPIcs.SAT.2025.30.pdf | 2025 | P | A |
| X16 | AlphaProof, Nature — https://www.nature.com/articles/s41586-025-09833-y ; DeepSeek-Prover-V2, arXiv 2504.21801 — https://arxiv.org/abs/2504.21801 | 2025 | P | A |
| X17 | AlphaEvolve, arXiv 2506.13131 — https://arxiv.org/abs/2506.13131 | 2025-06 | P (vendor) | A |
| X18 | "Practical Bandits: An Industry Perspective", arXiv 2302.01223 — https://arxiv.org/abs/2302.01223 | 2023 | P | A |
| X19 | Fast sim-to-real humanoid RL, arXiv 2512.01996 — https://arxiv.org/abs/2512.01996 | 2025-12 | P | A |
| X20 | Game-theoretic survey of LLM multi-agent systems, arXiv 2601.15047 — https://arxiv.org/abs/2601.15047 | 2026-01 | P | A |
| X21 | VLA survey by action tokenization, arXiv 2507.01925 — https://arxiv.org/abs/2507.01925 | 2025-07 | P | A |
| X22 | Price et al., GenCast, Nature (PubMed) — https://pubmed.ncbi.nlm.nih.gov/39633054/ ; ECMWF, "ECMWF's AI forecasts become operational" — https://www.ecmwf.int/en/about/media-centre/news/2025/ecmwfs-ai-forecasts-become-operational | 2024-12 / 2025-02 | P | A / O |
| X23 | Abramson et al., AlphaFold 3, Nature — https://www.nature.com/articles/s41586-024-07487-w | 2024-05 | P | A |
| X24 | Zeni et al., MatterGen, Nature — https://www.nature.com/articles/s41586-025-08628-5 | 2025 | P | A |
| X25 | Analysis of FDA-authorized AI-enabled medical devices (PMC) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12730494/ | 2025 | P | A |
| X26 | LLM-based active learning survey, arXiv 2502.11767 — https://arxiv.org/abs/2502.11767 | 2025-02 | P | A |
| X27 | "Federated Learning in Practice", arXiv 2410.08892 — https://arxiv.org/abs/2410.08892 ; FL deployment critique, Archives of Computational Methods in Engineering — https://link.springer.com/article/10.1007/s11831-026-10696-3 | 2024 / 2026 | P | A |
| X28 | From TinyML to tiny deep learning survey, arXiv 2506.18927 — https://arxiv.org/abs/2506.18927 | 2025-06 | P | A |
| X29 | Relational Deep Learning tutorial, KDD 2025 — https://cs.stanford.edu/people/jure/pubs/relational-deep-learning-kdd25.pdf | 2025 | P | A |

### E — Contemporary AI engineering

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| E1 | Anthropic Engineering, "Building effective agents" — https://www.anthropic.com/engineering/building-effective-agents | 2024-12-19 | P (vendor) | O |
| E2 | Anthropic Engineering, "Effective context engineering for AI agents" — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | P (vendor) | O |
| E3 | Anthropic Engineering, "How we built our multi-agent research system" — https://www.anthropic.com/engineering/multi-agent-research-system | 2025-06-13 | P (vendor) | O |
| E4 | Anthropic Engineering, "Code execution with MCP" — https://www.anthropic.com/engineering/code-execution-with-mcp | 2025-11-04 | P (vendor) | O |
| E5 | Cognition, "Multi-agents: what's actually working" — https://cognition.com/blog/multi-agents-working | 2026-04-22 | P (vendor) | O |
| E6 | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST), arXiv 2503.13657 — https://arxiv.org/abs/2503.13657 | 2025 (NeurIPS 2025 D&B) | P | O |
| E7 | JSONSchemaBench, arXiv 2501.10868 — https://arxiv.org/abs/2501.10868 ; "Let Me Speak Freely?", arXiv 2408.02442 — https://arxiv.org/abs/2408.02442 | 2025 / 2024 | P | O |
| E8 | Anthropic, "Introducing Contextual Retrieval" — https://www.anthropic.com/engineering/contextual-retrieval | 2024-09 | P (vendor) | O |
| E9 | LaRA ("No Silver Bullet for LC or RAG Routing"), arXiv 2502.09977 — https://arxiv.org/abs/2502.09977 | 2025 (ICML) | P | O |
| E10 | "Is Grep All You Need?", arXiv 2605.15184 — https://arxiv.org/abs/2605.15184 | 2026-05-14 | P | O |
| E11 | Malkov & Yashunin, HNSW, arXiv 1603.09320 — https://arxiv.org/abs/1603.09320 | 2016 | P | O |
| E12 | MCP specification release 2026-07-28 — https://blog.modelcontextprotocol.io/posts/2026-07-28/ ; MCP 2026 roadmap — https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ | 2026-07-28 / 2026-03 | P | O |
| E13 | Linux Foundation, formation of the Agentic AI Foundation — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | 2025-12-09 | P | O |
| E14 | Google, A2A donated to Linux Foundation — https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/ ; A2A joins AAIF — https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/ | 2025-06 / 2026-08-27 | P | O |
| E15 | H. Husain & S. Shankar, "LLM Evals FAQ" — https://hamel.dev/blog/posts/evals-faq/ ; SWE-bench Verified retirement report (secondary) — https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/ | 2025–2026 | S (practitioner) | O |
| E16 | Shankar et al., "Who Validates the Validators?", arXiv 2404.12272 — https://arxiv.org/abs/2404.12272 | 2024 (UIST) | P | O |
| E17 | OpenTelemetry blog, GenAI observability — https://opentelemetry.io/blog/2026/genai-observability/ | 2026 | P | O |
| E18 | Sculley et al., "Hidden Technical Debt in Machine Learning Systems", NeurIPS — https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html | 2015 | P | O |
| E19 | Google Cloud Architecture, "MLOps: Continuous delivery and automation pipelines in machine learning" — https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning | current | P (docs) | O |
| E20 | Kwon et al., PagedAttention / vLLM, arXiv 2309.06180 — https://arxiv.org/abs/2309.06180 | 2023 (SOSP) | P | O |
| E21 | Hao AI Lab, "Disaggregated Inference: 18 Months Later" — https://haoailab.com/blogs/distserve-retro/ | 2025-11-03 | P | O |
| E22 | CNCF, "Welcome llm-d to the CNCF" — https://www.cncf.io/blog/2026/03/24/welcome-llm-d-to-the-cncf-evolving-kubernetes-into-sota-ai-infrastructure/ | 2026-03-24 | P | O |
| E23 | EAGLE-3, arXiv 2503.01840 — https://arxiv.org/abs/2503.01840 | 2025-03 | P | O |
| E24 | Anthropic, Prompt caching documentation — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | current | P (docs) | O |
| E25 | RouteLLM, arXiv 2406.18665 — https://arxiv.org/abs/2406.18665 | 2024 | P | O |
| E26 | Temporal, OpenAI Agents SDK integration — https://temporal.io/blog/announcing-openai-agents-sdk-integration | 2025–2026 | P (vendor) | O |
| E27 | METR, early-2025 AI and experienced OSS developer productivity RCT — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ ; METR uplift update — https://metr.org/blog/2026-02-24-uplift-update/ | 2025-07-10 / 2026-02-24 | P | O |
| E28 | DORA State of AI-assisted Software Development 2025 — https://dora.dev/dora-report-2025/ ; Stack Overflow Developer Survey 2025, AI — https://survey.stackoverflow.co/2025/ai | 2025 | P | O |
| E29 | OSWorld 2.0, arXiv 2606.29537 — https://arxiv.org/abs/2606.29537 ; OSWorld-Human, arXiv 2506.16042 — https://arxiv.org/abs/2506.16042 | 2026-06 / 2025-06 | P | O |
| E30 | Hugging Face, "The Ultra-Scale Playbook: Training LLMs on GPU Clusters" — https://nanotron-ultrascale-playbook.static.hf.space/ | 2025-02 | P | A |
| E31 | Zhu et al., "A Survey on Model Compression for Large Language Models", TACL — https://aclanthology.org/2024.tacl-1.85/ | 2024 | P | A |
| E32 | OmniDocBench, arXiv 2412.07626 — https://arxiv.org/abs/2412.07626 | 2024-12 (CVPR 2025) | P | A |
| E33 | Gartner press release on agentic AI project cancellations (forecast) — https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 | 2025-06-25 | P (analyst) | A |

### T — Evaluation, trust, safety, security, governance

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| T1 | "Measuring what Matters: Construct Validity in LLM Benchmarks", arXiv 2511.04703 — https://arxiv.org/abs/2511.04703 | 2025-11 (NeurIPS) | P | O |
| T2 | Humanity's Last Exam, arXiv 2501.14249 — https://arxiv.org/abs/2501.14249 | 2025-01 | P | O |
| T3 | NeurIPS Blog, "From Art to Science in AI Evaluations" — https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/ | 2025-12-05 | P | O |
| T4 | Large-scale LLM-judge reliability/validity study, arXiv 2606.19544 — https://arxiv.org/abs/2606.19544 | 2026-06 | P | O |
| T5 | METR, "Measuring AI Ability to Complete Long Tasks", arXiv 2503.14499 — https://arxiv.org/abs/2503.14499 ; METR time horizons tracker — https://metr.org/time-horizons/ | 2025-03 / 2026-05 | P | O |
| T6 | Lundberg & Lee (SHAP), arXiv 1705.07874 ; Sundararajan et al. (Integrated Gradients), arXiv 1703.01365 ; Adebayo et al., "Sanity Checks for Saliency Maps", arXiv 1810.03292 — https://arxiv.org/abs/1810.03292 | 2017–2018 | P | K |
| T7 | Google DeepMind Safety Research, "Negative Results for SAEs on Downstream Tasks" — https://deepmindsafetyresearch.medium.com/negative-results-for-sparse-autoencoders-on-downstream-tasks-and-deprioritising-sae-research-6cadcfc125b9 | 2025-03 | P | O |
| T8 | Anthropic, "On the Biology of a Large Language Model" (attribution graphs) — https://transformer-circuits.pub/2025/attribution-graphs/biology.html | 2025 | P | O |
| T9 | Sharkey et al., "Open Problems in Mechanistic Interpretability", arXiv 2501.16496 — https://arxiv.org/abs/2501.16496 | 2025 (TMLR) | P | O |
| T10 | Anthropic, "Reasoning models don't always say what they think" — https://www.anthropic.com/research/reasoning-models-dont-say-think ; "Chain of Thought Monitorability" position paper, arXiv 2507.11473 — https://arxiv.org/abs/2507.11473 | 2025-04 / 2025-07 | P | O |
| T11 | "Natural Emergent Misalignment from Reward Hacking in Production RL", arXiv 2511.18397 — https://arxiv.org/abs/2511.18397 | 2025-11 | P | O |
| T12 | Apollo Research & OpenAI, "Stress Testing Deliberative Alignment for Anti-Scheming Training", arXiv 2509.15541 — https://arxiv.org/abs/2509.15541 | 2025-09 | P | O |
| T13 | Anthropic RSP v3.0 — https://www.anthropic.com/responsible-scaling-policy/rsp-v3-0 ; Google DeepMind Frontier Safety Framework v3.1 — https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf ; OpenAI Preparedness Framework v2 — https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf | 2025–2026 | P | O |
| T14 | Koh et al., WILDS, arXiv 2012.07421 ; Madry et al., arXiv 1706.06083 — https://arxiv.org/abs/1706.06083 | 2017–2020 | P | K |
| T15 | Nasr et al., "The Attacker Moves Second", arXiv 2510.09023 — https://arxiv.org/abs/2510.09023 | 2025-10 | P | O |
| T16 | Debenedetti et al., CaMeL, arXiv 2503.18813 — https://arxiv.org/abs/2503.18813 ; Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", arXiv 2506.08837 — https://arxiv.org/abs/2506.08837 | 2025 | P | O |
| T17 | Meta AI, "Agents Rule of Two" — https://ai.meta.com/blog/practical-ai-agent-security/ ; S. Willison, "The lethal trifecta" — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | 2025-10-31 / 2025-06-16 | P / S | O |
| T18 | "Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples", arXiv 2510.07192 — https://arxiv.org/abs/2510.07192 | 2025-10 | P | O |
| T19 | OpenSSF, model-signing v1.0 — https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/ | 2025-04-04 | P | O |
| T20 | NIST AI 100-2e2025, Adversarial Machine Learning taxonomy — https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf | 2025-03 | P | O |
| T21 | OWASP Top 10 for LLM Applications 2025 — https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ ; OWASP GenAI LLM Top 10 2026 — https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ ; OWASP Top 10 for Agentic Applications 2026 — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | 2024-11 / 2026-08-03 / 2025-12-09 | P | O |
| T22 | MITRE ATLAS data releases — https://github.com/mitre-atlas/atlas-data/releases | 2026-09 | P | O |
| T23 | NIST SP 800-226, Guidelines for Evaluating Differential Privacy Guarantees — https://csrc.nist.gov/pubs/sp/800/226/final ; Google Research, VaultGemma — https://research.google/blog/vaultgemma-the-worlds-most-capable-differentially-private-llm/ | 2025-03 / 2025-09 | P | O |
| T24 | Cooper et al., "Machine Unlearning Doesn't Do What You Think", arXiv 2412.06966 — https://arxiv.org/abs/2412.06966 | 2024-12 (NeurIPS 2025) | P | O |
| T25 | Kleinberg, Mullainathan, Raghavan, arXiv 1609.05807 ; Chouldechova, arXiv 1703.00056 | 2016–2017 | P | K |
| T26 | Mitchell et al., Model Cards, arXiv 1810.03993 ; Gebru et al., Datasheets for Datasets, arXiv 1803.09010 ; Longpre et al., Data Provenance Initiative, Nature Machine Intelligence — https://www.nature.com/articles/s42256-024-00878-8 ; "Consent in Crisis", arXiv 2407.14933 — https://arxiv.org/abs/2407.14933 | 2018–2024 | P | K / K / A / A |
| T27 | European Commission, Code of Practice on marking and labelling of AI-generated content — https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content | 2026-06 | P | O |
| T28 | Gibson Dunn, EU AI Act Omnibus agreement analysis — https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ ; EU AI Act implementation timeline — https://artificialintelligenceact.eu/implementation-timeline/ ; Latham & Watkins on GPAI obligations — https://www.lw.com/en/insights/eu-ai-act-gpai-model-obligations-in-force-and-final-gpai-code-of-practice-in-place | 2025–2026 | S | O |
| T29 | NIST AI Risk Management Framework — https://www.nist.gov/itl/ai-risk-management-framework | 2023 (+ profiles) | P | O |
| T30 | California SB 53 (Transparency in Frontier AI Act) — https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB53 | 2025-09 | P | O |
| T31 | Google Cloud, "Measuring the environmental impact of AI inference" — https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference | 2025-08 | P (vendor) | O |
| T32 | Bartz v. Anthropic summary (secondary) — https://en.wikipedia.org/wiki/Bartz_v._Anthropic ; U.S. Copyright Office AI reports — https://www.copyright.gov/ai/ | 2025–2026 | S / P | O |
| T33 | Dathathri et al., SynthID-Text, Nature — https://www.nature.com/articles/s41586-024-08025-4 | 2024-10 | P | K |

### A — Additions from completeness audits

| ID | Source | Date | Type | Access |
| --- | --- | --- | --- | --- |
| A1 | Zha et al., "Data-centric Artificial Intelligence: A Survey", ACM Computing Surveys — https://dl.acm.org/doi/10.1145/3711118 ; arXiv 2303.10158 | 2023 / 2025 | P | A |
| A2 | Li et al., "DataComp-LM", arXiv 2406.11794 — https://arxiv.org/abs/2406.11794 | 2024 (NeurIPS) | P | A |
| A3 | Northcutt et al., "Pervasive Label Errors in Test Sets Destabilize ML Benchmarks", arXiv 2103.14749 — https://arxiv.org/abs/2103.14749 ; "Confident Learning", JAIR — https://dl.acm.org/doi/10.1613/jair.1.12125 | 2021 | P | A |
| A4 | LLM annotation reproducibility, arXiv 2412.14461 — https://arxiv.org/abs/2412.14461 ; LLM–human annotation evaluation, arXiv 2507.00543 — https://arxiv.org/abs/2507.00543 | 2024–2025 | P | A |
| A5 | NeurIPS 2025 Call for Papers (paper checklist) — https://neurips.cc/Conferences/2025/CallForPapers ; NeurIPS 2019 Reproducibility Program report, arXiv 2003.12206 — https://arxiv.org/abs/2003.12206 | 2025 / 2020 | P | A |
| A6 | Mandi et al., "Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities", JAIR 80 — https://doi.org/10.1613/jair.1.15320 | 2024 | P | A |
| A7 | "Opportunities for AutoML in the Agentic Era" — https://link.springer.com/chapter/10.1007/978-981-92-1468-6_6 ; ML-Agent, arXiv 2505.23723 — https://arxiv.org/abs/2505.23723 | 2025 | P | A |
| A8 | Amershi et al., "Guidelines for Human-AI Interaction", CHI 2019 — https://dl.acm.org/doi/10.1145/3290605.3300233 | 2019 | P | A |
| A9 | Wiegrebe et al., "Deep Learning for Survival Analysis: A Review", arXiv 2305.14961 — https://arxiv.org/abs/2305.14961 | 2023 (AI Review 2024) | P | A |
| A10 | "Knowledge Editing for Large Language Models: A Survey", ACM Computing Surveys — https://dl.acm.org/doi/full/10.1145/3698590 ; "Model Editing at Scale leads to Gradual and Catastrophic Forgetting", arXiv 2401.07453 — https://arxiv.org/abs/2401.07453 | 2024 | P | A |
| A11 | "LLM-Based Social Simulations Require a Boundary", arXiv 2506.19806 — https://arxiv.org/abs/2506.19806 ; Science news on AI-generated participants — https://www.science.org/content/article/ai-generated-participants-can-lead-social-science-experiments-astray-study-finds | 2025 | P / S | A |
| A12 | "Quantum Machine Learning in 2026: State of the Field" (secondary) — https://postquantum.com/quantum-ai/quantum-machine-learning-reality/ ; "Quantum Deep Learning Still Needs a Quantum Leap", arXiv 2511.01253 — https://arxiv.org/abs/2511.01253 | 2025–2026 | S / P | A |
| A13 | Starace et al., "PaperBench", arXiv 2504.01848 — https://arxiv.org/abs/2504.01848 | 2025 (ICML) | P | A |

[⬆ Back to Contents](#contents)

---

## Research Record

**When:** Executed on **2026-09-17** in a single research session.

**Inputs consulted from the repository before and during the independent reconstruction:** [AGENTS.md](../AGENTS.md) (operating rules) and [prompts/landscape-research.md](../prompts/landscape-research.md) (research process). [ROADMAP.md](../ROADMAP.md) was not opened until after this report was complete; [README.md](../README.md) was not opened. No previous research reports existed in `research/`.

**Method**

```mermaid
flowchart TD
    P1["1. Discovery pass: field maps from independent communities"] --> P2["2. Candidate areas identified from recurrence across maps"]
    P2 --> P3["3. Five parallel deep-research threads (primary sources)"]
    P3 --> P4["4. Lead-researcher gap research: data-centric AI, reproducibility"]
    P4 --> P5["5. Completeness audits J1–J7 with new searches"]
    P5 --> P6["6. Cross-checks of consequential claims"]
    P6 --> P7["7. Taxonomy stress test (J8) and synthesis"]
```

1. **Discovery pass.** Sources were chosen to span communities rather than confirm a structure:
   - AAAI-26 keywords and AAAI-27 areas;
   - the arXiv category taxonomy;
   - ACL 2026, KDD 2026, ICLR 2026, NeurIPS 2026 and IJCAI-ECAI 2026 calls;
   - the Stanford AI Index 2026 and the International AI Safety Report 2026;
   - ISO/IEC 22989/23053;
   - a contemporary AI engineering text;
   - job-description analyses (low weight).

   Candidate areas were those that recurred independently across several maps.
2. **Deep research threads.** Five scoped threads ran in parallel, each instructed to use fresh primary sources, avoid repository files, avoid vendor/framework categories, and record maturity, relevance, lineage, boundaries and uncertainties:
   - (a) mathematical, statistical and classical learning foundations;
   - (b) deep learning, generative models and foundation models;
   - (c) modalities, retrieval, decision-making, classical AI, domains;
   - (d) contemporary AI engineering;
   - (e) evaluation, trustworthy AI, safety, security and governance.
3. **Gap research and audits.** New searches targeted areas outside the emerging taxonomy (see **J**).
4. **Cross-checks.** Consequential claims were re-opened at primary sources:
   - MCP 2026-07-28 specification changes `[E12]`;
   - Agentic AI Foundation formation, date and founding projects `[E13]`;
   - NeurIPS 2026 track rename rationale `[G8]`;
   - production-agent statistics `[G16]`;
   - AlphaEvolve claims `[X17]`;
   - OWASP 2026 publication date `[T21]`.

**Limitations that affect interpretation**

- **Search budget.** The session's web-search allowance was exhausted partway through the parallel research threads. Afterwards, threads verified claims by opening known primary URLs directly. Areas with thinner fresh evidence as a result:
  - kernel methods usage, clustering, dimensionality reduction;
  - off-policy evaluation recent work;
  - robotics data-scarcity evidence;
  - independent production data on routing and quantization;
  - feature-store adoption;
  - normalizing flows;
  - some computer vision/robotics conference calls (CVPR 2026 call could not be fetched).
- **Access.** Several publisher pages (Nature, ISO, some government pages) blocked full-text fetching. Their claims rest on abstracts or secondary summaries and are marked **A** in **L**.
- **One OWASP detail unverified.** The exact ordering of the OWASP GenAI LLM Top 10 2026 items was reported by the research thread from the OWASP announcement and a secondary analysis, but the lead researcher's direct fetch of the resource page showed only publication date and methodology. The ordering is therefore not reproduced in this report.
- **Vendor evidence.** Many architecture, post-training and engineering findings come from organizations reporting on their own systems. They are labeled "P (vendor)" in **L** and qualified in **C**, **F** and **K**.
- **Recency effects.** Evidence volume is highest for foundation models and agents, which may inflate their relative detail (see **J8**).
- **Excluded claims.** Statistics that could not be traced to primary sources were excluded. Examples: a widely circulated "agent deployment failure rate", an unsourced benchmark contamination percentage.

**Why the taxonomy took its final form:** see [Why the Taxonomy Took This Form](#why-the-taxonomy-took-this-form) and [J. Completeness Audit](#j-completeness-audit).

**How to challenge this baseline in a future review**

1. Re-run the discovery pass against the then-current conference calls and taxonomies and check whether the 19 areas still recur.
2. Re-open every source marked **A** or **K** that supports a Contested or Emerging label.
3. Fill the evidence gaps listed above before relying on the corresponding maturity labels.
4. Test whether any area's detail level reflects publication volume rather than intellectual structure.
5. Check the frontier rows in **F** for resolution.

[⬆ Back to Contents](#contents)

</div>
