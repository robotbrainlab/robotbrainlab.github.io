<div align="justify">

# Learner-Experience Review — 2026-09-20

| | |
| --- | --- |
| **Type** | Learner-experience reconciliation: presentation findings, a statistics audit, and a review of selected-reading decisions |
| **Date** | 2026-09-20 |
| **Trigger** | The owner reviewed the finished roadmap as a long-term learner and reported that the curriculum is well researched but the learner experience explains too little: steps read as topic lists and reading assignments, statistics is hard to see as a progression, resources feel fragmented, and no single place builds a mental model of AI |
| **Status** | **Presentation changes are implemented.** The two curriculum proposals in [4](#4-proposals-requiring-approval) are **not** implemented; they change assigned reading and need human approval under [MAINTENANCE.md §6](../MAINTENANCE.md#6-human-approval-boundary) |
| **Inputs** | [ROADMAP.md](../ROADMAP.md) (Baseline 2) · [LEARNING-GUIDE.md](../LEARNING-GUIDE.md) · [design/curriculum-proposal.md](../design/curriculum-proposal.md) · [design/learner-guide.md](../design/learner-guide.md) · [resource coverage audit](../research/2026-09-18-resource-coverage-audit.md) · [targeted resource research](../research/2026-09-18-targeted-resource-research.md) · [independence audit](../research/2026-09-18-project-wide-independence-audit.md) · [current-practice register](modern-practice-register.md) · narrow verification of two tables of contents (see [5](#5-sources)) |

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Statistics Audit](#1-statistics-audit)
2. [Probability → Statistics → Evaluation](#2-probability--statistics--evaluation)
3. [Selected-Reading Review](#3-selected-reading-review)
4. [Proposals Requiring Approval](#4-proposals-requiring-approval)
5. [Sources](#5-sources)

</details>

---

## 1. Statistics Audit

**Question.** A learner's first impression was "where are the fundamentals of statistics?" Is the statistical foundation present, hidden, or genuinely incomplete?

**Where statistical material lives.** Probability is in **E2** (step 2). Inference and experimentation are in **E3** (step 4). Measurement and testing are in **E10** (step 6). The science of measurement is in **F3** (step 12). Agreement statistics appear in E3 and again in F3; calibration is in E3; repeated-trial reliability is in E3 and used from step 11 onwards.

**Checklist result.** Each concept the owner listed was traced to the block that teaches it and the assigned portion that carries it.

| Concept | Status | Where |
| --- | --- | --- |
| Populations and samples; parameters versus statistics | Present | E3 · *Computational and Inferential Thinking* ch 10 |
| Descriptive versus inferential reasoning | Present | E1 (exploratory analysis) → E3 chs 10–13 |
| Random variables, distributions | Present | E2 · Piech Parts 2–3; *Dive into Deep Learning* §22.1 |
| Expectation and variance | Present | E2 · Piech Part 2 |
| Covariance and correlation | **Present in the resource, outside the assigned portion** | Piech Part 3 includes a correlation chapter; E2 assigns Part 3 only "to joint and marginal" |
| Sampling variability; sampling distributions; standard error | Present | E3 · *Computational and Inferential Thinking* chs 10, 13, 14.5 |
| Estimation; estimator bias and variance | Present | E3 (estimation) and E4 (bias–variance for models) |
| Confidence intervals; the bootstrap | Present, at Implement depth | E3 · ch 13 |
| Central limit theorem | Present | E3 · 14.4 |
| Hypothesis testing; null and alternative; Type I and II error | Present | E3 · chs 11–12 |
| Statistical power | Present | E3 · Miller, "Adding Error Bars to Evals"; *Computational and Inferential Thinking* 14.6 |
| Statistical versus practical significance | Present, framed as costed errors | E10 success specification; Kohavi ch 1 |
| Paired comparisons | Present | E3 · Miller (paired model comparison on shared items) |
| Repeated stochastic trials; pass@k versus pass^k | Present | E3, with a planned simulation |
| Calibration | Present | E3 · scikit-learn §1.16, with a planned exercise |
| Annotator agreement | Present | E3 · *AI Measurement Science* ch 5 |
| Confounding; controlled experiments | Present | E3 · *Computational and Inferential Thinking* ch 2; Kohavi ch 1 |
| Basic regression interpretation | Present | E4 · *Hands-On ML* chs 1–8 |

**Finding.** The statistical foundation is **present and adequate for the accepted capability**. Nothing required by an accepted block is missing. Two items deserve attention:

1. **A presentation failure, now fixed.** The material is spread across four blocks and the guide never drew the line between them, so a learner scanning step 4 saw a list of procedures rather than a progression. The guide now states the progression explicitly ([2](#2-probability--statistics--evaluation)), groups step 4's concepts into five areas, and shows which source teaches each one.
2. **Two reading boundaries worth revisiting**, both in [4](#4-proposals-requiring-approval): the correlation chapter that falls just outside E2's assigned portion of Piech, and the first three sections of *Computational and Inferential Thinking* chapter 14, which precede the assigned 14.4–14.6.

**Not proposed.** Multiple-comparison procedures, sequential testing, Bayesian inference, and causal-inference methods beyond recognizing confounding. Each was considered by the [targeted resource research](../research/2026-09-18-targeted-resource-research.md#d-r2-statistics-inference-and-experimentation) and left out deliberately; nothing in the learner feedback changes that. The roadmap is not a statistics degree.

[⬆ Back to Contents](#contents)

---

## 2. Probability → Statistics → Evaluation

The learner asked for the distinction to be visible. It is now stated in the guide, at the point where each transition happens, and it reflects the accepted curriculum rather than a new taxonomy:

| Stage | Question it answers | Where |
| --- | --- | --- |
| Probability | Given a process, what outcomes should we expect? | Step 2 (E2) |
| Statistics | Given the finite sample we observed, what can we conclude? | Step 4 (E3) |
| Evaluation | Does this system work, and what evidence says so? | Step 6 (E10) |
| Evaluation science | Does the measurement itself mean what we claim? | Step 12 (F3) |

Step 4 renders this as a small diagram and step 12 closes it in prose. No curriculum content changed.

[⬆ Back to Contents](#contents)

---

## 3. Selected-Reading Review

Every core resource that is read selectively was re-examined against the questions the owner posed: how much is already assigned, what the omitted material teaches, whether it is relevant, whether omitting it interrupts a coherent argument, and whether another source teaches it better.

| Resource | Currently assigned | Omitted material | Relevant? | Recommendation |
| --- | --- | --- | --- | --- |
| Piech, *Probability for Computer Scientists* | Parts 1–3 "to joint and marginal", Part 5, the information-theory chapter | Part 3's later chapters (correlation, Bayesian networks, general inference) and most of Part 4 (beta distribution, adding random variables, central limit theorem, sampling, bootstrapping, algorithmic analysis, distance between distributions) | Yes — Part 4 is the probability-to-statistics bridge, and the guide already reaches into it for information theory | **Change to complete** — see [4.1](#41-read-piech-complete) |
| *Computational and Inferential Thinking* | Chs 2, 10–13, 14.4–14.6 | Chs 1, 3–9 (Python, tables, visualization); 14.1–14.3 (properties of the mean, variability, the SD and the normal curve); chs 15–18 (prediction, regression, classification) | Chs 3–9 and 15–18: no, duplicated by step 1 and *Hands-On ML*. 14.1–14.3: yes, they are the three short sections immediately before the assigned 14.4 | **Keep selected, extend chapter 14 to the whole chapter** — see [4.2](#42-read-chapter-14-whole) |
| *Dive into Deep Learning* | §2.3–2.6, §12.1–12.4, §12.11, §22.1, §22.4, §22.7, §22.11 | The rest of a reference-scale textbook | No — its deep-learning chapters duplicate *Hands-On ML*, which is read whole | Keep selected |
| *Speech and Language Processing* | Chs 2, 5, 11, 10, §1.9, §1.10, bias sections; Volume III as specialization | 26-chapter living textbook | Partly, as specialization | Keep selected — reference-scale, and the guide now says so at each use |
| *Natural Language Processing in Action* | §10.3.2–10.3.6; ch 11 as specialization | Classical and neural NLP on dated framework versions | No — duplicated by *Hands-On ML* and the from-scratch book | Keep selected |
| Kohavi, Tang and Xu | Ch 1 only (free) | Chs 2–23, paid | Yes but optional: running experiments at scale | Keep selected — the [targeted research](../research/2026-09-18-targeted-resource-research.md#d-r2-statistics-inference-and-experimentation) preferred more chapters; cost keeps them optional depth. Recorded as a standing item, not a defect |
| *AI Measurement Science* | Ch 5 agreement sections (E3); chs 1, 5, 11, 13 (F3) | Item-response theory, fitting measurement models | No — beyond the required depth | Keep selected |
| Hardt, *Emerging Science of ML Benchmarks* | Chs 11, 14 | Research monograph; ch 3 duplicates step 4 | No | Keep selected |
| *How To Scale Your Model* | Inference chapter §§1, 2, 4 and problems 1–3 | Training at scale on accelerators | No — machine-learning-systems specialization | Keep selected |
| Husain and Shankar evals FAQ | Error-analysis, evaluation-design, annotation sections | FAQ entries outside those topics | No | Keep selected |
| NIST AI 100-2 E2025 | §2.1–2.4, §3.1–3.5, §4.1 | The rest of a standard | No — a reference | Keep selected |
| Moslem and Kelleher | §§1–3 and cascades | Survey remainder | No | Keep selected |
| *Hands-On ML*; *Designing Machine Learning Systems*; *Practical SQL*; *Python for Data Analysis*; *The Python Tutorial*; *Build a Large Language Model (From Scratch)*; *Hands-On Large Language Models*; *AI Engineering*; *LLM Engineer's Handbook* | Read whole already | — | — | No change |

**Principle applied.** Prefer complete reading when a core resource is reasonably scoped and most of it serves the intended capability; read selectively for reference-scale texts, specialist or dated material, substantial duplication with no pedagogical benefit, or content outside Data & Intelligence. Overlap is not by itself a reason to stop reading a coherent book: the same idea met twice, in theory and in simulation, is usually a gain.

[⬆ Back to Contents](#contents)

---

## 4. Proposals Requiring Approval

Both change assigned reading, which [MAINTENANCE.md §7](../MAINTENANCE.md#7-minor-changes) says is **not** minor. Neither is implemented. Both are small, and neither adds a resource, changes a capability, depth, prerequisite or sequence.

### 4.1 Read Piech complete

**Current state.** E2 assigns Parts 1–3 "to joint and marginal distributions", Part 5, and the information-theory chapter, stopping "before sampling, bootstrap and the CLT, which E3 teaches".

**Finding.** The verified table of contents shows the information-theory chapter is *inside* Part 4, so the assignment already crosses the stated stopping line. Part 4 — adding random variables, the central limit theorem, sampling, bootstrapping — is exactly the bridge from probability to statistics, and the guide asks the learner to cross it two steps later with a different book and a different style. The three omitted chapters at the end of Part 3 include correlation, which the learner's own checklist names.

**Evidence.** Piech's table of contents ([5](#5-sources)); [targeted resource research M3 and S1](../research/2026-09-18-targeted-resource-research.md#c-r1-mathematics-for-learning-systems); the book is free, short-chaptered and written as a sequence.

**Capability consequence.** None required — E3 already delivers sampling and the bootstrap at Implement depth. The gain is coherence: one continuous treatment of probability ending where statistics begins, and a second, theory-first encounter with the central limit theorem before step 4 teaches it by simulation.

**Learning cost.** Roughly ten additional short chapters in a free book, with material step 4 then reinforces.

**Proposed change.** In ROADMAP.md §14, change Piech's reading-plan row from "Named parts" to "Complete book", and change the E2 assigned portion to the complete book with a note that Part 4 prepares step 4's inference work. **Alternative if rejected:** add Part 3's correlation chapter and Part 4's "Adding Random Variables" to the assigned portion, which is the minimum that keeps the checklist item and the standard-error intuition inside E2.

### 4.2 Read chapter 14 whole

**Current state.** E3 assigns *Computational and Inferential Thinking* chapters 2, 10–13 and **14.4–14.6**.

**Finding.** Chapter 14 is "Why the Mean Matters": 14.1 properties of the mean, 14.2 variability, 14.3 the SD and the normal curve, then 14.4 the central limit theorem, 14.5 the variability of the sample mean, 14.6 choosing a sample size. The assignment begins at 14.4, three short sections into an argument that builds to it.

**Evidence.** The chapter's section list ([5](#5-sources)). The omitted sections are not duplicated elsewhere in a simulation-first form; E2 covers variance in probability terms.

**Capability consequence.** None required; the gain is that 14.4 stops arriving mid-argument.

**Learning cost.** Three short sections.

**Proposed change.** In ROADMAP.md §14 and the E3 block, replace "14.4–14.6" with "ch 14".

### Classification

Both are **Optional** under [MAINTENANCE.md §5](../MAINTENANCE.md#5-12-week-curriculum-review) — refinements, not defects. Neither blocks use of the roadmap. If approved, they are implemented together as a minor reading-plan revision; [MAINTENANCE.md §9](../MAINTENANCE.md#9-baseline-versioning) decides whether the result warrants a baseline increment, and on the present evidence it does not: no capability, depth, prerequisite or resource set changes.

[⬆ Back to Contents](#contents)

---

## 5. Sources

Verified for this review on 2026-09-20. No other external research was performed.

| ID | Source | Used for | Tier |
| --- | --- | --- | --- |
| L1 | Piech, *Probability for Computer Scientists*, table of contents — https://chrispiech.github.io/probabilityForComputerScientists/en/index.html | Part and chapter list, including the location of the information-theory chapter | P (direct) |
| L2 | *Computational and Inferential Thinking*, chapter list — https://inferentialthinking.com | Chapter titles | P (direct) |
| L3 | *Computational and Inferential Thinking*, "Why the Mean Matters" — https://inferentialthinking.com/chapters/14/why-the-mean-matters/ | Section list 14.1–14.6 | P (direct) |

[⬆ Back to Contents](#contents)

</div>
