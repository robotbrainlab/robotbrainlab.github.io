# Consolidated candidate areas — `modern artificial intelligence`

> **SUPERSEDED 2026-11-12.** Run `g` consolidated: 63 areas from 283 categories. **Void with run `g`** — the owner revoked the source register those 283 came from, and confirmed on 2026-11-12 that the 283 and the 63 are history. This cycle's framing runs are `../2026-11-11-h.md` and `../2026-11-11-i.md`. It is input to nothing.

Consolidation run `g`, 2026-11-07. Input: `frame-g.md` (283 category records, 19 sources, two
appendices), read in full. No searches, no fetches, no evidence added. Every verdict is from the
records.

## How to read this file

- `## The level I picked` states the resolution choice and what sits below it.
- `## Areas` holds one UNIT block per surviving area, alphabetical. The order carries no judgement.
- `## Rejected`, `## Merged`, `## Unclear` follow.
- `## Verdict ledger` lists **all 283 input categories** with exactly one verdict each, so none is
  silently dropped. A category whose verdict is `AREA` is either a kept area name in `## Areas`, a
  name merged into one, or a finer category filed under one area's `BELOW`.
- `MODE` on each unit is the clause of the rule it serves: science of AI / research in AI /
  engineering of AI (engineering includes its tools, its measurement, its operation).

## Counts

| | |
|---|---|
| Input categories | 283 |
| Kept areas | 63 |
| Names merged into a kept area | 47 |
| Finer categories filed under an area (`BELOW`) | 123 |
| Rejected `DOMAIN` | 36 |
| Rejected `RECORD` | 0 |
| Rejected `FORMAT` | 9 |
| Rejected `PRODUCT` | 0 |
| `UNCLEAR` | 5 |
| Total accounted for | 63 + 47 + 123 + 36 + 0 + 9 + 0 + 5 = 283 |

`PRODUCT` is empty by the rule's own instruction: "A product or tool name is not dropped. It is
reported as the engineering area it instances, with the product named as evidence." So AILuminate,
AlgoPerf, the twelve MLPerf suites and MCP are reported as the measurement or harness work they
instance, with the product named. The three MLCommons groups whose page gives no scope at all
(Chakra, Croissant, MLCube) are `UNCLEAR`, not `PRODUCT`, because a record carrying no scope cannot
be judged.

## The level I picked

**The level is: the top-level subject list of a source whose own scope is AI as a whole.**

That is the level at which arXiv publishes categories, AAAI publishes submission areas, NeurIPS,
ICLR and ICML publish topics, IJCAI publishes areas, ACM CCS publishes the children of its
`Artificial intelligence` and `Machine learning` nodes, LF AI & Data publishes categories, ISO/IEC
SC 42 publishes working groups, and the AI Engineer World's Fair publishes tracks.

**Why this level and not a coarser one.** One level coarser is the whole field — ACM CCS's
`Artificial intelligence` node and arXiv's `cs.AI` are exactly that, an umbrella and a residual, and
at that level the areas stop differing in what work goes in them. At the level I picked they still
differ: optimization work is not planning work, serving work is not evaluation work, vision work is
not language work. Both umbrella records are still reported as areas (they pass the rule and may not
be dropped), each flagged as sitting above the level rather than beside the others.

**Why this level and not a finer one.** Three sources in the register cover one subfield each and
publish their own top-level list one level below this one. The records say so in their own words:
the `Natural Language Processing` record states that "all 34 of ACL's submission topics sit a level
below this category"; the `Computer vision` record states that "in CVPR's carving, each of its 37
subject areas is a distinct sub-area of this category"; the `Multiagent Systems` record states that
"the whole of AAMAS's eleven areas sits inside this one category at the other venues". So CVPR's 37,
ACL's 34 and AAMAS's 11 are filed under Computer vision, Natural Language Processing and Multiagent
Systems respectively — named, never dropped.

**What sits below the level, by parent.**

| Parent area | What sits below it |
|---|---|
| Computer vision | CVPR's 37 subject areas (32 of them; the other 5 are rejected as `DOMAIN`), plus the WF26 track `Vision & OCR` |
| Natural Language Processing | ACL's 34 submission topics (29 of them; 4 rejected as `DOMAIN`, 1 merged into Agentic Engineering) |
| Machine learning | the 13 ACM CCS children of `Machine learning approaches`, plus ICLR's `metric learning, kernel learning` |
| Multiagent Systems | 6 of AAMAS's 11 areas, plus ACM CCS's `Distributed artificial intelligence` |
| Evals | MLCommons' 12 suites and the MLPerf-family working groups, and the 7 Areas of the MLPerf inference rules |
| Agentic Engineering, AI Infrastructure, Harness Engineering, Inference, Data, CMS, Intelligent Robotics, DMKM, trustworthy machine learning | one to six finer categories each, listed in those units |

**What this level loses** is recorded in `## What this run could not settle`.

## Areas

### Agentic Engineering
- VERDICT: AREA
- WHY: the engineering of AI — building and operating LLM agent systems.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme); ACL 2026 main conference call (review-venue), as `AI/LLM Agents`
- ATTESTED BY: 2 — WF26, ACL
- COVERS: building and operating LLM agent systems; agentic systems built on language models
- EXCLUDES: the harness and runtime around them (Harness Engineering); commerce-specific agents and
  personal agents, filed below; multi-agent coordination theory (Multiagent Systems)
- MERGED FROM: AI/LLM Agents (ACL) — its `ALSO CALLED` names WF26 "Agentic Engineering"
- BELOW: Agent Reliability (WF25); Agentic Commerce (WF26); Autoresearch (WF26); Claws & Personal
  Agents (WF26); Computer Use (WF26); Generative and Agentic AI (GAAI) (AAMAS area)
- FAMILY: both

### AI Infrastructure
- VERDICT: AREA
- WHY: the engineering of AI — the serving, compute and platform layer under AI systems.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF25 (programme); MLCommons benchmarks index (practitioner), as `Infra`; ICML 2026 call
  (review-venue), as `machine learning systems`; ICLR 2026 call (review-venue), as `infrastructure,
  software libraries, hardware, etc.`; NeurIPS 2026 call (review-venue), as `SysML Infrastructure`
- ATTESTED BY: 5 — WF25, MLC, ICML, ICLR, NEURIPS
- COVERS: implementation and scalability, hardware, libraries, distributed methods (ICML); serving,
  compute and platform layer under AI products (WF25); benchmarking infrastructure (MLC)
- EXCLUDES: serving performance as such (Inference); sandbox and code isolation (Sandbox & Platform
  Engineering); data infrastructure (Data-centric aspects of AI)
- MERGED FROM: Infra; infrastructure, software libraries, hardware, etc.; machine learning systems;
  SysML Infrastructure — each record's `ALSO CALLED` names the others reciprocally
- BELOW: AI Architects: AI Factories (WF26); Distributed Computing (LF AI & Data category)
- FAMILY: both

### Artificial intelligence (ACM CCS)
- VERDICT: AREA
- WHY: the science of AI — the index's own umbrella node for the field.
- MODE: science of AI; research in AI
- SOURCES: ACM CCS 2012 via UCT (index); ACM CCS 2012 on the TemaTres vocabulary server (index)
- ATTESTED BY: 2 — UCT, CCSVS
- COVERS: by its 8 CCS children — computer vision, control methods, distributed AI, knowledge
  representation and reasoning, natural language processing, philosophical and theoretical
  foundations, planning and scheduling, search methodologies
- EXCLUDES: machine learning, which CCS files as a **sibling** of this node, not inside it; also
  graphics, modeling and simulation, and the concurrent/parallel/distributed methodologies
- MERGED FROM: none. **Explicitly not merged** with `Artificial Intelligence (cs.AI)`: the input
  record states the labels match but the categories are opposite — this node is the parent of the
  five areas arXiv's cs.AI excludes
- BELOW: its 8 children, every one of which is a kept area or merged into one — Computer vision;
  Natural Language Processing; Knowledge Representation and Reasoning (KRR); Control methods;
  Distributed artificial intelligence; Philosophical/theoretical foundations of AI (merged into
  PEAI); Planning and scheduling (merged into PRS); Search methodologies (merged into SO)
- FAMILY: academic
- NOTE: sits **above** the level I picked. Kept because it passes the rule and may not be dropped.

### Artificial Intelligence (cs.AI)
- VERDICT: AREA
- WHY: the research in AI — the archive's residual class for AI work outside the five categories it
  defers to.
- MODE: research in AI
- SOURCES: arXiv category taxonomy (index)
- ATTESTED BY: 1 — ARXIV
- COVERS: in the source's words, "all areas of AI except Vision, Robotics, Machine Learning,
  Multiagent Systems, and Computation and Language … In particular, includes Expert Systems,
  Theorem Proving …, Knowledge Representation, Planning, and Uncertainty in AI"
- EXCLUDES: by name — vision, robotics, machine learning, multiagent systems, natural language
  processing
- MERGED FROM: none. Explicitly not merged with `Artificial intelligence (ACM CCS)` — see that unit
- BELOW: the subjects its own description names — expert systems, theorem proving, knowledge
  representation, planning, uncertainty in AI (the last three are kept areas in their own right:
  KRR, PRS, RU)
- FAMILY: academic
- NOTE: a residual class, not a peer of the other areas. Kept because the rule admits it and the
  record carries a stated scope.

### Audio and Speech Processing (AUD)
- VERDICT: AREA
- WHY: the research in AI — a modality of AI research with its own 13-topic scope.
- MODE: research in AI; science of AI
- SOURCES: AAAI-27 areas and topics (review-venue)
- ATTESTED BY: 1 — A27
- COVERS: by its 13 topics — audio deepfake detection and anti-spoofing; audio representation
  learning and foundation models; audio-visual and multimodal learning; ASR and spoken language
  understanding; bias, fairness, privacy, low-resource and multilingual speech; datasets and
  benchmarks for audio and speech; environmental sound and acoustic scenes; music information
  retrieval and generation; other foundations; paralinguistics and affective speech; speaker
  recognition, diarization and verification; speech enhancement and separation; speech synthesis and
  voice conversion
- EXCLUDES: text-only language work (Natural Language Processing); vision-side multimodality
  (Computer vision)
- MERGED FROM: none
- BELOW: none in this file. The same ground is also named by `Speech Processing and Spoken Language
  Understanding` (filed below Natural Language Processing as one of ACL's 34) and by the MLPerf Area
  `Audio` (filed below Evals); the applied tracks are the kept area `Voice & Realtime AI`
- FAMILY: academic
- NOTE: the input records that this is the one area AAAI-27 has that AAAI-26 does not.

### causal reasoning
- VERDICT: AREA
- WHY: the science of AI — causality as a learning topic.
- MODE: science of AI; research in AI
- SOURCES: ICLR 2026 call (review-venue)
- ATTESTED BY: 1 — ICLR
- COVERS: causal reasoning as a learning topic
- EXCLUDES: logical and symbolic reasoning (neurosymbolic & hybrid AI systems; and ACL's
  Mathematical, Symbolic, Neurosymbolic, and Logical Reasoning, filed below NLP)
- MERGED FROM: none. ICML folds causality into `trustworthy machine learning` and AAAI into a KRR
  keyword; neither record equates the categories, so no merge was made
- BELOW: none
- FAMILY: academic
- NOTE: thin scope — the record's `INCLUDES` restates the name. Anchored by its `EXCLUDES` and by
  ICML's and AAAI's placements of the same word. Listed in `What this run could not settle`.

### Cognitive Modeling & Cognitive Systems (CMS)
- VERDICT: AREA
- WHY: the science of AI — cognitive architectures and the modelling of intelligence itself.
- MODE: science of AI; research in AI
- SOURCES: AAAI-26 keywords (review-venue); AAAI-27 areas and topics (review-venue)
- ATTESTED BY: 2 — A26K, A27
- COVERS: AAAI-26's 13 keywords — adaptive behavior; affective computing; agent architectures;
  analogy; applications; (computational) cognitive architectures; computational creativity;
  conceptual inference and reasoning; neural spike coding; other foundations; simulating human
  behavior; social cognition and interaction; symbolic representations. AAAI-27 keeps six merged
  topics
- EXCLUDES: human-facing interaction (Humans and AI (HAI))
- MERGED FROM: none
- BELOW: Neuroscience and cognitive science (NeurIPS topic)
- FAMILY: academic

### Computational approaches and characteristics of artificial intelligence systems
- VERDICT: AREA
- WHY: the engineering of AI — standardisation of the computational approaches AI systems use and
  the characteristics they exhibit.
- MODE: engineering of AI (its measurement and its operation)
- SOURCES: ISO/IEC JTC 1/SC 42, WG 5, via Wikipedia quoting the titles (practitioner)
- ATTESTED BY: 1 — SC42
- COVERS: standardisation of the computational approaches AI systems use and the characteristics
  they exhibit
- EXCLUDES: foundational vocabulary and concepts (Foundational standards); trust properties
  (trustworthy machine learning, via SC 42's `Trustworthiness`)
- MERGED FROM: none
- BELOW: individual standards projects, which the source does not name
- FAMILY: applied

### Computer vision
- VERDICT: AREA
- WHY: the research in AI — image processing, pattern recognition and scene understanding.
- MODE: research in AI; science of AI
- SOURCES: ACM CCS 2012 via UCT (index); ACM CCS 2012 on the vocabulary server (index); arXiv
  taxonomy as cs.CV (index); AAAI-26 keywords (review-venue); AAAI-27 areas and topics
  (review-venue); AAAI-26 main technical track call (review-venue); NeurIPS 2026 call
  (review-venue); IJCAI-ECAI 2026 call via AEPIA (review-venue)
- ATTESTED BY: 8 — UCT, CCSVS, ARXIV, A26K, A27, A26M, NEURIPS, IJCAI
- COVERS: image processing, pattern recognition and scene understanding (arXiv); CCS's computer
  vision problems, representations, tasks, and image and video acquisition; AAAI's 26 keywords from
  3D and low-level vision to large vision models, diffusion models for vision and vision for robots
- EXCLUDES: natural language (Natural Language Processing); graphics (rejected as `DOMAIN`)
- MERGED FROM: Computer Vision and Pattern Recognition (cs.CV) was already merged into this record
  by the framing run on arXiv's own description. **Not merged** with the MLPerf Area `Vision`, which
  is a set of benchmark tasks (filed below Evals)
- BELOW: CVPR 2026's 37 subject areas, 32 of which pass the rule — 3D from multi-view and sensors;
  3D from single images; Adversarial attack and defense; Biometrics; Computational imaging; Computer
  Vision for Robotics; Computer vision theory; Datasets and evaluation; Deep learning architectures
  and techniques; Document analysis and understanding; Efficient and scalable vision; Embodied
  vision: Active agents, simulation; Event-based cameras; Explainable computer vision; Humans: Face,
  body, pose, gesture, movement; Image and video synthesis and generation; Low-level vision; Machine
  learning (other than deep learning); Multimodal learning; Optimization methods (other than deep
  learning); Physics-based vision and shape-from-X; Recognition: Categorization, detection,
  retrieval; Representation learning; Scene analysis and understanding; Segmentation, grouping and
  shape analysis; Self-, semi-, meta- and unsupervised learning; Transfer/ low-shot/ continual/
  long-tail learning; Transparency, fairness, accountability, privacy and ethics in vision; Video:
  Action and event understanding; Video: Low-level analysis, motion, and tracking; Vision +
  graphics; Vision, language, and reasoning. Plus the applied track Vision & OCR (WF26). The other
  5 CVPR areas are rejected as `DOMAIN` and named there
- FAMILY: both

### Constraint Satisfaction and Optimization (CSO)
- VERDICT: AREA
- WHY: the science of AI — constraint and satisfiability methods.
- MODE: science of AI; research in AI
- SOURCES: AAAI-26 keywords (review-venue); AAAI-27 areas and topics (review-venue); IJCAI-ECAI
  2026 call via AEPIA (review-venue), as `Constraints and Satisfiability`
- ATTESTED BY: 3 — A26K, A27, IJCAI
- COVERS: AAAI-26's 12 keywords — applications; constraint learning and acquisition; constraint
  optimization; constraint programming; constraint satisfaction; distributed CSP/optimization; mixed
  discrete/continuous optimization; other foundations; satisfiability; satisfiability modulo
  theories; search; solvers and tools
- EXCLUDES: continuous and learning-side optimization (Search and Optimization (SO); Optimization)
- MERGED FROM: Constraints and Satisfiability (IJCAI) — its `ALSO CALLED` names AAAI's CSO
- BELOW: none
- FAMILY: academic

### Context Engineering
- VERDICT: AREA
- WHY: the engineering of AI — assembling and managing what a model is given to work with.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: assembling and managing what a model is given to work with
- EXCLUDES: retrieval itself (Search & Retrieval); memory across sessions (Memory & Continual
  Learning)
- MERGED FROM: none
- BELOW: none
- FAMILY: applied
- NOTE: the input records that no academic source names context engineering; the nearest is ACL's
  `Retrieval-Augmented Language Models`, filed below NLP.

### Data
- VERDICT: AREA
- WHY: the engineering of AI — its tools: the data tool chain AI systems are built on.
- MODE: engineering of AI (its tools)
- SOURCES: LF AI & Data landscape source file (practitioner)
- ATTESTED BY: 1 — LFAI
- COVERS: its 13 subcategories — Education, Lineage, Relational DB, Store & Format, Versioning,
  Operations, Feature Engineering, Stream Processing, SQL Engine, Visualization, Pipeline
  Management, Labeling & Annotation, Governance
- EXCLUDES: model-side concerns (Model); notebooks (Notebook Environment)
- MERGED FROM: none. Kept separate from `Data-centric aspects of AI`, which is the research side —
  the two differ in what work goes in them, which is the level test
- BELOW: Big Data (SC 42 WG 2) — its `ALSO CALLED` names this category
- FAMILY: applied

### Data Mining & Knowledge Management (DMKM)
- VERDICT: AREA
- WHY: the research in AI — mining and managing knowledge in data.
- MODE: research in AI; engineering of AI (its tools)
- SOURCES: AAAI-26 keywords (review-venue); AAAI-27 areas and topics (review-venue); AAAI-26 main
  technical track call (review-venue), as `Data Mining`; IJCAI-ECAI 2026 via AEPIA (review-venue),
  as `Data Mining`
- ATTESTED BY: 4 — A26K, A27, A26M, IJCAI
- COVERS: AAAI-26's 19 keywords — anomaly/outlier detection; applications; conversational systems
  for recommendation and retrieval; data compression; data stream mining; data visualization and
  summarization; graph mining and social network analysis; intelligent query processing; knowledge
  acquisition from the web; linked open data and knowledge graphs; mining of spatial/temporal data;
  mining of visual/multimedia/multimodal data; other foundations; recommender systems; provenance
  and trust; rule and pattern mining; scalability and distributed systems; semantic web; web
- EXCLUDES: knowledge representation and reasoning (KRR)
- MERGED FROM: Data Mining (A26M + IJCAI) — the `Data Mining` record states that AAAI's own keywords
  page "calls the same ground" DMKM
- BELOW: LLM Recsys (WF26, WF25)
- FAMILY: academic

### Data-centric aspects of AI
- VERDICT: AREA
- WHY: the research in AI, and its measurement — the data side of AI as a subject in its own right.
- MODE: research in AI; engineering of AI (its measurement)
- SOURCES: NeurIPS 2026 call (review-venue); WF26 (programme), as `Data Quality`; MLCommons
  benchmarks index (practitioner), as `Data-centric ML`
- ATTESTED BY: 3 — NEURIPS, WF26, MLC
- COVERS: the data side of AI as a research topic; the quality of data used to build and evaluate AI
  systems
- EXCLUDES: datasets as artefacts for release (datasets and benchmarks); evaluation of model outputs
  (Evals); the data tool chain as tooling (Data)
- MERGED FROM: Data Quality (WF26) and Data-centric ML (MLC) — both records' `ALSO CALLED` name this
  NeurIPS topic, and the NeurIPS record names both of them
- BELOW: none
- FAMILY: both

### datasets and benchmarks
- VERDICT: AREA
- WHY: the engineering of AI — its measurement: the resources measurement is done with.
- MODE: engineering of AI (its measurement)
- SOURCES: ICLR 2026 call (review-venue); MLCommons benchmarks index (practitioner), as `Datasets`
- ATTESTED BY: 2 — ICLR, MLC
- COVERS: new datasets and benchmarks as a submission category; the working group that publishes
  MLCommons' own datasets (Cognata, Dollar Street, Multilingual Spoken Words, People's Speech,
  Unsupervised People's Speech)
- EXCLUDES: evaluation methodology (Evals); benchmark rules and suites (filed below Evals)
- MERGED FROM: Datasets (MLC) — its `ALSO CALLED` names ICLR's "datasets and benchmarks"
- BELOW: none here. CVPR's `Datasets and evaluation` sits below Computer vision and ACL's `Resources
  and Evaluation` below Natural Language Processing, by the level rule
- FAMILY: both
- NOTE: the input records that NeurIPS 2026 moved this ground out of its main call into a separate
  "Call for Evaluations & Datasets" track.

### Deep learning
- VERDICT: AREA
- WHY: the science of AI — deep architectures, their training and their theory.
- MODE: science of AI; research in AI; engineering of AI (its tools)
- SOURCES: NeurIPS 2026 call (review-venue); ICML 2026 call (review-venue); LF AI & Data landscape
  (practitioner)
- ATTESTED BY: 3 — NEURIPS, ICML, LFAI
- COVERS: architectures, generative models and theory (ICML); frameworks, platforms, libraries and
  tools (LF AI & Data's 4 subcategories)
- EXCLUDES: machine learning that is not deep — CVPR names that exclusion explicitly
- MERGED FROM: none beyond the framing run's own merge of the three identical labels
- BELOW: none here. CVPR's `Deep learning architectures and techniques` sits below Computer vision
  and ACM CCS's `Neural networks` below Machine learning, by the level rule
- FAMILY: both
- NOTE: the input records that ACM CCS 2012 has no deep-learning node anywhere.

### Design Engineering
- VERDICT: AREA
- WHY: the engineering of AI — the design side of building AI products.
- MODE: engineering of AI (its tools)
- SOURCES: WF26 (programme); WF25 (programme)
- ATTESTED BY: 2 — WF26, WF25
- COVERS: the design side of building AI products
- EXCLUDES: back-end platform work (Sandbox & Platform Engineering; AI Infrastructure)
- MERGED FROM: none beyond the framing run's merge of the two editions' identical labels
- BELOW: none
- FAMILY: applied
- NOTE: the nearest academic category is AAAI's keyword "HAI: User Experience and Usability", one
  level below the kept area Humans and AI (HAI).

### Evals
- VERDICT: AREA
- WHY: the engineering of AI — its measurement: whether a deployed AI system is doing its job.
- MODE: engineering of AI (its measurement)
- SOURCES: WF26 (programme); WF25 (programme); ICML 2026 call (review-venue), as `evaluation`;
  ISO/IEC JTC 1/SC 42 JWG 2 (practitioner), as `Testing of AI-based systems`
- ATTESTED BY: 4 — WF26, WF25, ICML, SC42
- COVERS: measuring whether a deployed AI system is doing its job; methodology, meta studies,
  replicability and validity, human-in-the-loop (ICML); standardisation of how AI-based systems are
  tested (SC 42)
- EXCLUDES: dataset construction (datasets and benchmarks); data quality (Data-centric aspects of
  AI); functional safety in a controlled process (Functional safety and AI systems)
- MERGED FROM: evaluation (ICML) and Testing of AI-based systems (SC 42) — both records' `ALSO
  CALLED` name "Evals", and the SC 42 record names ICML's "evaluation" and MLCommons' AILuminate
- BELOW: the whole measurement apparatus the practitioner sources publish, named here so none is
  dropped — AI Risk & Reliability; AILuminate; AlgoPerf: Training Algorithms; Algorithms; MLPerf
  Automotive; MLPerf Client; MLPerf Endpoints; MLPerf Inference; MLPerf Inference: Datacenter;
  MLPerf Inference: Edge; MLPerf Inference: Mobile; MLPerf Inference: Tiny; MLPerf Storage; MLPerf
  Tiny; MLPerf Training; MLPerf Training: HPC; Mobile; Power; and the 7 Areas of the MLPerf
  inference rules — Audio, Automotive, Commerce, Generative, Graph, Language, Vision
- FAMILY: both
- NOTE: the products are named as evidence, per the rule: AILuminate instances safety measurement,
  AlgoPerf instances training-algorithm measurement, the MLPerf suites instance speed, power and
  storage measurement.

### Foundational standards
- VERDICT: AREA
- WHY: the engineering of AI — the concepts and terminology its engineering is written in.
- MODE: engineering of AI (its operation)
- SOURCES: ISO/IEC JTC 1/SC 42, WG 1, via Wikipedia quoting the titles (practitioner)
- ATTESTED BY: 1 — SC42
- COVERS: the subcommittee's foundational standards work — concepts and terminology for AI
- EXCLUDES: trust properties (SC 42's Trustworthiness, merged into trustworthy machine learning);
  use cases (rejected as `DOMAIN`); computational approaches (WG 5, its own area)
- MERGED FROM: none
- BELOW: individual standards projects, which the source does not name
- FAMILY: applied
- NOTE: the input records that no research source has a vocabulary-and-concepts category.

### Functional safety and AI systems
- VERDICT: AREA
- WHY: the engineering of AI — its operation: hazard and harm where AI is in a controlled process.
- MODE: engineering of AI (its operation and its measurement)
- SOURCES: ISO/IEC JTC 1/SC 42, JWG 4 with IEC/TC 65/SC 65A, via Wikipedia (practitioner)
- ATTESTED BY: 1 — SC42
- COVERS: functional safety where AI is in the loop, run jointly with the industrial-process control
  committee
- EXCLUDES: model-output (content) safety — the kept area Safety, and ACL's `Safety and Alignment in
  LLMs` below NLP
- MERGED FROM: none. **Deliberately not merged** with Safety: the input record states that the two
  senses "share a word and not a subject"
- BELOW: individual standards projects, which the source does not name
- FAMILY: applied

### Game Theory and Economic Paradigms (GTEP)
- VERDICT: AREA
- WHY: the science of AI — the strategic and economic theory AI systems reason with.
- MODE: science of AI; research in AI
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics; AAMAS 2026 main track; IJCAI-ECAI 2026 via
  AEPIA (all review-venue)
- ATTESTED BY: 4 — A26K, A27, AAMAS, IJCAI
- COVERS: auctions and mechanism design; bargaining and negotiation; behavioural and evolutionary
  game theory; equilibrium concepts and computation; voting and preference aggregation; social
  choice; judgment aggregation; fair allocation and fair division; tournaments; matching; digital and
  liquid democracy; coalition formation; cooperative games
- EXCLUDES: non-strategic team formation (COINE, below Multiagent Systems)
- MERGED FROM: none beyond the framing run's merge of four identical labels including the code
- BELOW: none
- FAMILY: academic
- NOTE: ICML places game theory inside `theory of machine learning`; three venues give it an area.

### general machine learning
- VERDICT: AREA
- WHY: the science of AI — core supervised and unsupervised method work.
- MODE: science of AI; research in AI
- SOURCES: NeurIPS 2026 call; ICLR 2026 call; ICML 2026 call (all review-venue)
- ATTESTED BY: 3 — NEURIPS, ICLR, ICML
- COVERS: active learning, clustering, online learning, ranking, supervised, semi- and
  self-supervised learning, time-series analysis (ICML); core supervised and unsupervised
  contributions (NeurIPS)
- EXCLUDES: deep learning, which all three name separately; at ICLR this topic is explicitly the
  residual, "none of the above"
- MERGED FROM: none beyond the framing run's merge of three identical labels
- BELOW: none
- FAMILY: academic

### Generalization and multi-task learning
- VERDICT: AREA
- WHY: the science of AI — how learned ability carries across tasks and over time.
- MODE: science of AI; research in AI
- SOURCES: NeurIPS 2026 call (review-venue); ICLR 2026 call (review-venue), as `transfer learning,
  meta learning, and lifelong learning`
- ATTESTED BY: 2 — NEURIPS, ICLR
- COVERS: generalisation and multi-task learning; transfer, meta and lifelong learning
- EXCLUDES: learning theory (theory of machine learning); supervision regimes (unsupervised,
  self-supervised, semi-supervised, and supervised representation learning)
- MERGED FROM: transfer learning, meta learning, and lifelong learning (ICLR) — the two records name
  each other in `ALSO CALLED`. **Thin merge**: the framing run declined it because no two of the five
  names for this ground share word-sets. Listed in `What this run could not settle`
- BELOW: none here. ACL's `Generalizability and Transfer` sits below NLP and CVPR's `Transfer/
  low-shot/ continual/ long-tail learning` below Computer vision, by the level rule. `Memory &
  Continual Learning` is kept separate, because its record names memory first
- FAMILY: academic

### generative models
- VERDICT: AREA
- WHY: the science of AI — generative modelling, and the models and tools it produces.
- MODE: science of AI; research in AI; engineering of AI (its tools)
- SOURCES: ICLR 2026 call (review-venue); LF AI & Data landscape (practitioner), as `Generative AI`
- ATTESTED BY: 2 — ICLR, LFAI
- COVERS: generative modelling as a learning topic; generative models and the tools around them, as
  open-source projects (LF AI & Data's 2 subcategories, Models and Tools)
- EXCLUDES: media production practice (Generative Media); agentic work (Agentic Engineering)
- MERGED FROM: Generative AI (LFAI) — its `ALSO CALLED` names ICLR's "generative models", and the
  ICLR record names LF AI & Data's category
- BELOW: none here. The MLPerf Area `Generative` sits below Evals; CVPR's `Image and video synthesis
  and generation` below Computer vision
- FAMILY: both
- NOTE: the input records that NeurIPS names generative AI in its opening sentence but has no
  generative topic in its 21-item list.

### Generative Media
- VERDICT: AREA
- WHY: the engineering of AI — generating images, video and audio as a production practice.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme); WF25 (programme)
- ATTESTED BY: 2 — WF26, WF25
- COVERS: generating images, video and audio as a production practice
- EXCLUDES: the modelling methods themselves (generative models)
- MERGED FROM: none beyond the framing run's merge of the two editions' identical labels
- BELOW: none
- FAMILY: applied
- NOTE: kept separate from `generative models` because the records divide the work — methods at the
  venues, production at the programme. NeurIPS's `AI/ML for creatives` is rejected as `DOMAIN`.

### Graphs
- VERDICT: AREA
- WHY: the engineering of AI — its tools: graph-shaped data and knowledge in AI applications.
- MODE: engineering of AI (its tools)
- SOURCES: WF26 (programme); WF25 (programme), as `GraphRAG`
- ATTESTED BY: 2 — WF26, WF25
- COVERS: graph-shaped data and knowledge in AI applications; retrieval-augmented generation over
  graph-structured knowledge (WF25)
- EXCLUDES: graph learning as a method — the kept area `learning on graphs and other geometries &
  topologies`; node classification as a benchmark task (MLPerf Area `Graph`, below Evals)
- MERGED FROM: GraphRAG (WF25) — the `Graphs` record states "the 2025 edition named the same track
  'GraphRAG' and the 2026 edition shortened it to 'Graphs'"
- BELOW: none
- FAMILY: applied
- NOTE: this is one of the records the brief warns about. Its scope is thin but it is a scope, not a
  restatement: it says graph data and knowledge **in applications**, and excludes graph learning by
  name. **Not merged** with the MLPerf Area `Graph`, which the input says means node classification —
  same word, different subject.

### Harness Engineering
- VERDICT: AREA
- WHY: the engineering of AI — its tools: the scaffolding, tools and runtime a model runs inside.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: building the scaffolding, tools and runtime that an agent or model runs inside
- EXCLUDES: the agent logic itself (Agentic Engineering); serving performance (Inference)
- MERGED FROM: none
- BELOW: MCP (WF25) — the Model Context Protocol, reported as the harness-interface engineering it
  instances, with the protocol named as evidence
- FAMILY: applied
- NOTE: the second record the brief warns about. The `WHY` here cites the rule's engineering-tools
  clause against the record's stated scope (scaffolding, tools, runtime) and its stated exclusion
  (agent logic), not the name. Still thin, and listed in `What this run could not settle`.

### Humans and AI (HAI)
- VERDICT: AREA
- WHY: the research in AI — people interacting with AI systems, and AI built around them.
- MODE: research in AI; engineering of AI (its tools)
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics; IJCAI-ECAI 2026 via AEPIA (all
  review-venue); NeurIPS 2026 call (review-venue), as `Human interaction in AI systems`; AAAI-26
  main technical track call (review-venue), as `human-in-the-loop AI`
- ATTESTED BY: 5 — A26K, A27, IJCAI, NEURIPS, A26M
- COVERS: AAAI-26's 21 keywords — applications; brain-sensing and analysis; crowd sourcing and human
  computation; emotional intelligence; game design; human-aware planning and behavior prediction;
  human-computer interaction; human-in-the-loop machine learning; intelligent user interfaces;
  interaction techniques and devices; learning human values and preferences; other foundations;
  planning and decision support for human-machine teams; teamwork and team formation; understanding
  people; user experience and usability; voting; human-AI collaboration and teaming; explainable AI
  for human understanding; AI for accessibility
- EXCLUDES: philosophy and ethics (PEAI); the socio-technical analysis of AI (merged into
  trustworthy machine learning)
- MERGED FROM: Human interaction in AI systems (NeurIPS) and human-in-the-loop AI (A26M) — both
  records' `ALSO CALLED` name AAAI's "Humans and AI (HAI)", and the A26M record states that AAAI's own
  keywords page holds human-in-the-loop as one keyword inside HAI. **Not merged** with AAMAS's
  `Human-Agent Interaction (HAI)`: the input says the codes collide and the categories do not match
- BELOW: Human-Agent Interaction (HAI) is **not** here — it is filed below Multiagent Systems. ACL's
  `Human-AI Interaction/Cooperation and Human-Centric NLP` sits below NLP, by the level rule
- FAMILY: academic

### Inference
- VERDICT: AREA
- WHY: the engineering of AI — its operation: serving models at a latency, throughput and cost.
- MODE: engineering of AI (its operation and its measurement)
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: serving models — latency, throughput and cost of running them
- EXCLUDES: training (Posttraining & Midtraining; and MLPerf Training below Evals); local and
  on-device running (Local AI)
- MERGED FROM: none. The MLCommons working group `MLPerf Inference` and the four `MLPerf Inference:
  …` suites measure this ground and are filed below Evals, because at MLCommons they are benchmark
  suites rather than the practice
- BELOW: AI Architects: Tokenmaxxing (WF26) — token budgets and spend
- FAMILY: applied
- NOTE: the input calls this "the clearest instance of the register's own note that the academic and
  applied halves are nearly disjoint" — no review venue has an inference-serving category.

### Intelligent Robotics
- VERDICT: AREA
- WHY: the research in AI — robots, embodiment, control and the world models they act on.
- MODE: research in AI; science of AI; engineering of AI (its operation)
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics; IJCAI-ECAI 2026 via AEPIA; arXiv taxonomy as
  cs.RO; AAMAS 2026 main track as `Robotics and Control (ROBOT)`; NeurIPS 2026 call as `Robotics,
  embodied systems, and engineering`; ICLR 2026 call as `applications to robotics, autonomy,
  planning`; AAAI-26 main technical track call as `robotics and perception`; WF25 as `Autonomy +
  Robotics`; WF26 as `Robotics & World Models`
- ATTESTED BY: 10 — A26K, A27, IJCAI, ARXIV, AAMAS, NEURIPS, ICLR, A26M, WF25, WF26
- COVERS: AAAI-26's 12 keywords — behavior learning and control; cognitive robotics; human-robot
  interaction; learning and optimization for robotics; localization, mapping and navigation;
  manipulation; motion and path planning; multi-robot systems; multimodal perception and sensor
  fusion; other foundations and applications; state estimation; embodied AI. Plus control
  (AAMAS, CCS), embodiment and engineering (NeurIPS), and learned world models (WF26)
- EXCLUDES: vision for robots, which AAAI holds as a vision keyword and CVPR as the subject area
  `Computer Vision for Robotics`, filed below Computer vision
- MERGED FROM: Robotics (cs.RO); Robotics and Control (ROBOT); Robotics, embodied systems, and
  engineering; applications to robotics, autonomy, planning; Autonomy + Robotics; Robotics & World
  Models; robotics and perception — every one of these records names one or more of the others in
  `ALSO CALLED`, and the input's own cross-references run in both directions. The framing run
  declined these merges on wording alone; this run merges them because they are the same area under
  different names. **The merge of `Robotics & World Models` carries the only subject no other source
  names — world models.** Listed in `What this run could not settle`
- BELOW: Control methods (ACM CCS child of Artificial intelligence)
- FAMILY: both

### Knowledge Representation and Reasoning (KRR)
- VERDICT: AREA
- WHY: the science of AI — how knowledge is represented and reasoned over.
- MODE: science of AI; research in AI
- SOURCES: ACM CCS 2012 via UCT (index); ACM CCS 2012 on the vocabulary server (index); AAAI-26
  keywords; AAAI-27 areas and topics; IJCAI-ECAI 2026 via AEPIA (all review-venue); AAAI-26 main
  technical track call (review-venue), as `Knowledge representation` and as `Reasoning`
- ATTESTED BY: 6 — UCT, CCSVS, A26K, A27, IJCAI, A26M
- COVERS: AAAI-26's 19 keywords — action, change and causality; applications; argumentation;
  automated reasoning and theorem proving; common-sense reasoning; computational complexity of
  reasoning; description logics; diagnosis and abductive reasoning; geometric, spatial and temporal
  reasoning; knowledge acquisition; knowledge engineering; knowledge representation languages; logic
  programming; nonmonotonic reasoning; ontologies; other foundations; preferences; qualitative
  reasoning; reasoning with beliefs. CCS adds logic and answer-set programming, belief revision,
  ontology engineering and probabilistic reasoning
- EXCLUDES: reasoning under uncertainty (Reasoning under Uncertainty (RU))
- MERGED FROM: Knowledge representation (A26M) and Reasoning (A26M) — the `Knowledge representation`
  record states that AAAI's own keywords page, CCS, IJCAI and arXiv all bind the two halves into one
  category, and the `Reasoning` record states that AAAI's keywords page has no bare Reasoning area,
  "only Knowledge Representation and Reasoning (KRR) and Reasoning under Uncertainty (RU)". **Both
  merges undo a split the AAAI-26 main-track prose makes.** Listed in `What this run could not settle`
- BELOW: none here. AAMAS's `Representation, and Reasoning (RR)` sits below Multiagent Systems and
  ACL's `Mathematical, Symbolic, Neurosymbolic, and Logical Reasoning` below NLP, by the level rule
- FAMILY: academic

### Language and multimodal language models
- VERDICT: AREA
- WHY: the science of AI — language models and multimodal language models themselves.
- MODE: science of AI; research in AI
- SOURCES: NeurIPS 2026 call (review-venue)
- ATTESTED BY: 1 — NEURIPS
- COVERS: language models and multimodal language models in one topic
- EXCLUDES: computer vision, which NeurIPS names separately
- MERGED FROM: none. The input's `Natural Language Processing` record states explicitly that this
  category was **not merged** with NLP, and that NeurIPS 2026 has no NLP topic at all. ACL's
  `Language Models` is filed below NLP by the level rule. Whether this should instead be folded into
  Natural Language Processing is in `What this run could not settle`
- BELOW: none
- FAMILY: academic

### learning on graphs and other geometries & topologies
- VERDICT: AREA
- WHY: the science of AI — learning on graph, geometric and topological structure.
- MODE: science of AI; research in AI
- SOURCES: ICLR 2026 call (review-venue)
- ATTESTED BY: 1 — ICLR
- COVERS: learning on graphs and on other geometries and topologies
- EXCLUDES: network science as a subject (rejected as `DOMAIN`); graph data stores in applications
  (the kept area Graphs)
- MERGED FROM: none
- BELOW: none. The MLPerf Area `Graph` (node classification) sits below Evals
- FAMILY: academic
- NOTE: thin scope — the record's `INCLUDES` restates the name, anchored by its `EXCLUDES`. Listed
  in `What this run could not settle`.

### Local AI
- VERDICT: AREA
- WHY: the engineering of AI — its operation: running models on local and personal hardware.
- MODE: engineering of AI (its operation)
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: running models on local and personal hardware
- EXCLUDES: datacenter serving (Inference)
- MERGED FROM: none. The four MLCommons suites that measure the same ground — MLPerf Client, MLPerf
  Inference: Edge, Mobile and Tiny — are filed below Evals as measurement
- BELOW: none
- FAMILY: applied

### Machine learning
- VERDICT: AREA
- WHY: the science of AI — all aspects of learning from data.
- MODE: science of AI; research in AI; engineering of AI (its tools)
- SOURCES: ACM CCS 2012 via UCT (index); ACM CCS 2012 on the vocabulary server (index); arXiv
  taxonomy as cs.LG **and** stat.ML (index); AAAI-26 keywords; AAAI-27 areas and topics; AAAI-26
  main technical track call; IJCAI-ECAI 2026 via AEPIA (all review-venue); LF AI & Data landscape
  (practitioner)
- ATTESTED BY: 8 — UCT, CCSVS, ARXIV, A26K, A27, A26M, IJCAI, LFAI
- COVERS: all aspects of machine-learning research including robustness, explanation, fairness and
  methodology (arXiv cs.LG); learning paradigms and learning approaches (CCS); AAAI-26's 55
  keywords, the largest single block on that page; frameworks, platforms and libraries (LF AI & Data)
- EXCLUDES: in CCS only, everything under `Artificial intelligence` — vision, NLP, KRR, planning and
  search are siblings of this node, not inside it
- MERGED FROM: none beyond the framing run's own merges. arXiv's split into cs.LG and stat.ML is
  carried forward as recorded, not resolved
- BELOW: the 13 ACM CCS children of `Machine learning approaches` — Classification and regression
  trees; Factorization methods; Instance-based learning; Kernel methods; Learning in probabilistic
  graphical models; Learning latent representations; Learning linear models; Logical and relational
  learning; Markov decision processes; Neural networks; Partially-observable Markov decision
  processes; Rule learning; Stochastic games. Plus ICLR's `metric learning, kernel learning`
- FAMILY: both

### Memory & Continual Learning
- VERDICT: AREA
- WHY: the engineering of AI, and its science — giving systems memory, and learning after deployment.
- MODE: engineering of AI (its operation); science of AI
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: giving systems memory, and learning that continues after deployment
- EXCLUDES: context assembly within a single session (Context Engineering)
- MERGED FROM: none. Kept separate from `Generalization and multi-task learning` because the input
  record states that this programme "names memory first and continual learning second, which is a
  different emphasis in the same words"
- BELOW: none
- FAMILY: applied

### Model
- VERDICT: AREA
- WHY: the engineering of AI — its tools: the model lifecycle from training to serving.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: LF AI & Data landscape source file (practitioner)
- ATTESTED BY: 1 — LFAI
- COVERS: its 9 subcategories — Inference, Federated Learning, Training, Parameter, Format &
  Interface, Marketplace, Workflow, Benchmarking, Tool
- EXCLUDES: the data side (Data); notebooks (Notebook Environment)
- MERGED FROM: none
- BELOW: none
- FAMILY: applied
- NOTE: the input records that no review venue has a model-lifecycle category, and that federated
  learning, model formats and model marketplaces appear nowhere in the academic half of the register.

### Multiagent Systems
- VERDICT: AREA
- WHY: the science of AI — many agents, their coordination and their interaction.
- MODE: science of AI; research in AI; engineering of AI (its tools)
- SOURCES: arXiv taxonomy as cs.MA (index); AAAI-26 keywords; AAAI-27 areas and topics; AAAI-26
  main technical track call; IJCAI-ECAI 2026 via AEPIA (all review-venue)
- ATTESTED BY: 5 — ARXIV, A26K, A27, A26M, IJCAI
- COVERS: in arXiv's words, "multiagent systems, distributed artificial intelligence, intelligent
  agents, coordinated interactions. and practical applications"; AAAI-26's 15 keywords
- EXCLUDES: single-agent AI, which goes to the other areas
- MERGED FROM: none. **Not merged** with ACM CCS's `Distributed artificial intelligence`, which the
  input keeps separate because CCS makes it a child of AI while arXiv and the venues make it a peer —
  it is filed `BELOW` instead
- BELOW: 6 of AAMAS 2026's 11 areas of interest — Coordination, Organizations, Institutions, Norms,
  and Ethics (COINE); Engineering and Analysis of Multiagent Systems (EMAS); Human-Agent Interaction
  (HAI); Learning and Adaptation (LEARN); Representation, and Reasoning (RR); Search, Optimization,
  Planning, and Scheduling (SOPS). Plus ACM CCS's `Distributed artificial intelligence`. Of the
  remaining AAMAS areas, GTEP is a kept area, GAAI is filed below Agentic Engineering, ROBOT is
  merged into Intelligent Robotics, and IA and SIM are rejected as `DOMAIN`
- FAMILY: academic
- NOTE: the input calls this "the sharpest difference of grain in the register" — one category at
  AAAI, IJCAI and arXiv; 11 areas and about 150 topics at AAMAS.

### Natural Language Processing
- VERDICT: AREA
- WHY: the research in AI — language as a subject of AI.
- MODE: research in AI; science of AI; engineering of AI (its tools)
- SOURCES: ACM CCS 2012 via UCT (index); ACM CCS 2012 on the vocabulary server (index); arXiv
  taxonomy as cs.CL (index); AAAI-26 keywords; AAAI-27 areas and topics; AAAI-26 main technical
  track call; IJCAI-ECAI 2026 via AEPIA (all review-venue); LF AI & Data landscape (practitioner)
- ATTESTED BY: 8 — UCT, CCSVS, ARXIV, A26K, A27, A26M, IJCAI, LFAI
- COVERS: by CCS — language resources, machine translation, natural language generation, phonology
  and morphology, speech recognition; by arXiv — natural language processing, computational
  linguistics, speech and text retrieval; by AAAI-26, 24 keywords
- EXCLUDES: in arXiv's words, "work on artificial languages (programming languages, logics, formal
  systems) that does not explicitly address natural-language issues broadly construed"
- MERGED FROM: `Computation and Language (cs.CL)` was already merged into this record by the framing
  run on arXiv's own description. **Not merged** with the MLPerf Area `Language` or with NeurIPS's
  `Language and multimodal language models`
- BELOW: ACL 2026's 34 submission topics, 29 of which pass the rule — Code Models; Dialogue and
  Interactive Systems; Discourse, Pragmatics, and Reasoning; Ethics, Bias, and Fairness;
  Generalizability and Transfer; Hierarchical Structure Prediction, Syntax, and Parsing; Human-AI
  Interaction/Cooperation and Human-Centric NLP; Information Extraction and Retrieval;
  Interpretability and Analysis of Models for NLP; Language Models; Linguistic theories, Cognitive
  Modeling and Psycholinguistics; LLM Efficiency; Low-resource Methods for NLP; Machine Learning for
  NLP; Machine Translation; Mathematical, Symbolic, Neurosymbolic, and Logical Reasoning;
  Multilinguality and Language Diversity; Multimodality and Language Grounding to Vision, Robotics
  and Beyond; Natural Language Generation; Phonology, Morphology and Word Segmentation; Question
  Answering; Resources and Evaluation; Retrieval-Augmented Language Models; Safety and Alignment in
  LLMs; Semantics: Lexical, Sentence-level Semantics, Textual Inference and Other areas; Sentiment
  Analysis, Stylistic Analysis, and Argument Mining; Special Theme: Explainability of NLP Models;
  Speech Processing and Spoken Language Understanding; Summarization. Of the other 5, four are
  rejected as `DOMAIN` and `AI/LLM Agents` is merged into Agentic Engineering
- FAMILY: both

### Neural and Evolutionary Computing (cs.NE)
- VERDICT: AREA
- WHY: the science of AI — connectionism, evolutionary computation and artificial life.
- MODE: science of AI; research in AI
- SOURCES: arXiv category taxonomy (index)
- ATTESTED BY: 1 — ARXIV
- COVERS: in the source's words, "neural networks, connectionism, genetic algorithms, artificial
  life, adaptive behavior"
- EXCLUDES: machine learning generally (Machine learning) — the category is cs.AI's sibling, not its
  child
- MERGED FROM: none
- BELOW: none. ACM CCS's `Neural networks` sits below Machine learning, by the level rule
- FAMILY: academic
- NOTE: the input records that arXiv is the only source giving evolutionary computation and
  artificial life a category at this level.

### neurosymbolic & hybrid AI systems
- VERDICT: AREA
- WHY: the science of AI — hybrid systems joining learning with logic and physics.
- MODE: science of AI; research in AI
- SOURCES: ICLR 2026 call (review-venue)
- ATTESTED BY: 1 — ICLR
- COVERS: by the source's parenthetical — physics-informed systems, logic and formal reasoning
- EXCLUDES: pure logical reasoning (KRR)
- MERGED FROM: none. ACL's `Mathematical, Symbolic, Neurosymbolic, and Logical Reasoning` sits below
  NLP and ACM CCS's `Logical and relational learning` below Machine learning, by the level rule
- BELOW: none
- FAMILY: academic

### Notebook Environment
- VERDICT: AREA
- WHY: the engineering of AI — its tools, which the rule names explicitly.
- MODE: engineering of AI (its tools)
- SOURCES: LF AI & Data landscape source file (practitioner)
- ATTESTED BY: 1 — LFAI
- COVERS: notebook environments as a category of open-source AI tooling
- EXCLUDES: programming languages and libraries (Programming)
- MERGED FROM: none
- BELOW: none
- FAMILY: applied
- NOTE: the input's own `SOURCE DISAGREES` line argues against it — "A notebook environment is a
  place work is done, not a subject work is about". That is the framing run's judgement, not the
  rule's; the rule says engineering includes its tools, so the category is kept and the objection
  is carried to `What this run could not settle`.

### Optimization
- VERDICT: AREA
- WHY: the science of AI — the optimization methods learning runs on.
- MODE: science of AI; research in AI
- SOURCES: NeurIPS 2026 call; ICLR 2026 call; ICML 2026 call (all review-venue)
- ATTESTED BY: 3 — NEURIPS, ICLR, ICML
- COVERS: convex and non-convex optimization, matrix and tensor methods, stochastic, online,
  non-smooth and composite optimization (ICML)
- EXCLUDES: constraint optimization (CSO); combinatorial search (SO)
- MERGED FROM: none beyond the framing run's merge of three identical labels
- BELOW: none. CVPR's `Optimization methods (other than deep learning)` sits below Computer vision
  and AAMAS's SOPS below Multiagent Systems, by the level rule
- FAMILY: academic

### Philosophy and Ethics of AI (PEAI)
- VERDICT: AREA
- WHY: the science of AI — its philosophical and theoretical foundations, and the ethics of the
  field itself.
- MODE: science of AI
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics (review-venue); AAAI-26 main technical track
  call (review-venue), as `Ethics`; ACM CCS 2012 via UCT and on the vocabulary server (index), as
  `Philosophical/theoretical foundations of artificial intelligence`
- ATTESTED BY: 5 — A26K, A27, A26M, UCT, CCSVS
- COVERS: philosophy and ethics of AI, across 12 AAAI-26 keywords and 12 AAAI-27 topics; CCS's
  philosophical and theoretical foundations, whose visible child is cognitive science
- EXCLUDES: alignment, which AAAI-26 gives a separate reviewed track (merged into Safety); and the
  model-property side of trust (trustworthy machine learning)
- MERGED FROM: Ethics (A26M) — its `ALSO CALLED` states that AAAI's own keywords page calls the area
  PEAI; Philosophical/theoretical foundations of artificial intelligence (UCT, CCSVS) — its `ALSO
  CALLED` names PEAI. The second merge joins a node that CCS keeps **without** ethics to an area that
  binds the two; listed in `What this run could not settle`
- BELOW: none
- FAMILY: academic

### Planning, Routing, and Scheduling (PRS)
- VERDICT: AREA
- WHY: the science of AI — planning, routing and scheduling.
- MODE: science of AI; research in AI
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics (review-venue); AAAI-26 main technical track
  call (review-venue), as `Planning`; IJCAI-ECAI 2026 via AEPIA (review-venue), as `Planning and
  Search`; ACM CCS 2012 on the vocabulary server (index), as `Planning and scheduling`
- ATTESTED BY: 5 — A26K, A27, A26M, IJCAI, CCSVS
- COVERS: planning, routing and scheduling, across AAAI-26's 18 keywords; CCS's planning and
  scheduling node; IJCAI's planning-and-search area
- EXCLUDES: search, which AAAI gives the separate area `Search and Optimization (SO)`
- MERGED FROM: Planning (A26M) — `ALSO CALLED` names PRS; Planning and scheduling (CCSVS) — `ALSO
  CALLED` names PRS; Planning and Search (IJCAI) — `ALSO CALLED` names PRS plus SO. **The IJCAI merge
  is imperfect**: that one area spans both PRS and SO, and this run put it here. Listed in `What this
  run could not settle`
- BELOW: none. AAMAS's SOPS sits below Multiagent Systems
- FAMILY: academic

### Posttraining & Midtraining
- VERDICT: AREA
- WHY: the engineering of AI — the training stages after pre-training.
- MODE: engineering of AI (its operation); research in AI
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: the training stages after pre-training — mid-training and post-training of models
- EXCLUDES: pre-training itself, which no source in the register names; inference (Inference)
- MERGED FROM: none
- BELOW: none
- FAMILY: applied
- NOTE: the input records that no index, review venue or standards body names a training stage as a
  category; MLPerf measures training as one thing.

### probabilistic methods
- VERDICT: AREA
- WHY: the science of AI — Bayesian and Monte Carlo method work.
- MODE: science of AI; research in AI
- SOURCES: NeurIPS 2026 call; ICLR 2026 call; ICML 2026 call (all review-venue)
- ATTESTED BY: 3 — NEURIPS, ICLR, ICML
- COVERS: Bayesian methods, variational inference, sampling and uncertainty quantification (ICLR);
  Bayesian methods, graphical models and Monte Carlo methods (ICML)
- EXCLUDES: reasoning under uncertainty as an AI area (Reasoning under Uncertainty (RU))
- MERGED FROM: none beyond the framing run's merge of three identical labels. **Not merged** with RU,
  although the records cross-name: the input says the dispute is precisely whether this is a method
  or a kind of reasoning, and merging would decide that dispute. Listed in `What this run could not
  settle`
- BELOW: none. ACM CCS's `Learning in probabilistic graphical models` sits below Machine learning
- FAMILY: academic

### Programming
- VERDICT: AREA
- WHY: the engineering of AI — its tools: the languages and libraries AI is written in.
- MODE: engineering of AI (its tools)
- SOURCES: LF AI & Data landscape source file (practitioner)
- ATTESTED BY: 1 — LFAI
- COVERS: programming languages and tools as a category of open-source AI projects
- EXCLUDES: notebooks (Notebook Environment)
- MERGED FROM: none
- BELOW: none. ACL's `Code Models` sits below NLP and the WF tracks about building software with AI
  are the kept area `Software Factories`
- FAMILY: applied

### Reasoning + RL
- VERDICT: AREA
- WHY: the science and engineering of AI — reasoning models and the reinforcement learning that
  trains them.
- MODE: science of AI; engineering of AI (its operation)
- SOURCES: WF25 (programme)
- ATTESTED BY: 1 — WF25
- COVERS: reasoning models and the reinforcement learning used to train them
- EXCLUDES: the 2026 programme carries no track of this name; its nearest is `Posttraining &
  Midtraining`
- MERGED FROM: none. The same page names the track two ways, "Reasoning + RL" and "RL+Reasoning";
  the framing run recorded that and so does this one
- BELOW: none
- FAMILY: applied
- NOTE: the input records that no review venue binds reasoning to reinforcement learning in one
  category. Whether this is one area or two is in `What this run could not settle`.

### Reasoning under Uncertainty (RU)
- VERDICT: AREA
- WHY: the science of AI — reasoning when the facts are uncertain.
- MODE: science of AI; research in AI
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics (review-venue); IJCAI-ECAI 2026 via AEPIA
  (review-venue), as `Uncertainty in AI`
- ATTESTED BY: 3 — A26K, A27, IJCAI
- COVERS: reasoning under uncertainty, across AAAI-26's 11 keywords
- EXCLUDES: knowledge representation and deterministic reasoning (KRR)
- MERGED FROM: Uncertainty in AI (IJCAI) — its `ALSO CALLED` names AAAI's RU
- BELOW: none. The method side is the kept area `probabilistic methods`; ACM CCS's
  `Partially-observable Markov decision processes` sits below Machine learning
- FAMILY: academic
- NOTE: arXiv names the phrase "Uncertainty in AI" as something **inside** cs.AI; the input records
  that disagreement and this run does not resolve it.

### reinforcement learning
- VERDICT: AREA
- WHY: the science of AI — learning by acting, and the control and decision-making around it.
- MODE: science of AI; research in AI; engineering of AI (its tools)
- SOURCES: ICLR 2026 call; ICML 2026 call (review-venue); LF AI & Data landscape (practitioner);
  NeurIPS 2026 call (review-venue), as `Decision-making, reinforcement learning, and control`
- ATTESTED BY: 4 — ICLR, ICML, LFAI, NEURIPS
- COVERS: decision and control, planning, hierarchical RL and robotics inside it (ICML); sequential
  decision making, reinforcement learning and control in one topic (NeurIPS); one LF AI & Data
  category of tooling
- EXCLUDES: robotics as such, which NeurIPS names separately and which is the kept area Intelligent
  Robotics
- MERGED FROM: Decision-making, reinforcement learning, and control (NeurIPS) — its `ALSO CALLED`
  states that "ICLR and ICML both name 'reinforcement learning' alone"
- BELOW: none. ACM CCS's `Markov decision processes`, `Partially-observable Markov decision
  processes` and `Stochastic games` sit below Machine learning, where CCS puts them
- FAMILY: both

### representation learning for computer vision, audio, language, and other modalities
- VERDICT: AREA
- WHY: the science of AI — representation learning across modalities.
- MODE: science of AI; research in AI
- SOURCES: ICLR 2026 call (review-venue)
- ATTESTED BY: 1 — ICLR
- COVERS: representation learning across the named modalities — vision, audio, language and others
- EXCLUDES: the supervision regimes, which ICLR names in a separate topic (its own kept area)
- MERGED FROM: none
- BELOW: none. CVPR's `Representation learning` sits below Computer vision and ACM CCS's `Learning
  latent representations` below Machine learning
- FAMILY: academic
- NOTE: the input records that ICLR has no vision, NLP or audio area at all and files all three as
  modalities of representation learning — a carving no other source uses.

### Safety
- VERDICT: AREA
- WHY: the engineering of AI — its measurement and operation: whether a model's outputs are safe,
  and whether a system remains under oversight.
- MODE: engineering of AI (its measurement and its operation); research in AI
- SOURCES: MLCommons benchmarks index (practitioner); AAAI-26 main technical track call
  (review-venue), as `Special Track on AI Alignment`
- ATTESTED BY: 2 — MLC, A26M
- COVERS: safety of AI systems as a risk-and-reliability working group (MLC); and, from the AAAI
  track, "scalable oversight, mechanistic interpretability, empirical robustness evaluation,
  red-teaming, human cognitive and psychological factors, and safe-by-design engineering—including
  formal safety cases", plus transparent governance frameworks, economic incentives, institutional
  accountability, human-centered modeling and evaluation, and pluralistic coordination methods
- EXCLUDES: functional safety in a controlled process (Functional safety and AI systems) — the input
  states the two senses share a word and not a subject; security (Security)
- MERGED FROM: Special Track on AI Alignment (A26M) — its `ALSO CALLED` names ACL's `Safety and
  Alignment in LLMs` and MLCommons' `Safety` working group. **This merge folds alignment into
  safety**, which three of the register's sources do and AAAI's rubric does not. Listed in `What this
  run could not settle`
- BELOW: none here. ACL's `Safety and Alignment in LLMs` sits below NLP and MLCommons' AILuminate
  below Evals, by the level rule
- FAMILY: both

### Sandbox & Platform Engineering
- VERDICT: AREA
- WHY: the engineering of AI — its tools: the sandboxes and platform layer AI code runs inside.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme)
- ATTESTED BY: 1 — WF26
- COVERS: sandboxes and the platform layer that AI code runs inside
- EXCLUDES: serving performance (Inference); the agent-side scaffolding (Harness Engineering)
- MERGED FROM: none. Its `ALSO CALLED` names WF25 `AI Infrastructure`, MLCommons `Infra` and ICML
  `machine learning systems`, all merged into the kept area AI Infrastructure; this run kept the
  sandbox category separate because the input states "code isolation is not a category anywhere else
  in the register". Listed in `What this run could not settle`
- BELOW: none
- FAMILY: applied

### Search & Retrieval
- VERDICT: AREA
- WHY: the engineering of AI — its tools: retrieving what a model needs from internal and external
  sources.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme); WF25 (programme), as `Retrieval + Search`
- ATTESTED BY: 2 — WF26, WF25
- COVERS: search and retrieval for AI applications; in WF25's own words, "top-k embedding and
  retrieval from internal data, and agentic search from external web and docs"
- EXCLUDES: graph-structured retrieval (Graphs); context assembly (Context Engineering)
- MERGED FROM: Retrieval + Search (WF25) — each record's `ALSO CALLED` names the other as the same
  event's other-year label. The framing run declined the merge because the word order and separator
  differ and the 2025 page states a scope the 2026 page does not. Listed in `What this run could not
  settle`
- BELOW: none. ACL's `Information Extraction and Retrieval` and `Retrieval-Augmented Language
  Models` sit below NLP
- FAMILY: applied
- NOTE: WF25 states in prose that the organisers "killed the lazy 'RAG track' everyone does" — the
  one place in the register where a source rejects a peer's category by name.

### Search and Optimization (SO)
- VERDICT: AREA
- WHY: the science of AI — combinatorial search and the optimization bound to it.
- MODE: science of AI; research in AI
- SOURCES: AAAI-26 keywords; AAAI-27 areas and topics (review-venue); AAAI-26 main technical track
  call (review-venue), as `Search`; ACM CCS 2012 on the vocabulary server (index), as `Search
  methodologies`
- ATTESTED BY: 4 — A26K, A27, A26M, CCSVS
- COVERS: search and optimization across AAAI-26's 15 keywords; CCS's search-methodologies node
- EXCLUDES: constraints and satisfiability (CSO); planning (PRS)
- MERGED FROM: Search (A26M) — `ALSO CALLED` names SO; Search methodologies (CCSVS) — `ALSO CALLED`
  names SO
- BELOW: none. AAMAS's SOPS sits below Multiagent Systems
- FAMILY: academic

### Security
- VERDICT: AREA
- WHY: the engineering of AI — its operation: the security of AI systems.
- MODE: engineering of AI (its operation and its measurement)
- SOURCES: MLCommons benchmarks index (practitioner); WF26 (programme); WF25 (programme); LF AI &
  Data landscape (practitioner), as `Security & Privacy`
- ATTESTED BY: 4 — MLC, WF26, WF25, LFAI
- COVERS: the security of AI systems, as a working group at MLCommons and a track at both
  programmes; security and privacy tooling as open-source projects (LF AI & Data)
- EXCLUDES: privacy where a source separates it — MLCommons gives privacy its own working group,
  filed below trustworthy machine learning
- MERGED FROM: Security & Privacy (LFAI) — its `ALSO CALLED` states that MLCommons splits the same
  ground into `Security` and `Privacy and Confidentiality`. **The merge pulls privacy in with
  security**; listed in `What this run could not settle`
- BELOW: none. CVPR's `Adversarial attack and defense` sits below Computer vision
- FAMILY: applied
- NOTE: the input records that no review venue has a security area; AAAI holds security only as an
  application keyword and arXiv's cs.CR is outside the register's branch.

### Software Factories
- VERDICT: AREA
- WHY: the engineering of AI — building software at scale with AI, and the agents that do it.
- MODE: engineering of AI (its tools and its operation)
- SOURCES: WF26 (programme); WF25 (programme), as `SWE Agents`
- ATTESTED BY: 2 — WF26, WF25
- COVERS: building software at scale with AI; agents that do software-engineering work
- EXCLUDES: the models of code themselves (ACL's `Code Models`, below NLP)
- MERGED FROM: SWE Agents (WF25) — the `Software Factories` record states "the 2025 edition named
  the agents; the 2026 edition names the factory. Same subject, a different unit of account"
- BELOW: none
- FAMILY: applied
- NOTE: a close call against `DOMAIN` — software engineering is a neighbouring discipline. Kept
  because the work is the building and operating of AI systems that write software, which the rule's
  engineering clause covers. Listed in `What this run could not settle`.

### theory of machine learning
- VERDICT: AREA
- WHY: the science of AI — the theory under learning.
- MODE: science of AI
- SOURCES: ICML 2026 call (review-venue); ICLR 2026 call (review-venue), as `learning theory`;
  NeurIPS 2026 call (review-venue), as `Theory`
- ATTESTED BY: 3 — ICML, ICLR, NEURIPS
- COVERS: in ICML's words, "statistical learning theory, bandits, game theory, decision theory, etc."
- EXCLUDES: evaluation methodology (Evals); vision theory (CVPR's `Computer vision theory`, below
  Computer vision)
- MERGED FROM: learning theory (ICLR) and Theory (NeurIPS) — both records' `ALSO CALLED` name the
  other two. **The kept name is ICML's because it is the only one of the three that states a scope**:
  NeurIPS's `Theory` is one word with no stated scope, and the input says whether it is narrower,
  wider or the same "cannot be read from the page". If the owner splits this merge, NeurIPS's
  `Theory` becomes `UNCLEAR`. Listed in `What this run could not settle`
- BELOW: none
- FAMILY: academic

### trustworthy machine learning
- VERDICT: AREA
- WHY: the research in AI, and its engineering — the trust properties of models and the standards
  that hold them.
- MODE: research in AI; engineering of AI (its measurement and its operation)
- SOURCES: ICML 2026 call (review-venue); IJCAI-ECAI 2026 via AEPIA (review-venue), as `Fairness,
  Ethics, and Trust`; ICLR 2026 call (review-venue), as `societal considerations including fairness,
  safety, privacy`; NeurIPS 2026 call (review-venue), as `Socio-technical aspects of AI`; LF AI &
  Data landscape (practitioner), as `Trusted & Responsible AI`; ISO/IEC JTC 1/SC 42 WG 3
  (practitioner), as `Trustworthiness`
- ATTESTED BY: 6 — ICML, IJCAI, ICLR, NEURIPS, LFAI, SC42
- COVERS: in ICML's words, "reliability, causality, fairness, interpretability, privacy, robustness,
  safety"; fairness, ethics and trust (IJCAI); explainability, adversarial robustness, bias and
  fairness (LF AI & Data's 3 subcategories); standardisation of trustworthiness (SC 42); the
  socio-technical study of AI systems (NeurIPS)
- EXCLUDES: evaluation methodology (Evals); the philosophy of AI (PEAI); functional safety
  (Functional safety and AI systems)
- MERGED FROM: Fairness, Ethics, and Trust; societal considerations including fairness, safety,
  privacy; Socio-technical aspects of AI; Trusted & Responsible AI; Trustworthiness — every one of
  these records names two or more of the others in `ALSO CALLED`, and the input's own
  `Fairness, Ethics, and Trust` record says "six sources carve the same ground six ways". **This is
  the largest merge in this run and the least settled**: the six are not agreed on whether trust is
  a property, a subject, a perspective or a standards stream, and `Socio-technical aspects of AI` may
  belong under `RECORD` instead. Listed in `What this run could not settle`
- BELOW: Privacy and Confidentiality (MLCommons working group)
- FAMILY: both

### unsupervised, self-supervised, semi-supervised, and supervised representation learning
- VERDICT: AREA
- WHY: the science of AI — representation learning under each supervision regime.
- MODE: science of AI; research in AI
- SOURCES: ICLR 2026 call (review-venue), listed first in its non-exhaustive list
- ATTESTED BY: 1 — ICLR
- COVERS: representation learning under all four supervision regimes, supervised included
- EXCLUDES: modality-specific representation learning (ICLR's other representation-learning topic,
  its own kept area)
- MERGED FROM: none. **Not merged** with CVPR's `Self-, semi-, meta- and unsupervised learning`: the
  input records that CVPR's list omits supervised learning and adds meta-learning
- BELOW: none
- FAMILY: academic

### visualization or interpretation of learned representations
- VERDICT: AREA
- WHY: the science of AI — reading what a model has learned.
- MODE: science of AI; engineering of AI (its measurement)
- SOURCES: ICLR 2026 call (review-venue)
- ATTESTED BY: 1 — ICLR
- COVERS: visualizing or interpreting what a model has learned
- EXCLUDES: societal considerations (trustworthy machine learning)
- MERGED FROM: none. CVPR's `Explainable computer vision`, ACL's `Interpretability and Analysis of
  Models for NLP` and ACL's explainability theme track all sit below their modality's area, by the
  level rule; the input records that ICLR frames the subject as representations and ACL and CVPR as
  models, "Representation or model is the boundary in dispute"
- BELOW: none
- FAMILY: academic

### Voice & Realtime AI
- VERDICT: AREA
- WHY: the engineering of AI — voice interfaces and realtime systems in operation.
- MODE: engineering of AI (its operation and its tools)
- SOURCES: WF26 (programme); WF25 (programme), as `Voice`
- ATTESTED BY: 2 — WF26, WF25
- COVERS: voice interfaces together with realtime AI; voice AI as an engineering practice (WF25)
- EXCLUDES: batch and offline serving (Inference); speech research (Audio and Speech Processing
  (AUD), and ACL's speech topic below NLP)
- MERGED FROM: Voice (WF25) — each record names the other as the same event's other-year label. The
  framing run declined the merge because the 2026 name adds realtime AI, "which is not voice".
  Listed in `What this run could not settle`
- BELOW: none
- FAMILY: applied
- NOTE: the input records that "realtime" appears as a category word in no other source.

## Rejected

Every rejection cites the clause of the rule it fails. **No category is rejected for being small,
quiet, unfashionable or not worth covering.** Where a rejection was close, it is named again in
`What this run could not settle`.

### DOMAIN — ordinary AI pointed at another field's data (36)

Clause failed: "Drop it if it belongs to none of the three … AI applied to another field's problems."

| Name | Source | What the record shows |
|---|---|---|
| AI and network science | NEURIPS | network-science methods and subjects met with AI — another field's subject. **Close** |
| AI enabled health informatics | SC42 | standardisation of AI used in health informatics |
| AI in Finance | WF26 | AI applied in financial firms and products |
| AI in GTM | WF26 | AI in sales, marketing and revenue operations |
| AI in Healthcare | WF26 | AI systems built for clinical and healthcare use |
| AI/ML for creatives | NEURIPS | AI and ML serving creative practice |
| AI/ML for health and biotechnology | NEURIPS | AI and ML applied to health and biotechnology |
| AI/ML for physical sciences | NEURIPS | AI and ML for the physical sciences |
| AI/ML for social sciences | NEURIPS | AI and ML for the social sciences |
| AI/ML for sustainability | NEURIPS | AI and ML for sustainability |
| Application Domains (APP) | A26K, A27 | a container of application domains — humanities, IoT, mobility, natural sciences, transportation, web |
| application-driven machine learning | ICML | techniques "driven by the needs of end-users in applications such as healthcare, physical sciences, biosciences, social sciences, sustainability, and climate" |
| applications to neuroscience & cognitive science | ICLR | "representation-learning work **applied to** neuroscience and cognitive science". **Close** — NeurIPS's differently worded record is kept, below CMS |
| applications to physical sciences | ICLR | physics, chemistry and biology as named by the source |
| Autonomous driving | CVPR | vision and perception for self-driving — a transport sector. **Close**: a CVPR subject area, and perception for autonomy is core AI research |
| Clinical and Biomedical Applications | ACL | language technology for clinical and biomedical use |
| Computational Social Science, Cultural Analytics, and NLP for Social Good | ACL | computational social science, cultural analytics, NLP for social benefit |
| Computer graphics | UCT, CCSVS | animation, rendering, shape modeling — a neighbouring field, and in CCS a **sibling** of Artificial intelligence, not AI work. **Close**, and the verdict label fits badly |
| Computer vision for social good | CVPR | vision work aimed at social benefit |
| Concurrent computing methodologies | UCT, CCSVS | concurrency as a computing methodology — a CCS sibling of AI, not AI. **Close**, label fits badly |
| Distributed computing methodologies | CCSVS | distributed computing as a computing methodology — a CCS sibling of AI. **Close**, label fits badly |
| Financial Applications and Time Series | ACL | financial applications of language technology |
| Financial Services | MLC | risk and reliability work for AI in financial services |
| Innovative Applications (IA) | AAMAS | applications of agent and multi-agent technology |
| Medical AI | MLC | the medical-AI working group |
| Medical and biological vision, cell microscopy | CVPR | medical and biological imaging, cell microscopy. **Close**: a CVPR subject area |
| Modeling and simulation | UCT, CCSVS | modeling methodologies, simulation techniques, molecular and quantum simulation — a CCS sibling of AI. **Close**, label fits badly |
| Modeling and Simulation of Societies (SIM) | AAMAS | agent-based modelling and simulation of societies. **Close**: an AAMAS area of interest |
| Multidisciplinary Topics | IJCAI | "work that crosses disciplines" — IJCAI's residual for applications. **Close**: it is a residual, and a residual can hold method work too |
| NLP Applications | ACL | applications of language technology not covered by the named topics |
| Parallel computing methodologies | UCT, CCSVS | parallelism as a computing methodology — a CCS sibling of AI. **Close**, label fits badly |
| Photogrammetry and remote sensing | CVPR | photogrammetry and remote sensing. **Close**: a CVPR subject area |
| Science | — | see `Unclear`; not counted here |
| Special Track on AI for Social Impact | A26M | work judged on "the fit between the techniques used and a problem of social importance". **Close**: it is also a review format, so `FORMAT` would fit too |
| Symbolic and algebraic manipulation | CCSVS | symbolic and algebraic manipulation as a computing methodology — a CCS sibling of AI. **Close**, label fits badly |
| Use cases and applications | SC42 | the collection and standardisation of AI use cases and applications |
| Vision applications and systems | CVPR | applications and systems built from vision — CVPR's residual applications bucket. **Close** |

(The `Science` row is a cross-reference only; the 36 counted rejections are the other rows.)

### RECORD — about AI's effect on the world rather than about AI (0)

None. Two records came close and were **not** rejected: `Socio-technical aspects of AI` (NeurIPS),
which was merged into trustworthy machine learning, and `AI in the Fortune 500` (WF25), which was
rejected as `FORMAT` on the company-size clause instead. Both are in `What this run could not
settle`.

### FORMAT — a session shape, a track slot, an audience, a company size, a working arrangement (9)

| Name | Source | Clause failed |
|---|---|---|
| AI Architects | WF25 | "an audience" — "sessions for senior technical leaders, gated behind the AI Leadership pass"; the page states the track seats 300 |
| AI Architects: Show my Workflow | WF26 | "a session shape" — "practitioners demonstrating their own working process" |
| AI in the Fortune 500 | WF25 | "a company size" — AI adoption inside very large incumbent companies |
| AI-Native Enterprises | WF26 | "a working arrangement" — companies built around AI from the start, and the practice of running them. **Close** |
| Forward Deployed Engineering | WF26 | "a working arrangement" — engineers deployed with customers to build AI systems in place; a delivery model. **Close** |
| Hosting Companies | LFAI | "an organisation" — the organisations that host projects in the landscape; the input itself calls it an organisational category, not a technical one |
| LF AI & Data Member Company | LFAI | "an organisation" — member companies by membership tier |
| Product Management | WF25 | belongs to none of the three — a job function, not the science, research or engineering of AI. **Close** |
| Tiny Teams | WF25 | "a company size" — the input calls it "the only registered category defined by the size of the organisation doing the work" |

### PRODUCT — one organisation's branded suite or tool (0)

None, by the rule's instruction that a product or tool name is not dropped but reported as the
engineering area it instances. The products so reported, with the area each instances:

| Product name | Reported as | Filed |
|---|---|---|
| AILuminate | safety measurement of general chatbot AI systems | below Evals |
| AlgoPerf: Training Algorithms | measurement of training algorithms | below Evals |
| MLPerf Automotive / Client / Endpoints / Inference (+ Datacenter, Edge, Mobile, Tiny) / Storage / Tiny / Training / Training: HPC | speed, power and storage measurement of AI systems | below Evals |
| MCP | the harness interface an agent runs against | below Harness Engineering |

## Merged

47 names were folded into a kept area. Each row gives the kept name, the name merged into it, and
the evidence from the records.

| Kept name | Merged in | Evidence |
|---|---|---|
| Agentic Engineering | AI/LLM Agents | the ACL record's `ALSO CALLED` names WF26 "Agentic Engineering" |
| AI Infrastructure | Infra | `ALSO CALLED` names WF25 "AI Infrastructure" and NeurIPS "SysML Infrastructure" |
| AI Infrastructure | infrastructure, software libraries, hardware, etc. | `ALSO CALLED` names ICML, NeurIPS and MLCommons' names for the same ground |
| AI Infrastructure | machine learning systems | `ALSO CALLED` names SysML Infrastructure, ICLR's topic, Infra and AI Infrastructure |
| AI Infrastructure | SysML Infrastructure | `ALSO CALLED` names the other four |
| Constraint Satisfaction and Optimization (CSO) | Constraints and Satisfiability | `ALSO CALLED` names AAAI's CSO |
| Data Mining & Knowledge Management (DMKM) | Data Mining | the record states AAAI's keywords page "calls the same ground" DMKM |
| Data-centric aspects of AI | Data Quality | `ALSO CALLED` names the NeurIPS topic and MLCommons' group |
| Data-centric aspects of AI | Data-centric ML | `ALSO CALLED` names the NeurIPS topic |
| datasets and benchmarks | Datasets | `ALSO CALLED` names ICLR's "datasets and benchmarks" |
| Evals | evaluation | `ALSO CALLED` names "Evals" |
| Evals | Testing of AI-based systems | `ALSO CALLED` names ICML "evaluation", WF "Evals" and MLCommons "AILuminate" |
| Generalization and multi-task learning | transfer learning, meta learning, and lifelong learning | the two records name each other in `ALSO CALLED`. **Thin** |
| generative models | Generative AI | `ALSO CALLED` names ICLR "generative models", reciprocally |
| Graphs | GraphRAG | the Graphs record: the 2025 edition "named the same track 'GraphRAG'" |
| Humans and AI (HAI) | Human interaction in AI systems | `ALSO CALLED` names AAAI's "Humans and AI (HAI)" |
| Humans and AI (HAI) | human-in-the-loop AI | the record states AAAI's keywords page holds it as one keyword **inside** HAI |
| Intelligent Robotics | Robotics (cs.RO) | `ALSO CALLED` names "Intelligent Robotics" |
| Intelligent Robotics | Robotics and Control (ROBOT) | `ALSO CALLED` names "Intelligent Robotics" and cs.RO |
| Intelligent Robotics | Robotics, embodied systems, and engineering | `ALSO CALLED` names "Intelligent Robotics", cs.RO and ROBOT |
| Intelligent Robotics | applications to robotics, autonomy, planning | `ALSO CALLED` names the NeurIPS and AAMAS robotics areas; `EXCLUDES` points to "Intelligent Robotics" |
| Intelligent Robotics | Autonomy + Robotics | `EXCLUDES` names "research-side robotics … Intelligent Robotics" |
| Intelligent Robotics | Robotics & World Models | `ALSO CALLED` names WF25's robotics track; `OVERLAPS` names Intelligent Robotics and cs.RO. **Carries "world models", which no other source names** |
| Intelligent Robotics | robotics and perception | `ALSO CALLED` names AAAI's own "Intelligent Robotics (ROB)" |
| Knowledge Representation and Reasoning (KRR) | Knowledge representation | `ALSO CALLED`: AAAI's keywords page, CCS, IJCAI and arXiv all use the longer name. **Undoes an AAAI-26 prose split** |
| Knowledge Representation and Reasoning (KRR) | Reasoning | `ALSO CALLED`: AAAI's keywords page has no bare Reasoning area, "only KRR and RU". **Undoes the same split** |
| Philosophy and Ethics of AI (PEAI) | Ethics | `ALSO CALLED`: AAAI's keywords page "calls the area" PEAI |
| Philosophy and Ethics of AI (PEAI) | Philosophical/theoretical foundations of artificial intelligence | `ALSO CALLED` names PEAI. **CCS keeps the node without ethics; AAAI binds the two** |
| Planning, Routing, and Scheduling (PRS) | Planning | `ALSO CALLED`: AAAI's keywords page says PRS |
| Planning, Routing, and Scheduling (PRS) | Planning and scheduling | `ALSO CALLED` names PRS |
| Planning, Routing, and Scheduling (PRS) | Planning and Search | `ALSO CALLED` names PRS **plus** SO; the merge is imperfect |
| reinforcement learning | Decision-making, reinforcement learning, and control | `ALSO CALLED`: "ICLR and ICML both name 'reinforcement learning' alone" |
| Reasoning under Uncertainty (RU) | Uncertainty in AI | `ALSO CALLED` names AAAI's RU |
| Safety | Special Track on AI Alignment | `ALSO CALLED` names ACL's safety-and-alignment topic and MLCommons' Safety group. **Folds alignment into safety** |
| Search & Retrieval | Retrieval + Search | each record names the other as the same event's other-year label |
| Search and Optimization (SO) | Search | `ALSO CALLED`: AAAI's keywords page says SO |
| Search and Optimization (SO) | Search methodologies | `ALSO CALLED` names SO |
| Security | Security & Privacy | `ALSO CALLED`: MLCommons splits the same ground into Security and Privacy and Confidentiality. **Pulls privacy in** |
| Software Factories | SWE Agents | `ALSO CALLED` names Software Factories as the 2026 label for the same ground |
| theory of machine learning | learning theory | `ALSO CALLED` names ICML's and NeurIPS's names |
| theory of machine learning | Theory | `ALSO CALLED` names ICLR's and ICML's names. **NeurIPS's record states no scope**, so this merge supplies one |
| trustworthy machine learning | Fairness, Ethics, and Trust | `ALSO CALLED` names ICML, LF AI & Data and SC 42 |
| trustworthy machine learning | societal considerations including fairness, safety, privacy | `ALSO CALLED` names ICML "trustworthy machine learning" |
| trustworthy machine learning | Socio-technical aspects of AI | `ALSO CALLED` names ICML "trustworthy machine learning" and ICLR's topic. **Thin, and may be `RECORD`** |
| trustworthy machine learning | Trusted & Responsible AI | `ALSO CALLED` names ICML "trustworthy machine learning" |
| trustworthy machine learning | Trustworthiness | `ALSO CALLED` names ICML "trustworthy machine learning" and LF AI & Data |
| Voice & Realtime AI | Voice | each record names the other as the same event's other-year label |

## Unclear

Five records do not settle their own case. **A record that carries no scope cannot be an `AREA`.**
These go to the owner undecided.

| Name | Source | Why it is unclear | What would settle it |
|---|---|---|---|
| Chakra | MLC | `INCLUDES` reads "the named working group; the page gives no description of its scope"; `EXCLUDES` reads "unclear from this page"; `OVERLAPS` none found | a scope statement from MLCommons for the Chakra working group |
| Croissant | MLC | `INCLUDES` reads "the named working group; the page gives no scope description" | a scope statement from MLCommons for the Croissant working group |
| Emerging Trends in AI Track | A26M | `INCLUDES` reads "not stated on this page"; the page's own Summary counts three technical tracks and does not count this one | a scope statement from AAAI for the track, and whether it is a technical track at all |
| MLCube | MLC | `INCLUDES` reads "the named working group"; the only other fact recorded is that MLCube is a registered trademark | a scope statement from MLCommons for the MLCube working group |
| Science | MLC | `INCLUDES` reads "the science working group, filed by MLCommons under Research" — the name restated. Its `ALSO CALLED` points at two `DOMAIN` categories, which would make it a rejection, but rejecting on a record this thin would take the decision from the owner | a scope statement from MLCommons: whether the group does AI **for** the sciences (then `DOMAIN`) or the science **of** AI measurement (then `AREA`) |

## Verdict ledger — all 283 input categories, one verdict each

In input order (the input is alphabetical). `Disposition` says where the category went: `kept` (a
unit in `## Areas`), `merged → X`, `below X`, or the clause it failed.

| # | Category | Verdict | Disposition |
|---|---|---|---|
| 1 | 3D from multi-view and sensors | AREA | below Computer vision |
| 2 | 3D from single images | AREA | below Computer vision |
| 3 | Adversarial attack and defense | AREA | below Computer vision |
| 4 | Agent Reliability | AREA | below Agentic Engineering |
| 5 | Agentic Commerce | AREA | below Agentic Engineering |
| 6 | Agentic Engineering | AREA | kept |
| 7 | AI Architects | FORMAT | an audience |
| 8 | AI Architects: AI Factories | AREA | below AI Infrastructure |
| 9 | AI Architects: Show my Workflow | FORMAT | a session shape |
| 10 | AI Architects: Tokenmaxxing | AREA | below Inference |
| 11 | AI and network science | DOMAIN | AI applied to another field's problems |
| 12 | AI enabled health informatics | DOMAIN | AI applied to another field's problems |
| 13 | AI in Finance | DOMAIN | AI applied to another field's problems |
| 14 | AI in GTM | DOMAIN | AI applied to another field's problems |
| 15 | AI in Healthcare | DOMAIN | AI applied to another field's problems |
| 16 | AI in the Fortune 500 | FORMAT | a company size |
| 17 | AI Infrastructure | AREA | kept |
| 18 | AI Risk & Reliability | AREA | below Evals |
| 19 | AI-Native Enterprises | FORMAT | a working arrangement |
| 20 | AI/LLM Agents | AREA | merged → Agentic Engineering |
| 21 | AI/ML for creatives | DOMAIN | AI applied to another field's problems |
| 22 | AI/ML for health and biotechnology | DOMAIN | AI applied to another field's problems |
| 23 | AI/ML for physical sciences | DOMAIN | AI applied to another field's problems |
| 24 | AI/ML for social sciences | DOMAIN | AI applied to another field's problems |
| 25 | AI/ML for sustainability | DOMAIN | AI applied to another field's problems |
| 26 | AILuminate | AREA | below Evals (product as evidence) |
| 27 | AlgoPerf: Training Algorithms | AREA | below Evals (product as evidence) |
| 28 | Algorithms | AREA | below Evals |
| 29 | Application Domains (APP) | DOMAIN | AI applied to another field's problems |
| 30 | application-driven machine learning | DOMAIN | AI applied to another field's problems |
| 31 | applications to neuroscience & cognitive science | DOMAIN | AI applied to another field's problems |
| 32 | applications to physical sciences | DOMAIN | AI applied to another field's problems |
| 33 | applications to robotics, autonomy, planning | AREA | merged → Intelligent Robotics |
| 34 | Artificial intelligence (ACM CCS) | AREA | kept (umbrella, above the level) |
| 35 | Artificial Intelligence (cs.AI) | AREA | kept (residual) |
| 36 | Audio | AREA | below Evals (MLPerf Area) |
| 37 | Audio and Speech Processing (AUD) | AREA | kept |
| 38 | Automotive | AREA | below Evals (MLPerf Area) |
| 39 | Autonomous driving | DOMAIN | AI applied to another field's problems |
| 40 | Autonomy + Robotics | AREA | merged → Intelligent Robotics |
| 41 | Autoresearch | AREA | below Agentic Engineering |
| 42 | Big Data | AREA | below Data |
| 43 | Biometrics | AREA | below Computer vision |
| 44 | causal reasoning | AREA | kept |
| 45 | Chakra | UNCLEAR | no scope in the record |
| 46 | Classification and regression trees | AREA | below Machine learning |
| 47 | Claws & Personal Agents | AREA | below Agentic Engineering |
| 48 | Clinical and Biomedical Applications | DOMAIN | AI applied to another field's problems |
| 49 | Code Models | AREA | below Natural Language Processing |
| 50 | Cognitive Modeling & Cognitive Systems (CMS) | AREA | kept |
| 51 | Commerce | AREA | below Evals (MLPerf Area) |
| 52 | Computational approaches and characteristics of artificial intelligence systems | AREA | kept |
| 53 | Computational imaging | AREA | below Computer vision |
| 54 | Computational Social Science, Cultural Analytics, and NLP for Social Good | DOMAIN | AI applied to another field's problems |
| 55 | Computer graphics | DOMAIN | belongs to none of the three — a neighbouring field |
| 56 | Computer Use | AREA | below Agentic Engineering |
| 57 | Computer vision | AREA | kept |
| 58 | Computer vision for social good | DOMAIN | AI applied to another field's problems |
| 59 | Computer Vision for Robotics | AREA | below Computer vision |
| 60 | Computer vision theory | AREA | below Computer vision |
| 61 | Concurrent computing methodologies | DOMAIN | belongs to none of the three — a neighbouring field |
| 62 | Constraint Satisfaction and Optimization (CSO) | AREA | kept |
| 63 | Constraints and Satisfiability | AREA | merged → CSO |
| 64 | Context Engineering | AREA | kept |
| 65 | Control methods | AREA | below Intelligent Robotics |
| 66 | Coordination, Organizations, Institutions, Norms, and Ethics (COINE) | AREA | below Multiagent Systems |
| 67 | Croissant | UNCLEAR | no scope in the record |
| 68 | Data | AREA | kept |
| 69 | Data Mining | AREA | merged → DMKM |
| 70 | Data Mining & Knowledge Management (DMKM) | AREA | kept |
| 71 | Data Quality | AREA | merged → Data-centric aspects of AI |
| 72 | Data-centric aspects of AI | AREA | kept |
| 73 | Data-centric ML | AREA | merged → Data-centric aspects of AI |
| 74 | Datasets | AREA | merged → datasets and benchmarks |
| 75 | datasets and benchmarks | AREA | kept |
| 76 | Datasets and evaluation | AREA | below Computer vision |
| 77 | Decision-making, reinforcement learning, and control | AREA | merged → reinforcement learning |
| 78 | Deep learning | AREA | kept |
| 79 | Deep learning architectures and techniques | AREA | below Computer vision |
| 80 | Design Engineering | AREA | kept |
| 81 | Dialogue and Interactive Systems | AREA | below Natural Language Processing |
| 82 | Discourse, Pragmatics, and Reasoning | AREA | below Natural Language Processing |
| 83 | Distributed artificial intelligence | AREA | below Multiagent Systems |
| 84 | Distributed computing methodologies | DOMAIN | belongs to none of the three — a neighbouring field |
| 85 | Distributed Computing | AREA | below AI Infrastructure |
| 86 | Document analysis and understanding | AREA | below Computer vision |
| 87 | Efficient and scalable vision | AREA | below Computer vision |
| 88 | Embodied vision: Active agents, simulation | AREA | below Computer vision |
| 89 | Emerging Trends in AI Track | UNCLEAR | no scope in the record |
| 90 | Engineering and Analysis of Multiagent Systems (EMAS) | AREA | below Multiagent Systems |
| 91 | Ethics | AREA | merged → PEAI |
| 92 | Ethics, Bias, and Fairness | AREA | below Natural Language Processing |
| 93 | evaluation | AREA | merged → Evals |
| 94 | Evals | AREA | kept |
| 95 | Event-based cameras | AREA | below Computer vision |
| 96 | Explainable computer vision | AREA | below Computer vision |
| 97 | Factorization methods | AREA | below Machine learning |
| 98 | Fairness, Ethics, and Trust | AREA | merged → trustworthy machine learning |
| 99 | Financial Applications and Time Series | DOMAIN | AI applied to another field's problems |
| 100 | Financial Services | DOMAIN | AI applied to another field's problems |
| 101 | Forward Deployed Engineering | FORMAT | a working arrangement |
| 102 | Foundational standards | AREA | kept |
| 103 | Functional safety and AI systems | AREA | kept |
| 104 | Game Theory and Economic Paradigms (GTEP) | AREA | kept |
| 105 | general machine learning | AREA | kept |
| 106 | Generalizability and Transfer | AREA | below Natural Language Processing |
| 107 | Generalization and multi-task learning | AREA | kept |
| 108 | Generative | AREA | below Evals (MLPerf Area) |
| 109 | Generative AI | AREA | merged → generative models |
| 110 | Generative and Agentic AI (GAAI) | AREA | below Agentic Engineering |
| 111 | generative models | AREA | kept |
| 112 | Generative Media | AREA | kept |
| 113 | Graph | AREA | below Evals (MLPerf Area) |
| 114 | Graphs | AREA | kept |
| 115 | GraphRAG | AREA | merged → Graphs |
| 116 | Harness Engineering | AREA | kept |
| 117 | Hierarchical Structure Prediction, Syntax, and Parsing | AREA | below Natural Language Processing |
| 118 | Hosting Companies | FORMAT | an organisation |
| 119 | Human interaction in AI systems | AREA | merged → Humans and AI (HAI) |
| 120 | Human-Agent Interaction (HAI) | AREA | below Multiagent Systems |
| 121 | Human-AI Interaction/Cooperation and Human-Centric NLP | AREA | below Natural Language Processing |
| 122 | human-in-the-loop AI | AREA | merged → Humans and AI (HAI) |
| 123 | Humans and AI (HAI) | AREA | kept |
| 124 | Humans: Face, body, pose, gesture, movement | AREA | below Computer vision |
| 125 | Image and video synthesis and generation | AREA | below Computer vision |
| 126 | Inference | AREA | kept |
| 127 | Infra | AREA | merged → AI Infrastructure |
| 128 | infrastructure, software libraries, hardware, etc. | AREA | merged → AI Infrastructure |
| 129 | Information Extraction and Retrieval | AREA | below Natural Language Processing |
| 130 | Innovative Applications (IA) | DOMAIN | AI applied to another field's problems |
| 131 | Instance-based learning | AREA | below Machine learning |
| 132 | Intelligent Robotics | AREA | kept |
| 133 | Interpretability and Analysis of Models for NLP | AREA | below Natural Language Processing |
| 134 | Kernel methods | AREA | below Machine learning |
| 135 | Knowledge representation | AREA | merged → KRR |
| 136 | Knowledge Representation and Reasoning (KRR) | AREA | kept |
| 137 | Language | AREA | below Evals (MLPerf Area) |
| 138 | Language and multimodal language models | AREA | kept |
| 139 | Language Models | AREA | below Natural Language Processing |
| 140 | learning on graphs and other geometries & topologies | AREA | kept |
| 141 | Learning and Adaptation (LEARN) | AREA | below Multiagent Systems |
| 142 | Learning in probabilistic graphical models | AREA | below Machine learning |
| 143 | Learning latent representations | AREA | below Machine learning |
| 144 | Learning linear models | AREA | below Machine learning |
| 145 | learning theory | AREA | merged → theory of machine learning |
| 146 | LF AI & Data Member Company | FORMAT | an organisation |
| 147 | Linguistic theories, Cognitive Modeling and Psycholinguistics | AREA | below Natural Language Processing |
| 148 | LLM Efficiency | AREA | below Natural Language Processing |
| 149 | LLM Recsys | AREA | below Data Mining & Knowledge Management (DMKM) |
| 150 | Local AI | AREA | kept |
| 151 | Logical and relational learning | AREA | below Machine learning |
| 152 | Low-level vision | AREA | below Computer vision |
| 153 | Low-resource Methods for NLP | AREA | below Natural Language Processing |
| 154 | Machine learning | AREA | kept |
| 155 | Machine learning (other than deep learning) | AREA | below Computer vision |
| 156 | Machine Learning for NLP | AREA | below Natural Language Processing |
| 157 | machine learning systems | AREA | merged → AI Infrastructure |
| 158 | Machine Translation | AREA | below Natural Language Processing |
| 159 | Markov decision processes | AREA | below Machine learning |
| 160 | Mathematical, Symbolic, Neurosymbolic, and Logical Reasoning | AREA | below Natural Language Processing |
| 161 | MCP | AREA | below Harness Engineering (product as evidence) |
| 162 | Medical AI | DOMAIN | AI applied to another field's problems |
| 163 | Medical and biological vision, cell microscopy | DOMAIN | AI applied to another field's problems |
| 164 | Memory & Continual Learning | AREA | kept |
| 165 | metric learning, kernel learning | AREA | below Machine learning |
| 166 | MLCube | UNCLEAR | no scope in the record |
| 167 | MLPerf Automotive | AREA | below Evals (product as evidence) |
| 168 | MLPerf Client | AREA | below Evals (product as evidence) |
| 169 | MLPerf Endpoints | AREA | below Evals (product as evidence) |
| 170 | MLPerf Inference | AREA | below Evals (product as evidence) |
| 171 | MLPerf Inference: Datacenter | AREA | below Evals (product as evidence) |
| 172 | MLPerf Inference: Edge | AREA | below Evals (product as evidence) |
| 173 | MLPerf Inference: Mobile | AREA | below Evals (product as evidence) |
| 174 | MLPerf Inference: Tiny | AREA | below Evals (product as evidence) |
| 175 | MLPerf Storage | AREA | below Evals (product as evidence) |
| 176 | MLPerf Tiny | AREA | below Evals (product as evidence) |
| 177 | MLPerf Training | AREA | below Evals (product as evidence) |
| 178 | MLPerf Training: HPC | AREA | below Evals (product as evidence) |
| 179 | Mobile | AREA | below Evals |
| 180 | Model | AREA | kept |
| 181 | Modeling and simulation | DOMAIN | belongs to none of the three — a neighbouring field |
| 182 | Modeling and Simulation of Societies (SIM) | DOMAIN | AI applied to another field's problems |
| 183 | Multiagent Systems | AREA | kept |
| 184 | Multidisciplinary Topics | DOMAIN | AI applied to another field's problems |
| 185 | Multilinguality and Language Diversity | AREA | below Natural Language Processing |
| 186 | Multimodal learning | AREA | below Computer vision |
| 187 | Multimodality and Language Grounding to Vision, Robotics and Beyond | AREA | below Natural Language Processing |
| 188 | Natural Language Generation | AREA | below Natural Language Processing |
| 189 | Natural Language Processing | AREA | kept |
| 190 | Neural and Evolutionary Computing (cs.NE) | AREA | kept |
| 191 | Neural networks | AREA | below Machine learning |
| 192 | Neuroscience and cognitive science | AREA | below Cognitive Modeling & Cognitive Systems (CMS) |
| 193 | neurosymbolic & hybrid AI systems | AREA | kept |
| 194 | NLP Applications | DOMAIN | AI applied to another field's problems |
| 195 | Notebook Environment | AREA | kept |
| 196 | Optimization | AREA | kept |
| 197 | Optimization methods (other than deep learning) | AREA | below Computer vision |
| 198 | Parallel computing methodologies | DOMAIN | belongs to none of the three — a neighbouring field |
| 199 | Partially-observable Markov decision processes | AREA | below Machine learning |
| 200 | Philosophical/theoretical foundations of artificial intelligence | AREA | merged → PEAI |
| 201 | Philosophy and Ethics of AI (PEAI) | AREA | kept |
| 202 | Phonology, Morphology and Word Segmentation | AREA | below Natural Language Processing |
| 203 | Photogrammetry and remote sensing | DOMAIN | AI applied to another field's problems |
| 204 | Physics-based vision and shape-from-X | AREA | below Computer vision |
| 205 | Planning | AREA | merged → PRS |
| 206 | Planning and scheduling | AREA | merged → PRS |
| 207 | Planning and Search | AREA | merged → PRS (spans SO too) |
| 208 | Planning, Routing, and Scheduling (PRS) | AREA | kept |
| 209 | Posttraining & Midtraining | AREA | kept |
| 210 | Power | AREA | below Evals |
| 211 | Privacy and Confidentiality | AREA | below trustworthy machine learning |
| 212 | probabilistic methods | AREA | kept |
| 213 | Product Management | FORMAT | belongs to none of the three — a job function |
| 214 | Programming | AREA | kept |
| 215 | Question Answering | AREA | below Natural Language Processing |
| 216 | Reasoning | AREA | merged → KRR |
| 217 | Reasoning + RL | AREA | kept |
| 218 | Reasoning under Uncertainty (RU) | AREA | kept |
| 219 | Recognition: Categorization, detection, retrieval | AREA | below Computer vision |
| 220 | reinforcement learning | AREA | kept |
| 221 | Representation, and Reasoning (RR) | AREA | below Multiagent Systems |
| 222 | Representation learning | AREA | below Computer vision |
| 223 | representation learning for computer vision, audio, language, and other modalities | AREA | kept |
| 224 | Resources and Evaluation | AREA | below Natural Language Processing |
| 225 | Retrieval + Search | AREA | merged → Search & Retrieval |
| 226 | Retrieval-Augmented Language Models | AREA | below Natural Language Processing |
| 227 | Robotics (cs.RO) | AREA | merged → Intelligent Robotics |
| 228 | Robotics & World Models | AREA | merged → Intelligent Robotics |
| 229 | Robotics and Control (ROBOT) | AREA | merged → Intelligent Robotics |
| 230 | Robotics, embodied systems, and engineering | AREA | merged → Intelligent Robotics |
| 231 | robotics and perception | AREA | merged → Intelligent Robotics |
| 232 | Rule learning | AREA | below Machine learning |
| 233 | Safety | AREA | kept |
| 234 | Safety and Alignment in LLMs | AREA | below Natural Language Processing |
| 235 | Sandbox & Platform Engineering | AREA | kept |
| 236 | Scene analysis and understanding | AREA | below Computer vision |
| 237 | Science | UNCLEAR | the record restates the name; see Unclear |
| 238 | Search | AREA | merged → SO |
| 239 | Search & Retrieval | AREA | kept |
| 240 | Search and Optimization (SO) | AREA | kept |
| 241 | Search methodologies | AREA | merged → SO |
| 242 | Search, Optimization, Planning, and Scheduling (SOPS) | AREA | below Multiagent Systems |
| 243 | Security | AREA | kept |
| 244 | Security & Privacy | AREA | merged → Security |
| 245 | Segmentation, grouping and shape analysis | AREA | below Computer vision |
| 246 | Self-, semi-, meta- and unsupervised learning | AREA | below Computer vision |
| 247 | Semantics: Lexical, Sentence-level Semantics, Textual Inference and Other areas | AREA | below Natural Language Processing |
| 248 | Sentiment Analysis, Stylistic Analysis, and Argument Mining | AREA | below Natural Language Processing |
| 249 | societal considerations including fairness, safety, privacy | AREA | merged → trustworthy machine learning |
| 250 | Socio-technical aspects of AI | AREA | merged → trustworthy machine learning |
| 251 | Software Factories | AREA | kept |
| 252 | Special Theme: Explainability of NLP Models | AREA | below Natural Language Processing |
| 253 | Special Track on AI Alignment | AREA | merged → Safety |
| 254 | Special Track on AI for Social Impact | DOMAIN | AI applied to another field's problems |
| 255 | Speech Processing and Spoken Language Understanding | AREA | below Natural Language Processing |
| 256 | Stochastic games | AREA | below Machine learning |
| 257 | Summarization | AREA | below Natural Language Processing |
| 258 | SWE Agents | AREA | merged → Software Factories |
| 259 | Symbolic and algebraic manipulation | DOMAIN | belongs to none of the three — a neighbouring field |
| 260 | SysML Infrastructure | AREA | merged → AI Infrastructure |
| 261 | Testing of AI-based systems | AREA | merged → Evals |
| 262 | Theory | AREA | merged → theory of machine learning |
| 263 | theory of machine learning | AREA | kept |
| 264 | Tiny Teams | FORMAT | a company size |
| 265 | transfer learning, meta learning, and lifelong learning | AREA | merged → Generalization and multi-task learning |
| 266 | Transfer/ low-shot/ continual/ long-tail learning | AREA | below Computer vision |
| 267 | Transparency, fairness, accountability, privacy and ethics in vision | AREA | below Computer vision |
| 268 | Trusted & Responsible AI | AREA | merged → trustworthy machine learning |
| 269 | Trustworthiness | AREA | merged → trustworthy machine learning |
| 270 | trustworthy machine learning | AREA | kept |
| 271 | Uncertainty in AI | AREA | merged → Reasoning under Uncertainty (RU) |
| 272 | unsupervised, self-supervised, semi-supervised, and supervised representation learning | AREA | kept |
| 273 | Use cases and applications | DOMAIN | AI applied to another field's problems |
| 274 | Video: Action and event understanding | AREA | below Computer vision |
| 275 | Video: Low-level analysis, motion, and tracking | AREA | below Computer vision |
| 276 | Vision | AREA | below Evals (MLPerf Area) |
| 277 | Vision + graphics | AREA | below Computer vision |
| 278 | Vision & OCR | AREA | below Computer vision |
| 279 | Vision applications and systems | DOMAIN | AI applied to another field's problems |
| 280 | Vision, language, and reasoning | AREA | below Computer vision |
| 281 | visualization or interpretation of learned representations | AREA | kept |
| 282 | Voice | AREA | merged → Voice & Realtime AI |
| 283 | Voice & Realtime AI | AREA | kept |

## What this run could not settle

### 1. Every `UNCLEAR`, and what would settle it

Five, listed in full in `## Unclear` above: **Chakra**, **Croissant**, **MLCube** (MLCommons working
groups whose page gives no scope — a scope statement from MLCommons would settle each),
**Emerging Trends in AI Track** (AAAI names it in a Calls list and describes nothing; a scope
statement, and whether it is a technical track at all, would settle it), and **Science** (an
MLCommons group whose record restates its name; whether the group does AI **for** the sciences or
the science of AI measurement would settle it).

### 2. Rejections I was unsure about

Each of these is a rejection the owner would otherwise never see.

- **The five ACM CCS siblings of Artificial intelligence** — Computer graphics, Concurrent computing
  methodologies, Distributed computing methodologies, Parallel computing methodologies, Modeling and
  simulation, and Symbolic and algebraic manipulation (six names). They are not AI, so the rule drops
  them, but **none of the six verdict labels fits them**: they are not AI pointed at another field's
  data, not a record, not a format, not a product. I used `DOMAIN` as the nearest label and said so
  on every row. If the owner reads the rule as dropping only the four named kinds, these come back.
- **Autonomous driving**, **Medical and biological vision, cell microscopy**, **Photogrammetry and
  remote sensing** (CVPR subject areas). Rejected as sector-defined. Perception for autonomy and
  medical imaging are also core vision research, and CVPR carries them beside its method areas.
- **Vision applications and systems** and **Multidisciplinary Topics** are residual buckets, not
  domains proper. A residual can hold method work that the named areas missed.
- **AI and network science** (NeurIPS). Network science supplies methods to AI as well as problems.
- **applications to neuroscience & cognitive science** (ICLR) rejected while **Neuroscience and
  cognitive science** (NeurIPS) was kept. The two were separated on one word in the records —
  "applied to" against "alongside".
- **Special Track on AI for Social Impact** (AAAI-26). Rejected as `DOMAIN`; it is equally a review
  format, and its record is a rubric rather than a subject.
- **Product Management** (WF25) and **Forward Deployed Engineering** (WF26). Both name work people
  really do around AI systems. I rejected them as a job function and a delivery model. If the
  owner counts the practice of building AI products as the engineering of AI, both return.
- **AI-Native Enterprises** (WF26) and **AI in the Fortune 500** (WF25). Rejected on the
  company-size and working-arrangement clauses. `AI in the Fortune 500` may instead be `RECORD`.
- **AI Architects: Show my Workflow** rejected as a session shape while **AI Architects: AI
  Factories** and **AI Architects: Tokenmaxxing** were kept. All three are slots in one
  audience-gated leadership track; I judged each on its own record, which split the family.
- **Hosting Companies** and **LF AI & Data Member Company**. Clearly organisations, and the input
  says so itself; the only doubt is the label (`FORMAT` for want of an "organisation" verdict).

### 3. Merges made on thin evidence, so they can be split again

- **trustworthy machine learning** absorbs five names (Fairness, Ethics, and Trust; societal
  considerations including fairness, safety, privacy; Socio-technical aspects of AI; Trusted &
  Responsible AI; Trustworthiness). The input's own record says six sources carve this ground six
  ways. `Socio-technical aspects of AI` is the weakest member and may be `RECORD`; SC 42's
  `Trustworthiness` is a standards stream, not a research subject.
- **Intelligent Robotics** absorbs seven names. The merge is well-evidenced by cross-reference but
  it flattens real differences: AAMAS binds control to robotics, AAAI gives control no area, NeurIPS
  puts "engineering" in the category, and **WF26's `Robotics & World Models` carries world models,
  which no other source in the register names at any level.** If the owner wants world models as its
  own area, that is the split to make.
- **KRR** absorbs `Knowledge representation` and `Reasoning`, undoing a split the AAAI-26 main-track
  prose makes deliberately. Reasoning as its own area is a live option.
- **PRS** absorbs IJCAI's `Planning and Search`, which spans both PRS and `Search and Optimization
  (SO)`. The half that belongs to SO is lost by this filing.
- **theory of machine learning** absorbs NeurIPS's `Theory`, whose record states no scope at all. If
  that merge is split, `Theory` becomes a sixth `UNCLEAR`.
- **Safety** absorbs AAAI-26's `Special Track on AI Alignment`. Alignment, scalable oversight and
  mechanistic interpretability may deserve an area of their own; AAAI reviews them under a different
  rubric from everything else.
- **Security** absorbs LF AI & Data's `Security & Privacy`, which pulls privacy in; MLCommons keeps
  privacy separate, and `Privacy and Confidentiality` is filed below trustworthy machine learning,
  so privacy now appears in two places.
- **Generalization and multi-task learning** absorbs ICLR's `transfer learning, meta learning, and
  lifelong learning`. The framing run declined this merge because no two of the five names for this
  ground share word-sets.
- **PEAI** absorbs ACM CCS's `Philosophical/theoretical foundations of artificial intelligence`,
  which CCS keeps **without** ethics.
- **Search & Retrieval** absorbs `Retrieval + Search` and **Voice & Realtime AI** absorbs `Voice`.
  Both are same-event renamings; in each case the earlier record states a scope the later one does
  not, and the 2026 voice name adds realtime AI, which is not voice.
- **Agentic Engineering** absorbs ACL's `AI/LLM Agents` on one `ALSO CALLED` line.
- Kept **separate** where a merge was arguable, so the owner may still merge: `probabilistic
  methods` against `Reasoning under Uncertainty (RU)` (the input says the dispute is exactly whether
  this is a method or a kind of reasoning); `Data` against `Data-centric aspects of AI`;
  `generative models` against `Generative Media`; `Sandbox & Platform Engineering` against `AI
  Infrastructure`; `Memory & Continual Learning` against `Generalization and multi-task learning`;
  `Language and multimodal language models` against `Natural Language Processing`; `Audio and Speech
  Processing (AUD)` against `Voice & Realtime AI`; `Functional safety and AI systems` against
  `Safety`.

### 4. Areas kept on thin scope

The brief warns that a record carrying no scope cannot be an area, and names two examples. Both are
kept here, on scope statements rather than on their names, and both are thin: **Graphs** ("graph-
shaped data and knowledge in AI applications", excluding graph learning) and **Harness
Engineering** ("the scaffolding, tools and runtime that an agent or model runs inside", excluding
agent logic). Others kept on thin scope: `causal reasoning`, `learning on graphs and other
geometries & topologies`, `Autoresearch`, `Claws & Personal Agents`, `Agentic Commerce`, `Software
Factories`, `Design Engineering`, `AI Architects: AI Factories`, `Algorithms`, `metric learning,
kernel learning`, `Code Models`. If the owner applies the brief's no-scope test more strictly than I
did, these move to `UNCLEAR`, not to rejection.

### 5. Whether the level I picked loses something

It does, in four ways.

1. **A general subject that only a single-modality venue names gets filed under that modality.**
   CVPR's `Deep learning architectures and techniques`, `Machine learning (other than deep
   learning)`, `Optimization methods (other than deep learning)`, `Datasets and evaluation`,
   `Transparency, fairness, accountability, privacy and ethics in vision` and `Computer vision
   theory` sit below Computer vision; ACL's `Ethics, Bias, and Fairness`, `Language Models`,
   `Resources and Evaluation`, `Safety and Alignment in LLMs`, `LLM Efficiency` and `Machine
   Learning for NLP` sit below Natural Language Processing. Their subjects are not vision or
   language subjects. The level puts them where their venue puts them, not where their subject
   belongs.
2. **The MLCommons apparatus collapses into one area.** 25 suites, groups and benchmark Areas sit
   below `Evals`. That is where the records put them, but it means storage measurement, power
   measurement and content-safety measurement are one line apart from each other in this file,
   when the input shows they measure different things — and `Power` is the only energy category in
   the whole register.
3. **AAMAS's eleven areas collapse into Multiagent Systems**, on the input's own statement that
   the other venues hold all of it in one category. About 150 topics sit below six of those areas,
   unnamed here because the framing run reported them as topic counts, not as categories.
4. **Two umbrella records sit above the level and are still listed as areas** — `Artificial
   intelligence (ACM CCS)` and `Artificial Intelligence (cs.AI)`. They are not peers of the other
   61. Reading the list as a flat list of 63 would double-count their contents.

### 6. Areas the rule implies that no framing run reported

Named here, never as areas, per the brief. The input's own closing notes point at three gaps and I
add none of my own: **pre-training** (the WF26 record for `Posttraining & Midtraining` says
pre-training "no 2026 track names"), **role- and job-shaped categories** (the register records that
the job-board sources were unreachable), and **categories named only in non-English languages**
(the register records that these are invisible to every source read).

### 7. Project files visible in my context, and what they told me

None was used as evidence; the framing file was the only evidence. Named for completeness:

- `/Users/lakshmideepak/LearningLab/towards-intelligence/robotbrainlab.github.io/.claude/CLAUDE.md`
  — session instructions for the website repository. Told me the repository wins over stale
  instructions, and that the book projects govern themselves. Nothing about areas.
- `.../.claude/HANDOVER.md` — the website handover. Told me that `_book/` holds a finished
  interview-prep book and `_future-books/DECISIONS.md` holds the decisions for the two books that
  follow, neither started, and that no book may start before its rules are written and its table of
  contents approved. That is the decision this list feeds; it is also why this run does not choose
  areas for the owner.
- `/Users/lakshmideepak/.claude/projects/-Users-lakshmideepak-LearningLab-towards-intelligence-robotbrainlab-github-io/memory/MEMORY.md`
  — the memory index. One line bears on this task: "Modern AI book objective — the career goal
  behind the second book, and the five questions every area must answer." **I did not read or apply
  those five questions**: the brief says the rule it gave is the only rule I apply, and that I must
  not supplement it. If the owner wants areas tested against those five questions, that is a
  separate pass over this file.
- The git status in my context named `_book-modern-ai/docs/briefs/TEMPLATE-area-frame.md` and
  `_book-modern-ai/docs/CHECK-consolidation-2026-11-07-g.md` as modified or untracked, and recent
  commits about a source register, a scout brief and an earlier consolidator run. I opened none of
  them.

## Written to

`/private/tmp/claude-501/-Users-lakshmideepak-LearningLab-towards-intelligence-robotbrainlab-github-io/5df60113-a1a6-4930-9133-b34c516fdbb7/scratchpad/consol-g/CONSOLIDATED-2026-11-07-g.md`

283 categories in, 283 verdicts out: 63 areas kept, 47 names merged, 123 finer categories filed
below an area, 36 `DOMAIN`, 0 `RECORD`, 9 `FORMAT`, 0 `PRODUCT`, 5 `UNCLEAR`.
