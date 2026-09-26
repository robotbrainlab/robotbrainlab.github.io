<div align="justify">

# Targeted Resource Research — R1 to R9

| | |
| --- | --- |
| **Research type** | Targeted resource research for the nine open needs in [curriculum proposal §Q](../design/curriculum-proposal.md#q-resolved-decisions-and-targeted-research-needs) |
| **Execution date** | 2026-09-18 |
| **Fixed inputs** | [AGENTS.md](../AGENTS.md) · [PROJECT-STATE.md](../PROJECT-STATE.md) · [design/curriculum-proposal.md](../design/curriculum-proposal.md) (revision 2, decisions D1–D7) · [resource coverage audit](2026-09-18-resource-coverage-audit.md) · [ROADMAP.md](../ROADMAP.md) · [landscape](2026-09-17-data-intelligence-landscape.md) · [comparison](2026-09-17-roadmap-comparison.md) |
| **Status** | **Evidence only.** Nothing here changes the curriculum, the proposal, or `ROADMAP.md`. |

This report answers one question for each of the six unresourced blocks and three verification questions: *given the reviewed curriculum architecture, what is the smallest, strongest, evidence-supported set of resources that can actually teach the required capabilities?* The curriculum defines the requirements; resources are judged against them.

> ⚠️ Every disposition in this report is a research recommendation.
>
> Resource roles are provisional. Adoption requires human review against the curriculum proposal.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

- [A. Executive Summary](#a-executive-summary)
- [B. Research Method and Evidence Standard](#b-research-method-and-evidence-standard)
- [C. R1: Mathematics for Learning Systems](#c-r1-mathematics-for-learning-systems)
- [D. R2: Statistics, Inference and Experimentation](#d-r2-statistics-inference-and-experimentation)
- [E. R3: Compound AI Systems](#e-r3-compound-ai-systems)
- [F. R4: AI Security](#f-r4-ai-security)
- [G. R5: Evaluation Science](#g-r5-evaluation-science)
- [H. R6: Modern Serving](#h-r6-modern-serving)
- [I. R7: Existing Resource Uncertainties](#i-r7-existing-resource-uncertainties)
- [J. R8: E7 Book Versus Repository](#j-r8-e7-book-versus-repository)
- [K. R9: NLP in Action Reassessment](#k-r9-nlp-in-action-reassessment)
- [L. Cross-Resource Coverage Matrix](#l-cross-resource-coverage-matrix)
- [M. Proposed Minimal Resource Set](#m-proposed-minimal-resource-set)
- [N. Existing Baseline Resource Disposition](#n-existing-baseline-resource-disposition)
- [O. Modern Practice Reference Layer](#o-modern-practice-reference-layer)
- [P. Remaining Gaps and Uncertainty](#p-remaining-gaps-and-uncertainty)
- [Q. Resource Anti-Bloat Audit](#q-resource-anti-bloat-audit)
- [R. Research Conclusions](#r-research-conclusions)
- [S. Proposed Next Step](#s-proposed-next-step)
- [Sources](#sources)

</details>

---

## A. Executive Summary

**What was researched.** The six blocks the proposal left without an adequate resource — E2 Mathematics, E3 Statistics and Experimentation, F2 Compound AI Systems, the AI-security part of F4, F3 Evaluation Science, the modern-serving part of F5 — and three verification questions about existing resources: the publisher-blocked uncertainties from the audit (R7), book versus repository for the E7 anchor (R8), and whether *Natural Language Processing in Action* still earns learner time (R9).

**The strongest conclusions.**

1. **No block is well served by a single resource.** Every one of the six needs a small combination. That is a structural finding, not a quality judgment: in each case the required capabilities span sub-disciplines that no single author covers.
2. **E2 and E3 can be taught from durable, mostly free resources.** E2: *Dive into Deep Learning* in selected sections, Piech's *Probability for Computer Scientists* for probability, and Karpathy's micrograd lecture for reverse-mode implementation. E3: Berkeley's *Computational and Inferential Thinking* for inference, Kohavi, Tang and Xu's *Trustworthy Online Controlled Experiments* for experimentation, plus two short targeted readings for paired model comparison and calibration. **A one-resource E3 is not credible**: inference texts omit experiment failure modes and calibration; the experimentation book omits computational inference.
3. **One paid book is the strongest cross-block anchor:** Chip Huyen's *AI Engineering* (O'Reilly, 2025). Selected sections serve both F2 (structured outputs, RAG, agents, memory, architecture) and F5 (inference optimization, routing, caching) — about 127 of its roughly 500 pages. Its table of contents is verified to page level; its subsection depth is not, because the publisher blocks body text. Its agent-evaluation section is **two pages**, so it cannot carry trajectory evaluation.
4. **For F2, F3 and F4 the durable knowledge lives mainly in 2024–2026 papers and new texts, not in established textbooks.** F4 security in particular has no textbook: the architecture core is two 2025 papers — *Design Patterns for Securing LLM Agents against Prompt Injections* and CaMeL — which are the only resources found that teach containment design rather than risk lists.
5. **Evaluation science now has real teaching texts that did not exist in the baseline:** Stanford's *AI Measurement Science* textbook (free, living, updated 2026-09-07) for validity and reliability, and Hardt's *The Emerging Science of Machine Learning Benchmarks* (free online; print due 2026-10-06) for contamination, test-set reuse and why rankings rather than scores are the reliable product.
6. **Several prior audit statements are corrected** (section [I](#i-r7-existing-resource-uncertainties)): the NLP textbook *does* teach late-interaction retrieval; the ML/DL book *does* contain a post-training section covering SFT, RLHF, DPO and MCP; the operations handbook implements LLM-as-judge evaluation but has no statistics.
7. **R8:** the published book is frozen by the author's policy and stable; the repository is actively maintained but unversioned. Tokenization implemented by hand, RoPE and the KV cache are **repository-only**. Reasoning and RL are in a sequel book.
8. **R9:** *NLP in Action* no longer earns a place on the universal path as a whole book. One section — approximate-nearest-neighbour index selection and vector quantization — is the only verified teaching source for an E8 requirement, and one chapter serves the EX7 extension.

**Where one resource suffices for a sub-requirement.** Reverse-mode implementation (micrograd); experiment-design failure modes (Kohavi); containment architecture (the design-patterns paper); routing and cascades (one 2026 survey); quantization trade-off evidence (one large-scale study).

**Where combinations are required.** All six blocks, with the smallest combinations in section [M](#m-proposed-minimal-resource-set): **34 items** in the provisional normal path — 8 books or textbooks used in selected sections, 8 tutorials, guides or technical documents, and 18 papers. Three items are paid; the rest are freely available.

**Remaining uncertainty.** Subsection depth of the paid anchor; a self-published F2 text verified only indirectly; **four F2 capabilities with no teaching resource anywhere**; agent-evaluation validity, which is an unresolved research problem rather than a missing resource; the learning cost of a paper-based F4; and the ageing rate of every fast-moving item.

**Can this resource set support the reviewed architecture?** For E2, E3, F3, the F4 security layer and the F5 serving layer — **yes**, at the required depths, with the named supplements. For F2 — **partially**: its durable concepts are resourced, but four capabilities at Design depth will need curriculum-authored material. One **Architecture Concern** is recorded for human review (section [P](#p-remaining-gaps-and-uncertainty)).

[⬆ Back to Contents](#contents)

---

## B. Research Method and Evidence Standard

**Execution.** Seven parallel research threads ran on 2026-09-18 — one for each of R1–R6 and one for R7–R9 — followed by synthesis and two direct verification checks by the report author: the official table of contents of *AI Engineering*, and a text search of the freely published retrieval chapter of *Speech and Language Processing*.

**Independent discovery before comparison.** For R1–R6, each thread derived search concepts from the block's required capabilities as written in the proposal — for example "paired model comparison power analysis", "prompt injection defense design patterns", "construct validity benchmarks", "KV cache memory arithmetic" — and built a candidate set across formats (textbooks, university courses, papers, technical reports, standards, engineering guides) **before** comparing against Baseline v0 resources. No thread searched for "replacement for" an existing book. Each thread recorded which candidates came from search and which from prior knowledge; prior-knowledge candidates were then checked against primary pages or marked as unverified. Search was available to every thread this time; roughly a hundred queries were run in total.

**Source hierarchy.** Official resource page → official table of contents → author site → official repository → university course page → primary papers and technical reports → standards and specifications → strong independent analysis where primary evidence was insufficient.

**Evidence tiers** used in every table:

| Tier | Meaning |
| --- | --- |
| **Direct** | The primary page, table of contents, repository, chapter or paper section list was retrieved and read |
| **Indirect** | The source is primary but was reached only through search snippets, a summarizing fetch, or the thread's prior knowledge |
| **Uncertain** | Contents could not be verified from any primary source |

**How coverage was verified.** Tables of contents, course schedules, repository notebooks and file listings, paper section lists and, where available, full chapter text. For publishers that block automated access, the R7–R9 thread read **section headings only** from O'Reilly's table-of-contents endpoint through the desktop application's built-in browser; no paywalled body text was read. The retrieval chapter of the NLP textbook was downloaded from the authors' own site into the session scratchpad and text-searched.

**Controlling popularity and marketing bias.** Affiliate listicles, SEO "best books" pages, social media, star counts and bestseller status were excluded as evidence. One author's own book-ranking post, which ranks his own book, was used only to discover titles. Vendor engineering posts were classified as Modern Practice unless no durable alternative exists; the single exception is flagged where it occurs.

**Limitations.**

- Body text of several paid books could not be read, so depth claims for them rest on headings plus prior knowledge and are labelled accordingly.
- Several recent papers were assessed from abstracts only.
- Some 2026 course materials are not yet public.
- Coverage is not the same as pedagogical quality in use. No resource was studied end to end by a learner.
- Everything here reflects availability on 2026-09-18. Fast-moving items will age.

**Security note.** All fetched content was treated as data. Security material in particular contains example attack strings; none was acted upon.

[⬆ Back to Contents](#contents)

---

## C. R1: Mathematics for Learning Systems

**Requirement (proposal E2).** Linear algebra for representation and transformation; multivariate calculus and the chain rule; reverse-mode differentiation semantics; probability — distributions, expectation, variance, conditioning, likelihood; optimization — convexity intuition, gradient-descent behaviour, learning-rate dynamics, conditioning; entropy and cross-entropy. Target depth **Understand**, with **Implement** for gradient descent and for reverse mode on a toy graph. Not a proof course. The audit's key finding: **probability is the dependency failure** — the ML/DL book supplies refreshers for linear algebra and calculus only.

**Candidates investigated.**

| ID | Candidate | Access | Evidence | Verified relevant content | Depth | Currency | Role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **M1** | *Dive into Deep Learning* (Zhang, Lipton, Li, Smola), online v1.0.3 | Free | Direct | §2.3–2.6 linear algebra, calculus, autodiff (API-level), probability (conditioning, Bayes, expectation, variance — **no named distributions, no MLE**); §12.2 convexity; §12.3 gradient descent with divergence at η = 1.1 and preconditioning; §12.11 schedules; §22.7 maximum likelihood; §22.11 entropy, KL, cross-entropy ↔ log-likelihood. Exercises in every section | Understand; Implement for GD | Periodically Updated | **Primary (Selected Sections)** |
| **M2** | *Mathematics for Machine Learning* (Deisenroth, Faisal, Ong), 2020 | Free PDF | Direct (section contents) | Ch 2 linear algebra, ch 5 vector calculus incl. §5.6 backpropagation and autodiff, ch 6 probability incl. Gaussian and exponential family, ch 7 optimization, §8.3 MLE/MAP. **No entropy or cross-entropy section. No code in Part I** | Understand, derivation-heavy | Durable | Reference |
| **M3** | *Probability for Computer Scientists* (Piech, Stanford CS109), v0.923 | Free | Direct (TOC, MLE page); Indirect (other parts) | Conditional probability, Bayes, log probabilities; PMFs, expectation, variance; Bernoulli, binomial, Poisson, categorical, uniform, exponential, normal; joint and marginal; MLE, MAP, logistic regression. Part 4 covers sampling, bootstrap and CLT — **E3 territory** | Understand | Periodically Updated | **Supplement** |
| **M4** | micrograd and "The spelled-out intro to neural networks and backpropagation" (Karpathy) | Free, MIT licence | Direct | About 100 lines of reverse-mode autodiff over a dynamically built scalar graph, built live in a 2h25m lecture | Implement | Durable | **Selected Sections** |
| **M5** | *Deep Learning* (Goodfellow, Bengio, Courville), Part I | Free HTML | Direct (TOC) | Ch 2 linear algebra; ch 3 probability and §3.13 information theory; §4.2 poor conditioning; no exercises | Understand, terse | Durable | Reference |
| **M6** | Mathematics for ML and Data Science (DeepLearning.AI, Coursera) | Paid certificate; free audit unclear | Direct (syllabus) | Calculus, GD and backpropagation, probability through MLE and MAP; week 4 is inference and A/B testing (E3); no reverse-mode semantics, no explicit entropy module | Use → Understand | Periodically Updated | Secondary alternative |
| **M7** | Matrix Calculus for ML and Beyond (MIT 18.S096, Jan 2026) | Free | Direct (repo) | Derivatives as linear operators, forward vs reverse mode, adjoints, AD on graphs | Understand → Implement | Durable | Specialization — prerequisites exceed E2 entry |
| **M8** | CS231n "Backpropagation, Intuitions" | Free | Direct | Circuit diagrams, gate gradient patterns, matrix-multiplication gradients; no exercises | Understand | Durable | Optional supplement |
| **M9** | "Why Momentum Really Works" (Goh, Distill, 2017) | Free | Direct | Eigen-decomposed GD on quadratics, condition number, divergence bound 0 < αλ < 2 | Understand | Durable | Optional supplement |
| **M10** | CS229 "Review of Probability Theory" | Free | Direct | Twelve-page reference sheet; no likelihood, no exercises | Awareness | Durable | Reference |

Also examined and set aside: Murphy's *Probabilistic ML: An Introduction* and Blitzstein and Hwang's *Introduction to Probability* (both far beyond E2's scope); 3Blue1Brown (contents unverifiable). The ML/DL book's repository was re-checked and confirms the audit: `math_linear_algebra` and `math_differential_calculus` notebooks exist, **no probability or statistics notebook**.

**Coverage matrix** (S Strong · P Partial · I Introductory · R Reference · — None · ? Uncertain)

| E2 capability | M1 D2L | M3 Piech | M4 micrograd | M2 MML | M5 Goodfellow | M6 Coursera |
| --- | --- | --- | --- | --- | --- | --- |
| Linear algebra for representation | P | — | — | S | P | S |
| Multivariate calculus, chain rule | S | — | I | S | P | S |
| Reverse-mode semantics | P | — | **S** | P | I | I |
| Distributions | P | **S** | — | S | P | S |
| Expectation, variance, conditioning | S | S | — | S | P | S |
| Likelihood as training objective | S | S | — | P | I | P |
| Convexity, GD behaviour, learning-rate divergence | **S** | — | I | P | P | P |
| Conditioning | P | — | — | P | P | I |
| Entropy and cross-entropy | **S** | P | — | **—** | P | ? |
| Implement GD by hand | S | — | P | I | — | S |
| Implement reverse mode on a toy graph | I | — | **S** | I | — | — |

**Analysis.** No candidate combines runnable code, gentle probability and a reverse-mode implementation exercise. D2L carries optimization behaviour and the likelihood → cross-entropy → loss chain with code; its probability preliminaries introduce no distributions and no MLE, which is precisely the failure the audit found, so a probability supplement is required. Piech is the most learner-friendly free source that goes from distributions to MLE; it derives MLE in closed form only. MML was investigated seriously because of its title and its strong linear algebra and probability, but it **has no entropy or cross-entropy section and no code in Part I** — a clear case where the title would have misled.

**Overlap.** Piech Part 4 (sampling, bootstrap, CLT) overlaps E3 and should be the stopping point. *AI Engineering* ch 3 contains three pages on entropy, cross-entropy and perplexity (pp. 119–122, verified headings), which overlaps D2L §22.11 at a lighter level.

**Gaps no candidate covers well.** Conditioning tied to divergence with exercises in one place; reverse mode over vectors and tensors (vector–Jacobian products) at beginner level; linking closed-form MLE to iterative optimization.

**Provisional recommendation.** D2L selected sections (Primary) + Piech (Supplement) + micrograd (Selected Sections); MML as Reference. Thread estimate: **25–40 hours**, not timed.

**Status: Resolved.**

[⬆ Back to Contents](#contents)

---

## D. R2: Statistics, Inference and Experimentation

**Requirement (proposal E3).** Estimation and sampling variability; confidence intervals and the bootstrap; hypothesis testing and **paired model comparison on a shared test set**; power and sample size; **calibration**; online controlled experiments, randomization and experimental units, common failure modes; confounding and enough causal framing to recognize an invalid comparison. Target **Understand**, **Use** for procedures, **Implement** for the bootstrap. Descriptive statistics, ML metrics, inference, experimentation and causal inference were kept distinct throughout.

**Candidates investigated.**

| ID | Candidate | Access | Evidence | Verified relevant content | Depth | Currency | Role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **S1** | *Computational and Inferential Thinking* (Adhikari, DeNero, Wagner; Berkeley Data 8), living 2nd ed. | Free, CC BY-NC-ND, Python | Direct (TOC) | Ch 2 causality and experiments; ch 10 sampling; ch 11 hypothesis testing incl. error probabilities; ch 12 A/B testing (permutation) and RCTs; ch 13 bootstrap and CIs incl. using CIs; ch 14.4–14.6 CLT and sample size | Understand/Use; **Implement** bootstrap and permutation tests | Durable | **Primary (inference)** |
| **S2** | *Introduction to Modern Statistics* 2e (Çetinkaya-Rundel, Hardin; OpenIntro) | Free, CC BY-SA, R | Direct (TOC) | Study design; randomization, bootstrap, mathematical models, decision errors; paired means; many means | Understand/Use | Durable | Optional alternative |
| **S3** | *Think Stats* 3e (Downey) | Free, Python | Direct | Ch 8 estimation via parametric resampling; ch 9 permutation tests; **no power**, no experiment design | Understand | Durable | Alternative to S1 |
| **S4** | *Trustworthy Online Controlled Experiments* (Kohavi, Tang, Xu; Cambridge UP, 2020) | Paid; ch 1 free | Direct (TOC); Indirect (internal content) | Chs 1–3 incl. Twyman's law; 7 overall evaluation criterion; 11 observational causal studies; 14 randomization unit; 17 statistics (t-test, CIs, power, multiple testing); 18 variance reduction; 19 A/A tests; 20 triggering; 21 sample-ratio mismatch; 22 leakage and interference; 23 long-term effects. No code | Use/Design for experimentation; light Understand for statistics | Durable | **Primary (experimentation, selected chapters)** |
| **S5** | "Adding Error Bars to Evals" (Miller, arXiv 2411.00640, Nov 2024) | Free | Direct | Independent and clustered standard errors; variance reduction; **unpaired vs paired analysis of two models on shared questions**; power and minimum detectable effect | Use/Understand | Periodically Updated | **Selected Sections (read in full)** |
| **S6** | scikit-learn User Guide §1.16 Probability calibration (v1.9.1) | Free | Direct | Definition of calibration, reliability diagrams, sigmoid, isotonic and temperature scaling, Brier score and log loss | Use | Periodically Updated | **Selected Sections** |
| **S7** | "On Calibration of Modern Neural Networks" (Guo et al., ICML 2017) | Free | Direct (abstract); Indirect (sections) | Reliability diagrams, ECE/MCE, temperature scaling | Understand | Durable | **Selected Sections (§§1–3)** |
| **S8** | *Causal Inference for the Brave and True* (Facure) | Free, Python | Direct | Chs 1–3 causality, randomized experiments, statistics review; ch 4 onward econometric methods | Understand (chs 1–3) | Durable | Optional supplement; later chapters Specialization |
| **S9** | *Learning Data Science* (Lau, Gonzalez, Nolan; 2023) | Free online | Direct | Data scope and access frames; simulation and data design; theory for inference | Understand | Durable | Supplement (overlaps S1) |
| **S10** | MIT 18.05 Introduction to Probability and Statistics (2022) | Free, R | Direct (syllabus) | Frequentist and Bayesian inference, NHST, CIs, bootstrap; calculus prerequisite; no experiment design or calibration | Understand | Durable | Reference |
| **S11** | *Modern Statistics for Modern Biology* ch 6 (Holmes, Huber) | Free | Direct | Testing, p-hacking, multiple testing, FWER/FDR, with exercises | Understand | Durable | Selected Sections if multiple testing is wanted |
| **S12** | "Hitchhiker's Guide to Testing Statistical Significance in NLP" (Dror et al., ACL 2018) | Free | Direct (abstract) | Test-selection protocol by metric and setting | Use | Durable | Reference |
| **S13** | "With Little Power Comes Great Responsibility" (Card et al., EMNLP 2020) | Free | Direct (abstract) | Underpowered NLP comparisons; power-analysis notebooks | Understand | Durable | Optional supplement (motivating case) |
| **S14** | *Causal Inference: What If* (Hernán, Robins) | Free PDF | Direct | Graduate-level causal methods | Research | Durable | Reject for E3 |

Also noted without verification: Wasserman, *All of Statistics*; Stanford MS&E 226 (public notes uncertain); a calibration survey; two recent arXiv evaluation-statistics preprints.

**Coverage matrix**

| E3 capability | S1 Data 8 | S2 IMS | S3 ThinkStats | S4 Kohavi | S5 Miller | S6+S7 Calibration | S8 Facure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Estimation, sampling variability | S | S | S | P | P | — | P |
| CIs and what they do not assert | S | S | P | I | P | — | P |
| Bootstrap (Implement) | **S** | S (R) | P | I | I | — | — |
| Hypothesis testing | S | S | S | P | P | — | P |
| Paired comparison, general | ? | S | — | I | S | — | — |
| **Paired model comparison on a shared test set** | — | — | — | — | **S** | — | — |
| Power and sample size | P | P | — | P–S | **S** | — | — |
| **Calibration** | — | — | — | — | — | **S** | — |
| Online controlled experiment design | I | P | — | **S** | — | — | P |
| Randomization, experimental units | P | P | — | **S** | P | — | P |
| Experiment failure modes | — | I | — | **S** | P | — | I |
| Confounding, causal framing | P | P | ? | P | — | — | S |

**One resource or a combination?** **A combination is required, and the reason is structural.** Every inference text omits calibration, model-comparison statistics and real-world experiment failure modes (sample-ratio mismatch, randomization-unit mismatch, interference); the experimentation book has thin uncertainty treatment, no code and no ML setting; paired model comparison and evaluation power exist only in Miller; calibration exists only in the ML literature. S1 and S4 overlap only at A/B testing, and productively: S1 teaches the permutation test, S4 teaches what invalidates it at scale. S2 would cover paired tests and power better than S1, but in R with non-ML examples and at the cost of the "implement the bootstrap" target for a Python learner; S5 closes that gap in the ML setting instead.

**Overlap with other blocks.** S5 is also recommended by R5; it is **homed in E3** and cross-referenced from F3 (see [G](#g-r5-evaluation-science)). The existing NLP textbook's paired-bootstrap section (§4.11) is a useful cross-reference for a hands-on paired bootstrap, which no candidate teaches as an exercise.

**Gaps no candidate covers well.** Calibration at textbook quality with exercises, including the binning bias of ECE and calibration of LLM confidences; a paired bootstrap on per-example evaluation differences as a lab; multiple comparisons across many models; sequential testing and peeking; non-independence in LLM evaluations (only S5).

**Provisional recommendation.** S1 (Primary, chs 2, 10–13, 14.4–14.6; thread estimate 15–20 hours with coding) + S4 (Primary for experimentation, chs 1–3, 14, 17, 19, 21, 22, about 110 pages) + S5 (read in full, about 15 pages) + S6 with S7 §§1–3 (2–3 hours). Optional: S13, S8 chs 1–3, S2 paired-means sections.

**Status: Resolved**, with calibration pedagogy recorded as a gap the curriculum must fill with its own exercise.

[⬆ Back to Contents](#contents)

---

## E. R3: Compound AI Systems

**Requirement (proposal F2, Advanced, target Design).** Workflows versus agents and least autonomy; context as a finite, non-uniform budget; context management and compaction; structured generation and constrained decoding; tool-interface design and least privilege; RAG built on IR fundamentals; memory; verification and generate-and-verify with solvers and checkers as tools; human oversight, intervention budgets, approval gates; multi-agent orchestration **and the evidence that it is not a default**; standard tool and agent interfaces as a concept; evaluation of trajectories and multi-component systems. Readiness includes *diagnosing whether a failure originated in retrieval, context, tool use or generation*.

**Candidates investigated — books.**

| ID | Candidate | Access | Evidence | Verified relevant content | Depth | Binding | Currency | Role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **C1** | *AI Engineering* (Huyen, O'Reilly, 2025) | Paid; agents section free as author excerpt | **Direct (official TOC with page numbers)**; Indirect (body) | Ch 2 Structured Outputs pp. 99–105; ch 5 Context Length and Context Efficiency pp. 218–220; ch 6 RAG pp. 253–275 (architecture, retrieval algorithms, optimization), Agents pp. 275–300 (tools, planning, **failure modes and evaluation pp. 298–300**), Memory pp. 300–305; ch 10 architecture pp. 449–474 (enhance context, guardrails, router and gateway, caches, agent patterns, monitoring, orchestration) | Understand → Design | None | Periodically Updated (written late 2024) | **Primary (Selected Sections)** — also F5 |
| **C2** | *Designing Multi-Agent Systems* (Dibia, self-published 2025; digital edition updated through Aug 2026) | Paid; two chapters free | **Indirect** (partial chapter numbers) | Builds a teaching framework from scratch: agent loop, tools, structured output, memory, human input, workflows as graphs, trajectory evaluation, failure modes, protocols; states when a single agent or plain code is better | Implement → Design | Own from-scratch framework | Periodically Updated | **Provisional Primary — verification required** |
| **C3** | *The Hitchhiker's Guide to Agentic AI* (Roitman, arXiv 2606.24937, Jun–Jul 2026, 603 pp.) | Free, CC BY-SA | Indirect | Harness and context management, multi-agent architectures and protocols, evaluation, deployment; "build the least complex system that reliably passes the evaluation" | Understand → Implement | Low | New, single author, unreviewed | Reference |
| **C4** | *Generative AI Design Patterns* (Lakshmanan, Hapke, O'Reilly, 2025) | Paid | Direct (pattern list) | 32 patterns incl. Logits Masking and Grammar (constrained decoding), RAG, LLM-as-judge, reflection, tool calling, multi-agent, long-term memory | Use → Implement | Low | Periodically Updated | Optional supplement (constrained decoding) |
| **C5** | *Agentic Design Patterns* (Gullí, Springer, 2025) | Paid | Direct (description) | 21 patterns, code in LangChain, LangGraph, CrewAI, ADK | Use | **Framework-bound** | Fast-Moving | Reject (Modern Practice at most) |
| **C6** | *Building Applications with AI Agents* (Albada, O'Reilly, 2025) | Paid | Indirect | Workflows and agents; principles; multi-framework comparison chapter | Understand | Multi-framework | Periodically Updated | Reject (introductory, overlaps C1/C2) |
| **C7** | *An Illustrated Guide to AI Agents* (Grootendorst, Alammar; print due 2026-10-13) | Paid, early release | Indirect | Memory, tooling and protocols, planning and reflection, evaluating agents, multi-agent, coding agents, training agents | Understand | Low | Not final | Re-evaluate after release |

Also examined and set aside: Koenigstein, *AI Agents: The Definitive Guide* (contents unverifiable); a Packt agents-with-knowledge-graphs book (spends its length on prerequisites); a 2026 Springer *Architectures for Agentic AI* (contents unverified).

**Candidates investigated — courses.**

| ID | Candidate | Evidence | Verified relevant content | Role |
| --- | --- | --- | --- | --- |
| **C8** | Stanford CS329Z "Engineering AI Agents" (Fall 2026, starts 2026-09-23) | Direct (schedule) | Compound-AI landscape; structured I/O and context engineering; RAG; tool design and sandboxes; workflows-vs-agents taxonomy; memory; multi-agent coordination; evaluation and LLM-as-judge; safety. HW1 builds a harness from scratch with human-in-the-loop; HW2 builds an evaluation suite. **Materials not yet public** | Reference and assignment template; re-check after 2026-12 |
| **C9** | Berkeley CS294/194-196 Agentic AI MOOC (Fall 2025) | Direct | Twelve guest lectures; slides and videos public; no labs | Modern Practice |
| **C10** | CMU 11-766 LLM Applications (Spring 2026) | Direct | Strong retrieval; one lecture each on tool use and multi-agent | Reject for F2 |
| **C11** | CU Boulder CSCI 7000 Building AI Agents (Spring 2026) | Direct | Paper-critique seminar | Reject for F2 |

**Candidates investigated — papers and reports.** Evidence is Direct (abstract or page) unless stated.

| ID | Paper | Durable concept taught | Role |
| --- | --- | --- | --- |
| **C12** | Liu et al., "Lost in the Middle", TACL 2024 | Position-dependent use of long context; more context can reduce quality | **Required** |
| **C13** | Hong, Troynikov, Huber, "Context Rot", Chroma technical report, Jul 2025 | Degradation with input length across 18 models; code released; vendor report, not peer-reviewed | Optional supplement |
| **C14** | Tam et al., "Let Me Speak Freely?", EMNLP Industry 2024 | Format constraints can degrade reasoning — a constrained-decoding trade-off | Optional supplement |
| **C15** | JSONSchemaBench (2025) | Constrained-decoding engines compared on about 10,000 schemas | Reference |
| **C16** | Feng, McDonald, Zhang, "Levels of Autonomy for AI Agents", arXiv 2506.12469, 2025 | User as operator, collaborator, consultant, approver, observer; autonomy as a design decision | **Required** |
| **C17** | Kambhampati et al., "LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks", ICML 2024 | External verifiers and solvers; generate-and-verify | **Required** |
| **C18** | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST), arXiv 2503.13657 v3, Oct 2025 | Fourteen failure modes from over 1,600 traces, κ = 0.88; venue unconfirmed | Optional supplement |
| **C19** | Kim et al., "Towards a Science of Scaling Agent Systems", arXiv 2512.08296, Dec 2025 | 260 configurations; multi-agent ranges from +80.8% to −70.0% against a single agent; error amplification up to 17.2×; preprint | **Required** |
| **C20** | Kapoor et al., "AI Agents That Matter", arXiv 2407.01502, 2024 | Cost-controlled evaluation; simple baselines are Pareto-competitive | **Required** (home F2; cross-referenced from F3) |
| **C21** | Yao et al., τ-bench, arXiv 2406.12045 | pass^k reliability | Reference (concept taught in F3) |
| **C22** | Yehudai et al., survey of agent evaluation, ACL Findings, revised Apr 2026 | Map of agent-evaluation methods | Reference |
| **C23** | Sumers et al., CoALA, arXiv 2309.02427 | Memory taxonomy and action space; venue Uncertain | Optional supplement |
| **C24** | Zaharia et al., "The Shift from Models to Compound AI Systems", BAIR blog, Feb 2024 | Framing | Reference |
| **C25** | Mei et al., survey of context engineering, arXiv 2507.13334 | Literature map of over 1,400 papers | Reference |

Engineering guides examined (all Modern Practice, see [O](#o-modern-practice-reference-layer)): Anthropic "Building effective agents" (Dec 2024), "Effective context engineering for AI agents" (Sep 2025), "Writing effective tools for agents" (2025, Indirect). The design-patterns paper for prompt-injection containment and Anthropic's agent-evaluation post were also found by this thread; they are homed in [F](#f-r4-ai-security) and [G](#g-r5-evaluation-science).

**Coverage matrix**

| F2 requirement | C1 Huyen | C2 Dibia | C3 Roitman | C8 CS329Z | Required papers | Modern Practice guides |
| --- | --- | --- | --- | --- | --- | --- |
| Workflows vs agents, least autonomy | P | S | P | S | P (C16, C19, C20) | S |
| Context as finite, non-uniform budget | I (2 pp.) | P | P | P | **S** (C12) | S |
| Context management, compaction | I | P | P | P | — | S |
| Structured generation, constrained decoding | P (6 pp.) | P | ? | P | P (optional C14) | I |
| Tool-interface design, least privilege | P | S | P | S | S for privilege (homed in F4) | S for interfaces |
| RAG on IR fundamentals | **S** (22 pp.) | I | P | S | — | — |
| Memory | P (5 pp.) | P | P | P | P (optional C23) | P |
| Verification, generate-and-verify | P | P | P | P | **S** (C17) | P |
| Human oversight, intervention budgets, approval gates | I | P | ? | P | P (C16) | I |
| Multi-agent, and evidence against default | I | S/P | P | P | **S** (C19; optional C18) | P |
| Standard interfaces as a concept | — | S (spec-bound) | P | P | — | P |
| Trajectory and multi-component evaluation | I (2 pp.) | P | P | S | P (C20) | S |
| Diagnosing where a failure originated | I | P | ? | P | P (multi-agent only, C18) | I |

**Analysis.** C1 is the strongest spine for system-level understanding and is framework-free, but its page budget is revealing: agents get about 25 pages and agent evaluation two, context management two, structured outputs six. It was written in late 2024 and therefore predates the 2025 context-engineering and compaction practice. C2 is the only resource found that takes the learner through building an agent loop, tools, memory and workflows **from scratch without a framework** and states when not to use multiple agents — exactly the Implement-to-Design path F2 needs — but it is self-published, its chapter structure is verified only indirectly, and it is continuously revised. The durable evidence that F2's key judgments rest on — context degradation, autonomy as a design choice, verifier-backed planning, the conditional value of multi-agent systems, cost-controlled evaluation — lives in five papers.

**Fair competition with baseline resources.** *Hands-On Large Language Models* has one agents chapter (confirmed by R7) and a strong code-level RAG chapter (dense retrieval, reranking, BM25 comparison, retrieval and RAG evaluation); its RAG chapter and C1's RAG section overlap substantially — **one of them suffices for F2's RAG requirement**, and this research does not settle which. The *LLM Engineer's Handbook* has no agent chapter. The NLP textbook's agents chapter remains an unwritten placeholder.

**Gaps no resource covers well.**

1. Diagnosing whether a failure originated in retrieval, context, tool use or generation — nothing teaches it systematically.
2. Intervention budgets — no resource treats the budget explicitly.
3. Least autonomy as a worked decision procedure — argued by essays and evidence, not taught as a method.
4. Standard tool and agent interfaces as a durable abstraction separate from any specification.
5. Trajectory evaluation as a textbook topic (the closest structured treatments are in [G](#g-r5-evaluation-science)).

**Provisional recommendation.** C1 selected sections (Primary; ch 2 §Structured Outputs, ch 5 §Context Length and Context Efficiency, ch 6 entire, ch 10 steps 1, 2 and 5 and orchestration — about 71 pages) + C2 selected sections (Provisional Primary, **conditional on verifying its contents**; if verification fails, the Implement path becomes a curriculum-authored exercise modelled on C8's HW1) + C12, C16, C17, C19, C20 (required papers). Cross-referenced from other blocks: the prompt-injection design patterns for least privilege ([F](#f-r4-ai-security)); Anthropic's agent-evaluation post and the Agentic Benchmark Checklist for trajectory evaluation ([G](#g-r5-evaluation-science)). Optional: C13, C14, C18, C23. Reference: C3, C8, C22, C24, C25.

**Status: Partially resolved** — durable concepts are resourced; four capabilities require curriculum-authored material.

[⬆ Back to Contents](#contents)

---

## F. R4: AI Security

**Requirement (AI-specific part of proposal F4).** Prompt injection, direct and indirect, and why detection alone fails; untrusted context and content; unsafe tool use; model and data poisoning; model extraction; adversarial examples; containment; capability limitation; architectural separation; AI-specific threat modeling; attack evaluation. Target **Understand**, with **Design** for security architecture. **Boundary (decision D7):** general security foundations belong to the future CS&E roadmap and are recorded here only as declared prerequisites. A resource that is mainly a risk list is insufficient as a teaching resource.

**Candidates investigated.**

| ID | Candidate | Access | Evidence | Verified relevant content | Depth | Teaching or reference | Currency | Role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **X1** | Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", arXiv 2506.08837, v3 Jun 2025 | Free, CC BY | Direct (sections) | Six patterns (action-selector, plan-then-execute, map-reduce, dual LLM, code-then-execute, context minimization); ten case studies each with its own threat model and candidate designs; security–utility trade-offs; states that detection filters remain heuristic and cannot guarantee prevention | **Design** | **Teaching** | Patterns Durable; examples Periodically Updated | **Primary** |
| **X2** | Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL), arXiv 2503.18813, 2025 | Free; code released | Direct (abstract) | Control flow extracted from the trusted query so untrusted data cannot alter it; capabilities and policies block exfiltration; 77% of tasks with provable security vs 84% undefended on AgentDojo | Design → Implement | Teaching (reference design) | Principles Durable | **Primary companion** |
| **X3** | Greshake et al., "Not what you've signed up for", arXiv 2302.12173, 2023 | Free | Direct (abstract) | Founding account of indirect prompt injection: applications blur data and instructions; data theft, worming, information pollution | Understand | Teaching | Durable concept | **Supplement** |
| **X4** | Nasr, Carlini et al., "The Attacker Moves Second", arXiv 2510.09023, Oct 2025 | Free | Direct (abstract) | Twelve published defenses broken above 90% success with adaptive attacks; a human red-team competition defeated all defenses; static evaluation judged methodologically flawed | Understand → Research | Teaching (evaluation) | Argument Durable | **Primary (evaluation)** |
| **X5** | Carlini et al., "On Evaluating Adversarial Robustness", arXiv 1902.06705, living document | Free | Direct (abstract) | Evaluation methodology and pitfalls for robustness claims | Understand | Teaching | Durable | Optional supplement |
| **X6** | Debenedetti et al., AgentDojo, arXiv 2406.13352 | Free, open code | Direct (abstract) | 97 tasks, 629 security test cases; extensible for defenses and adaptive attacks; measures utility and attack success together | **Implement** | Lab environment | Periodically Updated | **Selected Sections (lab)** |
| **X7** | Kolter and Madry, "Adversarial Robustness — Theory and Practice", NeurIPS 2018 tutorial | Free | Direct (chapters) | Chs 1–4: linear models, adversarial examples as inner maximization (FGSM/PGD), adversarial training | Implement (Understand required) | Teaching | Durable | **Selected Sections (chs 1–4)** |
| **X8** | NIST AI 100-2 E2025, *Adversarial Machine Learning: A Taxonomy and Terminology*, Mar 2025 | Free | Direct (TOC) | Evasion, poisoning, privacy and extraction for predictive AI; supply-chain poisoning, direct and indirect prompt injection, a one-page agent-security section, evaluation for generative AI | Understand | **Reference**, but mechanism-level | Periodically Updated | **Selected Sections** (§2.1–2.4, §3.1–3.5, §4.1) |
| **X9** | Bullwinkel et al., "Lessons From Red Teaming 100 Generative AI Products", arXiv 2501.07238, Jan 2025 | Free | Direct | Threat-model ontology; red teaming is not safety benchmarking; automation plus humans | Understand | Teaching (process) | Periodically Updated | Optional supplement |
| **X10** | Souly et al., "Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples", arXiv 2510.07192, Oct 2025 | Free | Direct | About 250 poisoned documents backdoor models from 600M to 13B parameters regardless of dataset size | Understand | Teaching (corrective finding) | Fast-Moving | **Supplement** |
| **X11** | Carlini et al., "Stealing Part of a Production Language Model", arXiv 2403.06634, ICML 2024 | Free | Direct | Extracts the embedding-projection layer through production APIs; defenses | Understand | Teaching | Periodically Updated | **Supplement** |
| **X12** | UMass COMPSCI 684 Trustworthy and Responsible AI (Bagdasarian), Fall 2026 | Free syllabus; slides not public | Direct | Jailbreaks, prompt injection, multimodal adversarial examples, poisoning and backdoors, privacy attacks; eight assignments | — | Syllabus model | Periodically Updated | Reference (sequencing and assignment templates) |
| **X13** | Wilson, *The Developer's Playbook for LLM Security* (O'Reilly, 2024) | Paid | Indirect | Practitioner, organized around the OWASP list; predates the 2025 design-pattern and adaptive-attack literature | Use/Understand | Mostly reference | Ageing | Reject as primary |
| **X14** | Joseph, Nelson, Rubinstein, Tygar, *Adversarial Machine Learning* (Cambridge, 2019) | Paid | Direct (contents) | Causative and exploratory attacks; spam and network case studies | Understand | Teaching, pre-LLM | Durable but dated | Reject (X7 + X8 cover this free and better aligned) |
| **X15** | OWASP Top 10 for LLM Applications 2025; OWASP Top 10 for Agentic Applications 2026; MITRE ATLAS | Free | Indirect | Risk taxonomies and technique catalogues | Awareness | **Reference only** | Fast-Moving | Reference |

Also examined and set aside: Vorobeychik and Kantarcioglu (2018, pre-LLM); *AI-Native LLM Security* (contents blocked, appears OWASP-organized); Stanford Online XACS134 AI Security (paid, contents unverified — a candidate to re-check); commercial short courses (marketing only). Four 2025–2026 practitioner and position pieces are listed in [O](#o-modern-practice-reference-layer).

**Coverage matrix**

| Capability | X1+X2 | X3 | X4 | X6 | X7 | X8 | X10+X11 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Direct prompt injection | P | P | S | P | — | R | — |
| Indirect prompt injection, untrusted content | **S** | **S** | S | S | — | R | — |
| Why detection alone fails | **S** | I | **S** | P | P | I | — |
| Unsafe tool use | **S** | P | P | **S** | — | I | — |
| Poisoning | — | — | — | — | — | **S** | S (LLM-scale) |
| Model extraction | — | — | — | — | — | P | S (LLM-era) |
| Adversarial examples | — | — | P | — | **S** | R | — |
| Containment, capability limitation | **S** | — | — | P | — | I | — |
| Architectural separation | **S** | — | — | P | — | — | — |
| AI-specific threat modeling | **S** (per case study) | P | P | P | I | P | — |
| Attack evaluation, measuring attack success | P | — | **S** | **S** | P | P | — |

**Analysis.** No textbook teaches LLM or agent security as an engineering discipline. The Design-depth requirement — design containment rather than a detection filter — is met only by X1 with X2; everything else either explains the attack surface (X3), proves that detection-based defenses fail under adaptive attack (X4), provides the measurement environment (X6), or covers the classical attack families (X7, X8, X10, X11). The one-page agent-security section in NIST confirms that standards are not yet a teaching substitute.

**Fair competition with baseline resources.** The NLP textbook mentions prompt injection once. *NLP in Action* implements output guardrails with an early guardrail-library interface and gives red teaming about fifty lines of awareness-level prose ([K](#k-r9-nlp-in-action-reassessment)); its approach is detection filtering, which this block teaches as insufficient. *AI Engineering* ch 5 has a sixteen-page Defensive Prompt Engineering section (pp. 235–251, verified headings) at practitioner level that predates the 2025 design-pattern work — Reference.

**Declared prerequisites for the future CS&E roadmap (D7) — not taught here.** Threat-modeling foundations (assets, adversaries, trust boundaries); least privilege and privilege separation; capability-based security and zero trust; information-flow control and taint tracking; sandboxing and process isolation; authentication, authorization and scoped credentials; classical injection vulnerabilities and the confused-deputy problem; software supply-chain integrity; web and API exfiltration channels.

**Learning cost.** About 230 pages of reading across nine items plus two labs (adversarial examples and AgentDojo). This is the heaviest reading load of any block and a direct consequence of there being no textbook.

**Provisional recommendation.** X1 (Primary, whole paper, three or four case studies as design exercises) + X2 (Primary companion, threat model, design, policy and evaluation sections) + X3 (Supplement) + X4 (Primary for evaluation) + X6 (lab: baseline, one defense, one adaptive attack; report utility and attack success) + X8 (Selected Sections) + X7 (chs 1–4) + X10 + X11 (Supplements). Optional: X5, X9. Reference: X12, X15.

**Status: Resolved**, with a recorded learning-cost concern and ageing risk.

[⬆ Back to Contents](#contents)

---

## G. R5: Evaluation Science

**Requirement (proposal F3, Advanced, target Design).** Construct validity; benchmark validity; contamination and its effect on model selection; statistical comparison; model-based judges and their validation against humans; reliability versus validity; human evaluation and annotation operations; application-level regression suites, failure taxonomies, error analysis; capability evaluation; trajectory and agent evaluation; recognizing unresolved validity problems. The learner must understand **measurement**, not catalogues of benchmarks or metrics.

**Candidates investigated.**

| ID | Candidate | Access | Evidence | Verified relevant content | Measurement or catalogue | Depth | Currency | Role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **V1** | *AI Measurement Science* (Truong, Koyejo; Stanford AIMS Lab), updated 2026-09-07 | Free, CC BY-NC | Direct (index, chs 1, 5, 11, 12) | Ch 1 validity (content, criterion, construct, external, consequential; construct-irrelevant variance; contamination; differential item functioning; 6 exercises); ch 3 item response theory; ch 5 reliability (generalizability theory, κ, weighted κ, Fleiss, Krippendorff's α, LLM judges as a rater facet, test–retest; 26 exercises); ch 11 design (Goodhart, hidden test sets, construct-validity protocol); ch 12 red teaming as measurement; ch 13 lists agent evaluation as **open** | **Measurement** | Implement → Design | Periodically Updated (living) | **Primary (Selected Sections)** |
| **V2** | *The Emerging Science of Machine Learning Benchmarks* (Hardt), free online; print 2026-10-06 | Free online | Direct (chs 3, 11, 13, 14) | Ch 3 sample size and paired comparisons; ch 5 test-set reuse; ch 11 training on the test task, contamination, tune-before-test, automated judges and self-preference, human and arena evaluation; ch 14 judge bias reversing rankings, agreement is not enough, the judge becomes a target, prediction-powered inference, rubrics; thesis: the ranking, not the score, is the reliable product | **Measurement** | Understand → Design | Durable | **Primary (Selected Sections)** |
| **V3** | Bean et al., "Measuring what Matters: Construct Validity in LLM Benchmarks", NeurIPS 2025 D&B, arXiv 2511.04703 | Free | Direct (abstract) | Review of 445 benchmarks; eight recommendations and a checklist | Measurement (empirical) | Understand | Durable | **Supplement** |
| **V4** | Wallach et al., "Evaluating Generative AI Systems Is a Social Science Measurement Challenge", ICML 2025 | Free | Direct (abstract) | Background concept → systematized concept → instrument → measurement; validity lenses | Measurement | Understand | Durable | Optional supplement |
| **V5** | Salaudeen, Koyejo et al., "Measurement to Meaning", arXiv 2505.10573 | Free | Direct (abstract) | Validity attaches to the claim a score supports | Measurement | Understand | Durable | Modern Practice (overlaps V1, V4) |
| **V6** | Artstein, Poesio, "Inter-Coder Agreement for Computational Linguistics", CL 2008 | Free | Direct (metadata) | π, κ, α, weighting, interpretation | Measurement | Understand | Durable | Reference (V1 ch 5 covers the coefficients) |
| **V7** | van der Lee et al., "Best practices for the human evaluation of automatically generated text", INLG 2019 | Free | Direct (abstract) | Criteria, number of raters and items, scales, statistics, reporting | Measurement (study design) | Understand | Durable | **Supplement** |
| **V8** | Pustejovsky, Stubbs, *Natural Language Annotation for Machine Learning* (O'Reilly, 2012) | Paid | Uncertain | Annotation cycle, guidelines, adjudication | Practice | Use | Dated | Specialization only |
| **V9** | Shankar et al., "Who Validates the Validators?" (EvalGen), UIST 2024 | Free | Direct | Aligning LLM evaluators with human grades; **criteria drift** | Measurement (HCI) | Understand | Durable | Optional supplement |
| **V10** | Husain, Shankar, "AI Evals: Everything You Need to Know" (FAQ), updated 2026-09-17 | Free (course paid) | Direct | Error analysis by open then axial coding into a failure taxonomy; judge validation with 100–200 labels per failure mode, train/dev/test split, true-positive and true-negative rates; annotation operations; CI vs production monitoring; locating the first upstream failure in agent traces | Measurement-aware practice | Use → Implement | Periodically Updated | **Primary (application evaluation)** |
| **V11** | Anthropic, "Demystifying evals for AI agents", 2026-01-09 | Free | Direct | Task vs trial; pass@k vs pass^k; code, model and human graders; transcript vs outcome; capability vs regression suites; saturation | Practice | Use → Implement | **Fast-Moving** | **Selected Sections — flagged exception** (see below) |
| **V12** | Zhu et al., Agentic Benchmark Checklist, arXiv 2507.02825, rev. Aug 2025 | Free | Direct | Task validity vs outcome validity; documented flaws in widely used agent benchmarks; misestimation up to 100% | Measurement (agents) | Understand → Design | Periodically Updated | **Supplement** |
| **V13** | Biderman et al., "Lessons from the Trenches on Reproducible Evaluation", arXiv 2405.14782 | Free | Direct (abstract) | Sensitivity to evaluation setup; fair comparison | Practice | Use | Periodically Updated | Modern Practice |
| **V14** | Benchmark-contamination surveys (arXiv 2406.04244; EMNLP 2025) | Free | Indirect | Catalogues of detection methods | Catalogue | Awareness | Periodically Updated | Reference |
| **V15** | Norman et al., "Reliability without Validity", arXiv 2606.19544, Jun 2026 | Free | Direct (abstract) | Twenty-one judges; exact match overstates agreement by 33–41 points vs κ; judge rankings shift up to 14 positions by benchmark | Measurement | Understand | Fast-Moving, unreviewed | Modern Practice |
| **V16** | Jacobs, Wallach, "Measurement and Fairness", FAccT 2021 | Free | Indirect | Construct reliability and validity defined | Measurement | Understand | Durable | Reference |

Also counted from other threads and not re-listed: Miller's error-bars paper (S5, homed in E3), Kapoor et al. (C20, homed in F2), *AI Engineering* chs 3–4 (C1). Benchmark-catalogue surveys, evaluation-platform blogs and SEO explainers were rejected under the bias rules.

**Coverage matrix**

| F3 requirement | V1 AIMS | V2 Hardt | V3 Bean | V7 van der Lee | V10 H&S FAQ | V11+V12 Agent eval | S5 Miller (E3) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Construct validity | **S** | P | **S** | — | I | P | — |
| Benchmark validity | S | **S** | S | — | — | S (agentic) | — |
| Contamination → model selection | P | **S** | I | — | — | P | — |
| Statistical comparison of models | S | S | I | — | — | P | **S** |
| Judges validated against humans | S | S | — | — | **S** (procedure) | P | — |
| Reliability vs validity | **S** | P | P | P | I | — | P |
| Human evaluation, annotation operations | P (agreement) | ? (print-only chapter) | — | **S** (study design) | S (operations) | I | — |
| Regression suites, failure taxonomy, error analysis | P | — | — | — | **S** | P | — |
| Capability evaluation | **S** (IRT, adaptive testing) | P | P | — | — | P | P |
| Trajectory and agent evaluation | — (open problem) | I | — | — | I | **S** practice / P validity | P (clustered errors) |
| Unresolved validity problems | S | S | S | — | — | P | — |
| Saturation | P | P | P | — | — | I | P |

**Combination analysis — which disciplines are needed.** All five named in the task are needed, and each leaves a gap no other fills.

| Discipline | Unique contribution | Carried by |
| --- | --- | --- |
| Measurement theory and psychometrics | Construct validity; reliability vs validity; the judge as a rater | V1 |
| Empirical ML methodology | Contamination and test-task training distort rankings; test-set reuse; why saturated benchmarks stop informing | V2 (statistics already in E3 via S5) |
| NLP evaluation | The empirical state of LLM benchmark validity | V3 |
| HCI and human evaluation | Human-evaluation study design | V7 |
| Software and application evaluation | Error-analysis workflow; failure taxonomies; regression vs capability suites; agent traces | V10, V11, V12 |

**The flagged exception.** V11 is vendor-authored practice guidance and would normally sit in the Modern Practice layer. It is placed on the normal path because **no durable resource teaches trajectory-evaluation vocabulary and practice at all** — the measurement textbook lists agent evaluation as an open problem. It is paired with V12, which supplies the validity reasoning, and marked Fast-Moving.

**Fair competition with baseline resources.** The NLP textbook's §1.9 remains a good introduction to contamination, judges and Goodhart's law. The operations handbook implements an LLM-judge evaluation (R7) but has no statistics and no validity treatment — Reference. *AI Engineering* chs 3–4 (AI-as-judge pp. 136–148, evaluation pipeline pp. 200–208, verified headings) are an engineering survey rather than measurement theory — optional alternative.

**Gaps and unresolved science.** A validity theory for grading multi-step trajectories does not exist; it must be taught as an open problem. Annotation-guideline writing at a rigorous level exists only in a dated paid book or a print-only chapter. Saturation has no single strong treatment. Judge validation has no consensus protocol. See also the Architecture Concern in [P](#p-remaining-gaps-and-uncertainty) about the statistical prerequisites of V1 ch 5.

**Provisional recommendation.** V1 (ch 1; ch 5 §5.1–5.3, 5.6, 5.9, 5.12–5.13; ch 11 §11.1, 11.6, 11.8; ch 13; ch 3 as needed) + V2 (chs 5, 11, 14) + V3 + V7 + V10 + V11 + V12. Cross-referenced: S5 (from E3), C20 (from F2). Optional: V4, V6, V9, V2 chs 3 and 12.

**Status: Resolved for teachable capabilities**; trajectory-evaluation validity recorded as an open research problem rather than a missing resource.

[⬆ Back to Contents](#contents)

---

## H. R6: Modern Serving

**Requirement (serving part of proposal F5, target Understand, Design for cost reasoning).** KV-cache behaviour and memory; batching and continuous batching; prefill versus decode and disaggregation as a concept; speculative decoding; quantization trade-offs; routing and cascades; token economics and prompt caching; latency, throughput and memory; cost–quality trade-offs; serving architecture at decision depth. **Boundary:** no kernels, distributed-systems implementation, cluster administration or generic cloud infrastructure.

**Candidates investigated.**

| ID | Candidate | Access | Evidence | Verified relevant content | Depth | Boundary fit | Currency | Role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **N1** | *AI Engineering* (Huyen) ch 9 and ch 10 | Paid | **Direct (TOC with pages)**; Indirect (body) | Ch 9 pp. 405–447: inference overview, **performance metrics**, AI accelerators, model optimization, inference-service optimization; ch 10 **router and gateway** pp. 456–460, **caches** pp. 460–463, monitoring and observability pp. 465–472; ch 7 quantization pp. 328–332 | Understand → Design | Excellent | Periodically Updated | **Primary supplement** (same book as C1) |
| **N2** | Stanford CS336 Lecture 10 "Inference" (Liang; 2025 notes, 2026 videos) | Free | Direct (2025 lecture source) | Workload and metrics; arithmetic intensity of prefill vs generation; KV-cache reduction (GQA, MLA); quantization; pruning; speculative sampling; continuous batching; paged attention | Understand | Good (skip kernel lectures) | Durable | Optional alternative (fails strict removal test given N3 and N1) |
| **N3** | "All About Transformer Inference", *How To Scale Your Model* (Austin, Douglas et al., Google DeepMind, Feb 2025) | Free | Direct | KV-cache basics; prefill vs generation; decode is memory-bandwidth bound; critical batch size; GQA, local attention, quantization, paged attention; continuous batching, prefix caching, disaggregation; speculative sampling appendix; **seven worked problems** | Understand → Design | §§1, 2, 4 in scope; sharding sections are CS&E | Durable | **Selected Sections** (§§1, 2, 4; problems 1–3) |
| **N4** | kipply, "Transformer Inference Arithmetic" (2022) | Free | Direct | KV-cache formula, flops-to-bandwidth ratio, latency regimes | Understand | Good | Durable, dated numbers | Optional (subsumed by N3) |
| **N5** | efficient-dl-systems (HSE/YSDA, 2026) | Free | Direct | Week 8 inference and serving, week 9 quantization and speculative decoding; seminars drift into kernels | Implement | Partly beyond boundary | Periodically Updated | Reference (slides) |
| **N6** | MIT 6.5940 TinyML and Efficient AI Computing (Fall 2026) | Free (materials pending) | Direct (schedule) | Quantization, LLM deployment, long context; compression-research depth | Implement → Research | Partly beyond | Periodically Updated | Specialization |
| **N7** | CMU 11-868 LLM Systems | Free | Indirect | CUDA assignments, distributed training | Implement | **Beyond boundary** | — | Reject |
| **N8** | Pan, Li, "A Survey of LLM Inference Systems", arXiv 2506.21901 | Free | Direct (abstract) | Batching, paged memory, eviction, offloading, disaggregated and serverless architectures | Research | Mixed | Fast-Moving | Reference |
| **N9** | Leviathan et al. (speculative decoding, ICML 2023); Kwon et al. (PagedAttention, SOSP 2023); Zhong et al. (DistServe, OSDI 2024) | Free | Direct (abstracts) | The originating papers for three durable mechanisms | Research | Introductions only | Durable concepts | Modern Practice (introductions) |
| **N10** | Hao AI Lab, "Disaggregated Inference: 18 Months Later", Nov 2025 | Free | Indirect | Disaggregation now standard across major engines | Awareness | Good | Fast-Moving | Modern Practice |
| **N11** | Databricks, "LLM Inference Performance Engineering: Best Practices" (2023) | Free | Direct | TTFT, TPOT, memory-bandwidth utilization; weak multi-GPU scaling; measure, don't predict | Understand → Design | Good | Concepts Durable, numbers dated | Optional |
| **N12** | Anyscale, "How continuous batching enables 23x throughput" (2023) | Free | Direct | Static vs iteration-level batching | Understand | Good | Concept Durable | Modern Practice |
| **N13** | Modular LLM Inference Handbook (CC BY 4.0, maintained) | Free | Direct | Metrics, optimization techniques, KV-cache calculator; kernel and infrastructure sections out of scope | Use → Understand | Partly beyond | Periodically Updated | Modern Practice |
| **N14** | Moslem, Kelleher, "Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey", TMLR 2026 (v. 2026-08-30) | Free | Direct (abstract) | When routing decisions are made, what information they use, which mechanism; cascades | Understand → Design | Good | Periodically Updated | **Selected Sections** (§§1–3 and cascades) |
| **N15** | Ong et al., RouteLLM (2024/25); Chen et al., FrugalGPT (2023) | Free | Direct / Indirect | Preference-trained routers; cascades with a quality scorer | Understand | Good | Periodically Updated | Optional |
| **N16** | Kurtic et al., "Give Me BF16 or Give Me Death", ACL 2025 (rev. May 2026) | Free | Direct | Over 500,000 evaluations: FP8 near-lossless; INT8 1–3% loss; W4A16 competitive; format choice depends on synchronous vs batched serving | Understand → Design | Good | Periodically Updated | **Selected Sections** |
| **N17** | Erdil, "Inference economics of language models", arXiv 2506.04645 | Free | Direct | Cost-per-token vs speed frontiers | Design → Research | Good | Periodically Updated | Optional stretch |
| **N18** | Provider prompt-caching documentation (two major providers) | Free | Direct | Prefix reuse, time-to-live, write and read pricing multipliers, minimum lengths | Use | Good | **Fast-Moving** | Modern Practice |

**Coverage matrix**

| Concept | N1 Huyen | N3 Scaling book | N14 Routing survey | N16 Quantization study | N2 CS336 (optional) |
| --- | --- | --- | --- | --- | --- |
| KV-cache behaviour and memory | ? | **S** (+ exercises) | — | — | S |
| Batching, continuous batching | ? | S | — | P | S |
| Prefill vs decode | ? | **S** | — | — | S |
| Disaggregation as a concept | ? | P | — | — | ? |
| Speculative decoding | ? | P | — | — | S |
| Quantization trade-offs | P | P | — | **S** | P |
| Routing and cascades | P (4 pp.) | — | **S** | — | — |
| Token economics, prompt caching | P (3 pp.) | P | P | P | I |
| Latency, throughput, memory metrics | P | S | — | S | S |
| Cost–quality trade-offs | P | P | **S** | **S** | I |
| Serving architecture at decision depth | P | P | P | P | P |

Cells marked **?** for N1 reflect the evidence rule: the relevant subsections are not visible in the verified table of contents, so depth is not claimed even though the section headings make coverage likely.

**Durable versus Modern Practice, concept by concept.**

| Concept | Durable curriculum | Modern Practice |
| --- | --- | --- |
| KV cache | Size formula; linear growth with context; how grouped and latent attention shrink it; paging as an idea | Specific offload tiers |
| Batching | Static vs continuous; latency–throughput tension; critical batch size | Engine scheduler settings |
| Prefill / decode | Compute-bound prefill vs bandwidth-bound decode; why the two latency metrics behave differently; disaggregation and goodput | Which engines ship disaggregation |
| Speculative decoding | Draft-then-verify; lossless acceptance; speed-up depends on acceptance rate | Current variants and engine support |
| Quantization | Fewer bytes per token raises decode speed; weight-only vs weight-and-activation; measure accuracy on the task | Which formats are safe now; hardware support |
| Routing and cascades | Router, cascade and escalation patterns; expected-cost arithmetic; calibrated quality estimation | Gateway products and router libraries |
| Token economics | Prefix reuse; the input/output/cached-read cost structure; stable content first | Provider time-to-live, minimums and multipliers |
| Metrics | Time to first token, time per output token, throughput, goodput, roofline reasoning | Hardware specification numbers |

**Fair competition with baseline resources.** The operations handbook's inference chapter has verified headings for KV cache, continuous batching, speculative decoding, optimized attention, parallelism and quantization (R7) — genuine conceptual overlap with N1 ch 9 — but no metrics, routing or caching headings, and the book is otherwise bound to one cloud stack. The ML/DL book's quantization appendix and the LLM-from-scratch repository's KV-cache material ([J](#j-r8-e7-book-versus-repository)) are useful bridges from E7 mechanics but not decision-level resources.

**Provisional recommendation.** N1 (ch 9; ch 10 router, caches and monitoring — about 56 pages) + N3 (§§1, 2, 4 and problems 1–3; thread estimate 2–3 hours) + N14 (§§1–3 and cascades; about 1.5 hours) + N16 (findings and deployment guidance; about 1 hour). Optional: N2 as an alternative lecture format, N11, N15, N17. A capstone exercise sizing memory, latency and monthly cost for three serving options was proposed by the research thread and is recorded, not specified.

**Status: Resolved**, with routing and cascades flagged as having no textbook-grade treatment.

[⬆ Back to Contents](#contents)

---

## I. R7: Existing Resource Uncertainties

**Evidence route.** Public product pages for the two blocked publishers still refuse automated access. Section and subsection headings were read from O'Reilly's table-of-contents endpoint through the desktop application's built-in browser — headings only, no paywalled body text — and depth was cross-checked against companion repositories, publisher contents PDFs and notebook code.

**Uncertainties recorded in the resource coverage audit.**

| Audit item | Resource | Previous status | Evidence found | Revised status | Confidence | Remaining unknown |
| --- | --- | --- | --- | --- | --- | --- |
| Preference-tuning depth | *Hands-On Large Language Models* | Uncertain | Ch 12 headings: preference tuning, alignment, RLHF; reward models (training with and without a reward model); **preference tuning with DPO**. Notebook runs DPO with QLoRA on top of the SFT model. No PPO or ORPO code in the repository | **Covered — DPO at Use depth (library)**; RLHF and reward models conceptual only | High | Whether ORPO is mentioned in prose |
| Retrieval-fundamentals depth | *Hands-On Large Language Models* | Uncertain | Ch 8 headings: dense retrieval, reranking, **retrieval evaluation metrics**, advanced RAG, RAG evaluation. Notebook compares BM25 with dense search, reranks a BM25 first stage, builds a local RAG pipeline. No metric code | **Partially covered** — BM25 used as a baseline, not explained as a scoring model; dense retrieval and reranking via APIs; evaluation metrics in prose only | High (structure); Medium (prose depth) | Which metrics the prose covers |
| Evaluation content | *LLM Engineer's Handbook* | Uncertain | Ch 7 headings: model evaluation, RAG evaluation (Ragas, ARES), evaluating the project's model. Repository code implements an **LLM judge** scoring accuracy and style on a 1–3 scale. Aggregation is a plain mean — no variance, intervals or tests. Data decontamination appears in ch 5 as dataset hygiene | **Judge-based evaluation covered at Implement depth; statistical treatment not covered; benchmark validity not visible** | High / Medium | Whether ch 7 prose discusses contamination |
| Security content | *LLM Engineer's Handbook* | Uncertain | Ch 11 headings: human feedback, **guardrails**, prompt monitoring. No prompt-injection heading; no guardrail code in the repository | **Partially covered** — guardrails conceptual; prompt injection not visible | Medium | Prose of the guardrails section |
| Drift and monitoring | *LLM Engineer's Handbook* | Uncertain | Appendix headings: monitoring, logs, metrics, **drifts**, observability, alerts; prompt monitoring implemented with an observability tool | **Covered conceptually**; prompt monitoring implemented | High | Drift-detection code (none seen) |
| A/B methodology depth | *Designing Machine Learning Systems* | Uncertain | Publisher contents PDF with page numbers: test in production p. 279, shadow deployment p. 280, **A/B testing p. 281**, canary p. 282, interleaving p. 283, bandits pp. 285–289. No significance, sample-size or power heading | **Partially covered** — five strategies described; A/B testing about one page; bandits about four | High (structure); Medium (absence of significance/power in prose) | Whether the one-page section mentions significance in passing |
| Trustworthy-AI prose | *Hands-On ML with Scikit-Learn and PyTorch* | Uncertain | None of about 410 headings matches fairness, ethics, privacy, bias, robustness, safety, harm, toxicity or red teaming; repository text search finds none | **Not covered as a topic** | Medium | Incidental prose mentions |
| Transformer build depth | *NLP in Action* | Uncertain | Ch 9: positional encoding by hand; attention explained with equations; translation model **subclasses PyTorch's built-in transformer** with a custom decoder layer to expose attention weights | **Resolved** — Understand/Use, not a build from primitives | High | — |
| Tokenization, judge evaluation, RoPE | *Build a LLM from Scratch* | Uncertain | See [J](#j-r8-e7-book-versus-repository) | **Resolved** | High | — |
| Chapter-level intent (audit uncertainty 11) | All | Uncertain | Settled as **policy** by decision D1, not by evidence | Policy settled | — | — |
| Speaker diarization; course last-updated date | Hugging Face Audio Course | Uncertain | Not investigated — outside R7's four themes | **Unchanged** | — | As before |
| `EXPLAIN` in body text | *Practical SQL* | Uncertain | Not investigated | **Unchanged** | — | As before |
| Server version | PostgreSQL Exercises | Uncertain | Not investigated | **Unchanged** | — | As before |

**Additional findings that correct the resource coverage audit.** These were found while resolving the items above. They are recorded so later work does not inherit inaccurate statements; this report does not re-audit the affected blocks.

| # | Audit statement | Evidence | Correction | Confidence |
| --- | --- | --- | --- | --- |
| **K1** | NLP textbook: learned sparse and **late-interaction retrieval absent** | Text of the 2026-08-19 draft of ch 11, retrieved from the authors' site: §11.3 teaches ColBERT — separate token-level encoding, MaxSim scoring, a dedicated figure — and two-stage BM25-then-neural reranking | **Late interaction and reranking are taught at Understand depth.** Learned sparse retrieval is absent (zero occurrences). nDCG and MRR: zero occurrences, confirming the audit. Approximate nearest-neighbour search: **mentioned only**, with FAISS named; no HNSW, IVF or product quantization | High (Direct) |
| **K2** | ML/DL book: post-training appears only via LoRA and quantization; no LLM-application content | Full heading list: a section **"Turning an LLM into a Chatbot"** with SFT, RLHF, DPO, a preference-training library, "From a Chatbot Model to a Full Chatbot System" and MCP | The book contains a post-training and chatbot-system section. Relevant to F1 and, marginally, F2; **not re-audited here** | High (headings) |
| **K3** | ML/DL book: deployment, serving and monitoring **Not Covered** | Ch 2 heading "Launch, Monitor, and Maintain Your System" | Read the audit as "no dedicated chapter", not zero coverage. The deployment-at-scale regression still stands | Medium |
| **K4** | *Hands-On LLMs*: evaluation beyond RAG not recorded | Ch 12 heading "Evaluating Generative Models": word-level metrics, benchmarks, leaderboards, automated and human evaluation | A conceptual evaluation section exists | High (headings) |

**Status: Resolved for the four named themes**; three peripheral audit uncertainties remain unchanged by design.

[⬆ Back to Contents](#contents)

---

## J. R8: E7 Book Versus Repository

**Resource.** *Build a Large Language Model (From Scratch)*, Sebastian Raschka, Manning, September 2024, 368 pages; repository `rasbt/LLMs-from-scratch`.

**What belongs to the published book.** Seven chapters — understanding LLMs; working with text data; coding attention mechanisms; implementing a GPT model; pretraining on unlabeled data; fine-tuning for classification; fine-tuning to follow instructions — and appendices A (PyTorch, including a distributed-data-parallel script), B (references), C (exercise solutions), D (training-loop extras) and E (LoRA). Main-chapter notebook headings match the book's section numbering.

**Three specific resolutions.**

| Question | Answer | Evidence |
| --- | --- | --- |
| Is byte-pair encoding implemented by hand in ch 2? | **No.** §2.5 uses a production tokenizer library. BPE from scratch exists **only** in repository bonus material (added 2025-01-17) | Main notebook and bonus folder |
| Does §7.8 use an LLM as judge? | **Yes**, through a locally run open model, with larger alternatives | Chapter README and evaluation script |
| Is RoPE taught? | **Not in the book.** The book uses GPT-2 learned absolute position embeddings; RoPE appears only in repository bonus folders on newer architectures | Zero occurrences in main ch 4, 5 and 7 notebooks |

**Book versus repository.**

| Location | Content | Status | Relevance |
| --- | --- | --- | --- |
| Main chapter code, appendices A–E | Book code and solutions | **Book** | E7 core mechanics and fine-tuning |
| Ch 2 bonus | BPE implementations compared; **BPE from scratch**; embedding vs matrix multiplication; data-loader intuition | Repository only | E6/E7 mechanics |
| Ch 3 bonus | Efficient multi-head attention implementations | Repository only | E7 mechanics |
| Ch 4 bonus | FLOPs analysis; **KV cache** (2025-06); grouped-query and multi-head latent attention (2025-10); sliding-window attention; **mixture of experts** (2025-10); gated DeltaNet; sparse attention and cross-layer KV sharing (2026-05) | Repository only | E7 mechanics; F5 bridge |
| Ch 5 bonus | Alternative weight loading; learning-rate schedules; **GPT → Llama conversion**; Qwen3, Gemma 3 and 4, OLMo 3 and later architectures (2024-09 to 2026-04); memory-efficient loading; optimizer experiments | Repository only | E7 mechanics; architectural currency |
| Ch 6 bonus | Additional fine-tuning experiments | Repository only | F1 |
| Ch 7 bonus | Near-duplicate detection; instruction-data generation; **LLM-as-judge evaluation** (2024-05); **preference-data generation and DPO from scratch** (2024-06) | Repository only | F1 post-training and evaluation |
| Package | Installable package re-exporting chapter code | Repository only | Infrastructure |
| Linked sequel repository | Qwen3 walkthrough, verifier-based evaluation, self-consistency, self-refinement, **GRPO and RL from verifiable rewards** | Sequel | F1 |

**Stability.** No tags and no GitHub releases; only the main branch. The installable package is the only versioned artifact. The licence is Apache-2.0 text with a modified definition that excludes the book itself. Several bonus folders have been **renamed** over the repository's history; new folders are appended with numeric prefixes that are mostly, but not guaranteed to be, chronological.

**Maintenance.** Latest commit 2026-09-17; between one and thirteen commits in every month of 2026; recent commits fix correctness bugs (a causal mask, KV-cache generation) and upgrade Python. Two open issues; recent issues typically closed within one or two days; continuous-integration tests on three operating systems. The author describes bonus material as **optional** and does not accept contributions that would change main-chapter code, so the code stays consistent with the printed book.

**Sequel.** *Build a Reasoning Model (From Scratch)*, Raschka, Manning. The publisher page, reached through a summarizing fetch, reports publication in **June 2026**, 440 pages (Medium confidence). Its contents cover evaluating reasoning models, inference-time scaling, self-refinement, reinforcement learning for reasoning, GRPO improvements and distillation; the repository describes it as standalone but usable as a sequel. It bears on F1, not E7, and is recorded here for later F1 resourcing — **not evaluated**.

**Maintenance-risk assessment.** Book chapters and main code are frozen by explicit policy and are low risk. Repository-only folders are well maintained but unversioned and occasionally renamed; citing them safely requires a folder path plus a commit identifier (current head `ace7c08`, 2026-09-17) or a version of the installable package.

**What the evidence supports — no curriculum decision.** Citing **the book** for tokenization use, attention, the GPT architecture, pretraining, SFT, LoRA and LLM-judge basics; citing **the repository, pinned and marked supplementary**, for BPE from scratch, KV cache, RoPE and modern architectures, grouped and latent attention, mixture of experts, and DPO; and noting the sequel for reasoning and RL. One consequence for review: the proposal's E7 requirement that tokenization be *implemented rather than described* is met **only by repository material**, not by the book.

**Status: Resolved** as an evidence question.

[⬆ Back to Contents](#contents)

---

## K. R9: NLP in Action Reassessment

**Resource.** *Natural Language Processing in Action*, 2nd edition, Lane and Dyshel, Manning, January 2025, 688 pages. Code at `gitlab.com/tangibleai/nlpia2`, AGPL-3.0; last substantive commits 2025-12 and 2026-04.

**The question.** Not whether the book is good, but *what required capability it teaches better than the rest of the proposed resource set*.

**Distinctive content, verified.**

| Topic | Location | Depth | Tools and currency | Required by | Stronger alternative in the proposed set? |
| --- | --- | --- | --- | --- | --- |
| Full-text search | §10.3.1 | Understand | Search engines named; **no BM25** | E8 | Yes — NLP textbook ch 11 teaches BM25 and IR evaluation |
| **ANN index selection and vector quantization** | §10.3.2–10.3.6 | Understand; hand-coded scalar quantization; product and inverted-file quantization described | FAISS through an **outdated question-answering framework API** | **E8, F6** | **None verified.** The NLP textbook only mentions ANN (K1); *Hands-On LLMs* uses FAISS without index choice; *AI Engineering*'s Retrieval Algorithms section (pp. 257–268) could not be checked |
| RAG question-answering application | §10.3.7–10.3.13 | Use | 2023-era models and framework | F2 | Yes — *AI Engineering* ch 6 or *Hands-On LLMs* ch 8 |
| Guardrails | §10.1.3 | Use (code) | Early guardrail-library interface; spaCy matcher filters | F4 | Yes — the F4 bundle, which teaches why detection filtering is insufficient |
| Red teaming | §10.1.4, about fifty lines | Awareness | — | F4 | Yes — adaptive-attack evaluation and the AgentDojo lab |
| Transformer | Ch 9 | Understand/Use; subclasses the framework transformer | A text-data library no longer developed | E5, E7 | Yes — the ML/DL book and the LLM-from-scratch book both build from primitives |
| **Knowledge-graph construction, relation extraction, SPARQL over Wikidata** | Ch 11 | Implement (pattern-based extraction, KG queries); Awareness (neural relation extraction) | spaCy, constituency parser, Wikidata | **EX7**, EX3 | Not in the universal set; the NLP textbook covers extraction conceptually |
| Dialog engines | Ch 12 | Use | Framework dependency pinned to a 2023 release | No block | — |
| Classical toxicity classification | Ch 4 | Implement | Current | No block | — |
| Containerized NLU microservice | Appendix E | Use | — | CS&E boundary | — |

**Overlap.** Tokenization, TF-IDF, embeddings, RNNs, transformer theory and BERT fine-tuning overlap heavily with the NLP textbook, the ML/DL book and *Hands-On LLMs*.

**Learning cost.** 688 pages; code dependencies on a superseded question-answering framework API, an unmaintained text-data library and an early framework release — each a currency cost.

**Provisional future disposition.**

| Portion | Disposition | Reason |
| --- | --- | --- |
| The book as a whole | **Remove candidate** from the universal path | No universal block needs more than one section of it |
| §10.3.2–10.3.6 | **Selected Sections, conditional** — for E8 and F6 | The only verified teaching treatment of ANN index choice and vector quantization. Drop the condition if *AI Engineering*'s Retrieval Algorithms section proves to cover the same ground. Teach the concepts; do not rely on the code |
| Ch 11 | **Specialization reference** for EX7 | Unique hands-on knowledge-graph construction; not universal |
| Guardrails, red teaming, ch 9, ch 12 | **Reject** for the normal path | Stronger or more current alternatives exist in the proposed set, or no block requires the content |

**Status: Resolved** as a disposition; one conditional depends on a check of a paid book's body text.

[⬆ Back to Contents](#contents)

---

## L. Cross-Resource Coverage Matrix

Rows are the required capabilities of the six researched blocks. Columns are the twelve anchor resources of the proposed set; the last column names the short items that carry the remaining coverage. The block-diagonal shape is the finding: overlap between blocks is small and deliberate.

**Legend:** S Strong · P Partial · I Introductory · R Reference · — None · ? Uncertain. Column keys: **D2L** Dive into Deep Learning · **Pie** Piech · **D8** Data 8 · **Koh** Kohavi et al. · **Mil** Miller · **Huy** Huyen, *AI Engineering* · **Dib** Dibia · **AIMS** AI Measurement Science · **Har** Hardt · **DP** design-patterns paper (X1) · **NIST** NIST AI 100-2 · **Sca** scaling-book inference chapter.

| Block | Capability | D2L | Pie | D8 | Koh | Mil | Huy | Dib | AIMS | Har | DP | NIST | Sca | Other recommended coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E2 | Linear algebra for representation | P | — | — | — | — | — | — | — | — | — | — | — | MML (Reference) S |
| E2 | Multivariate calculus, chain rule | S | — | — | — | — | — | — | — | — | — | — | — | |
| E2 | Reverse-mode semantics | P | — | — | — | — | — | — | — | — | — | — | — | micrograd S |
| E2 | Distributions | P | **S** | — | — | — | — | — | — | — | — | — | — | |
| E2 | Expectation, variance, conditioning | S | S | — | — | — | — | — | — | — | — | — | — | |
| E2 | Likelihood as training objective | S | S | — | — | — | — | — | — | — | — | — | — | |
| E2 | Convexity, GD behaviour, divergence | **S** | — | — | — | — | — | — | — | — | — | — | — | |
| E2 | Conditioning | P | — | — | — | — | — | — | — | — | — | — | — | Distill (optional) S |
| E2 | Entropy, cross-entropy | S | P | — | — | — | I | — | — | — | — | — | — | |
| E2 | Implement GD by hand | S | — | — | — | — | — | — | — | — | — | — | — | |
| E2 | Implement reverse mode on a toy graph | I | — | — | — | — | — | — | — | — | — | — | — | micrograd S |
| E3 | Estimation, sampling variability | — | P¹ | **S** | P | P | — | — | — | — | — | — | — | |
| E3 | Confidence intervals and their meaning | — | — | S | I | P | — | — | — | P | — | — | — | |
| E3 | Bootstrap (Implement) | — | P¹ | **S** | I | I | — | — | — | — | — | — | — | |
| E3 | Hypothesis testing | — | — | S | P | P | — | — | — | — | — | — | — | |
| E3 | Paired model comparison, shared test set | — | — | — | — | **S** | — | — | — | P | — | — | — | NLP textbook §4.11 (baseline) P |
| E3 | Power and sample size | — | — | P | P | **S** | — | — | — | P | — | — | — | |
| E3 | Calibration | — | — | — | — | — | — | — | — | — | — | — | — | scikit-learn §1.16 + Guo et al. S |
| E3 | Online controlled experiment design | — | — | I | **S** | — | — | — | — | — | — | — | — | |
| E3 | Randomization, experimental units | — | — | P | S | P | — | — | — | — | — | — | — | |
| E3 | Experiment failure modes | — | — | — | **S** | P | — | — | — | — | — | — | — | |
| E3 | Confounding, causal framing | — | — | P | P | — | — | — | — | — | — | — | — | Facure chs 1–3 (optional) S |
| F2 | Workflows vs agents, least autonomy | — | — | — | — | — | P | S | — | — | — | — | — | Feng, Kim, Kapoor P |
| F2 | Context as finite, non-uniform budget | — | — | — | — | — | I | P | — | — | — | — | — | Liu et al. S |
| F2 | Context management, compaction | — | — | — | — | — | I | P | — | — | — | — | — | Modern Practice only |
| F2 | Structured generation, constrained decoding | — | — | — | — | — | P | P | — | — | — | — | — | Tam et al. (optional) P |
| F2 | Tool-interface design, least privilege | — | — | — | — | — | P | S | — | — | S | — | — | |
| F2 | RAG on IR fundamentals | — | — | — | — | — | **S** | I | — | — | — | — | — | *Hands-On LLMs* ch 8 (baseline) S |
| F2 | Memory | — | — | — | — | — | P | P | — | — | — | — | — | CoALA (optional) P |
| F2 | Verification, generate-and-verify | — | — | — | — | — | P | P | — | — | — | — | — | Kambhampati et al. S |
| F2 | Human oversight, intervention budgets | — | — | — | — | — | I | P | — | — | — | — | — | Feng et al. P |
| F2 | Multi-agent and evidence against default | — | — | — | — | — | I | S | — | — | — | — | — | Kim et al. S |
| F2 | Standard interfaces as a concept | — | — | — | — | — | — | S² | — | — | — | — | — | |
| F2 | Trajectory and multi-component evaluation | — | — | — | — | — | I | P | — | — | — | — | — | Agent-evals post S, ABC P, Kapoor P |
| F2 | Diagnosing where a failure originated | — | — | — | — | — | I | P | — | — | — | — | — | MAST (optional, multi-agent only) P |
| F3 | Construct validity | — | — | — | — | — | — | — | **S** | P | — | — | — | Bean et al. S |
| F3 | Benchmark validity | — | — | — | — | — | — | — | S | **S** | — | — | — | Bean et al. S, ABC S |
| F3 | Contamination → model selection | — | — | — | — | — | ? | — | P | **S** | — | — | — | |
| F3 | Statistical comparison of models | — | — | — | — | **S** | — | — | S | S | — | — | — | |
| F3 | Judges validated against humans | — | — | — | — | — | P | — | S | S | — | — | — | Husain & Shankar S |
| F3 | Reliability vs validity | — | — | — | — | P | — | — | **S** | P | — | — | — | |
| F3 | Human evaluation, annotation operations | — | — | — | — | — | — | — | P | ? | — | — | — | van der Lee S, Husain & Shankar S |
| F3 | Regression suites, failure taxonomy, error analysis | — | — | — | — | — | P | — | P | — | — | — | — | Husain & Shankar S, agent-evals post P |
| F3 | Capability evaluation | — | — | — | — | P | — | — | **S** | P | — | — | — | |
| F3 | Trajectory and agent evaluation | — | — | — | — | P | — | — | — | I | — | — | — | Agent-evals post S, ABC P |
| F3 | Unresolved validity problems | — | — | — | — | — | — | — | S | S | — | — | — | Bean et al. S |
| F3 | Saturation | — | — | — | — | P | — | — | P | P | — | — | — | |
| F4 | Direct prompt injection | — | — | — | — | — | I | — | — | — | P | R | — | Attacker Moves Second S |
| F4 | Indirect prompt injection, untrusted content | — | — | — | — | — | — | — | — | — | **S** | R | — | Greshake S, AgentDojo S |
| F4 | Why detection alone fails | — | — | — | — | — | — | — | — | — | **S** | I | — | Attacker Moves Second S |
| F4 | Unsafe tool use | — | — | — | — | — | — | — | — | — | S | I | — | AgentDojo S |
| F4 | Poisoning | — | — | — | — | — | — | — | — | — | — | **S** | — | Souly et al. S |
| F4 | Model extraction | — | — | — | — | — | — | — | — | — | — | P | — | Carlini "Stealing" S |
| F4 | Adversarial examples | — | — | — | — | — | — | — | — | — | — | R | — | Kolter–Madry S |
| F4 | Containment, capability limitation | — | — | — | — | — | — | — | — | — | **S** | I | — | CaMeL S |
| F4 | Architectural separation | — | — | — | — | — | — | — | — | — | **S** | — | — | CaMeL S |
| F4 | AI-specific threat modeling | — | — | — | — | — | — | — | — | — | S | P | — | |
| F4 | Attack evaluation | — | — | — | — | — | — | — | — | — | P | P | — | Attacker Moves Second S, AgentDojo S |
| F5 | KV-cache behaviour and memory | — | — | — | — | — | ? | — | — | — | — | — | **S** | |
| F5 | Batching, continuous batching | — | — | — | — | — | ? | — | — | — | — | — | S | Operations handbook ch 8 (baseline) P |
| F5 | Prefill vs decode | — | — | — | — | — | ? | — | — | — | — | — | **S** | |
| F5 | Disaggregation as a concept | — | — | — | — | — | ? | — | — | — | — | — | P | |
| F5 | Speculative decoding | — | — | — | — | — | ? | — | — | — | — | — | P | Operations handbook ch 8 (baseline) P |
| F5 | Quantization trade-offs | — | — | — | — | — | P | — | — | — | — | — | P | Kurtic et al. S |
| F5 | Routing and cascades | — | — | — | — | — | P | — | — | — | — | — | — | Routing survey S |
| F5 | Token economics, prompt caching | — | — | — | — | — | P | — | — | — | — | — | P | |
| F5 | Latency, throughput, memory metrics | — | — | — | — | — | P | — | — | — | — | — | S | Kurtic et al. S |
| F5 | Cost–quality trade-offs | — | — | — | — | — | P | — | — | — | — | — | P | Routing survey S, Kurtic et al. S |
| F5 | Serving architecture at decision depth | — | — | — | — | — | P | — | — | — | — | — | P | |

¹ Present in Piech Part 4 but deliberately **not assigned** in E2, to avoid doubling E3. ² Specification-bound treatment.

**Resources that appear in more than one block, and where each is homed.**

| Resource | Blocks touched | Home | Treatment elsewhere |
| --- | --- | --- | --- |
| *AI Engineering* (Huyen) | F2, F5; optional F3 and F4; light E2 overlap | F2 **and** F5 (different sections) | F3 chs 3–4 and F4 ch 5 are Reference only |
| Miller, error bars | E3, F3 | **E3** | F3 cross-reference; not re-read |
| Design-patterns paper (X1) | F4, F2 | **F4** | F2 cross-reference for least privilege |
| Kapoor et al. | F2, F3 | **F2** | F3 cross-reference |
| Agent-evals post and ABC | F3, F2 | **F3** | F2 cross-reference for trajectory evaluation |
| Hardt ch 3 | F3, E3 | **E3 covers the content** | Optional in F3 |
| Piech Part 4 | E2, E3 | **Not assigned** | E3 carries sampling and bootstrap |
| NLP textbook (baseline) | E3 §4.11, E8 ch 11, F3 §1.9, F4 §1.10 | As in the proposal | Cross-reference only in E3, F3, F4 |

[⬆ Back to Contents](#contents)

---

## M. Proposed Minimal Resource Set

The smallest coherent set found for the six researched blocks. **34 items**: 8 books or textbooks in selected sections, 8 tutorials, guides or technical documents, 18 papers. **3 paid**, 31 free. One further conditional item comes from R9. Baseline resources serving other blocks are not counted here.

| # | Resource | Block(s) | Role | Capability it contributes | Amount | Access | Currency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **MS1** | *Dive into Deep Learning* | E2 | Primary (Selected Sections) | Optimization behaviour; likelihood → cross-entropy → loss; runnable GD | About 15 sections: §2.3–2.6, §12.1–12.4, §12.11, §22.1, §22.4, §22.7, §22.11 | Free | Periodically Updated |
| **MS2** | Piech, *Probability for Computer Scientists* | E2 | Supplement | Distributions, expectation, variance, conditioning, MLE | Parts 1, 2, 3 (joint and marginal), 5, and the information-theory chapter; stop before sampling, bootstrap and CLT | Free | Periodically Updated |
| **MS3** | Karpathy, micrograd lecture and repository | E2 | Selected Sections | Reverse-mode differentiation at Implement depth | One 2h25m lecture and one source file | Free | Durable |
| **MS4** | *Computational and Inferential Thinking* (Data 8) | E3 | Primary | Computational inference; bootstrap and permutation tests implemented; CIs; causal framing | Chs 2, 10–13, 14.4–14.6 (thread estimate 15–20 h) | Free | Durable |
| **MS5** | Kohavi, Tang, Xu, *Trustworthy Online Controlled Experiments* | E3 | Primary (Selected Sections) | Experiment design, randomization units, A/A tests, sample-ratio mismatch, interference | Chs 1–3, 14, 17, 19, 21, 22 (about 110 pp.) | **Paid**; ch 1 free | Durable |
| **MS6** | Miller, "Adding Error Bars to Evals" | E3 (→ F3) | Selected Sections | Paired model comparison on a shared test set; evaluation power | Full (about 15 pp.) | Free | Periodically Updated |
| **MS7** | scikit-learn User Guide §1.16 | E3 | Selected Sections | Calibration in practice | One guide section | Free | Periodically Updated |
| **MS8** | Guo et al., "On Calibration of Modern Neural Networks" | E3 | Selected Sections | Calibration concepts: reliability diagrams, ECE, temperature scaling | §§1–3 | Free | Durable |
| **MS9** | Huyen, *AI Engineering* | F2, F5 | Primary (Selected Sections) | F2: structured outputs, context length, RAG, agents, memory, architecture. F5: inference optimization, metrics, routing, caching, monitoring | About 71 pp. (F2) + 56 pp. (F5) of about 500 | **Paid** | Periodically Updated |
| **MS10** | Dibia, *Designing Multi-Agent Systems* | F2 | **Provisional** Primary — verification required | Building an agent loop, tools, memory and workflows from scratch; when not to use multiple agents | Part I, first-agent, workflow, multi-agent, evaluation and failure-mode chapters | **Paid**; 2 chapters free | Periodically Updated |
| **MS11** | Liu et al., "Lost in the Middle" | F2 | Required paper | Context is non-uniform; more context can reduce quality | Full | Free | Durable |
| **MS12** | Feng et al., "Levels of Autonomy for AI Agents" | F2 | Required paper | Autonomy and human oversight as design variables | Full | Free | Periodically Updated |
| **MS13** | Kambhampati et al., LLM-Modulo | F2 | Required paper | Generate-and-verify with external verifiers and solvers | Full | Free | Durable |
| **MS14** | Kim et al., "Towards a Science of Scaling Agent Systems" | F2 | Required paper | Evidence that multi-agent is conditional, not a default | Findings and discussion | Free | Periodically Updated (preprint) |
| **MS15** | Kapoor et al., "AI Agents That Matter" | F2 (→ F3) | Required paper | Cost-controlled agent evaluation; simple baselines | Full | Free | Durable |
| **MS16** | Beurer-Kellner et al., design patterns for prompt-injection security | F4 (→ F2) | Primary | Containment architecture, capability limitation, AI threat modeling | Full; 3–4 case studies as exercises | Free | Durable |
| **MS17** | Debenedetti et al., CaMeL | F4 | Primary companion | Control-flow/data-flow separation; measured utility cost of security | Threat model, design, policy, evaluation (about 25 pp.) | Free | Periodically Updated |
| **MS18** | Greshake et al., indirect prompt injection | F4 | Supplement | Why untrusted content is an attack surface | Full (about 20 pp.) | Free | Durable |
| **MS19** | Nasr, Carlini et al., "The Attacker Moves Second" | F4 | Primary (evaluation) | Why detection fails; adaptive-attack evaluation | Full | Free | Periodically Updated |
| **MS20** | AgentDojo | F4 | Selected Sections (lab) | Measuring attack success and utility together | One lab: baseline, one defense, one adaptive attack | Free | Periodically Updated |
| **MS21** | NIST AI 100-2 E2025 | F4 | Selected Sections | Poisoning, extraction and evasion with mechanisms; shared vocabulary | §2.1–2.4, §3.1–3.5, §4.1 (about 45 pp.) | Free | Periodically Updated |
| **MS22** | Kolter and Madry, adversarial robustness tutorial | F4 | Selected Sections | Adversarial examples and robust optimization | Chs 1–4 | Free | Durable |
| **MS23** | Souly et al., near-constant poison samples | F4 | Supplement | LLM-scale poisoning risk | Full | Free | Fast-Moving |
| **MS24** | Carlini et al., "Stealing Part of a Production Language Model" | F4 | Supplement | LLM-era model extraction | Full | Free | Periodically Updated |
| **MS25** | Truong and Koyejo, *AI Measurement Science* | F3 | Primary (Selected Sections) | Construct validity, reliability vs validity, judges as raters, capability evaluation | Ch 1; ch 5 selected; ch 11 selected; ch 13; ch 3 as needed | Free | Periodically Updated (living) |
| **MS26** | Hardt, *The Emerging Science of Machine Learning Benchmarks* | F3 | Primary (Selected Sections) | Contamination, test-set reuse, rankings as the product, judge bias | Chs 5, 11, 14 | Free online | Durable |
| **MS27** | Bean et al., construct validity in LLM benchmarks | F3 | Supplement | Validity grounded in the actual benchmark ecosystem; checklist | Full | Free | Durable |
| **MS28** | van der Lee et al., human evaluation best practices | F3 | Supplement | Human-evaluation study design | Full | Free | Durable |
| **MS29** | Husain and Shankar, evals FAQ | F3 | Primary (application evaluation) | Error analysis → failure taxonomy; judge-validation procedure; annotation operations | Error-analysis, evaluation-design and annotation sections | Free | Periodically Updated |
| **MS30** | Anthropic, "Demystifying evals for AI agents" | F3 (→ F2) | Selected Sections — **flagged exception** | Trajectory-evaluation vocabulary and practice | Full | Free | **Fast-Moving** |
| **MS31** | Zhu et al., Agentic Benchmark Checklist | F3 (→ F2) | Supplement | Task validity vs outcome validity for agent benchmarks | Full | Free | Periodically Updated |
| **MS32** | *How To Scale Your Model*, "All About Transformer Inference" | F5 | Selected Sections | Serving arithmetic with worked problems | §§1, 2, 4 and problems 1–3 (2–3 h) | Free | Durable |
| **MS33** | Moslem and Kelleher, routing and cascading survey | F5 | Selected Sections | Routing and cascades | §§1–3 and cascades (about 1.5 h) | Free | Periodically Updated |
| **MS34** | Kurtic et al., "Give Me BF16 or Give Me Death" | F5 | Selected Sections | Evidence-based quantization decisions | Findings and deployment guidance (about 1 h) | Free | Periodically Updated |
| *MS35* | *NLP in Action* §10.3.2–10.3.6 | E8, F6 | *Selected Sections — conditional* | ANN index selection and vector quantization | One section | Paid (baseline) | Concepts Durable; code dated |

**Optional, not mandatory.** E2: MML (Reference), Distill momentum, CS231n backpropagation notes. E3: OpenIntro paired-means sections, Card et al., Facure chs 1–3. F2: Chroma "Context Rot", Tam et al., MAST, CoALA, Lakshmanan and Hapke. F4: Carlini et al. 2019, Microsoft red-team lessons. F3: Wallach et al., Artstein and Poesio, EvalGen, Hardt chs 3 and 12. F5: CS336 lecture 10, Databricks performance guide, RouteLLM and FrugalGPT, Erdil.

[⬆ Back to Contents](#contents)

---

## N. Existing Baseline Resource Disposition

Only resources affected by R1–R9. *The Python Tutorial*, *Practical SQL*, PostgreSQL Exercises, *Python for Data Analysis* and the Hugging Face Audio Course are unaffected; their provisional dispositions in the proposal stand.

| Resource | Baseline role → proposal role | New evidence | Provisional disposition | Reason |
| --- | --- | --- | --- | --- |
| *Hands-On ML with Scikit-Learn and PyTorch* | §5.1 ML & DL → split across E4, E5, F5, EX1, EX2 | No probability notebook (confirms the E2 gap); a post-training and chatbot-system section with SFT, RLHF, DPO and MCP (K2); a launch-and-monitor section in ch 2 (K3); no trustworthy-AI topic | **Retain, split as proposed; supplement** E2 with MS2 | The new post-training content is relevant to F1 and should be weighed when F1 is resourced |
| *Speech and Language Processing* | §6.1 NLP → selected portions across E5–E10, F3, F4, EX3, EX4 | Ch 11 teaches late interaction and reranking (K1); ANN only mentioned; §4.11 paired bootstrap; §1.9 evaluation validity; §1.10 prompt injection mention only | **Retain selected portions** | Stronger E8/F6 anchor than the audit recorded; does not teach ANN indexing; cross-reference for E3 and F3 |
| *Natural Language Processing in Action* | §6.2 NLP → selected portions | See [K](#k-r9-nlp-in-action-reassessment) | **Remove candidate** as a whole; conditional selected section for E8/F6; **Specialization** reference for EX7 | Unique required contribution confined to one section |
| *Build a LLM from Scratch* | §7.1 LLMs → E7 anchor | Tokenization implemented by hand, RoPE and KV cache are repository-only; book frozen and stable; repository maintained but unversioned; sequel published | **Retain** the book as E7 anchor; repository as a **pinned supplement** | Only the repository meets E7's "tokenization implemented" requirement |
| *Hands-On Large Language Models* | §7.2 LLMs → selected portions | DPO at Use depth; RAG chapter with BM25 comparison and reranking at code level; one agents chapter; conceptual generative-evaluation section | **Retain selected portions** | Its RAG chapter and *AI Engineering*'s RAG section overlap for F2 — one suffices; its agents chapter is insufficient for F2 |
| *Designing Machine Learning Systems* | MLOps → F5 anchor; data chapters to E9 | A/B testing about one page; no significance or power | **Retain** as F5 classical-operations anchor; **not** an E3 source | Experimentation moves to MS5; complementary with MS9 by the same author |
| *LLM Engineer's Handbook* | LLMOps → candidate for supplement or replacement | LLM-judge evaluation implemented, no statistics; guardrails conceptual; drift conceptual; inference chapter conceptually broad | **Reference** for F3 and F5 serving; replacement decision **left open** | MS25–MS31 teach measurement; MS9 and MS32 cover serving more broadly. Its remaining distinctive value — an end-to-end fine-tune-to-deploy pipeline — was not evaluated against alternatives |

[⬆ Back to Contents](#contents)

---

## O. Modern Practice Reference Layer

Useful now; **not** permanent curriculum anchors. Organized by capability. Vendor names appear only as the source of an item, never as a category.

| Capability | Current-practice references | Why not a permanent anchor | Review cadence |
| --- | --- | --- | --- |
| System architecture, least autonomy | Anthropic "Building effective agents" (Dec 2024) | Vendor practice; the durable claim is carried by MS12, MS14, MS15 | 12-week review |
| Context management | Anthropic "Effective context engineering" (Sep 2025); Chroma "Context Rot"; Mei et al. survey | Terminology and techniques still settling | 4-week scan |
| Tool interfaces and interoperability | Anthropic "Writing effective tools"; the current tool- and agent-interoperability specifications; Dibia's protocol chapter | Specifications change and deprecate | 4-week scan |
| Structured generation | Constrained-decoding engine documentation; JSONSchemaBench; Tam et al. | Engine support changes quickly | 12-week review |
| Agent memory | 2026 agent-memory surveys; CoALA | Fast-growing literature, no consensus | 12-week review |
| Agent security practice | Meta "Agents Rule of Two"; Google's secure-agents approach; lessons from defending against indirect injection (arXiv 2505.14534); Abdelnabi and Bagdasarian impossibility argument (arXiv 2605.17634); Microsoft red-team lessons; OWASP LLM 2025 and Agentic 2026 lists; MITRE ATLAS | Rapidly changing guidance and taxonomies; lists are references, not teaching | 4-week scan |
| Evaluation practice | Norman et al. 2026 on judge reliability; lm-evaluation-harness lessons; benchmark-saturation study (arXiv 2602.16763); holistic agent leaderboard logs; τ-bench and successors; contamination surveys | Unreviewed or tool-specific | 4-week scan |
| Serving mechanisms | Modular LLM Inference Handbook; Anyscale continuous batching; introductions of the speculative-decoding, PagedAttention and DistServe papers; Hao AI Lab disaggregation retrospective; Databricks performance guide; engine quantization docs | Engines and formats change quickly | 4-week scan |
| Token economics | Provider prompt-caching documentation; Erdil on inference economics | Pricing, retention and minimums change with each model generation | 4-week scan |
| Courses and books to re-check | Stanford CS329Z (after 2026-12); Berkeley Agentic AI MOOC; UMass COMPSCI 684; efficient-dl-systems; MIT 6.5940; *An Illustrated Guide to AI Agents* (after 2026-10-13); Hardt in print (after 2026-10-06) | Materials pending or not final | 12-week review |

[⬆ Back to Contents](#contents)

---

## P. Remaining Gaps and Uncertainty

**Capabilities still inadequately resourced.**

1. **F2** — diagnosing where a failure originated; intervention budgets; least autonomy as a decision procedure; standard interfaces as a durable abstraction. No teaching resource exists; the curriculum will need authored material.
2. **F3** — validity of trajectory evaluation (open research, not a missing book); annotation-guideline writing; saturation as a single topic.
3. **E3** — calibration pedagogy with exercises; a paired-bootstrap lab; multiple comparisons; sequential testing.
4. **F4** — AI-specific threat modeling taught only through case studies; model extraction beyond Understand depth.
5. **F5** — routing and cascades at textbook level.
6. **E2** — conditioning tied to divergence in one place; reverse mode over tensors at beginner level.

**Inaccessible evidence.** Body text of *AI Engineering* (subsection depth for serving and agents), Kohavi internals, Dibia's chapter structure, the XACS134 course, CS329Z materials; several 2025–2026 papers assessed from abstracts only.

**Contested or fragile recommendations.**

- MS10 Dibia — self-published, indirectly verified, continuously revised.
- MS30 — vendor practice placed on the normal path by necessity.
- MS9 — one paid book underpins two blocks; a second edition could shift sections.
- MS14 — preprint whose specific numbers will be superseded.
- MS25 and MS26 — a living textbook and a book whose online and print versions may diverge after 2026-10-06.
- MS35 — conditional on a check of *AI Engineering*'s retrieval-algorithms section.

**Likely to age quickly.** All F4 specifics; MS30; provider documentation; quantization-format guidance; MS9 (content from late 2024); MS10.

**No high-quality pedagogical resource exists** for LLM and agent security as an engineering discipline, a validity theory for trajectory evaluation, least autonomy as a method, or intervention budgets. "No adequate resource found" is the finding in each case.

**Architecture Concern — Human Review Required**

| ID | Concern | Evidence | Options (not decided here) |
| --- | --- | --- | --- |
| **AC1** | F3 targets **Design** depth, and its primary resource teaches reliability through generalizability theory and variance-components modelling (MS25 ch 5). **E3 as specified contains no random-effects or variance-components content.** F3's reliability requirement therefore presupposes statistics E3 does not supply | MS25 ch 5 contents (Direct); proposal E3 knowledge list | Teach reliability at Understand depth from the conceptual sections; or add the missing statistics to E3; or declare it an F3-internal prerequisite |

[⬆ Back to Contents](#contents)

---

## Q. Resource Anti-Bloat Audit

**For every mandatory item: without this resource, which required capability becomes inadequately taught?**

| # | Without it, the learner would not be adequately taught… |
| --- | --- |
| MS1 | …optimization behaviour, learning-rate divergence, and the chain from likelihood to cross-entropy to loss, with runnable code |
| MS2 | …named distributions and MLE — the exact dependency failure the audit found |
| MS3 | …reverse-mode differentiation at Implement depth |
| MS4 | …computational inference, the bootstrap at Implement depth, and confidence-interval interpretation in Python |
| MS5 | …experiment design, randomization units, A/A tests, sample-ratio mismatch and interference — no free candidate matches it |
| MS6 | …paired model comparison on a shared test set and evaluation power |
| MS7 | …calibration as a practical procedure |
| MS8 | …what a calibrated probability means and how miscalibration is measured |
| MS9 | …the system-level view of RAG, agents, memory and architecture, and serving choices framed as application decisions |
| MS10 | …building an agent from scratch without a framework — **conditional**: a curriculum-authored exercise is the fallback |
| MS11 | …why more context can reduce quality |
| MS12 | …autonomy and human oversight as design variables |
| MS13 | …generate-and-verify with external verifiers |
| MS14 | …the evidence that multi-agent systems are conditional, not a default |
| MS15 | …cost-controlled agent evaluation and the strength of simple baselines |
| MS16 | …containment architecture and AI threat modeling — nothing else teaches design reasoning |
| MS17 | …privilege and data-flow separation as a mechanism, and its utility cost |
| MS18 | …why reading untrusted content is itself an attack surface |
| MS19 | …why detection-based defenses fail under adaptive attack |
| MS20 | …measuring attack success and utility empirically |
| MS21 | …poisoning, extraction and evasion as structured attack families |
| MS22 | …adversarial examples and the robust-optimization intuition behind adaptive attacks |
| MS23 | …the corrected understanding that poisoning does not dilute with scale |
| MS24 | …model extraction through production interfaces |
| MS25 | …construct validity and reliability as formal measurement concepts |
| MS26 | …how contamination and test-set reuse distort rankings, and why saturated benchmarks stop informing |
| MS27 | …construct validity grounded in real LLM benchmarks, with a usable checklist |
| MS28 | …how to design a human-evaluation study |
| MS29 | …error analysis into failure taxonomies, and a procedure for validating a judge before relying on it |
| MS30 | …trajectory-evaluation vocabulary and practice — no durable alternative exists |
| MS31 | …validity reasoning specific to agent benchmarks |
| MS32 | …serving arithmetic with practice problems |
| MS33 | …routing and cascades — no other candidate covers them |
| MS34 | …an evidence-based rule for choosing quantization formats |

**Every mandatory item has a concrete answer.** Two are conditional: MS10 (if verification fails, replace with an authored exercise) and MS35 (drop if *AI Engineering* proves to cover ANN index choice).

**Candidates that failed the test and were demoted** — each because another retained item already teaches the capability:

| Demoted | Now | Covered instead by |
| --- | --- | --- |
| *Mathematics for Machine Learning* | Reference | MS1, MS2 |
| Distill momentum; CS231n notes | Optional | MS1; MS3 |
| OpenIntro IMS; Card et al.; Facure | Optional | MS4, MS6 |
| Chroma "Context Rot"; Tam et al.; MAST; CoALA | Optional | MS11; MS9; MS14; MS9 |
| Lakshmanan and Hapke | Optional | MS9 |
| Roitman guide | Reference | MS9, MS10 and the papers |
| Carlini et al. 2019; Microsoft red-team lessons | Optional | MS19, MS20 |
| Wallach et al.; Artstein and Poesio; EvalGen; Hardt chs 3 and 12 | Optional | MS25; MS25 ch 5; MS29; MS6 |
| CS336 lecture 10; Databricks guide; RouteLLM; kipply | Optional | MS32 and MS9; MS32; MS33; MS32 |
| *NLP in Action* as a whole | Remove candidate | See [K](#k-r9-nlp-in-action-reassessment) |
| Operations handbook ch 8 for serving | Reference | MS9, MS32 |

**Residual bloat risk.** F4 remains the heaviest block at about 230 pages across nine items. Every item passed the test, so the weight is a consequence of the field having no textbook, not of over-inclusion. It should be re-examined when a teaching text appears.

[⬆ Back to Contents](#contents)

---

## R. Research Conclusions

**Strong evidence**

- No single resource adequately covers any of the six unresourced blocks.
- E3 needs at least two resources plus targeted readings; inference, experimentation, model-comparison statistics and calibration are carried by different literatures.
- Containment architecture for LLM agents is taught only by 2025 design papers; detection-based defenses fail under adaptive attack.
- The published LLM-from-scratch book does not implement tokenization by hand or teach RoPE; the repository does.
- *NLP in Action*'s unique required contribution is confined to one section.
- The NLP textbook teaches late-interaction retrieval and reranking but not ANN indexing (K1).

**Moderate evidence**

- *AI Engineering* is the best cross-block anchor for F2 and F5 — page-level structure verified, subsection depth not.
- *AI Measurement Science* and Hardt together teach evaluation as measurement at the required depth.
- The E2 and E3 combinations are adequate at Understand and Implement depth.
- The serving supplement covers the durable concepts at decision depth.

**Weak or provisional**

- Dibia as the F2 Implement path.
- The Anthropic agent-evaluation post on the normal path.
- Kim et al.'s quantitative claims.
- Every Fast-Moving item.

**Still unresolved**

- Four F2 capabilities with no teaching resource.
- Trajectory-evaluation validity as science.
- AC1.
- The conditional MS35.
- Replacement of the LLM operations handbook.

**Answers to the twelve questions.**

| # | Question | Answer |
| --- | --- | --- |
| 1 | What should teach E2? | *Dive into Deep Learning* (selected) + Piech for probability + micrograd for reverse mode |
| 2 | What should teach E3? | *Computational and Inferential Thinking* + Kohavi et al. (selected) + Miller + scikit-learn and Guo on calibration |
| 3 | What should teach F2? | *AI Engineering* (selected) + five required papers; Dibia provisionally for the from-scratch path; four capabilities need authored material |
| 4 | What should teach AI security in F4? | The design-patterns paper and CaMeL for architecture; "The Attacker Moves Second" and AgentDojo for evaluation; Greshake, NIST, Kolter–Madry, Souly and Carlini for attack families |
| 5 | What should teach F3? | *AI Measurement Science* + Hardt (selected) + Bean + van der Lee + Husain and Shankar + the agent-evals post and ABC |
| 6 | What should teach modern serving in F5? | *AI Engineering* ch 9 and parts of ch 10 + the scaling-book inference chapter + the routing survey + the quantization study |
| 7 | Which uncertainties are resolved? | All four named themes: preference tuning, evaluation content, security content, A/B depth — plus four audit corrections (K1–K4) |
| 8 | Book, repository or both for E7? | Evidence supports **both**: the book for the core; the repository, pinned to a commit, for tokenization-by-hand, RoPE, KV cache and modern architectures |
| 9 | Does *NLP in Action* still earn learner time? | Not as a whole. One section conditionally for E8/F6; one chapter as an EX7 reference |
| 10 | Minimum coherent set? | 34 items, 3 paid, plus one conditional ([M](#m-proposed-minimal-resource-set)) |
| 11 | Where is a good teaching resource still missing? | LLM and agent security textbook; trajectory-evaluation validity; least-autonomy method; intervention budgets; failure-origin diagnosis; calibration pedagogy |
| 12 | Durable anchors vs Modern-track references? | Durable-class anchors are listed with their currency class in [M](#m-proposed-minimal-resource-set); Modern Practice items are in [O](#o-modern-practice-reference-layer) |

> ⚠️ None of these conclusions is a curriculum decision.
>
> They are evidence for human review.

[⬆ Back to Contents](#contents)

---

## S. Proposed Next Step

**Human review of this research artifact against [design/curriculum-proposal.md](../design/curriculum-proposal.md).**

Decisions this research surfaces for the reviewer, highest leverage first:

1. Whether to accept three paid anchors, especially one book underpinning two blocks (MS9).
2. Whether to accept a paper-based F4 of about 230 pages while no textbook exists.
3. Whether to verify Dibia (MS10) before adoption or plan an authored exercise instead.
4. How to resolve Architecture Concern AC1.
5. Whether to check *AI Engineering*'s retrieval-algorithms section to settle MS35.
6. Whether E7 may formally depend on pinned repository material.

> ⚠️ Do not update `ROADMAP.md`, the website or `PROJECT-STATE.md`, create a syllabus, or begin maintenance infrastructure on the basis of this report.

[⬆ Back to Contents](#contents)

---

## Sources

All accessed **2026-09-18**. Tier in parentheses: **D** Direct · **I** Indirect · **U** Uncertain.

**R1 — Mathematics**

- d2l.ai: [preliminaries](https://d2l.ai/chapter_preliminaries/index.html), [probability](https://d2l.ai/chapter_preliminaries/probability.html), [autograd](https://d2l.ai/chapter_preliminaries/autograd.html), [optimization](https://d2l.ai/chapter_optimization/index.html), [gradient descent](https://d2l.ai/chapter_optimization/gd.html), [maths appendix](https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html), [maximum likelihood](https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/maximum-likelihood.html), [information theory](https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/information-theory.html) (D)
- [mml-book.github.io](https://mml-book.github.io/) (D); [MML contents scan](https://toc.library.ethz.ch/objects/pdf03/z01_978-1-108-47004-9_01.pdf) (D); [Cambridge page](https://www.cambridge.org/highereducation/books/mathematics-for-machine-learning/5EE57FD1CFB23E6EB11E130309C7EF98) (D)
- [Piech index](https://chrispiech.github.io/probabilityForComputerScientists/en/index.html), [Piech MLE](https://chrispiech.github.io/probabilityForComputerScientists/en/part5/mle/) (D)
- [micrograd](https://github.com/karpathy/micrograd), [Zero to Hero](https://karpathy.ai/zero-to-hero.html) (D)
- [Deep Learning TOC](https://www.deeplearningbook.org/contents/TOC.html) (D); [handson-mlp](https://github.com/ageron/handson-mlp) (D)
- [Coursera specialization](https://www.coursera.org/specializations/mathematics-for-machine-learning-and-data-science) (D); [mitmath/matrixcalc](https://github.com/mitmath/matrixcalc) (D), [notes](https://arxiv.org/pdf/2501.14787) (I)
- [CS231n backprop](https://cs231n.github.io/optimization-2/) (D); [Distill momentum](https://distill.pub/2017/momentum/) (D); [CS229 probability review](https://cs229.stanford.edu/section/cs229-prob.pdf) (D); [PML book 1](https://probml.github.io/pml-book/book1.html) (D); [probabilitybook.net](http://probabilitybook.net) (I)

**R2 — Statistics and experimentation**

- [inferentialthinking.com](https://inferentialthinking.com/) and chapters [2](https://inferentialthinking.com/chapters/02/causality-and-experiments/index.html), [11](https://inferentialthinking.com/chapters/11/testing-hypotheses/index.html), [12](https://inferentialthinking.com/chapters/12/comparing-two-samples/index.html), [13](https://inferentialthinking.com/chapters/13/estimation/index.html), [14](https://inferentialthinking.com/chapters/14/why-the-mean-matters/index.html) (D)
- [OpenIntro IMS](https://openintro-ims.netlify.app/) (D); [Think Stats](https://allendowney.github.io/ThinkStats/) (D)
- [experimentguide.com](https://experimentguide.com/) (D); [Cambridge contents](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59) (D)
- [Miller 2024](https://arxiv.org/abs/2411.00640) (D); [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html) (D); [Guo et al. 2017](https://arxiv.org/abs/1706.04599) (D)
- [Facure](https://matheusfacure.github.io/python-causality-handbook/landing-page.html) (D); [Learning Data Science](https://learningds.org/intro.html) (D); [MIT 18.05](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/syllabus/) (D); [MSMB ch 6](https://web.stanford.edu/class/bios221/book/06-chap.html) (D)
- [Dror et al. 2018](https://aclanthology.org/P18-1128/) (D); [Card et al. 2020](https://aclanthology.org/2020.emnlp-main.745/) (D); [Hernán and Robins](https://miguelhernan.org/whatifbook) (D)

**R3 — Compound AI systems**

- [*AI Engineering* TOC](https://github.com/chiphuyen/aie-book/blob/main/ToC.md) (D, verified by the report author); [agents excerpt](https://huyenchip.com/2025/01/07/agents.html) (D)
- [multiagentbook.com](https://multiagentbook.com/) (D, partial); [Dibia repository](https://github.com/victordibia/designing-multiagent-systems) (I)
- [Roitman](https://arxiv.org/abs/2606.24937) (D abstract); [Lakshmanan and Hapke](https://github.com/lakshmanok/generative-ai-design-patterns) (D); [Gullí](https://link.springer.com/book/10.1007/978-3-032-01402-3) (I); [Albada](https://www.oreilly.com/library/view/building-applications-with/9781098176495/) (I); [Illustrated Guide](https://www.oreilly.com/library/view/an-illustrated-guide/9798341662681/) (I)
- [CS329Z](https://cs329z.stanford.edu/) (D); [Berkeley Agentic AI](https://agenticai-learning.org/f25) (D); [CMU 11-766](https://cmu-llms.org/schedule/) (D); [CU Boulder CSCI 7000](https://danny.cs.colorado.edu/courses/csci7000-005_Sp26/index.html) (D)
- [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) (D); [Context Rot](https://www.trychroma.com/research/context-rot) (D); [Tam et al.](https://arxiv.org/abs/2408.02442) (D); [JSONSchemaBench](https://openreview.net/forum?id=FKOaJqKoio) (I)
- [Feng et al.](https://arxiv.org/abs/2506.12469) (D); [Kambhampati et al.](https://arxiv.org/abs/2402.01817) (D); [MAST](https://arxiv.org/abs/2503.13657) (D); [Kim et al.](https://arxiv.org/abs/2512.08296) (D); [Kapoor et al.](https://arxiv.org/abs/2407.01502) (D); [τ-bench](https://arxiv.org/abs/2406.12045) (D); [Yehudai et al.](https://arxiv.org/abs/2503.16416) (D); [CoALA](https://arxiv.org/abs/2309.02427) (D, venue U); [BAIR compound AI](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/) (I); [Mei et al.](https://arxiv.org/abs/2507.13334) (D)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (D); [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (D)

**R4 — AI security**

- [Design patterns](https://arxiv.org/abs/2506.08837) (D); [CaMeL](https://arxiv.org/abs/2503.18813) (D); [Greshake et al.](https://arxiv.org/abs/2302.12173) (D); [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) (D); [On Evaluating Adversarial Robustness](https://arxiv.org/abs/1902.06705) (D); [AgentDojo](https://arxiv.org/abs/2406.13352) (D)
- [Kolter–Madry tutorial](https://adversarial-ml-tutorial.org/) (D); [NIST AI 100-2 E2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) and [PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf) (D)
- [Microsoft red-team lessons](https://arxiv.org/abs/2501.07238) (D); [Souly et al.](https://arxiv.org/abs/2510.07192) (D); [Stealing](https://arxiv.org/abs/2403.06634) (D); [extraction survey](https://arxiv.org/abs/2506.22521) (I); [poisoning review](https://arxiv.org/abs/2506.06518) (I)
- [UMass COMPSCI 684](https://cs684-umass.github.io/) (D); [Wilson](https://www.oreilly.com/library/view/the-developers-playbook/9781098162191/) (I); [Joseph et al. contents](https://www.cambridge.org/core/books/abs/adversarial-machine-learning/contents/4F6DD3B05099A8EF62BD1AC3DDFF9671) (D); [XACS134](https://online.stanford.edu/courses/xacs134-ai-security) (U)
- [Meta Agents Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/) (D); [Google secure agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/) (I); [Gemini IPI lessons](https://arxiv.org/abs/2505.14534) (D); [Abdelnabi and Bagdasarian](https://arxiv.org/abs/2605.17634) (D); [OWASP Agentic 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (I); [MITRE ATLAS](https://atlas.mitre.org/) (I)

**R5 — Evaluation science**

- AIMS [textbook](https://aimslab.stanford.edu/textbook), [ch 1](https://aimslab.stanford.edu/textbook/src/chap1.html), [ch 5](https://aimslab.stanford.edu/textbook/src/chap5.html), [ch 11](https://aimslab.stanford.edu/textbook/src/chap11.html), [ch 12](https://aimslab.stanford.edu/textbook/src/chap12.html) (D)
- Hardt [home](https://mlbenchmarks.org/), [ch 3](https://mlbenchmarks.org/03-detecting-differences.html), [ch 11](https://mlbenchmarks.org/11-evaluating-language-models.html), [ch 13](https://mlbenchmarks.org/13-model-moves-data.html), [ch 14](https://mlbenchmarks.org/14-evaluation-frontier.html) (D); [Princeton UP](https://press.princeton.edu/books/hardcover/9780691284293/the-emerging-science-of-machine-learning-benchmarks) (I)
- [Bean et al.](https://arxiv.org/abs/2511.04703) (D); [Wallach et al.](https://arxiv.org/abs/2502.00561) (D); [Salaudeen et al.](https://arxiv.org/abs/2505.10573) (D); [Artstein and Poesio](https://aclanthology.org/J08-4004/) (D); [van der Lee et al.](https://aclanthology.org/W19-8643/) (D); [EvalGen](https://arxiv.org/abs/2404.12272) (I)
- [Husain and Shankar FAQ](https://hamel.dev/blog/posts/evals-faq/) (D); [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (D); [ABC](https://arxiv.org/abs/2507.02825) (D); [Biderman et al.](https://arxiv.org/abs/2405.14782) (D); [contamination survey](https://arxiv.org/abs/2406.04244) (I); [Norman et al.](https://arxiv.org/abs/2606.19544) (D); [Jacobs and Wallach](https://arxiv.org/abs/1912.05511) (I); [saturation study](https://arxiv.org/html/2602.16763v1) (I)

**R6 — Modern serving**

- [Scaling book inference](https://jax-ml.github.io/scaling-book/inference/) (D); [CS336](https://cs336.stanford.edu/) and [lecture 10 source](https://github.com/stanford-cs336/spring2025-lectures/blob/main/lecture_10.py) (D)
- [kipply](https://kipp.ly/transformer-inference-arithmetic/) (D); [efficient-dl-systems](https://github.com/mryab/efficient-dl-systems) (D); [MIT 6.5940](https://hanlab.mit.edu/courses/2026-fall-65940) (D); [CMU 11-868](https://llmsystem.github.io/llmsystem2026spring/) (I)
- [Pan and Li survey](https://arxiv.org/abs/2506.21901) (D); [speculative decoding](https://arxiv.org/abs/2211.17192) (D); [PagedAttention](https://arxiv.org/abs/2309.06180) (D); [DistServe](https://arxiv.org/abs/2401.09670) (D); [Hao AI Lab retrospective](https://haoailab.com/blogs/distserve-retro/) (I)
- [Databricks guide](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices) (D); [Anyscale continuous batching](https://www.anyscale.com/blog/continuous-batching-llm-inference) (D); [Modular handbook](https://handbook.modular.com/) (D)
- [Routing survey](https://arxiv.org/abs/2603.04445) (D); [RouteLLM](https://arxiv.org/abs/2406.18665) (D); [FrugalGPT](https://arxiv.org/abs/2305.05176) (I); [Kurtic et al.](https://arxiv.org/abs/2411.02355) (D); [Erdil](https://arxiv.org/abs/2506.04645) (D)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) (D); [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) (D)

**R7–R9 — Existing resources**

- O'Reilly table-of-contents endpoint for ISBNs 9781098150952, 9781098107956, 9798341607972, 9781836200079, 9781617299445 (D, headings only, via the desktop application's built-in browser)
- [Hands-On LLMs repository](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) (D); [LLM Engineer's Handbook repository](https://github.com/PacktPublishing/LLM-Engineers-Handbook) (D); [dmls-book](https://github.com/chiphuyen/dmls-book) (D); [handson-mlp](https://github.com/ageron/handson-mlp) (D)
- [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) (D); [reasoning-from-scratch](https://github.com/rasbt/reasoning-from-scratch) (D); [Manning: Build a LLM](https://www.manning.com/books/build-a-large-language-model-from-scratch) (D); [Manning: Build a Reasoning Model](https://www.manning.com/books/build-a-reasoning-model-from-scratch) (I)
- [Manning: NLP in Action 2e](https://www.manning.com/books/natural-language-processing-in-action-second-edition) (D); [liveBook ch 10](https://livebook.manning.com/book/natural-language-processing-in-action-second-edition/chapter-10) (D); [nlpia2 repository](https://gitlab.com/tangibleai/nlpia2) (D)
- [*Speech and Language Processing* ch 11](https://web.stanford.edu/~jurafsky/slp3/11.pdf), draft of 2026-08-19 (D, retrieved and text-searched by the report author)

[⬆ Back to Contents](#contents)

</div>
