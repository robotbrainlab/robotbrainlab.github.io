<div align="justify">

# Resource Coverage Audit — What the Baseline Roadmap's Resources Actually Teach

**Audit execution date:** 2026-09-18

**Question:** How much of the independently reconstructed Data & Intelligence landscape is already covered by the resources in the existing roadmap, at what depth, and where are the genuine coverage gaps?

**Status:** Evidence for the later curriculum-design step. This report makes **no curriculum changes**, assigns no topics to Fundamentals / Advanced / Mastery / Research, recommends no new resources, and removes nothing. [ROADMAP.md](../ROADMAP.md) was **not modified**.

**Inputs:** [ROADMAP.md](../ROADMAP.md) (resource inventory), [2026-09-17-data-intelligence-landscape.md](2026-09-17-data-intelligence-landscape.md) (areas C1–C19), [2026-09-17-roadmap-comparison.md](2026-09-17-roadmap-comparison.md) (prior gap analysis), [AGENTS.md](../AGENTS.md) (depth ladder, evidence standards).

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

- [A. Executive Summary](#a-executive-summary)
- [B. Methodology](#b-methodology)
- [C. Existing Resource Inventory](#c-existing-resource-inventory)
- [D. Resource-by-Resource Audits](#d-resource-by-resource-audits)
  - [D1. The Python Tutorial](#d1-the-python-tutorial)
  - [D2. Practical SQL](#d2-practical-sql)
  - [D3. PostgreSQL Exercises](#d3-postgresql-exercises)
  - [D4. Python for Data Analysis](#d4-python-for-data-analysis)
  - [D5. Hands-On Machine Learning with Scikit-Learn and PyTorch](#d5-hands-on-machine-learning-with-scikit-learn-and-pytorch)
  - [D6. Speech and Language Processing](#d6-speech-and-language-processing)
  - [D7. Natural Language Processing in Action](#d7-natural-language-processing-in-action)
  - [D8. Hugging Face Audio Course](#d8-hugging-face-audio-course)
  - [D9. Build a Large Language Model (From Scratch)](#d9-build-a-large-language-model-from-scratch)
  - [D10. Hands-On Large Language Models](#d10-hands-on-large-language-models)
  - [D11. Designing Machine Learning Systems](#d11-designing-machine-learning-systems)
  - [D12. LLM Engineer's Handbook](#d12-llm-engineers-handbook)
- [E. Cross-Resource Coverage Matrix](#e-cross-resource-coverage-matrix)
- [F. Foundation Coverage](#f-foundation-coverage)
- [G. Dependency Audit](#g-dependency-audit)
- [H. Overlap Audit](#h-overlap-audit)
- [I. Genuine Gap Analysis](#i-genuine-gap-analysis)
- [J. Answers to Special Questions](#j-answers-to-special-questions)
- [K. Completeness Audit](#k-completeness-audit)
- [L. Uncertainties](#l-uncertainties)
- [M. Sources](#m-sources)

</details>

---

## A. Executive Summary

**Twelve named resources were audited** (ten in Fundamentals, two in the pending engineering section), plus two placeholders with no resource attached (Mathematics Fundamentals, Python Projects).

**1. The baseline is stronger than a title-level reading suggests in three places, and weaker in several others.** Actual content inspection shows genuinely deep coverage of classical and deep machine learning, natural language processing, speech, transformer internals, and classical-ML production engineering. It also shows that several areas a reader might assume are covered are not.

**2. Three landscape areas are covered at or near "Core" across the board:** deep learning and representation learning (C5), modality work for language, vision, speech, time series and tabular data (C11), and — once the actual content is inspected — statistical/classical machine learning (C4).

**3. The single largest dependency-critical gap is mathematics, probability and statistics.** The roadmap's Mathematics section has **no resource at all**. The ML/DL book explicitly *names* probability and statistics as a prerequisite and supplies refresher notebooks for linear algebra and calculus **but not for statistics**. No audited resource teaches statistical inference as a subject. The only inferential statistics found anywhere is a significance-testing section and a bootstrap confidence-interval example in the NLP textbook.

**4. Reinforcement learning is covered — this corrects an assumption in the prior comparison report.** The current ML/DL book contains a full RL chapter (MDPs, Q-learning, DQN, actor-critic, PPO). What is absent is bandits, off-policy evaluation and multi-agent/game-theoretic material.

**5. Information retrieval *is* taught as a discipline, not only implicitly through RAG.** The NLP textbook has a retrieval chapter with BM25, dense retrieval and IR evaluation; the applied NLP book teaches search, ANN indexing and vector quantization. What is missing is ranking metrics (nDCG, MRR), learned sparse and late-interaction retrieval, and recommender systems entirely.

**6. The largest contemporary-practice gap is the compound-AI-systems layer (C13).** No audited resource teaches agents, tool-use protocols, context engineering, structured outputs/constrained decoding, memory, multi-agent orchestration or evaluation of agentic systems. Every LLM-era resource in the baseline predates the 2025–2026 agent and reasoning wave.

**7. Two important regressions were discovered inside resources the roadmap already lists.**
- The ML/DL book is a **new first edition of a PyTorch line published October 2025**, not a fourth edition of the TensorFlow line. Its changelog confirms the previous edition's **deployment-at-scale chapter was only partially merged** into a new chapter, and **SVMs were demoted to an online-only appendix**. A roadmap citing this book for deployment coverage no longer holds.
- The audio course's content is **2023-vintage** with no evidence of substantive updates, which is the largest currency risk in the baseline.

**8. Trustworthy AI coverage is real but lopsided.** Safety, bias, interpretability and benchmark validity are covered seriously in exactly one resource (the NLP textbook). Privacy (differential privacy), adversarial robustness, and AI security as an engineering discipline are effectively absent everywhere.

**9. Operations coverage is split across two books that barely overlap and both predate current practice.** The 2022 MLOps book owns data, monitoring, drift and organisational concerns but has essentially zero foundation-model content, as its own author states. The 2024 LLM ops handbook owns the fine-tune/serve/deploy path but binds it to nine specific commercial services and omits prompting, agents and statistics.

> ⚠️ Coverage classifications in this report describe what evidence shows a resource teaches.
>
> They are not judgments about whether a topic belongs in the curriculum, at what level, or in what order. Nothing here promotes a topic.

[⬆ Back to Contents](#contents)

---

## B. Methodology

**Fresh evidence.** Four parallel research threads investigated the resources independently on 2026-09-18, using official book pages, publisher tables of contents, author-maintained sites, official repositories and official documentation. Marketing descriptions were not accepted as evidence of detailed coverage. Where contents could not be verified, the finding is marked **Uncertain** rather than assumed.

**Evidence tiers used throughout:**

| Tier | Meaning |
| --- | --- |
| **Primary-direct** | The official page, repository, PDF or documentation was retrieved and read (for example the author's own changelog, an open-access edition, a course's table-of-contents file). |
| **Primary-indirect** | The source is primary but was reachable only through search-result snippets because the publisher blocked automated access (O'Reilly and Packt product pages both returned HTTP 403). |
| **Uncertain** | Could not be verified from any primary source. Stated explicitly rather than inferred. |

**Coverage scale** (conservative; a chapter title alone never justifies "Core"):

| Label | Meaning |
| --- | --- |
| **Core** | Substantial treatment; the learner is expected to understand or use the area meaningfully. |
| **Supporting** | Meaningful treatment, but not a principal focus. |
| **Introductory** | Introduces the concept without building substantial competence. |
| **Mentioned** | Brief exposure or reference only. |
| **Not Covered** | No evidence of treatment. |
| **Uncertain** | Evidence insufficient to classify. |

**Depth scale** ([AGENTS.md knowledge-depth ladder](../AGENTS.md#knowledge-depth)): Awareness · Use · Understand · Implement · Design · Research. Coverage and depth are recorded separately.

**Three kinds of statement are distinguished** throughout: **Observed** (verified from a primary source), **Inference** (reasoning from observed structure), **Open question** (unresolved).

**Supplementary foundation layer.** The independent landscape operated at the level of scientific and engineering disciplines and therefore under-represented programming, querying and exploratory analysis. As the landscape report itself records, this is a limitation of that report, not evidence that these foundations are unnecessary. This audit therefore adds a supplementary layer **F1–F6** (section F) so the audit does not inherit that blind spot. **This layer is an audit device, not a curriculum change.**

[⬆ Back to Contents](#contents)

---

## C. Existing Resource Inventory

Derived from [ROADMAP.md](../ROADMAP.md), not from any prior list.

| ID | Resource | Type | Baseline location | Identity verified |
| --- | --- | --- | --- | --- |
| — | *(none)* | — | Fundamentals §1 Mathematics Fundamentals | **No resource exists.** ROADMAP states detailed curriculum and resources "have not yet been finalized" |
| **R1** | The Python Tutorial (Python documentation) | Official tutorial | §2.1 Python | Python 3.14.7, page last updated 2026-09-17 |
| — | Python Projects | Practice (unspecified) | §2.2 Python | **No resource named**; sequence "will be designed later" |
| **R2** | *Practical SQL*, Anthony DeBarros, No Starch Press | Book | §3.1 SQL | 2nd edition, January 2022; no 3rd edition exists as of audit date |
| **R3** | PostgreSQL Exercises (pgexercises.com), Alisdair Owens | Interactive practice site | §3.2 SQL | 7 categories, 71 exercises |
| **R4** | *Python for Data Analysis*, Wes McKinney, O'Reilly | Book (free open-access web edition) | §4.1 Data Analysis | 3rd edition, 2022 |
| **R5** | *Hands-On Machine Learning with Scikit-Learn and PyTorch*, Aurélien Géron, O'Reilly | Book + notebooks | §5.1 ML & DL | **1st edition of the PyTorch line, October 2025** — not a 4th edition of the Keras/TensorFlow line, which remains a separate product |
| **R6** | *Speech and Language Processing*, Jurafsky & Martin | Free textbook draft | §6.1 NLP | 3rd edition draft of **19 August 2026**; no published final edition |
| **R7** | *Natural Language Processing in Action*, Lane & Dyshel, Manning | Book | §6.2 NLP | 2nd edition, January 2025 |
| **R8** | Hugging Face Audio Course | Free online course | §6.3 NLP (audio) | Content dated **2023**; no evidence of substantive updates |
| **R9** | *Build a Large Language Model (From Scratch)*, Sebastian Raschka, Manning | Book + actively maintained repo | §7.1 LLMs | September 2024; repository extended through 2026 |
| **R10** | *Hands-On Large Language Models*, Alammar & Grootendorst, O'Reilly | Book + notebooks | §7.2 LLMs | 2024 |
| **R11** | *Designing Machine Learning Systems*, Chip Huyen, O'Reilly | Book | Existing Engineering Section — MLOps | 2022 |
| **R12** | *LLM Engineer's Handbook*, Iusztin & Labonne, Packt | Book + end-to-end project repo | Existing Engineering Section — LLMOps | 1st edition, October 2024 |

**Resource-type distribution:** 8 books, 1 official tutorial, 1 free textbook draft, 1 online course, 1 interactive practice site. Project-based learning is named as an intent (§2.2) but has no resource. Two sections carry no resource at all.

[⬆ Back to Contents](#contents)

---

## D. Resource-by-Resource Audits

Each audit records identity, intended scope, actual structure (paraphrased), landscape mapping with coverage and depth, assumed prerequisites, and important omissions.

### D1. The Python Tutorial

**Identity.** Official Python documentation tutorial, Python Software Foundation; version 3.14.7 at audit; 16 top-level sections. **Baseline location:** Fundamentals §2.1.

**Intended scope (observed).** The tutorial states it "does not attempt to be comprehensive and cover every single feature" and aims to give "a good idea of the language's flavor and style", routing readers onward to the Library and Language References.

**Actual structure.** Interpreter use; informal introduction; control flow and functions (including `match`, argument forms, annotations, PEP-8); data structures and comprehensions; modules and packages; input/output and JSON; errors and exceptions (including exception groups); classes, iterators and generators; two standard-library tours (including `re`, `datetime`, `timeit`/`profile`, `doctest`/`unittest`, logging, decimal); virtual environments and pip; floating-point limitations.

**Foundation coverage.**

| Foundation area | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- |
| F1 Python programming | **Core** | Use | Full language tour with hands-on typing; **no exercises, no projects, no assessment** |
| F6 Practical tooling | **Supporting** | Use | `venv` and pip (§12); `timeit`/`profile`/`pstats`; `doctest`/`unittest` introduced with runnable examples (§10.11) |
| F3 Data manipulation | **Not Covered** | — | No dataframe concept; `array` module is compact storage, not vectorized computing |
| F5 Visualization | **Not Covered** | — | No plotting library appears anywhere |

**Landscape coverage.** None. No statistics, no ML, no data analysis.

**Assumes rather than teaches.** Ability to install software and use a shell.

**Important omissions.** Typing/`typing`, async, dataclasses, packaging and distribution, **version control (git is never mentioned)**, and the entire scientific Python stack.

---

### D2. Practical SQL

**Identity.** *Practical SQL: A Beginner's Guide to Storytelling with Data*, 2nd edition, No Starch Press, January 2022; PostgreSQL and pgAdmin; 20 chapters plus appendix; per-chapter "Try It Yourself" exercises with answers in the official repository. **Baseline location:** Fundamentals §3.1.

**Intended scope (observed).** Publisher and author present it as suitable for beginners including non-programmers, teaching SQL for data analysis and storytelling.

**Actual structure.** Setup; database and table creation; SELECT fundamentals; data types; import/export with real government datasets; basic math and descriptive statistics; joins; **table design (constraints, keys, indexes)**; grouping and summarising; **inspecting and modifying data, including transactions**; statistical functions (correlation, regression, rank, rolling averages); dates and times; advanced queries (subqueries, CTEs, cross-tab, CASE); text mining and full-text search; PostGIS spatial data; JSON; views, functions and triggers; psql and command-line utilities; maintenance (VACUUM, backup/restore); communicating findings.

**Foundation coverage.**

| Foundation area | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- |
| F2 SQL / querying | **Core** | Implement | Querying through window functions, CTEs, text search, spatial and JSON |
| F2b Database design and operation | **Core** | Understand | Constraints, keys, **indexes and their trade-offs**, transactions, views/functions/triggers, maintenance and backup |
| F4 Exploratory analysis / data quality | **Supporting** | Use | Ch. 10 "interviewing the dataset": missing, inconsistent and malformed values, then repairing them |
| F5 Visualization | **Not Covered** | — | No charting chapter; the communication chapter is prose guidance |

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C2 Statistics | Descriptive statistics, correlation, linear regression | **Introductory** | Use | Function-level only (percentiles, `corr()`, `regr_slope`); **no probability, sampling theory, significance testing or confidence intervals** |
| C10 Data for AI | Data quality, provenance questions | **Supporting** | Use | Ch. 10 quality checks; ch. 20 assessing data origins and consulting owners |
| C11 Modalities | Spatio-temporal / geospatial | **Introductory** | Use | PostGIS chapter is real but tool-specific |

**Assumes rather than teaches.** Almost nothing; it installs the tooling for the reader. Relational theory (normal forms, relational algebra) and query-plan analysis are not taught.

**Important omissions.** Visualization; probability and inference; experimentation; `EXPLAIN`/query-plan analysis (absent from the detailed contents — *Uncertain* whether mentioned in body text); version control.

---

### D3. PostgreSQL Exercises

**Identity.** pgexercises.com by Alisdair Owens; free browser-based SQL practice against a live PostgreSQL instance; 7 categories, 71 exercises; each with question, expected results, hint, and a commented reference solution with discussion. **Baseline location:** Fundamentals §3.2.

**Intended scope (observed).** The site states it is "designed for use as a partner to a good book or Postgres' excellent documentation" — it does not claim to teach SQL from scratch, and refers readers to other books when they struggle.

**Actual structure.** Basic (12), joins and subqueries (8), modifying data (9), aggregates (22, including window functions, running totals, rolling averages), date (10), string (7), recursive CTEs (3), over a three-table country-club schema.

**Foundation coverage.**

| Foundation area | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- |
| F2 SQL / querying | **Core** (practice) | Understand | Exercise discussions explain alternative solutions and correlated versus uncorrelated subqueries |
| F2b Database design | **Not Covered** | — | No DDL, normalisation, indexing, constraints, transactions or administration. The site explicitly warns its schema "is flawed in several aspects — please don't take it as an example of good design" |

**Landscape coverage.** None beyond aggregate functions.

**Assumes rather than teaches.** Basic SQL exposure; it is reinforcement, not instruction.

**Important omissions.** Schema design, indexing and performance (no `EXPLAIN`), data quality as a topic.

---

### D4. Python for Data Analysis

**Identity.** *Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter*, 3rd edition, O'Reilly, 2022; free open-access web edition; 13 chapters plus two appendices. **Baseline location:** Fundamentals §4.1.

**Intended scope (observed).** The author is explicit: the focus is "specifically on Python programming, libraries, and tools **as opposed to data analysis methodology**", and he endorses the framing of the work as data manipulation, wrangling or munging.

**Actual structure.** Python basics and IPython/Jupyter; built-in data structures; **NumPy arrays and vectorized computation**; pandas fundamentals; data loading and file formats; **data cleaning and preparation** (missing data, duplicates, binning, outliers, categorical types, string/regex); joining, combining and reshaping; **plotting and visualization** (matplotlib, pandas, seaborn); aggregation and group operations; **time series**; a short introduction to modelling libraries (Patsy, statsmodels, scikit-learn); five worked analyses. Appendix A covers ndarray internals, broadcasting, memory order, structured arrays and Numba; Appendix B covers IPython profiling and debugging.

**Foundation coverage.**

| Foundation area | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- |
| F3 Data manipulation | **Core** | Implement | The book's centre of gravity |
| F4 Exploratory data analysis | **Core** | Use | Missing data, duplicates, outlier filtering, group analysis; five full worked EDA examples; **no exercises or assessments** |
| F5 Visualization | **Core** (only source in baseline) | Use | matplotlib, pandas and seaborn plotting; API-teaching, not visual-design or perception theory |
| F6 Numerical computing | **Core** | Understand → Implement | dtypes, vectorization, broadcasting, memory layout, Numba JIT, profiling |
| F1 Python | **Supporting** | Use | Condensed language tutorial in ch. 2–3 |

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C2 Statistics | Descriptive statistics only | **Introductory** | Use | `describe`, correlation/covariance, quantile analysis; **no inference, hypothesis testing, confidence intervals or distributions** |
| C10 Data for AI | Cleaning and preparation | **Core** (technique) | Implement | Taught as pandas technique; **no data-quality framework** (validation rules, schemas, expectations, pipeline testing) |
| C11 Modalities | Time series (handling) | **Core** (handling) | Use | Resampling, rolling windows, time zones, periods; **no forecasting methodology, stationarity or ARIMA** |
| C4 Classical ML | scikit-learn introduction | **Introductory** | Use | One section; the author explicitly defers to other books |

**Assumes rather than teaches.** Statistics, ML methodology and domain knowledge. Ch. 12 assumes the reader already knows what OLS and AR models are.

**Important omissions.** Statistical methodology of any kind; experimentation; version control; testing; packaging.

---

### D5. Hands-On Machine Learning with Scikit-Learn and PyTorch

**Identity (corrected).** Aurélien Géron, O'Reilly, **released October 2025**, 878 pages, repository `ageron/handson-mlp`. The author's own changelog states this is **the first edition of the PyTorch version**, nicknamed *homlp* — **not** a fourth edition of the Keras/TensorFlow line, which continues as a separate product. **Baseline location:** Fundamentals §5.1.

**Intended scope (observed).** Concepts, tools and techniques to build intelligent systems, from classical ML through modern deep learning, with executable notebooks for every chapter.

**Actual structure.** Ch. 1–8 classical ML: the ML landscape; an end-to-end project; classification; training models (linear, polynomial, logistic, gradient descent, regularisation); decision trees; ensembles; dimensionality reduction; unsupervised learning. Ch. 9–19 deep learning: neural network introduction; **building networks with PyTorch**; training deep networks; CNNs; sequences with RNNs/CNNs; NLP with RNNs and attention; **transformers for NLP**; **vision and multimodal transformers**; **speeding up transformers** (online-only chapter); **autoencoders, GANs and diffusion**; **reinforcement learning**. Appendices: autodiff; mixed precision and quantization; SVMs (online-only); relative positional encoding; state-space models; other architectures.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C1 Mathematics | Optimization; autodiff | **Supporting** | Understand → Implement | Gradient descent (ch. 4), optimizer survey (ch. 11), autodiff appendix. Linear algebra/calculus only as *refresher notebooks* |
| C1 Mathematics | Probability and statistics | **Not Covered** | — | Named as a prerequisite; **refresher notebooks exist for linear algebra and calculus but not statistics** |
| C2 Statistics | Inference, testing, A/B, calibration | **Not Covered** | — | No such sections in any of the 19 notebooks; *Uncertain* whether prose mentions exist |
| C3 Methodology | Validation, cross-validation, error analysis | **Core** | Implement | Ch. 2 cross-validation and "analyze the best models and their errors"; ch. 3 has its own error-analysis section |
| C4 Classical ML | Linear/logistic, trees, ensembles, dimensionality reduction, clustering, GMM anomaly detection | **Core** | Implement | Ch. 4–8 |
| C4 Classical ML | Kernel methods / SVMs | **Supporting** | Understand | **Demoted to online-only appendix** in this edition |
| C4 Classical ML | Learning theory; probabilistic graphical models; online learning | **Introductory / Not Covered** | Awareness | Learning curves and bias–variance intuition only; Bayesian GMM is a clustering tool, not graphical-model instruction |
| C4 Classical ML | AutoML / hyperparameter optimization | **Supporting** | Use | Optuna introduced in ch. 10 |
| C5 Deep learning | Training mechanics; CNN/RNN lineage; transformers; ViT; stability and regularisation | **Core** | Implement | Ch. 9–16; ResNet-34, a translation transformer and ViT are each built from scratch |
| C5 Deep learning | Efficient attention; MoE; state-space models | **Supporting / Introductory** | Understand | Ch. 17 and online appendices |
| C5 Deep learning | Graph neural networks | **Not Covered** | — | Absent |
| C6 Generative modelling | Autoencoders, VAE, GAN, DCGAN, diffusion (+ flow matching extra) | **Core** | Implement | Ch. 18 — the baseline's only substantial non-text generative coverage |
| C7 Foundation models | Transformers, LoRA/PEFT, quantization, multimodal models | **Supporting** | Understand → Implement | Ch. 15–17, App. B; CLIP/BLIP-2/Gemini discussed in ch. 16 |
| C8 RL | MDPs, Q-learning, DQN, actor-critic, PPO | **Core** | Implement | Ch. 19 with Gymnasium and Stable-Baselines3 |
| C8 RL | Bandits, off-policy evaluation, multi-agent, imitation learning | **Not Covered** | — | Absent |
| C11 Modalities | Computer vision; time series; multimodal | **Core / Core / Supporting** | Implement | Ch. 12, 16; ch. 13 covers forecasting, ARMA family, multi-step and seq2seq |
| C11 Modalities | Speech; graphs; recommenders; documents | **Mentioned / Not Covered** | — | Audio appears as a single exercise |
| C15 Evaluation | Metrics, confusion matrix, ROC/PR, error analysis | **Core** | Implement | Ch. 3 |
| C15 Evaluation | Calibration; benchmark validity | **Not Covered** | — | No calibration section found |
| C16 Trustworthy AI | Fairness, privacy, robustness, safety | **Not Covered** (*Uncertain* for prose) | — | No such sections in any chapter heading; publisher page blocked automated verification |
| C17 Engineering | Distributed training (data/tensor/pipeline/context/expert parallelism, DDP, accelerate) | **Core** | Understand | Ch. 17 — the baseline's strongest distributed-training coverage |
| C17 Engineering | Model compression, mixed precision, quantization | **Supporting** | Understand | Appendix B |
| C17 Engineering | Deployment, serving, monitoring, MLOps | **Not Covered** | — | **Regression:** the previous edition's deployment-at-scale chapter was only "partially merged into Chapter 10" |
| C10 Data for AI | Cleaning, transformation pipelines, augmentation | **Supporting** | Implement | Ch. 2–3; no labelling, curation, synthetic data or documentation |

**Assumes rather than teaches.** Python basics; NumPy/pandas/matplotlib (tutorial notebooks provided); "some notions of linear algebra, calculus, statistics and probability".

**Important omissions.** Statistical inference; calibration; IR and ranking; fairness/privacy/robustness/safety as first-class topics; labelling and dataset documentation; **production serving, monitoring and MLOps**; graphs; recommender systems; symbolic AI.

**Note on exercise solutions (Observed).** Worked exercise solutions are published for ch. 1–13; solutions for ch. 14–19 (transformers, generative models, RL) are currently marked work-in-progress.

---

### D6. Speech and Language Processing

**Identity.** Jurafsky & Martin, 3rd edition **free online draft dated 19 August 2026**; 26 chapters in three volumes plus 11 web appendices; no published final edition ("When will the book be finished?" — "Don't ask."). **Baseline location:** Fundamentals §6.1.

**Intended scope (observed).** A comprehensive introduction to NLP, computational linguistics and speech recognition, now subtitled "with Language Models".

**Actual structure.** Volume I (language models): introduction; words and tokens; n-gram models; logistic regression; embeddings; neural networks; **transformers and pretraining**; **post-training**. Volume II (advanced topics): masked language models; **interpretability** (new, and described by the authors as about half-written); **retrieval-based models / IR and RAG**; **agents — an unwritten placeholder page**; machine translation; RNNs and LSTMs; **phonetics**; **automatic speech recognition**; **text-to-speech**. Volume III (linguistic structure): sequence labelling; constituency and dependency parsing; information extraction; semantic role labelling; sentiment lexicons; coreference; discourse; conversation. Appendices include HMMs, Naive Bayes, logical representations, WordNet.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C1 Mathematics | Probability in context; information theory | **Supporting** | Understand | N-gram probability, smoothing, perplexity ↔ entropy; derives logistic regression and gradient descent from scratch |
| C2 Statistics | Significance testing; confidence intervals | **Supporting** | Understand | §4.11 paired bootstrap significance testing; §13.6 constructs a 95% confidence interval by bootstrap — **the only inferential statistics found in the entire baseline** |
| C2 Statistics | A/B testing; causal inference; calibration | **Not Covered** | — | "A/B test" appears zero times; calibration is not a taught topic |
| C3 Methodology | Test sets, cross-validation, benchmark validity, contamination | **Supporting → Core** | Understand | §1.9 covers benchmarks, **data contamination**, LLM-as-a-judge, proxy metrics and Goodhart's Law by name |
| C4 Classical ML | Logistic regression; Naive Bayes | **Supporting** | Understand | Everything else (trees, ensembles, SVMs) absent |
| C5 Deep learning | Feedforward nets; transformers; pretraining | **Supporting** | Understand | Conceptual; **no code repository or notebooks anywhere** |
| C7 Foundation models | Pretraining; post-training (instruction tuning, RLHF, **DPO**); PEFT; decoding | **Core** | Understand | Ch. 7–9 |
| C8 RL | RL only as LLM post-training | **Introductory** | Awareness | Reward models, RLHF, DPO, PPO in passing; no MDPs or value iteration |
| C9 Symbolic AI | Parsing, SRL, logical representations, WordNet | **Supporting** | Understand | Volume III and web appendices; **no planning, search, constraint solving or knowledge graphs** |
| C10 Data for AI | Corpora; **datasheets and data statements**; **model cards** | **Supporting** | Understand | §2.5 and §4.12 — the baseline's only dataset-documentation coverage |
| C11 Modalities | NLP (full breadth); speech (phonetics, ASR, TTS) | **Core** | Understand | Ch. 15–17 include log-Mel, MFCC, CTC, WER, audio codecs, discrete tokens, spoken LMs |
| C12 IR | **BM25**, dense retrieval, IR evaluation, RAG, QA evaluation | **Core** | Understand | Ch. 11; **nDCG and MRR appear zero times** — ranking metrics limited to precision/recall/MAP |
| C13 Agents | — | **Not Covered** | — | **Chapter 12 exists as a single placeholder page; it is unwritten** |
| C15 Evaluation | Metrics across tasks; human evaluation; benchmark critique | **Core** | Understand | The most complete evaluation treatment in the baseline |
| C16 Trustworthy AI | Safety and alignment; bias in embeddings, MT and coreference; harms in classification; **interpretability** | **Core** (concepts) | Understand | §1.10, §4.12–4.13, §5.8, §13.7, §24.10, ch. 10; prompt injection appears in §1.10; **differential privacy appears zero times; "jailbreak" zero times**; ch. 10 is a half-written stub |
| C18 Governance | Environmental/cost accounting; societal impact | **Introductory** | Awareness | §1.9.5 and §1.10; no regulation or standards |
| C17 Engineering | — | **Not Covered** | — | "MLOps" and "monitor" appear zero times |

**Assumes rather than teaches.** **Not stated** — the current draft has no preface, and searches for prerequisite statements return nothing. By structure it builds its own mathematics but does not teach calculus or linear algebra.

**Important omissions.** No code or notebooks; the agents chapter is unwritten; interpretability is half-written; no calibration, no experiment design, no differential privacy, no non-language generative modelling, no classical ML beyond logistic regression, no deployment, no time series, graphs or recommenders.

---

### D7. Natural Language Processing in Action

**Identity.** Lane & Dyshel, Manning, **2nd edition, January 2025**, 688 pages; code at GitLab `tangibleai/nlpia2`. **Baseline location:** Fundamentals §6.2.

**Intended scope (observed).** Manning describes the audience as intermediate Python programmers familiar with deep-learning basics; remedial appendices lower the true floor.

**Actual structure.** Part 1 (classical): NLP overview and rule-based chatbot; **tokenization** (including WordPiece, n-grams, normalisation, logographic languages, sentiment with VADER and Naive Bayes); TF-IDF and relevance ranking; semantic analysis (LSA, PCA, SVD, LDA). Part 2 (neural): perceptron from scratch then PyTorch; **word embeddings** (Word2Vec training, GloVe, fastText, static versus contextual); CNNs for text; **RNNs and LSTMs built from scratch**. Part 3 (modern): **transformers** (positional encoding, assembling the pieces, translation, BERT fine-tuning); **LLMs in the real world** (scaling, smaller models, **semantic routing and guard rails**, **red teaming**, **hallucination**, and a substantial section on **search: full-text, semantic, approximate nearest neighbour, index choice, vector quantization**); **information extraction and knowledge graphs** (NER, coreference, dependency and constituency parsing, relation extraction, KG construction and QA); dialog engines (intent recognition, template/graph/generative responses, Rasa, LangChain). Appendices cover Python/regex, linear algebra, ML basics and **containerised deployment**.

**Balance (Observed).** Eight of twelve chapters are classical or pre-transformer neural NLP; four are transformer-era, and only two are transformer/LLM proper.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C1 Mathematics | Linear algebra refresher | **Introductory** | Awareness | Appendix C |
| C3 Methodology | Cross-validation, imbalanced data, metrics | **Introductory** | Use | Appendix D |
| C4 Classical ML | Naive Bayes, PCA/SVD, logistic neuron | **Supporting** | Implement | Chapters 2–5 |
| C5 Deep learning | Perceptron, CNN, **RNN/LSTM from scratch**; embeddings | **Core** | Implement | Chapters 5–8 |
| C5 Deep learning | Transformer architecture | **Supporting** | Understand → Implement | Ch. 9; *Uncertain* how deep the build is relative to a dedicated from-scratch book |
| C7 Foundation models | Fine-tuning (BERT classification, generative) | **Supporting** | Implement | §9.3.4, §10.2.2; **no instruction tuning, RLHF, DPO or RLVR** |
| C9 Symbolic AI | Parsing, IE, relation extraction, **knowledge graphs** | **Core** | Implement | Ch. 11 — the baseline's only KG-construction coverage |
| C11 Modalities | NLP tasks (sentiment, MT, IE, dialog) | **Core** | Implement | Across the book |
| C12 IR | Full-text search, semantic search, **ANN indexing, vector quantization** | **Supporting** | Use | §10.3; RAG by mechanism rather than by name |
| C13 Agents | Dialog systems, LangChain | **Introductory** | Use | Ch. 12 is dialog engines, **not tool-calling agents**; no protocols |
| C16 Trustworthy AI | **Guard rails, red teaming, hallucination, toxicity, data bias** | **Supporting** | Use | §10.1.3–10.1.4, §10.2.3, ch. 4, App. D — unusually explicit for an applied book; no prompt injection or privacy |
| C17 Engineering | Containerised microservice deployment | **Introductory** | Use | Appendix E (FastAPI, Docker, scaling) |

**Assumes rather than teaches.** Intermediate Python; deep-learning basics (partly remediated by appendices). PyTorch is taught in-line.

**Important omissions.** Speech; multimodality; agents and protocols; preference optimisation and RL; model quantization and serving optimisation; benchmark-driven LLM evaluation; pretraining at scale.

---

### D8. Hugging Face Audio Course

**Identity.** Free self-paced course by Hugging Face; units dated **2023**; no version number and **no evidence of substantive content updates since 2023**, although the repository remains active for translations. **Baseline location:** Fundamentals §6.3.

**Intended scope (observed).** Transformer-based audio applications for readers with a deep-learning background and general transformer familiarity; no audio expertise required.

**Actual structure.** Unit 1 audio data (sampling rate, amplitude, waveforms, **DFT/FFT, spectrograms, log-Mel**, preprocessing, dataset streaming); Unit 2 applications via pipelines; Unit 3 **architectures for audio (CTC, seq2seq, classification)**; Unit 4 **fine-tuning a music classifier**; Unit 5 **ASR (pre-trained models, dataset choice, evaluation, fine-tuning)**; Unit 6 **TTS (datasets, fine-tuning SpeechT5, evaluation)**; Unit 7 speech-to-speech translation, voice assistant, meeting transcription; Unit 8 certificate.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C11 Modalities | Speech and audio | **Core** | Use | Three fine-tuning projects shipped to the Hub with Gradio demos |
| C5 Deep learning | Audio architectures (CTC versus seq2seq trade-offs) | **Supporting** | Understand | Unit 3 states readers "don't need to know the inner details"; **no implementation** |
| C15 Evaluation | **WER, CER, word accuracy, RTFx, text normalisation; MOS for TTS** | **Core** (speech) | Understand | Worked example shows WER falling from 168% to 126% through normalisation alone — genuine error-analysis hygiene |
| C10 Data for AI | Audio preprocessing, streaming large datasets, dataset choice for ASR/TTS | **Supporting** | Use | TTS data quality treated as the binding constraint |
| C7 Foundation models | Supervised fine-tuning via the Trainer API | **Supporting** | Use | No instruction tuning, no preference optimisation |
| C16 Trustworthy AI | TTS misuse (voice fraud) | **Mentioned** | Awareness | No fairness evaluation across accents or dialects; no anti-spoofing |
| C17 Engineering | Latency awareness (RTFx), Gradio demos | **Introductory** | Use | No quantization, batching or serving infrastructure |

**Assumes rather than teaches.** Deep-learning background and transformer familiarity (readers are redirected to the NLP/LLM course); PyTorch in practice.

**Important omissions (currency).** No 2024–2026 audio developments: no Distil-Whisper or later Whisper variants, no native speech-to-speech duplex models, no neural audio codecs as a first-class topic, no streaming/real-time ASR, no diarization taught as a technique.

---

### D9. Build a Large Language Model (From Scratch)

**Identity.** Sebastian Raschka, Manning, **September 2024**; repository `rasbt/LLMs-from-scratch` actively maintained into 2026 with substantial additional material. **Baseline location:** Fundamentals §7.1.

**Intended scope (observed).** Implement a GPT-style model end to end: data pipeline, attention, architecture, pretraining, and fine-tuning.

**Actual structure (book).** Understanding LLMs (concept only); **working with text data** (tokenization, byte-pair encoding, sliding-window sampling, token and positional embeddings); **coding attention mechanisms** (self-attention without weights → with trainable weights → causal masking → multi-head); **implementing a GPT model** (layer norm, GELU feed-forward, residual connections, transformer block, text generation); **pretraining** (cross-entropy loss, training loop, temperature and top-k decoding, checkpointing, **loading real GPT-2 weights into the hand-built model**); **fine-tuning for classification**; **instruction fine-tuning** including evaluation. Appendices cover PyTorch and **LoRA**.

**Repository extensions (Observed, 2026 state).** Modern architectures implemented from scratch (Llama 3.2, Qwen3 dense and MoE, Gemma 3/4, OLMo 3); **KV cache**, FLOPs analysis, memory-efficient loading; attention variants (grouped-query, multi-head latent, sliding window, gated DeltaNet, sparse); **DPO with preference-dataset creation**; **LLM-as-judge evaluation via API/Ollama**; synthetic instruction-data generation and near-duplicate detection.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C5 Deep learning | Attention mechanics, transformer block, normalisation, residuals | **Core** | Implement | Attention is built four times, each more complete; correctness validated by loading GPT-2 weights |
| C7 Foundation models | Tokenization, embeddings, positional encoding, pretraining loop, decoding strategies | **Core** | Implement | Ch. 2–5 |
| C7 Foundation models | Supervised fine-tuning; instruction tuning; PEFT/LoRA | **Core** | Implement | Ch. 6–7, App. E |
| C7 Foundation models | Preference optimisation (DPO) | **Supporting** (repo only) | Implement | **Not in the book's chapters** |
| C7 Foundation models | RLVR, reasoning models, test-time compute | **Not Covered** | — | Deferred to a separate 2026 sequel that is not in the baseline |
| C10 Data for AI | Instruction dataset preparation; synthetic data; near-duplicate detection | **Supporting** | Implement | Book ch. 7 plus repo bonus |
| C15 Evaluation | Loss/perplexity; classification accuracy; fine-tuned-model evaluation | **Introductory** | Use | **No standard benchmarks**; LLM-as-judge is repo bonus material |
| C17 Engineering | KV cache, FLOPs, memory-efficient loading, MoE | **Supporting** (repo only) | Understand | Not in the book; no quantization or production serving |
| C12 IR / C13 Agents / C16 Trustworthy AI | — | **Not Covered** | — | Deliberately model-internals-only |

**Assumes rather than teaches.** Intermediate Python and some ML knowledge; PyTorch is taught in Appendix A; calculus and linear algebra are not taught.

**Important omissions.** Retrieval, agents, multimodality, safety/alignment/bias/privacy/security, quantization and serving, benchmark-based evaluation, distributed training at scale, and RL-based post-training in the book itself.

---

### D10. Hands-On Large Language Models

**Identity.** Alammar & Grootendorst, O'Reilly, **2024**; repository `HandsOnLLM/Hands-On-Large-Language-Models` with one notebook per chapter, built for a free Colab T4 GPU. **Baseline location:** Fundamentals §7.2.

**Intended scope (observed).** Practical use of language models for understanding and generation, for Python developers with ML familiarity.

**Actual structure.** Part I understanding: introduction; **tokens and embeddings**; looking inside transformer LLMs. Part II using pretrained models: text classification; **text clustering and topic modelling**; **prompt engineering**; advanced generation techniques and tools; **semantic search and RAG**; **multimodal LLMs**. Part III training: **creating text embedding models**; fine-tuning representation models; **fine-tuning generation models**.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C5 Deep learning | Tokenization behaviour, embeddings, transformer internals | **Supporting** | Understand | Part I is explanatory; the executable half is library invocation |
| C5 Deep learning | Embedding model training | **Supporting** | Implement | Ch. 10 (contrastive training via sentence-transformers) |
| C7 Foundation models | Fine-tuning representation and generation models; PEFT/LoRA | **Supporting** | Use | Via `peft`, `trl`, `bitsandbytes`; whether DPO/RLHF is walked through is *Uncertain* |
| C7 Foundation models | Multimodal models | **Introductory** | Use | Ch. 9 |
| C12 IR | Semantic search and RAG | **Supporting** | Use | In-process indexes (FAISS, Annoy), not production vector databases; IR fundamentals depth *Uncertain* |
| C13 Agents | Prompt engineering; tool use | **Introductory** | Use | Ch. 6–7 with LangChain and a search tool; **no protocols, no agent architecture** |
| C4 Classical ML | Text classification and clustering with modern embeddings | **Supporting** | Use | Ch. 4–5 |
| C15 Evaluation | Embedding benchmarks (MTEB) | **Introductory** | Use | *Uncertain*; no online evaluation or experiment tracking |
| C16 Trustworthy AI / C17 Engineering | — | **Not Covered** | — | No security, privacy, fairness, safety; no deployment, monitoring or MLOps |

**Assumes rather than teaches.** Python experience and machine-learning fundamentals.

**Important omissions.** Deployment and serving of any kind; monitoring; data provenance; trustworthy AI; distributed training; statistics. Its stack is pinned to mid-2024 libraries.

---

### D11. Designing Machine Learning Systems

**Identity.** Chip Huyen, O'Reilly, **2022**; companion repository holds chapter summaries and tool lists rather than project code. **Baseline location:** Existing Engineering Section — MLOps (pending reclassification).

**Intended scope (observed).** An iterative process for production-ready ML applications, for ML engineers, data scientists, data engineers, platform engineers and engineering managers.

**Actual structure.** Overview of ML systems; ML systems design (business objectives, reliability, scalability, maintainability, adaptability); **data engineering fundamentals** (storage, OLTP/OLAP, batch versus stream); **training data** (sampling, labelling, weak supervision, semi-supervision, class imbalance, active learning, augmentation); **feature engineering** (temporal splits, **data leakage**, lineage, stale features); model development and offline evaluation (selection, ensembles, experiment tracking, **distributed training**, baselines); **deployment and prediction service** (online versus batch, cloud versus edge, latency/cost); **data distribution shifts and monitoring**; **continual learning and testing in production**; **infrastructure and tooling for MLOps** (storage/compute, orchestrators, model stores, feature stores, build-versus-buy); **the human side of ML** (UX under probabilistic outputs, team structures, responsible AI).

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C10 Data for AI | Sampling, **labelling and weak supervision**, class imbalance, augmentation, lineage, leakage, feature stores | **Core** | Understand → Design | The strongest data coverage in the baseline; provenance/licensing and synthetic data are *Uncertain / likely thin* |
| C17 Engineering | ML lifecycle, infrastructure, orchestration, build-versus-buy | **Core** | Design | Ch. 10, deliberately tool-agnostic; the author's own note is that tooling is ephemeral |
| C17 Engineering | **Monitoring and drift** (covariate/label shift, concept drift, degenerate feedback loops) | **Core** | Understand | Ch. 8 |
| C17 Engineering | Deployment patterns; latency/cost trade-offs | **Supporting** | Understand | Ch. 7; no inference optimisation or LLM-specific serving |
| C17 Engineering | Distributed training (data, model, pipeline parallelism) | **Supporting** | Understand | Ch. 6 |
| C17 Engineering | ML technical debt; continual learning; production feedback loops | **Supporting** | Understand | Ch. 8–9 |
| C3 Methodology | Baselines, experiment tracking, offline evaluation | **Supporting** | Understand | Ch. 6 |
| C15 Evaluation | Testing in production | **Supporting** (*Uncertain* on A/B methodology) | Understand | Ch. 9 |
| C2 Statistics | Sampling methods | **Introductory** | Understand | No significance testing, power or sequential analysis evidenced |
| C18 Governance | Human factors, team design, responsible AI | **Supporting** | Awareness | Ch. 1 and 11; predates current regulation |
| C7 / C12 / C13 | Foundation models, RAG, prompting, agents | **Not Covered** | — | Published before the foundation-model application era; the author's own later framing confirms this boundary |

**Assumes rather than teaches.** Working ML knowledge (a separate basic-ML review is shipped outside the book), Python, cloud/infrastructure administration.

**Important omissions.** Everything foundation-model; security and prompt injection; regulation; inference optimisation.

---

### D12. LLM Engineer's Handbook

**Identity.** Iusztin & Labonne, Packt, **October 2024**, 522 pages; repository `PacktPublishing/LLM-Engineers-Handbook` implementing one end-to-end project. **Baseline location:** Existing Engineering Section — LLMOps (pending reclassification).

**Intended scope (observed).** Engineering LLM applications "from concept to production" for AI/NLP/LLM engineers with basic LLM, Python and AWS knowledge.

**Actual structure.** The "LLM Twin" project: architecture (FTI — feature/training/inference); tooling and installation; **data engineering** (crawling and ETL); **RAG feature pipeline**; **supervised fine-tuning**; **fine-tuning with preference alignment**; **evaluating LLMs**; **inference optimisation** (speculative decoding, model parallelism, weight quantization, engine comparison); **RAG inference pipeline**; **deployment**; **MLOps and LLMOps**; appendix on MLOps principles. The project crawls the author's writing, builds instruct and preference datasets, trains Llama 3.1 with SFT then DPO, evaluates, and serves a RAG-backed microservice.

**Landscape coverage.**

| Landscape area | Subarea | Coverage | Depth | Evidence and limits |
| --- | --- | --- | --- | --- |
| C17 Engineering | Inference optimisation (speculative decoding, parallelism, quantization) | **Supporting** | Use → Understand | Ch. 8; sub-chapter depth *Uncertain* (publisher blocked) |
| C17 Engineering | Deployment, LLMOps, CI/CD, orchestration | **Core** (within one stack) | Use | Implemented with specific commercial services rather than taught as portable concepts |
| C17 Engineering | Observability (prompt monitoring) | **Introductory** | Use | Drift, incident response and technical debt not evidenced |
| C7 Foundation models | SFT and **preference alignment (DPO)** end to end | **Core** | Implement (pipeline level) | Produces a published DPO-trained model |
| C10 Data for AI | Crawling/ETL; **synthetic instruct and preference dataset generation** | **Supporting** | Use | Labelling, quality and licensing not covered — notable given the project crawls third-party content |
| C12 IR | RAG feature and inference pipelines with a production vector database | **Supporting** | Use | The repository itself calls it "a simple RAG system"; IR fundamentals *Uncertain* |
| C15 Evaluation | LLM evaluation chapter incl. benchmarks and a worked evaluation | **Supporting** | Use | LLM-as-judge and online evaluation *Uncertain* |
| C13 Agents | Prompting, tool use, agents | **Not Covered** | — | No chapter; a notable omission for a 2024 production handbook |
| C16 Trustworthy AI | Guardrails under LLMOps | **Mentioned** (*Uncertain*) | Awareness | No security, privacy, fairness or governance chapter |
| C2 Statistics | — | **Not Covered** | — | No statistical methodology evidenced |

**Assumes rather than teaches.** Python, **AWS specifically**, basic LLM knowledge, Docker, and the ability to operate nine external services (ZenML, AWS SageMaker/ECR/S3, MongoDB, Qdrant, Comet ML, Opik, Hugging Face, OpenAI API, GitHub Actions). Three API keys are mandatory; the authors estimate roughly $25 per full run.

**Important omissions.** Prompting and agents; statistics; trustworthy AI; distributed *training*; portable (vendor-neutral) treatment of the operations concepts it teaches.

[⬆ Back to Contents](#contents)

---

## E. Cross-Resource Coverage Matrix

**Cell codes:** `Core` · `Supp` (Supporting) · `Intro` (Introductory) · `Ment` (Mentioned) · `—` (Not Covered) · `?` (Uncertain). A parenthesised note marks an important qualification. Columns group resources by baseline location.

**Columns:** **Found.** = R1–R4 foundations (Python Tutorial, Practical SQL, PGExercises, Python for Data Analysis) · **HOMLP** = R5 · **SLP3** = R6 · **NLPiA** = R7 · **Audio** = R8 · **BLLM** = R9 (Build a LLM from Scratch) · **HOLLM** = R10 · **DMLS** = R11 · **LLMEH** = R12.

| Landscape area / subarea | Found. | HOMLP | SLP3 | NLPiA | Audio | BLLM | HOLLM | DMLS | LLMEH |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **C1 Mathematical foundations** | | | | | | | | | |
| Linear algebra, calculus | Intro (arrays) | Supp (refreshers only) | Supp (derives) | Intro (App. C) | — | — | — | — | — |
| Probability | — | — (assumed) | Supp (in context) | — | — | — | — | — | — |
| Optimization, autodiff | — | Core | Supp | Intro | — | Supp (App. A) | — | — | — |
| Information theory | — | Ment | Supp | — | — | Ment | — | — | — |
| **C2 Statistics, causality, experimentation** | | | | | | | | | |
| Estimation and inference | — | — | **Supp** (only source) | — | — | — | — | Intro | — |
| Calibration / conformal prediction | — | — | — | — | — | — | — | — | — |
| Causal inference | — | — | — | — | — | — | — | — | — |
| Online experiments / A-B testing | — | — | — | — | — | — | — | ? (ch. 9) | — |
| Off-policy evaluation, survival analysis | — | — | — | — | — | — | — | — | — |
| **C3 Empirical methodology** | | | | | | | | | |
| Validation protocols, cross-validation | — | **Core** | Supp | Intro | — | — | — | Supp | — |
| Data leakage | — | Supp | — | — | — | — | — | **Core** | — |
| Baselines and ablations | — | Supp | Supp | — | — | — | — | Supp | — |
| Benchmark validity, contamination | — | — | **Supp** | — | — | — | — | — | ? |
| Reproducibility, experiment tracking | — | — | — | — | — | — | — | Supp | Supp (tooling) |
| **C4 Statistical and classical ML** | | | | | | | | | |
| Linear/logistic, trees, ensembles | Intro (PyDA) | **Core** | Supp (LR only) | Supp | — | — | — | — | — |
| Kernel methods / SVMs | — | Supp (online app.) | — | — | — | — | — | — | — |
| Unsupervised, dimensionality reduction | — | **Core** | — | Supp (SVD/LSA) | — | — | Supp (clustering) | — | — |
| Anomaly detection | — | Supp | — | — | — | — | — | — | — |
| Probabilistic graphical models, Bayesian ML | — | Intro (GMM) | Ment | — | — | — | — | — | — |
| Learning theory / generalization | — | Intro | — | — | — | — | — | — | — |
| AutoML, hyperparameter optimization | — | Supp (Optuna) | — | — | — | — | — | Ment | — |
| Tabular foundation models, online learning | — | — | — | — | — | — | — | — | — |
| **C5 Deep learning and representation learning** | | | | | | | | | |
| Training mechanics, regularization | — | **Core** | Supp | Supp | — | Supp | — | — | — |
| CNN / RNN lineage | — | **Core** | Supp (ch. 14) | **Core** (from scratch) | Supp | — | — | — | — |
| Attention and transformers | — | **Core** | Supp | Supp | Intro | **Core** (from scratch) | Supp | — | — |
| Efficient attention, MoE, SSMs | — | Supp | — | — | — | Supp (repo) | Ment | — | — |
| Self-supervised representation learning | — | Supp | Supp | Supp | Supp | — | Supp | — | — |
| Embedding models | — | Supp | Supp | **Core** | — | Supp | **Supp** (trains them) | — | — |
| Graph neural networks | — | — | — | — | — | — | — | — | — |
| **C6 Generative modeling** | | | | | | | | | |
| Autoregressive models | — | Supp | **Core** | Supp | — | **Core** | Supp | — | — |
| VAE, GAN, diffusion, flow matching | — | **Core** | — | — | — | — | — | — | — |
| Discrete diffusion LMs, world models | — | — | Ment | — | — | — | — | — | — |
| **C7 Foundation models** | | | | | | | | | |
| Tokenization | — | Supp | **Core** | **Core** | — | **Core** | Supp | — | — |
| Pretraining, scaling laws | — | Supp | **Core** (concepts) | Intro | — | **Core** (implements) | Intro | — | — |
| Supervised fine-tuning, instruction tuning | — | Supp | **Core** | Supp | Supp | **Core** | Supp | — | **Core** |
| Preference optimization (RLHF, DPO) | — | — | **Supp** | — | — | Supp (repo only) | ? | — | **Core** (pipeline) |
| RLVR, reasoning models, test-time compute | — | — | Ment | — | — | — | — | — | — |
| PEFT / LoRA | — | Supp | Supp | — | — | Supp (App. E) | Supp | — | Supp |
| Model merging, knowledge editing, continual learning | — | — | — | — | — | — | — | — | — |
| Synthetic data, model collapse | — | — | Ment | — | — | Supp (repo) | — | — | Supp |
| Multimodal foundation models | — | Supp | — | — | Supp (audio) | — | Intro | — | — |
| Small / on-device models, quantization | — | Supp (App. B) | — | Intro | — | — | Ment | — | Supp |
| **C8 Sequential decision-making and RL** | | | | | | | | | |
| MDPs, Q-learning, DQN, policy gradients, PPO | — | **Core** | — | — | — | — | — | — | — |
| Bandits, off-policy evaluation | — | — | — | — | — | — | — | — | — |
| Imitation learning, multi-agent, game theory | — | — | — | — | — | — | — | — | — |
| Decision-focused learning | — | — | — | — | — | — | — | — | — |
| **C9 Knowledge, reasoning, symbolic AI** | | | | | | | | | |
| Parsing, semantic roles, logic, lexicons | — | — | **Core** | Supp | — | — | — | — | — |
| Knowledge graphs | — | — | Ment | **Core** | — | — | — | — | — |
| Planning, constraint solving, theorem proving | — | — | — | — | — | — | — | — | — |
| Neuro-symbolic integration | — | — | — | — | — | — | — | — | — |
| **C10 Data for AI** | | | | | | | | | |
| Acquisition, provenance, licensing | Intro (SQL ch. 20) | — | Supp (documentation) | — | — | — | — | ? | Ment |
| Annotation and labeling | — | — | Supp | — | — | — | — | **Core** | — |
| Data quality, cleaning, validation | **Core** (PyDA, SQL) | Supp | — | Intro | Supp | Supp (repo) | — | **Core** | — |
| Feature engineering | Supp | Supp | — | — | — | — | — | **Core** | Supp (FTI sense) |
| Pretraining data curation | — | — | Supp | — | — | Supp (repo) | — | — | — |
| Dataset documentation (datasheets, model cards) | — | — | **Supp** (only source) | — | — | — | — | Ment | — |
| Drift and validation in production | — | — | — | — | — | — | — | **Core** | ? |
| **C11 Modality specializations** | | | | | | | | | |
| NLP beyond LLMs | — | Supp | **Core** | **Core** | — | — | Supp | — | — |
| Computer vision | — | **Core** | Ment | — | — | — | — | — | — |
| 3D vision, video understanding | — | — | — | — | — | — | — | — | — |
| Speech and audio | — | Ment | **Core** | — | **Core** | — | — | — | — |
| Time series | **Core** (handling) | **Core** (modelling) | — | — | — | — | — | — | — |
| Tabular | Supp | **Core** | — | — | — | — | — | Supp | — |
| Graphs and relational data | Supp (SQL) | — | — | Supp (KG) | — | — | — | — | — |
| Document understanding | — | — | — | — | — | — | — | — | — |
| Edge / TinyML | — | Ment | — | — | — | — | — | Intro (edge) | — |
| **C12 Information retrieval, ranking, recommendation** | | | | | | | | | |
| Lexical retrieval (BM25) | Supp (SQL FTS) | — | **Core** | Supp | — | — | — | — | — |
| Dense retrieval and embeddings | — | — | **Core** | Supp | — | — | Supp | — | Supp |
| ANN indexing | — | — | Ment | **Supp** | — | — | Supp | — | Supp (Qdrant) |
| IR evaluation | — | — | **Supp** (no nDCG/MRR) | — | — | — | — | — | ? |
| Learned sparse / late interaction | — | — | — | — | — | — | — | — | — |
| Recommender systems | — | — | — | — | — | — | — | Ment | — |
| **C13 Compound AI systems and agents** | | | | | | | | | |
| Prompting | — | Ment | Supp | Intro | — | — | **Supp** | — | — |
| Structured outputs, constrained decoding | — | — | — | — | — | — | ? | — | — |
| Tool use, agent architecture | — | — | — (ch. 12 unwritten) | Intro | — | — | Intro | — | — |
| RAG as a system | — | Ment | Supp | Supp | — | — | Supp | — | **Core** (one stack) |
| Memory, multi-agent, protocols, verification loops | — | — | — | — | — | — | — | — | — |
| Coding / computer-use agents | — | — | — | — | — | — | — | — | — |
| **C14 Embodied and interactive AI** | — | Ment (RL envs) | — | — | — | — | — | — | — |
| **C15 Evaluation science** | | | | | | | | | |
| Metrics and classical validation | Intro | **Core** | **Core** | Intro | **Core** (speech) | Intro | Intro | Supp | Supp |
| Error analysis | — | **Core** | Supp | — | Supp | — | — | Supp | — |
| Statistical rigor in evaluation | — | — | **Supp** | — | — | — | — | — | — |
| Benchmark design, contamination | — | — | **Supp** | — | — | — | — | — | ? |
| LLM-as-judge | — | — | Supp | — | — | Ment (repo) | ? | — | ? |
| Human evaluation | — | — | Supp | — | Supp (MOS) | — | — | — | — |
| Application / online evaluation | — | — | — | — | — | — | — | Supp | Supp |
| Capability and agentic evaluation | — | — | — | — | — | — | — | — | — |
| **C16 Trustworthy AI** | | | | | | | | | |
| Interpretability (post-hoc, probing, mechanistic) | — | Intro | **Supp** (stub ch.) | — | — | — | — | Ment | — |
| Fairness and bias | — | — | **Supp** | Supp | — | — | — | Intro | — |
| Privacy (DP, memorization, unlearning) | — | — | — | — | — | — | — | Ment | — |
| Robustness, distribution shift, adversarial | — | — | Ment | — | — | — | — | **Supp** (drift) | — |
| Safety and alignment | — | — | **Supp** | Intro (red teaming) | Ment | — | — | — | — |
| AI security (prompt injection, poisoning, supply chain) | — | — | Ment | Intro (guard rails) | — | — | — | — | ? |
| Provenance, watermarking | — | — | — | — | — | — | — | — | — |
| **C17 AI engineering, serving, operations** | | | | | | | | | |
| ML lifecycle and MLOps | — | — | — | — | — | — | — | **Core** | **Core** (one stack) |
| ML technical debt | — | — | — | — | — | — | — | Supp | Ment |
| Inference serving, batching, caching | — | Ment | — | — | Intro | — | — | Supp | Supp |
| Speculative decoding, compression, quantization | — | Supp (App. B) | — | — | — | Ment (repo) | — | — | Supp |
| Distributed training | — | **Core** | — | — | — | Ment (repo) | — | Supp | Ment |
| Cost and latency engineering | — | Ment | Ment (energy) | — | Intro (RTFx) | — | — | Supp | Supp |
| Observability and tracing | — | — | — | — | — | — | — | Supp | Supp (prompt monitoring) |
| Monitoring and drift | — | — | — | — | — | — | — | **Core** | ? |
| Durable execution, data flywheels | — | — | — | — | — | — | — | Supp (continual) | — |
| **C18 Human-AI interaction, governance, society** | | | | | | | | | |
| Interaction design, human oversight | — | — | Ment | — | — | — | — | Intro | — |
| Regulation, standards, risk frameworks | — | — | — | — | — | — | — | — | — |
| Data rights and copyright | — | — | Ment | — | — | — | — | — | — |
| Environmental and compute accounting | — | — | Intro | — | — | — | — | Ment | — |
| Societal impact | — | — | **Supp** | Intro | Ment | — | — | Supp | — |
| **C19 AI for science and domain applications** | — | — | — | — | — | — | — | Ment | — |

**What the matrix makes visible.**

| Pattern | Areas |
| --- | --- |
| **Strong, multi-resource coverage** | C5 deep learning; C7 foundation-model lifecycle (pretraining → fine-tuning); C11 language, speech, vision, time series, tabular; C15 metrics and error analysis |
| **Strong but single-resource (isolated) coverage** | C4 classical ML and C6 generative modelling and C8 RL and C17 distributed training — **all four rest on HOMLP alone**. C10 data and C17 operations rest on DMLS alone. C9 symbolic AI and C12 IR fundamentals and C16 trustworthy AI rest largely on SLP3 alone. C2 inferential statistics rests on two sections of SLP3 |
| **Partial coverage** | C12 (retrieval yes, ranking metrics and recommenders no); C13 (prompting and RAG yes, agents no); C16 (safety and bias yes, privacy and security no); C10 (labelling and quality yes, provenance and licensing no) |
| **Genuine blank rows across every resource** | Calibration and conformal prediction; causal inference; A/B testing; off-policy evaluation; bandits; graph neural networks; document understanding; 3D and video; learned sparse retrieval; recommender systems; memory/multi-agent/protocols; capability and agentic evaluation; privacy; provenance and watermarking; regulation and standards; C14 embodied AI; C19 AI for science |
| **Uncertain cells needing verification** | DMLS A/B methodology; LLMEH evaluation depth, drift and security; HOLLM preference tuning, IR depth and structured outputs; NLPiA transformer build depth |

[⬆ Back to Contents](#contents)

---

## F. Foundation Coverage

The supplementary layer that the independent landscape under-represented. **This layer is an audit device, not a proposed curriculum structure.**

| Foundation area | Covered by | Coverage | Depth | Notes |
| --- | --- | --- | --- | --- |
| **F1 Python / programming for Data & Intelligence** | R1 Python Tutorial (primary); R4 ch. 2–3; R7 App. B | **Core** | Use | The tutorial is a complete language tour but has **no exercises, projects or assessment**; ROADMAP §2.2 names projects as the intended remedy but specifies none |
| **F2 SQL / querying** | R2 (primary); R3 (practice) | **Core** | Implement | Together they cover querying through window functions, CTEs and recursion, with drilled practice |
| **F2b Database design and operation** | R2 only | **Core** | Understand | Constraints, keys, indexes, transactions, views, maintenance. R3 explicitly disclaims design |
| **F3 Data manipulation** | R4 (primary); R2 for set-based work | **Core** | Implement | pandas/NumPy in depth |
| **F4 Exploratory data analysis** | R4 (primary); R2 ch. 10 | **Core** | Use | Missing data, duplicates, outliers, grouping, five worked analyses. **No data-quality framework** (validation rules, schemas, expectations) |
| **F5 Visualization** | R4 ch. 9 only | **Core** (API) | Use | Only source in the baseline. Teaches plotting libraries, **not** visual design, perception, or communicating uncertainty |
| **F6 Practical numerical and data tooling** | R4 ch. 4 + App. A/B; R1 §10–12 | **Core** | Understand → Implement | Arrays, vectorization, broadcasting, memory layout, Numba, profiling, venv/pip |
| **F7 Software practice (testing, version control, packaging)** | R1 §10.11 only (doctest/unittest) | **Introductory** | Awareness | **Version control is taught by no resource**; git appears only as a way to download example code. Packaging and distribution are not taught |

**Observation.** The foundation layer is the most complete part of the baseline, with one systemic hole: **engineering hygiene** (version control, testing discipline, packaging, environment reproducibility) is assumed by every later resource and taught by none. Whether that belongs here or in the separate Computer Science & Engineering roadmap is a boundary question for the curriculum step, not an audit finding.

[⬆ Back to Contents](#contents)

---

## G. Dependency Audit

Documenting mismatches only; no reordering is proposed.

| # | Dependency issue | Evidence | Severity |
| --- | --- | --- | --- |
| **G1** | **Mathematics is a named prerequisite with no resource.** R5 states the reader needs "some notions of linear algebra, calculus, statistics and probability theory"; ROADMAP §1 has no resource at all. R5 supplies refresher notebooks for linear algebra and calculus **but none for statistics or probability** | R5 prerequisites and repository contents; ROADMAP §1 | **Dependency-critical** |
| **G2** | **Statistics is assumed everywhere and taught nowhere.** R5 assumes it; R4 explicitly teaches tooling "as opposed to data analysis methodology"; R11's sampling and production-testing chapters assume statistical literacy; only R6 §4.11 and §13.6 teach any inference | Sections D4, D5, D6, D11 | **Dependency-critical** |
| **G3** | **R12 assumes cloud and infrastructure competence that the roadmap never teaches.** It requires AWS specifically, Docker, Poetry, an orchestrator and nine external services, with three mandatory API keys | R12 repository requirements | **High** — though the boundary section of ROADMAP assigns general cloud/DevOps to the future CS & Engineering roadmap |
| **G4** | **R11 assumes working ML knowledge** and ships a separate basic-ML review precisely because it does not teach ML. Its baseline position (Existing Engineering Section) is unordered relative to §5 | R11 repository README | Moderate; resolved if ML precedes it |
| **G5** | **R7 assumes deep-learning basics**; R8 assumes a deep-learning background *and* transformer familiarity, redirecting readers to a separate NLP/LLM course. Both sit in §6, before §7 LLMs, while R8 assumes transformer knowledge that §7 supplies | ROADMAP §6–§7; R7/R8 stated prerequisites | Moderate |
| **G6** | **Retrieval knowledge is assumed by applied RAG material.** R10 ch. 8 and R12 ch. 4/9 build RAG systems; IR fundamentals live in R6 ch. 11, a chapter deep inside a 26-chapter textbook that the roadmap references as a whole | Sections D6, D10, D12 | Moderate |
| **G7** | **Evaluation and experimentation foundations are assumed by production material.** R11 ch. 9 (testing in production) and R12 ch. 7 (evaluating LLMs) assume evaluation literacy; the only statistical-evaluation content is in R6 | Sections D6, D11, D12 | Moderate |
| **G8** | **PyTorch fluency**: R5 ch. 10 introduces PyTorch; R9 teaches it in an appendix; R7 teaches it in-line. No conflict, but three separate introductions exist | Sections D5, D7, D9 | Low (overlap, not a gap) |
| **G9** | **R5's deployment regression breaks an inherited assumption.** The previous edition's deployment-at-scale chapter was only partially merged; any expectation that §5 supplies deployment knowledge before the engineering section no longer holds | R5 changelog | Moderate |

[⬆ Back to Contents](#contents)

---

## H. Overlap Audit

**Productive reinforcement** (same concept, different depth or perspective):

| Topic | Resources | Why the overlap appears productive |
| --- | --- | --- |
| Tokenization | R6 (linguistic and statistical), R7 (toolkit and multilingual), R9 (LLM input pipeline, implemented) | Three genuinely different angles on the same mechanism |
| Transformers | R6 (conceptual), R7 (applied build), R9 (from scratch, weight-validated), R5 (from scratch for translation and vision) | Understanding → implementation → application, plus vision transfer |
| Embeddings and semantic search | R6 ch. 5/11 (theory and IR framing), R7 §10.3 (search engineering), R10 ch. 10 (training embedding models) | Theory, system, and model-training perspectives |
| Data cleaning | R4 ch. 7 (pandas technique), R2 ch. 10 (set-based, in-database) | Complementary tools for the same task |
| Fine-tuning | R9 ch. 6–7 (implemented by hand), R10 ch. 11–12 (library), R12 ch. 5–6 (production pipeline) | Three abstraction levels; arguably a deliberate progression |

**Potential redundancy** (similar material at similar depth; flagged for the design step, not for removal):

| Topic | Resources | Observation |
| --- | --- | --- |
| RAG construction | R10 ch. 8 and R12 ch. 4/9 | Both build retrieval-augmented systems at library/pipeline depth. R12 adds a production vector database and deployment; R10 is notebook-scale. The conceptual content substantially overlaps |
| Text classification with pretrained models | R7 ch. 9, R10 ch. 4/11, R9 ch. 6 | Three resources fine-tune a classifier; R9's is from-scratch, the others library-based |
| Transformer architecture explanation | R5 ch. 15, R7 ch. 9, R9 ch. 3–4, R6 ch. 7 | Four treatments. R9 and R5 both build from scratch — the strongest candidate for genuine duplication, differing mainly in target (GPT pretraining versus translation/ViT) |
| PyTorch introduction | R5 ch. 10, R9 App. A, R7 ch. 5 | Three introductions to the same framework |
| MLOps principles | R11 (tool-agnostic) and R12 ch. 11 + appendix (stack-specific) | Complementary in philosophy, overlapping in content |

[⬆ Back to Contents](#contents)

---

## I. Genuine Gap Analysis

Gaps are stated as findings about resource coverage. **Classification is not urgency, and none of these is a curriculum decision.**

### I1. Dependency-Critical Gaps

| Gap | Evidence | Note |
| --- | --- | --- |
| **Mathematics for ML** (linear algebra, calculus, probability) as taught content | ROADMAP §1 has no resource; R5 provides refreshers only for linear algebra and calculus | Later resources assume it |
| **Probability and statistical inference** | No resource teaches it as a subject; R6 §4.11/§13.6 is the only inferential content found | Assumed by R5, R11, R12 |
| **Evaluation as measurement** (sampling error, confidence in comparisons) | Metrics are taught well (R5 ch. 3, R6 throughout); the statistics of comparing systems is not | Underpins every later claim about model quality |
| **Software practice** (version control, testing discipline, environment reproducibility) | Taught by no resource; R1 introduces two testing modules only | Assumed by every code-bearing resource; may belong to the CS & Engineering roadmap |

### I2. Core Landscape Gaps

| Gap | Landscape area | Evidence |
| --- | --- | --- |
| Calibration and uncertainty quantification (including conformal prediction) | C2 | No calibration section in R5; not a taught topic in R6 |
| Causal inference and online controlled experiments | C2 | Absent everywhere; "A/B test" appears zero times in R6 |
| Bandits and off-policy evaluation | C8 | Absent; R5's RL chapter is single-agent deep RL |
| Recommender systems | C12 | Absent; R11 mentions feedback loops only |
| Graph machine learning | C5, C11 | Absent everywhere |
| Probabilistic and Bayesian modelling | C4 | Only Gaussian mixtures as a clustering tool |
| Privacy (differential privacy, memorization, unlearning) | C16 | Differential privacy appears zero times in R6; absent elsewhere |
| Provenance, licensing and content authenticity | C10, C16 | Only R2 ch. 20 (origins) and R6 (datasheets/model cards) touch adjacent ground |

### I3. Depth Gaps

| Topic | Present at | Depth reached | Depth the landscape indicates |
| --- | --- | --- | --- |
| Interpretability | R6 ch. 10 | Understand, and the chapter is **half-written** by the authors' own statement | Mechanistic interpretability is an active research area |
| Evaluation science beyond metrics | R6 §1.9 | Understand (one section) | Construct validity, contamination and judge validity are contested research topics |
| IR evaluation | R6 §11.2 | Precision/recall/MAP | Ranking metrics (nDCG, MRR) absent |
| Preference optimization | R6 ch. 8 (concept), R12 (pipeline), R9 (repo bonus) | Use / Understand | No RLVR or reward-design treatment |
| Inference optimization | R12 ch. 8, R5 App. B | Use | Production serving architecture (paged attention, continuous batching, disaggregation) absent |
| Data quality | R4 ch. 7, R11 ch. 4 | Implement / Understand | No data-validation frameworks, schemas or expectations |

### I4. Breadth Gaps

| Strong subarea | Weak or absent neighbour |
| --- | --- |
| Vision: detection and classification (R5 ch. 12, 16) | 3D vision, video understanding, segmentation-specific work |
| Retrieval: BM25 and dense retrieval (R6 ch. 11) | Learned sparse, late interaction, reranking, recommender systems |
| Speech: ASR and TTS (R6, R8) | Diarization, streaming/real-time, neural audio codecs as a topic |
| Time series: handling and classical forecasting (R4, R5 ch. 13) | Modern forecasting practice, anomaly detection benchmarks |
| Text data (all NLP resources) | Document understanding (layout, OCR, tables) — absent entirely |

### I5. Contemporary Practice Gaps

Every LLM-era resource in the baseline predates the 2025–2026 agent and reasoning wave.

| Gap | Evidence |
| --- | --- |
| Agents, tool use, orchestration, memory | R6 ch. 12 is **unwritten**; R7 ch. 12 is dialog systems; R10 ch. 7 is a single chapter; R12 has no agent chapter |
| Interoperability protocols (MCP-class) | Chronologically impossible for all resources |
| Context engineering, structured outputs, constrained decoding | Absent (R10 prompting is the closest) |
| Reasoning models and test-time compute; RLVR | Absent; R9's sequel covers it but is not in the baseline |
| LLM application evaluation (judge validity, error-analysis workflow, regression sets) | Only R6 §1.9 conceptually; R12 ch. 7 at *Uncertain* depth |
| AI security as engineering practice (prompt injection defense, poisoning, supply chain) | R6 §1.10 mentions prompt injection; R7 covers guard rails and red teaming at introductory depth; no threat-model treatment anywhere |
| LLM serving stack (continuous batching, KV-cache management, speculative decoding in production) | R12 ch. 8 at *Uncertain* depth; R5 App. B partial |
| Observability for LLM systems | R12 prompt monitoring only |
| Governance and regulation affecting engineering artifacts | Absent everywhere |
| Modern MLOps for foundation models | R11 predates it; R12 teaches one vendor stack |

### I6. Specialization Gaps

Embodied AI and robotics (C14); AI for science (C19); 3D vision; TinyML and edge deployment; quantum ML; computational social science. **Observation:** their absence is consistent with a general AI-engineering baseline, and the landscape itself labels most of them specialization-dependent.

### I7. Research-Frontier Gaps

Mechanistic interpretability beyond R6's stub; scaling-law science; world models; continual learning and forgetting; model merging and editing; alignment research beyond preference optimization. **Observation:** the landscape marks these Active research or Contested; absence from a resource baseline is expected rather than alarming.

[⬆ Back to Contents](#contents)

---

## J. Answers to Special Questions

**1. How much statistics and experimentation do the existing mathematics/ML resources actually teach?**
**Very little, and none systematically.** ROADMAP §1 has no resource. R5 names probability and statistics as a prerequisite and supplies refreshers only for linear algebra and calculus. R4 teaches descriptive statistics as pandas technique and states explicitly that methodology is out of scope. R2 teaches statistical *functions* (correlation, regression, percentiles) without probability or inference. The only inferential statistics anywhere is R6 §4.11 (paired-bootstrap significance testing) and §13.6 (bootstrap confidence intervals). **No resource teaches hypothesis testing generally, experiment design, A/B testing, power, or calibration.**

**2. Is reinforcement learning meaningfully covered anywhere?**
**Yes — this corrects the prior comparison report's assumption.** R5 ch. 19 covers Markov decision processes, Q-value iteration, Q-learning, DQN, policy gradients, actor-critic and PPO, with Gymnasium and Stable-Baselines3, at implementation depth. R6 ch. 8 covers RL only as LLM post-training (reward models, RLHF, DPO, PPO in passing). **Absent:** bandits, off-policy evaluation, offline RL, imitation learning, multi-agent and game theory, and RL from verifiable rewards.

**3. How much generative modeling beyond language is covered?**
**One resource carries it.** R5 ch. 18 covers autoencoder variants, VAEs, GANs, DCGAN and diffusion models at implementation depth, with flow matching as extra material. No other audited resource covers non-text generative modelling. Discrete diffusion language models, world models and video generation are absent everywhere.

**4. Is Information Retrieval taught as a discipline, or only implicitly through later RAG material?**
**As a discipline, in one place.** R6 ch. 11 teaches information retrieval proper — BM25, dense retrieval, IR evaluation, RAG and QA evaluation — at understanding depth. R7 §10.3 adds applied search engineering (full-text, semantic, ANN indexing, vector quantization). RAG-only treatments appear in R10 ch. 8 and R12 ch. 4/9. **Limits:** ranking metrics (nDCG, MRR) are absent; learned sparse and late-interaction retrieval are absent; recommender systems are absent entirely.

**5. How much Data for AI is covered: collection, labeling, quality, provenance, curation, synthetic data?**
**Mixed, with one strong source and clear holes.** R11 is the strongest: sampling, labelling including weak supervision and active learning, class imbalance, augmentation, feature engineering, leakage, lineage and feature stores. R4 covers cleaning at implementation depth as pandas technique. R2 covers in-database quality checks and asks provenance questions. R6 uniquely teaches **dataset documentation** (datasheets, data statements, model cards). R9's repository and R12 cover **synthetic dataset generation**. **Holes:** provenance and licensing as an engineering concern (*Uncertain* in R11, absent elsewhere — notable given R12's project crawls third-party content); data-validation frameworks; model collapse.

**6. How much Evaluation Science is already present?**
**Metrics are well covered; evaluation as a science is thin.** R5 ch. 3 teaches metrics, ROC/PR and a dedicated error-analysis section at implementation depth. R6 teaches task-appropriate metrics across the book plus **benchmark validity, contamination, LLM-as-judge and Goodhart's Law** in §1.9 and significance testing in §4.11. R8 teaches speech metrics rigorously, including normalisation pitfalls and the subjectivity of MOS. **Absent:** calibration, capability and agentic evaluation, construct-validity methodology beyond one section, evaluation regression suites, and the statistics of comparing systems (outside R6).

**7. How much Trustworthy AI is present: robustness, interpretability, privacy, fairness, safety/alignment?**
**Concentrated in one resource and uneven.** R6 covers safety and alignment (§1.10, including a prompt-injection mention), bias in embeddings, machine translation and coreference, harms in classification, and has a dedicated interpretability chapter that its authors describe as half-written. R7 covers guard rails, red teaming, hallucination and toxicity at introductory-to-use depth. R11 frames fairness and responsible AI organisationally. **Effectively absent across the baseline:** differential privacy (zero occurrences in R6), adversarial robustness, jailbreaks, poisoning and supply-chain security, provenance and watermarking. R5 shows no trustworthy-AI section in any chapter heading (*Uncertain* for prose).

**8. How broad is modality coverage beyond language/audio?**
**Vision, time series and tabular are covered; several modalities are not.** R5 covers computer vision (CNNs, ViT, DINO, CLIP/BLIP-2 discussion) and time series (forecasting, ARMA, multi-step, seq2seq) at implementation depth; tabular data is its native territory. R4 covers time-series *handling*. **Absent:** 3D vision, video understanding, document understanding, graph data, and geospatial beyond R2's PostGIS chapter.

**9. Is classical/symbolic AI represented?**
**Partly, through language.** R6 Volume III covers constituency and dependency parsing, semantic role labelling, information extraction and lexicons, with web appendices on logical representations, CCG and WordNet. R7 ch. 11 covers knowledge-graph construction and relation extraction at implementation depth. **Absent:** search, classical planning, constraint satisfaction, theorem proving, and neuro-symbolic integration as a design pattern.

**10. Which AI engineering/serving/operations knowledge is genuinely covered by the existing MLOps/LLMOps resources?**
**R11 (2022):** data engineering, training data, feature engineering, offline evaluation, distributed training, deployment patterns, **monitoring and drift**, continual learning and production testing, MLOps infrastructure and team concerns — tool-agnostic, at understand-to-design depth, with **no foundation-model content**, as the author's own framing confirms. **R12 (2024):** an end-to-end fine-tune → evaluate → optimise → deploy → operate pipeline including SFT and DPO, RAG pipelines, inference optimisation and CI/CD — at use depth, **bound to nine specific commercial services**, with no prompting, agents, statistics or security chapters. **Neither covers:** LLM-specific serving architecture in depth, observability beyond prompt monitoring, cost governance, durable execution, or regulation.

**11. Which prerequisites do the LLM resources assume?**
R9: intermediate Python and some ML; PyTorch taught in an appendix; mathematics not taught. R10: Python experience and ML fundamentals; notebooks assume a free Colab T4, which bounds what the exercises can do. R12: Python, **AWS specifically**, basic LLM knowledge, Docker and orchestration familiarity; three mandatory API keys and roughly $25 per full run. R6 states no prerequisites at all (the current draft has no preface) but derives its own mathematics.

**12. Which parts of the discovered landscape are better treated as specialization rather than universal AI Engineer requirements?**
Descriptively, and without implying placement: the landscape itself labels **C14 embodied AI** and **C19 AI for science** as specialization or research-oriented, and marks 3D vision, video understanding, TinyML, federated learning, theorem proving and quantum ML as specializations. Their absence from the baseline is consistent with a general AI-engineering scope. By contrast, several **absent** areas are labelled *broadly useful* in the landscape — statistics and experimentation, IR evaluation, data provenance, privacy, AI security, agents and evaluation science — which is what makes their absence notable rather than expected. **Placement decisions belong to the curriculum-design step.**

[⬆ Back to Contents](#contents)

---

## K. Completeness Audit

Challenging this analysis from six perspectives before concluding.

| Perspective | Question | What the challenge surfaced |
| --- | --- | --- |
| **Learner** | What prerequisite or conceptual bridge might be missing? | Two bridges: (a) **mathematics and statistics**, which every later resource assumes and none teaches; (b) **engineering hygiene** (version control, testing, environments), assumed by every code-bearing resource. A third, softer bridge: the baseline moves from library use (R4) to from-scratch implementation (R9) with R5 as the only staging point |
| **Researcher** | What scientific foundations are underrepresented? | Statistical inference; learning theory and generalization; probabilistic/Bayesian modelling; causal reasoning; experimental design. Also the *methodology* of research itself — ablation design, reproducibility practice and evidence standards — which the landscape records as area C3 and which appears here only in fragments |
| **AI engineering** | What practical capability is underrepresented? | The compound-systems layer (C13) and modern serving (C17): agents, tool use, context management, structured outputs, observability, cost control, and security. Also: no resource teaches building an evaluation suite for an application |
| **Data** | Are data quality, experimentation, statistics and evaluation overshadowed by modeling? | **Yes, clearly.** Counting resources: 8 of 12 teach modelling substantially; 2 teach data work substantially (R4, R11); 1 teaches evaluation as a subject (R6); 0 teach experimentation. The baseline is modelling-weighted |
| **Historical** | Are modern resources hiding foundational ideas needed for understanding? | Partially. R5's demotion of SVMs to an online appendix and R6's relegation of HMMs and Naive Bayes to web appendices move classical lineage out of the main path. R7 is the counterweight, keeping TF-IDF, LSA and RNNs central. Net assessment: lineage survives, but increasingly in appendices |
| **Outside-hype** | Would the analysis look different if LLMs and agents were not dominant? | Yes, and usefully so. Removing C7/C13 concerns leaves a baseline that is **strong** on classical ML, deep learning, vision, speech, NLP and classical-ML operations, and **weak** in exactly the same places: statistics, experimentation, evaluation science, data provenance, privacy, recommenders and graphs. The most important gaps are therefore **not** artifacts of current fashion |
| **Resource-evidence** | Which conclusions rest on weak information? | Conclusions about R10 and R12 sub-chapter content rest on publisher pages that blocked automated access; both are marked *Uncertain* where relevant. Conclusions about R5's prose-level treatment of fairness and ethics are *Uncertain* for the same reason. Everything about R1, R2, R3, R4, R6, R9 and R11 rests on directly retrieved primary sources |

[⬆ Back to Contents](#contents)

---

## L. Uncertainties

**Verification limits.**

1. **Publisher blocking.** O'Reilly and Packt product pages returned HTTP 403 to automated access. Sub-chapter detail for R5, R10 and R12 could not be read directly; chapter-level structure for R5 came from the author's own repository and changelog, which is primary.
2. **R5 trustworthy-AI content** is classified Not Covered based on the absence of relevant sections in all 19 notebook headings. Whether the printed narrative contains brief fairness or ethics passages is **Uncertain**.
3. **R11 experimentation depth.** Whether ch. 9 develops real A/B methodology (shadow deployment, canary, interleaving, statistical significance) or describes it at a high level is **Uncertain**.
4. **R12 evaluation, security and drift.** Chapter 7's treatment of LLM-as-judge and benchmark validity, and any guardrail or drift content under LLMOps, are **Uncertain** (primary-indirect evidence only).
5. **R10 preference tuning and IR depth.** Whether DPO/RLHF is walked through, and how deeply retrieval fundamentals are treated, are **Uncertain**.
6. **R7 transformer build depth.** Chapter 9 contains sections implying a guided implementation; the code listings could not be read.
7. **R9 details.** Whether byte-pair encoding is implemented by hand in ch. 2 or used via a library (hand-rolled BPE is listed as repository bonus), whether §7.8 uses LLM-as-judge, and whether RoPE is taught explicitly, are **Uncertain**.
8. **R8 specifics.** Whether speaker diarization is taught as a technique, and the absence of a published last-updated date, are **Uncertain**; the 2023 dating is inferred from unit release dates.
9. **R2 query plans.** Whether `EXPLAIN` appears in body text is **Uncertain**; it is absent from the publisher's detailed contents.
10. **R3 server version** is not published.

**Structural uncertainties.**

11. **Chapter-level intent.** ROADMAP cites whole resources, not chapters. R6 in particular is 26 chapters spanning three volumes; coverage attributed to it assumes the whole book is in scope. If only parts are intended, several "Core" classifications weaken — most importantly IR (ch. 11) and trustworthy AI (§1.10, ch. 10).
12. **Repository versus book.** R9's repository now substantially exceeds the published book (modern architectures, DPO, KV cache, LLM-as-judge). Coverage attributed to "repository bonus" is real but outside the published text, and the roadmap cites the book.
13. **Resource currency.** R8 is 2023 content; R11 is 2022 and pre-foundation-model by its author's own framing; R10 and R12 are pinned to mid- and late-2024 stacks; R6 is a living draft with two unfinished chapters. These are factual observations about publication state, **not** quality judgments, and newer is not assumed better.

[⬆ Back to Contents](#contents)

---

## M. Sources

All URLs accessed **2026-09-18** unless stated. Evidence tier in parentheses: **direct** (retrieved and read) · **indirect** (primary source reached via search snippets because the publisher blocked automated access).

### Canonical repository inputs

- [ROADMAP.md](../ROADMAP.md) — resource inventory (direct)
- [research/2026-09-17-data-intelligence-landscape.md](2026-09-17-data-intelligence-landscape.md) — areas C1–C19 (direct)
- [research/2026-09-17-roadmap-comparison.md](2026-09-17-roadmap-comparison.md) — prior gap analysis (direct)
- [AGENTS.md](../AGENTS.md) — depth ladder and evidence standards (direct)

### R1 The Python Tutorial
- https://docs.python.org/3/tutorial/index.html · /appetite.html · /stdlib.html · /whatnow.html (direct; version 3.14.7, page updated 2026-09-17)

### R2 Practical SQL
- https://nostarch.com/practical-sql-2nd-edition (direct)
- https://nostarch.com/download/samples/DeBarros_TOC.pdf — publisher's detailed contents (direct)
- https://github.com/anthonydb/practical-sql-2 — official repository, audience statement, errata (direct)
- https://practicalsql.com/ (direct)

### R3 PostgreSQL Exercises
- https://pgexercises.com/ · /gettingstarted.html · /about.html · /questions/{basic,joins,updates,aggregates,date,string,recursive}/ (direct)

### R4 Python for Data Analysis
- https://wesmckinney.com/book/ — free open-access 3rd edition, including the preface scope statement (direct)
- https://github.com/wesm/pydata-book — code and datasets (direct)

### R5 Hands-On Machine Learning with Scikit-Learn and PyTorch
- https://ageron.github.io/ — author's site; edition, release date, book lines (direct)
- https://github.com/ageron/handson-mlp — official repository (direct)
- https://github.com/ageron/handson-mlp/blob/main/index.ipynb — chapter list and stated prerequisites (direct)
- https://github.com/ageron/handson-mlp/blob/main/CHANGES.md — **edition identity, dropped deployment chapter, SVM demotion** (direct)
- https://ageron.github.io/homlp/HOMLP_Chapter_17.pdf — free online chapter on speeding up transformers (direct)
- https://www.oreilly.com/catalog/errata.csp?isbn=0642572113490 — publication status (direct)
- https://github.com/ageron/handson-ml3 — previous (Keras/TensorFlow) edition, still live (direct)

### R6 Speech and Language Processing
- https://web.stanford.edu/~jurafsky/slp3/ — official page, draft status, release notes (direct)
- https://web.stanford.edu/~jurafsky/slp3/ed3book_aug26.pdf — full draft of 19 August 2026; table of contents, §1.9, §1.10, §4.10–4.13, §11.1–11.6, ch. 12 placeholder, ch. 15–17 (direct)
- https://web.stanford.edu/~jurafsky/slp3/4.pdf — chapter 4 including §4.11 significance testing (direct)

### R7 Natural Language Processing in Action
- https://www.manning.com/books/natural-language-processing-in-action-second-edition — edition, date, audience (direct)
- https://livebook.manning.com/book/natural-language-processing-in-action-second-edition — chapter and section headings (direct)
- https://gitlab.com/tangibleai/nlpia2 — official code repository (direct)

### R8 Hugging Face Audio Course
- https://huggingface.co/learn/audio-course/en/chapter0/introduction — prerequisites and course framing (direct)
- https://raw.githubusercontent.com/huggingface/audio-transformers-course/main/chapters/en/_toctree.yml — authoritative unit structure (direct)
- https://github.com/huggingface/audio-transformers-course — repository activity and dating (direct)
- Unit 5 evaluation page (WER/CER/RTFx and normalisation worked example) and Unit 6 TTS evaluation page (MOS) (direct)

### R9 Build a Large Language Model (From Scratch)
- https://www.manning.com/books/build-a-large-language-model-from-scratch — date, audience (direct)
- https://livebook.manning.com/book/build-a-large-language-model-from-scratch — chapter and section headings (direct)
- https://github.com/rasbt/LLMs-from-scratch — official repository, appendices, bonus material inventory (direct)
- https://www.manning.com/books/build-a-reasoning-model-from-scratch — the 2026 sequel, recorded as context only (direct)

### R10 Hands-On Large Language Models
- https://www.llm-book.com/ — author site (direct)
- https://github.com/HandsOnLLM/Hands-On-Large-Language-Models — chapter notebooks, bonus guides (direct)
- https://raw.githubusercontent.com/HandsOnLLM/Hands-On-Large-Language-Models/main/requirements.txt — pinned dependency evidence for library-versus-mechanism assessment (direct)
- https://books.google.co.in/books/about/Hands_On_Large_Language_Models.html?id=iE8hEQAAQBAJ — publisher metadata, part boundaries (direct)
- https://katalog.bibliothek.kit.edu/bib/1434969 — library catalogue record (direct)
- O'Reilly product page — chapter titles and preface (indirect; HTTP 403 to automated access)

### R11 Designing Machine Learning Systems
- https://github.com/chiphuyen/dmls-book — official companion repository (direct)
- https://raw.githubusercontent.com/chiphuyen/dmls-book/main/summary.md — **author's own chapter summaries** (direct; the strongest evidence in this audit)
- https://raw.githubusercontent.com/chiphuyen/dmls-book/main/mlops-tools.md — author's stance on tooling (direct)
- https://huyenchip.com/books/ — book line and successor (direct)
- https://raw.githubusercontent.com/chiphuyen/aie-book/main/README.md — **author's own statement of the coverage boundary** between the 2022 book and her 2025 successor (direct; recorded as context only)

### R12 LLM Engineer's Handbook
- https://books.google.co.in/books/about/LLM_Engineer_s_Handbook.html?id=jHEqEQAAQBAJ — publisher metadata and contents (direct)
- https://github.com/PacktPublishing/LLM-Engineers-Handbook and its README — project scope, required services, API keys, cost estimate (direct)
- Packt product page — "who this book is for", chapter descriptions (indirect; HTTP 403 to automated access)

[⬆ Back to Contents](#contents)

</div>
