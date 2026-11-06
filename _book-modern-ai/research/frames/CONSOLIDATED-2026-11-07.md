# Consolidated candidate areas — runs E and F judged against one rule

Consolidation run, 2026-11-07. Input: `2026-11-07-e.md` (104 category records) and
`2026-11-07-f.md` (77 category records) — **181 records, each given exactly one verdict**.
No source was fetched, no search was run, and no category was added that neither run reported.
Run E's heading `Responsible AI — see Trustworthy machine learning` is a pointer to a merge made
inside run E and is treated as the pointer it says it is, not as a record.

## The rule applied

Keep a category if it belongs to the science of AI, the research in AI, or the engineering of AI —
and engineering includes its tools, its measurement and its operation. Drop it if it belongs to none
of the three: AI applied to another field's problems, a report on AI's effect on the world, a meeting
format or audience, or an organisation. A product or tool name is not dropped; it is reported as the
engineering area it instances, with the product named as evidence.

## How the two runs' sources line up

| Source | Run E key | Run F key | Same document? |
|---|---|---|---|
| arXiv category taxonomy | `ARXIV` | S1 | yes |
| ACM CCS 2012 via the UCT repository | `CCS-UCT` | S5 | yes |
| ACM CCS 2012 via the aima.cs.berkeley.edu mirror | `CCS-AIMA` | — | run E only (run F rejected it as a textbook page) |
| AAAI-27 areas and topics | `AAAI` | S3 | yes |
| NeurIPS call for papers | `NEURIPS` (2026 cycle) | S2 (2025) | **no — two cycles of one venue** |
| ICML 2026 call for papers | `ICML` | — | run E only |
| IJCAI 2025 call for papers | — | S4 | run F only |
| MLCommons benchmarks | `MLPERF` (suite level) | S6 (label level) | yes, **taken at different levels** |
| LF AI & Data `landscape.yml` | `LFAI` | S7 | yes |
| Stanford HAI AI Index 2025 | `AIINDEX` | S8 | yes |
| AI Engineer World's Fair programme | `AIEWF` (2026) | S9 (2025) | **no — two editions of one meeting** |

`FAMILY` below reads **academic** for the `index`, `review-venue` and `survey` kinds, **applied**
for the `practitioner` and `programme` kinds. That mapping is mine and is stated so it can be undone.

---

# 1. Areas

69 areas. Alphabetical. No ordering, score or rank.

### Agent Reliability
- **VERDICT** AREA
- **WHY** The engineering of AI, in its operation: making deployed agents behave dependably in production.
- **SOURCES** S9 AI Engineer World's Fair 2025 programme, `programme`, FETCHED.
- **ATTESTED BY** F: 1 — S9.
- **COVERS** making deployed LLM agents behave dependably in production, as a track of its own.
- **EXCLUDES** multi-agent coordination theory (Multiagent Systems); measurement of agent quality (Evals).
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Agentic Engineering
- **VERDICT** AREA
- **WHY** The engineering of AI: building agent systems.
- **SOURCES** AIEWF 2026 programme, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** the record gives the track name and its level only; no scope statement.
- **EXCLUDES** not stated by the source.
- **MERGED FROM** none. Kept apart from Agent Reliability, SWE Agents and Claws & Personal Agents: different names, no `ALSO CALLED`, no matching `INCLUDES`.
- **BELOW** none reported.
- **FAMILY** applied.

### AI Safety
- **VERDICT** AREA
- **WHY** The engineering of AI, in its measurement: benchmarking the safety of AI systems.
- **SOURCES** S6 MLCommons Benchmarks, `practitioner`, FETCHED.
- **ATTESTED BY** F: 1 — S6.
- **COVERS** benchmarking the safety of AI systems.
- **EXCLUDES** performance benchmarking (MLPerf); training-algorithm benchmarking (AlgoPerf); fairness and explainability tooling (Trusted & Responsible AI, merged into Trustworthy machine learning).
- **MERGED FROM** none — run F's record states this label is *not* the same as `Responsible AI` (S8) or `Trusted & Responsible AI` (S7).
- **BELOW** the AILuminate suite (S6), named by the record as its one suite.
- **FAMILY** applied.

### Applications
- **VERDICT** AREA
- **WHY** Research in AI: its own gloss names AI modalities, not another field's problems.
- **SOURCES** S2 NeurIPS 2025 call for papers, `review-venue`, FETCHED.
- **ATTESTED BY** F: 1 — S2.
- **COVERS** in the call's words, "vision, language, speech and audio, Creative AI".
- **EXCLUDES** scientific applications, which the same call sends to Machine learning for sciences; method papers, which go to the method topics.
- **MERGED FROM** none. **Not** merged with Application Domains (AAAI), which the records show enumerating twelve other fields — run F's own record refuses that merge because the glosses differ.
- **BELOW** none reported.
- **FAMILY** academic.
- **NOTE** This is the closest keep on the list. See "What this run could not settle".

### Artificial intelligence
- **VERDICT** AREA
- **WHY** The science and research of AI: expert systems, theorem proving, knowledge representation, planning, uncertainty.
- **SOURCES** ARXIV / S1 arXiv `cs.AI`, `index`, FETCHED; S5 / CCS-UCT the ACM CCS level-2 node `Computing methodologies > Artificial intelligence`, `index`, FETCHED.
- **ATTESTED BY** E: 1 — ARXIV. F: 2 — S5, S1. Distinct documents across both runs: 2 (arXiv, CCS via UCT); run E also read the CCS-AIMA mirror of the same node under other units.
- **COVERS** arXiv: all areas of AI except those with their own subject areas — expert systems, theorem proving, knowledge representation, planning, uncertainty in AI. CCS: the parent of computer vision, NLP, KRR, control methods, distributed AI and the philosophical foundations.
- **EXCLUDES** arXiv excludes Vision, Robotics, Machine Learning, Multiagent Systems and Computation and Language, each its own category; in CCS, machine learning is a **sibling**, not a child.
- **MERGED FROM** `Artificial Intelligence (cs.AI)` (run E). Evidence: identical name and the same arXiv source; run F's `ALSO CALLED` is "Artificial Intelligence (cs.AI)".
- **BELOW** in CCS, every unit on this list that CCS files under it (Computer Vision, Natural Language Processing, Knowledge Representation and Reasoning, Control methods, Multiagent Systems as `Distributed artificial intelligence`, Philosophical/theoretical foundations).
- **FAMILY** academic.
- **NOTE** Both runs flag this as the sharpest disagreement they found: CCS makes AI the parent, arXiv makes it the residual that excludes those same categories. Carried forward unresolved.

### Audio and Speech Processing (AUD)
- **VERDICT** AREA
- **WHY** Research in AI: a method area of a review venue.
- **SOURCES** AAAI / S3 AAAI-27 areas and topics, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** speech recognition and spoken language understanding, speech synthesis and voice conversion, speaker recognition and diarization, speech enhancement and source separation, audio representation learning and foundation models, music information retrieval and generation, environmental sound and acoustic scenes, paralinguistics and affective speech, audio deepfake detection, audio-visual and multimodal learning, bias/fairness/privacy/low-resource and multilingual speech, datasets and benchmarks.
- **EXCLUDES** text-only language work (Natural Language Processing) — but CCS keeps `Speech recognition` inside NLP, so the sources disagree on this exclusion.
- **MERGED FROM** none. Both runs refuse to merge AIEWF's voice track into it.
- **BELOW** AAAI's 13 topic keywords under this area.
- **FAMILY** academic.

### Cognitive Modeling & Cognitive Systems (CMS)
- **VERDICT** AREA
- **WHY** The science of AI: building and modelling cognitive systems.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** affective computing and social cognition, cognitive architectures and conceptual reasoning, computational creativity, simulating human behaviour, symbolic representations and agent architectures.
- **EXCLUDES** the philosophy of AI (Philosophy and Ethics of AI); human-facing interaction work (Humans and AI); learning methodology (Machine Learning).
- **MERGED FROM** none — both runs refuse to merge NeurIPS's `Neuroscience and cognitive science`, whose gloss is neural coding and brain–computer interfaces.
- **BELOW** AAAI's 6 topic keywords.
- **FAMILY** academic.

### Computer Use
- **VERDICT** AREA
- **WHY** The engineering of AI: models operating a computer.
- **SOURCES** AIEWF 2026 programme, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Computer Vision
- **VERDICT** AREA
- **WHY** Research in AI: a method area in five source documents.
- **SOURCES** AAAI / S3 `review-venue`; NEURIPS `review-venue`; ARXIV / S1 `cs.CV` `index`; CCS-AIMA `index`; CCS-UCT / S5 `index`. All FETCHED.
- **ATTESTED BY** E: 5 — AAAI, NEURIPS, ARXIV, CCS-AIMA, CCS-UCT. F: 3 — S3, S5, S1. Distinct documents across both runs: 5.
- **COVERS** AAAI: 3D vision, adversarial attacks and robustness, bias/fairness/privacy/interpretability, biometrics and pose, computational photography and image/video synthesis, datasets and benchmarks, diffusion and generative models for vision, image and video retrieval, language-vision and multimodal, learning and optimization for CV, low-level and physics-based vision, medical and biological imaging, motion and tracking, object detection and segmentation, remote sensing and geospatial AI, representation learning and vision foundation models, vision for robotics and autonomous driving, visual reasoning. arXiv: image processing, computer vision, pattern recognition, scene understanding.
- **EXCLUDES** graphics and multimedia (arXiv `cs.GR`, `cs.MM`, off-list); robot perception (Intelligent Robotics); generative image production as a product track (Generative Media).
- **MERGED FROM** `Computer vision` (CCS), `Computer Vision and Pattern Recognition (cs.CV)` (arXiv) — both runs merged on the identical head name and arXiv's own description.
- **BELOW** CCS's 4 third-level terms (computer vision tasks, image and video acquisition, computer vision representations, computer vision problems); AAAI's 19–20 topic keywords.
- **FAMILY** both.

### Constraint Satisfaction and Optimization (CSO)
- **VERDICT** AREA
- **WHY** Research in AI: a method area of a review venue.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** constraint optimization and programming, constraint satisfaction and learning, distributed and mixed discrete/continuous optimization, satisfiability and SMT, search/solvers/tools.
- **EXCLUDES** heuristic and local search (Search and Optimization); planning (Planning, Routing, and Scheduling); continuous optimisation for learning (Optimization).
- **MERGED FROM** none.
- **BELOW** AAAI's 6 topic keywords.
- **FAMILY** academic.

### Context Engineering
- **VERDICT** AREA
- **WHY** The engineering of AI: assembling what a model is given to work with.
- **SOURCES** AIEWF 2026 programme, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source. Run E records that AAAI files prompt and in-context work as topics inside NLP, below the level it took.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Control methods
- **VERDICT** AREA
- **WHY** The science and research of AI: a branch of AI methodology in the ACM classification.
- **SOURCES** CCS-AIMA `index`; CCS-UCT / S5 `index`. Both FETCHED.
- **ATTESTED BY** E: 2 — CCS-AIMA, CCS-UCT. F: 1 — S5. Distinct documents: 2 renderings of ACM CCS 2012.
- **COVERS** robotic planning, evolutionary robotics, computational control theory, motion path planning.
- **EXCLUDES** systems-and-control work outside the AI branch (arXiv `cs.SY`, off-list); robot systems, which CCS's AI children do not carry; learning-based control, an example inside NeurIPS's reinforcement-learning topic.
- **MERGED FROM** none — run E refuses to merge NeurIPS's `Decision-making, reinforcement learning, and control`, which is a learning topic.
- **BELOW** CCS's 4 third-level terms, of which UCT shows `Motion path planning` populated.
- **FAMILY** academic.

### Data
- **VERDICT** AREA
- **WHY** The engineering of AI and its tools: the whole data side of the work.
- **SOURCES** LFAI / S7 LF AI & Data `landscape.yml`, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** the source's 13 subcategories — Education, Lineage, Relational DB, Store & Format, Versioning, Operations, Feature Engineering, Stream Processing, SQL Engine, Visualization, Pipeline Management, Labeling & Annotation, Governance.
- **EXCLUDES** model-side tooling (Model); compute (Distributed Computing); mining and knowledge extraction (Data Mining & Knowledge Management).
- **MERGED FROM** none — run E refuses to merge NeurIPS's `Data-centric aspects of AI`, which names research contributions where this names tooling.
- **BELOW** those 13 subcategories.
- **FAMILY** applied.
- **NOTE** Both runs single this out as the clearest category the review venues have no slot for.

### Data-centric aspects of AI
- **VERDICT** AREA
- **WHY** Research in AI: a topic a review venue invites submissions on.
- **SOURCES** NEURIPS 2026 call, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — NEURIPS.
- **COVERS** filed by the call as a topic; no gloss given.
- **EXCLUDES** not stated.
- **MERGED FROM** none, by run E's own refusal (see Data).
- **BELOW** none reported.
- **FAMILY** academic.

### Data Mining & Knowledge Management (DMKM)
- **VERDICT** AREA
- **WHY** Research in AI: a method area of a review venue.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** anomaly detection and pattern mining, conversational/query/retrieval systems, data stream and spatio-temporal mining, data visualization and summarization, datasets and benchmarks, graph mining and social network analysis, knowledge graphs and the semantic web, mining of visual and multimodal data, recommender systems, scalability and distributed systems.
- **EXCLUDES** logical knowledge representation (KRR); learning methods (Machine Learning); data tooling and pipelines (Data).
- **MERGED FROM** none.
- **BELOW** AAAI's 11 topic keywords.
- **FAMILY** academic.

### Data Quality
- **VERDICT** AREA
- **WHY** The engineering of AI, in its measurement: the quality of what is fed to models.
- **SOURCES** AIEWF 2026 programme, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none — no `ALSO CALLED` and no matching `INCLUDES` with Data or Data-centric aspects of AI.
- **BELOW** none reported.
- **FAMILY** applied.

### Deep learning
- **VERDICT** AREA
- **WHY** Research in AI, and its tools.
- **SOURCES** NEURIPS 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`; ICML 2026 `review-venue`; LFAI / S7 `practitioner`. All FETCHED.
- **ATTESTED BY** E: 3 — NEURIPS, ICML, LFAI. F: 2 — S2, S7. Distinct documents: 4.
- **COVERS** ICML: architectures, generative models, theory. NeurIPS 2025: architectures, generative models, optimization for deep networks, foundation models, LLMs. LFAI: frameworks, platforms, libraries and tools.
- **EXCLUDES** general machine learning, theory, optimization, probabilistic methods and reinforcement learning, each a separate topic in the same calls; classical ML tooling (Machine Learning).
- **MERGED FROM** `Deep Learning` (LFAI) — identical name.
- **BELOW** LFAI's 4 subcategories (Framework, Platform, Library, Tool).
- **FAMILY** both.

### Design Engineering
- **VERDICT** AREA
- **WHY** The engineering of AI: building the product surface of an AI system.
- **SOURCES** AIEWF 2026 `programme`; S9 AIEWF 2025 `programme`. Both FETCHED.
- **ATTESTED BY** E: 1 — AIEWF. F: 1 — S9. Two editions of one meeting.
- **COVERS** the design side of building AI products, as a track of its own (run F's gloss); run E has the name only.
- **EXCLUDES** product decision-making (Product Management, rejected below); human-factors research (Humans and AI).
- **MERGED FROM** `Design Engineering` (S9, 2025 edition) — identical name, same meeting.
- **BELOW** none reported.
- **FAMILY** applied.
- **NOTE** A close keep: the record describes product design work, not model work. Flagged below.

### Distributed Computing
- **VERDICT** AREA
- **WHY** The engineering of AI and its tools: the compute substrate.
- **SOURCES** LFAI / S7, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** computing and management tooling, and interfaces to it.
- **EXCLUDES** model-side tooling (Model); data tooling (Data); multi-agent AI (Multiagent Systems).
- **MERGED FROM** none. Both runs note it is **not** CCS's `Distributed artificial intelligence`.
- **BELOW** `Computing & Management`; **`Interface`** — run E reported Interface as a category of its own but records that it read the file across an offset boundary and the category header fell across it, while run F read Interface as a subcategory here. Filed here on run F's reading, not dropped.
- **FAMILY** applied.

### Evals
- **VERDICT** AREA
- **WHY** The engineering of AI, in its measurement.
- **SOURCES** AIEWF 2026 `programme`; S9 AIEWF 2025 `programme`; ICML 2026 `review-venue` (as `evaluation`); S2 NeurIPS 2025 `review-venue` (as `Evaluation`). All FETCHED.
- **ATTESTED BY** E: 2 — AIEWF, ICML. F: 1 — S9; and F: 1 — S2 for `Evaluation`. Distinct documents: 4.
- **COVERS** ICML and NeurIPS, in the same words: methodology, meta studies, replicability and validity, human-in-the-loop. AIEWF: the practice of evaluating LLM systems in product work.
- **EXCLUDES** NeurIPS routes dataset and benchmark papers to a separate submission track (off-list); run F's record puts standardised system benchmarking outside this category, in S6's suites.
- **MERGED FROM** `evaluation` (ICML, merged by run E), `Evals` (S9), `Evaluation` (S2). Evidence: run E's `ALSO CALLED` names ICML's `evaluation` as the same thing, and the ICML and NeurIPS glosses are word-for-word identical ("methodology, meta studies, replicability and validity, human-in-the-loop").
- **BELOW** the branded benchmark suites that instance this measurement work, named as evidence and not dropped: **MLPerf** (MLCommons) with its ten suites — MLPerf Client, Inference: Datacenter, Automotive, Endpoints, Inference: Edge, Inference: Mobile, Inference: Tiny, Storage, Training, Training: HPC — and **AlgoPerf** (training-algorithm benchmarking).
- **FAMILY** both.
- **NOTE** Run F explicitly declined to merge its `Evals` with its `Evaluation` ("the two may be the same category; this run could not establish it"). I merged them on run E's basis plus the identical glosses. Flagged below as a merge to check first.

### Game Theory and Economic Paradigms (GTEP)
- **VERDICT** AREA
- **WHY** Research in AI: game-theoretic and economic method inside AI.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** cooperative and behavioral game theory, coordination and adversarial interaction, equilibrium and imperfect information, mechanism design and auctions, social choice/voting/fair division.
- **EXCLUDES** agent architectures and coordination (Multiagent Systems); economic measurement of the field (Economy, rejected below).
- **MERGED FROM** none.
- **BELOW** AAAI's 6 topic keywords.
- **FAMILY** academic.

### General machine learning
- **VERDICT** AREA
- **WHY** Research in AI: core supervised and unsupervised method.
- **SOURCES** ICML 2026 `review-venue`; NEURIPS 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`. All FETCHED.
- **ATTESTED BY** E: 2 — ICML, NEURIPS. F: 1 — S2. Distinct documents: 3.
- **COVERS** ICML: active learning, clustering, online learning, ranking, supervised, semi- and self-supervised learning, time series analysis. NeurIPS: core contributions in supervised and unsupervised methods; "supervised, unsupervised, online, active, etc.".
- **EXCLUDES** deep learning, theory, optimization, probabilistic methods and reinforcement learning, each a separate topic in the same calls.
- **MERGED FROM** `General machine learning: core contributions in supervised and unsupervised methods` (NeurIPS) — identical opening name and the same enumerated content.
- **BELOW** none reported.
- **FAMILY** academic.
- **NOTE** This category exists only because NeurIPS and ICML split machine learning. See the Level section.

### Generalization and multi-task learning
- **VERDICT** AREA
- **WHY** Research in AI.
- **SOURCES** NEURIPS 2026 call, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — NEURIPS.
- **COVERS** filed by the call as a topic; no gloss.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** academic.

### Generative AI
- **VERDICT** AREA
- **WHY** The engineering of AI and its tools: generative models and the tooling around them.
- **SOURCES** LFAI / S7, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** generative-AI models and tools.
- **EXCLUDES** general deep-learning frameworks (Deep learning); NLP and Model, separate categories in the same landscape; media production work (Generative Media).
- **MERGED FROM** none.
- **BELOW** LFAI's 2 subcategories (Models, Tools).
- **FAMILY** applied.

### Generative Media
- **VERDICT** AREA
- **WHY** The engineering of AI: generating image, video and audio with models.
- **SOURCES** AIEWF 2026 `programme`; S9 AIEWF 2025 `programme`. Both FETCHED.
- **ATTESTED BY** E: 1 — AIEWF. F: 1 — S9. Two editions of one meeting.
- **COVERS** generating media — image, video, audio — as a track of practitioner work.
- **EXCLUDES** the model research behind it (Deep learning); arts scholarship (AI and Arts, rejected below).
- **MERGED FROM** `Generative Media` (S9, 2025) — identical name, same meeting.
- **BELOW** none reported.
- **FAMILY** applied.

### GraphRAG
- **VERDICT** AREA
- **WHY** The engineering of AI: graph-based retrieval feeding generation.
- **SOURCES** S9 AIEWF 2025, `programme`, FETCHED.
- **ATTESTED BY** F: 1 — S9.
- **COVERS** graph-based retrieval-augmented generation, separate from plain retrieval.
- **EXCLUDES** non-graph retrieval (Search & Retrieval); recommendation (LLM RecSys).
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Graphs
- **VERDICT** AREA
- **WHY** Research and engineering in AI: learning on graph-structured data.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Harness Engineering
- **VERDICT** AREA
- **WHY** The engineering of AI and its tools: the harness a model runs inside.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Human interaction in AI systems
- **VERDICT** AREA
- **WHY** Research in AI: a topic a review venue invites submissions on.
- **SOURCES** NEURIPS 2026, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — NEURIPS.
- **COVERS** filed by the call as a topic; no gloss.
- **EXCLUDES** not stated.
- **MERGED FROM** none — run E refuses to merge AAAI's `Humans and AI`, because neither name is plainly the other.
- **BELOW** none reported.
- **FAMILY** academic.

### Human-Centred AI
- **VERDICT** AREA
- **WHY** Research in AI: a refereed track of AI work centred on the human.
- **SOURCES** S4 IJCAI 2025 call for papers, `review-venue`, FETCHED.
- **ATTESTED BY** F: 1 — S4.
- **COVERS** AI work centred on the human, refereed in its own track.
- **EXCLUDES** the main track's method work; interface engineering (Design Engineering).
- **MERGED FROM** none — run F refuses to merge AAAI's `Humans and AI`: the labels differ and neither source equates them.
- **BELOW** none reported.
- **FAMILY** academic.

### Humans and AI (HAI)
- **VERDICT** AREA
- **WHY** Research in AI: a method area of a review venue.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** AI for accessibility, emotional intelligence and brain-sensing, explainable AI for human understanding, game design and procedural generation, human-AI collaboration and trust, human-aware planning and decision support, human-computer interaction and interfaces, human-in-the-loop ML and crowdsourcing, learning human values and preferences.
- **EXCLUDES** ethics and governance (Philosophy and Ethics of AI); cognitive modeling (CMS).
- **MERGED FROM** none, by both runs' refusals (see Human interaction in AI systems, Human-Centred AI).
- **BELOW** AAAI's 10 topic keywords.
- **FAMILY** academic.

### Inference
- **VERDICT** AREA
- **WHY** The engineering of AI, in its operation: serving models.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none — run E refuses to merge LFAI's `Inference` subcategory and the MLPerf inference suites, because one names a track, one a tooling subcategory and one a benchmark suite.
- **BELOW** LFAI's `Inference` subcategory sits under Model, not here.
- **FAMILY** applied.

### Intelligent Robotics (ROB)
- **VERDICT** AREA
- **WHY** Research and engineering of AI in the physical world.
- **SOURCES** AAAI / S3 `review-venue`; NEURIPS 2026 `review-venue`; ARXIV / S1 `cs.RO` `index`; S9 AIEWF 2025 (as `Autonomy + Robotics`) `programme`. All FETCHED.
- **ATTESTED BY** E: 3 — AAAI, NEURIPS, ARXIV. F: 3 — S3, S1, S9. Distinct documents: 4.
- **COVERS** embodied AI, human-robot interaction, localization/mapping/navigation, manipulation and cognitive robotics, motion and path planning, multi-robot systems, perception and sensor fusion, robot learning and control and foundation models, datasets and benchmarks for robotics.
- **EXCLUDES** arXiv keeps robotics out of `cs.AI`; general vision goes to Computer Vision and general planning to PRS; control method, which CCS keeps as a child of AI.
- **MERGED FROM** `Robotics, embodied systems, and engineering` (NeurIPS), `Robotics (cs.RO)` (arXiv), `Autonomy + Robotics` (S9) — merged by the runs on the shared head noun; the NeurIPS and S9 names add "engineering" and "autonomy".
- **BELOW** AAAI's 10 topic keywords.
- **FAMILY** both.

### Knowledge Representation and Reasoning (KRR)
- **VERDICT** AREA
- **WHY** The science and research of AI.
- **SOURCES** AAAI / S3 `review-venue`; CCS-AIMA `index`; CCS-UCT / S5 `index`. All FETCHED.
- **ATTESTED BY** E: 3 — AAAI, CCS-AIMA, CCS-UCT. F: 2 — S3, S5. Distinct documents: 3.
- **COVERS** AAAI: action/change/spatio-temporal reasoning, automated reasoning and theorem proving, common-sense and causal and qualitative reasoning, diagnosis/abduction/argumentation, knowledge acquisition and ontologies, KR languages and preferences and beliefs, logic programming and description logics, neuro-symbolic reasoning, nonmonotonic reasoning. CCS: description logics, semantic networks, nonmonotonic and default reasoning and belief revision, probabilistic reasoning, vagueness and fuzzy logic, causal reasoning and diagnostics, temporal reasoning, cognitive robotics, ontology engineering, logic programming and answer set programming, spatial and physical reasoning, reasoning about belief and knowledge.
- **EXCLUDES** uncertainty and probabilistic inference, which AAAI sends to Reasoning under Uncertainty — **but CCS keeps `Probabilistic reasoning` inside KRR**, so the sources disagree on this exclusion; knowledge management and mining (DMKM).
- **MERGED FROM** `Knowledge representation and reasoning` (CCS) — identical name, both runs.
- **BELOW** CCS's 12 third-level terms (UCT shows 4 populated, 33 of its 64 items at `Ontology engineering`); AAAI's 10 topic keywords.
- **FAMILY** academic.

### Language and multimodal language models
- **VERDICT** AREA
- **WHY** Research in AI: the models themselves.
- **SOURCES** NEURIPS 2026, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — NEURIPS.
- **COVERS** filed by the call as a topic; no gloss.
- **EXCLUDES** not stated.
- **MERGED FROM** none — run E refuses to merge Natural Language Processing: NeurIPS names models, not the field, and covers multimodal models the NLP categories exclude.
- **BELOW** none reported.
- **FAMILY** academic.

### LLM RecSys
- **VERDICT** AREA
- **WHY** Research and engineering of AI: recommendation built with language models.
- **SOURCES** AIEWF 2026 (as `LLM Recsys`) `programme`; S9 AIEWF 2025 `programme`. Both FETCHED.
- **ATTESTED BY** E: 1 — AIEWF. F: 1 — S9. Two editions of one meeting.
- **COVERS** recommender systems built with language models, as a track of its own.
- **EXCLUDES** general retrieval (Search & Retrieval); graph retrieval (GraphRAG).
- **MERGED FROM** `LLM Recsys` (run E) — identical name but for capitalisation, same meeting.
- **BELOW** none reported.
- **FAMILY** applied.

### Local AI
- **VERDICT** AREA
- **WHY** The engineering of AI, in its operation: running models on the device in front of you.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** the MLPerf Client, Inference: Edge, Inference: Mobile and Inference: Tiny suites are named by run E as the measurement of this ground; they are filed under Evals, and named here because run E records the overlap.
- **FAMILY** applied.

### Machine Learning
- **VERDICT** AREA
- **WHY** Research in AI: the largest single method category in five source documents.
- **SOURCES** AAAI / S3 `review-venue`; ARXIV / S1 `cs.LG` and `stat.ML` `index`; CCS-AIMA `index`; CCS-UCT / S5 `index`; LFAI / S7 `practitioner`. All FETCHED.
- **ATTESTED BY** E: 5 — AAAI, ARXIV, CCS-AIMA, CCS-UCT, LFAI. F: 4 — S3, S5, S1, S7. Distinct documents: 5.
- **COVERS** arXiv: all aspects of machine-learning research — supervised, unsupervised and reinforcement learning, bandit problems, robustness, explanation, fairness, methodology, and applications of ML methods; `stat.ML` the statistically and theoretically grounded part. AAAI: 37 topics from adversarial robustness and AutoML through deep learning architectures and foundation models, federated learning, mixture of experts, post-training and alignment, representation learning, reinforcement learning, time series, to world models. CCS: learning paradigms, multi-task learning, learning settings, ML approaches, ML algorithms. LFAI: frameworks, platforms, libraries.
- **EXCLUDES** arXiv keeps ML out of `cs.AI`; AAAI sends vision, language, audio and robotics learning to their own areas; in CCS as rendered by UCT, everything under `Artificial intelligence`, which is a sibling branch.
- **MERGED FROM** `cs.LG`, `stat.ML` (arXiv), `Machine learning` (CCS), `Machine Learning` (LFAI), `Machine learning` (run F) — identical name across all five sources.
- **BELOW** AAAI's 37 topic keywords; CCS's `Learning paradigms` and `Machine learning approaches` (reported as units by run F) and the dozens of fourth-level terms under them; LFAI's 3 subcategories.
- **FAMILY** both.
- **NOTE** Where it sits is disputed (child of AI in the CCS-AIMA rendering, sibling of AI in the UCT rendering, a category `cs.AI` excludes at arXiv). Whether it is one category at all is disputed: NeurIPS and ICML divide the same ground into six co-equal topics, all of which are on this list as areas. See the Level section.

### Machine learning systems
- **VERDICT** AREA
- **WHY** The engineering of AI: implementation, scalability, hardware and the libraries.
- **SOURCES** ICML 2026 `review-venue`; NEURIPS 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`; S9 AIEWF 2025 (as `AI Infrastructure`) `programme`. All FETCHED.
- **ATTESTED BY** E: 2 — ICML, NEURIPS. F: 2 — S2, S9. Distinct documents: 4.
- **COVERS** improved implementation and scalability, hardware, libraries, distributed methods and distributed solutions; in S9, the infrastructure track of an engineering conference.
- **EXCLUDES** optimization and general machine learning, separate topics in the same calls; method contributions, which go to the method areas; data pipelines (Data); serving tooling (Model).
- **MERGED FROM** `SysML Infrastructure` (NeurIPS 2026, merged by run E), `Infrastructure` (S2), `AI Infrastructure` (S9). Evidence: the `INCLUDES` of run E's unit and run F's `Infrastructure` state the same list in the same words — improved implementation and scalability, libraries, distributed methods/solutions — and both cite a NeurIPS call's systems-and-infrastructure topic; run F merged `Infrastructure` with `AI Infrastructure` on the subject qualifier alone.
- **BELOW** none reported.
- **FAMILY** both.

### Memory & Continual Learning
- **VERDICT** AREA
- **WHY** Research and engineering of AI: what a system keeps and how it keeps learning.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Model
- **VERDICT** AREA
- **WHY** The engineering of AI, in its operation: the model lifecycle as operations.
- **SOURCES** LFAI / S7, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** the source's 9 subcategories — Inference, Federated Learning, Training, Parameter, Format & Interface, Marketplace, Workflow, Benchmarking, Tool.
- **EXCLUDES** data work (Data); compute (Distributed Computing); framework code (Machine Learning, Deep learning).
- **MERGED FROM** none.
- **BELOW** those 9 subcategories.
- **FAMILY** applied.
- **NOTE** Both runs record that no review venue or index they read carries a model-operations category.

### Multiagent Systems (MAS)
- **VERDICT** AREA
- **WHY** Research and engineering of AI: several agents, and the orchestration between them.
- **SOURCES** AAAI / S3 `review-venue`; ARXIV / S1 `cs.MA` `index`; CCS-AIMA `index`; CCS-UCT / S5 `index`. All FETCHED.
- **ATTESTED BY** E: 4 — AAAI, ARXIV, CCS-AIMA, CCS-UCT. F: 3 — S3, S1, S5. Distinct documents: 4.
- **COVERS** AAAI: agent theories and architectures, agent-based simulation, agentic safety and alignment, LLM-based agents and agentic systems, MAS under uncertainty, mechanism design and modelling other agents, multiagent learning, multiagent planning and coordination, negotiation and argumentation, tool use and orchestration for LLMs. arXiv: multiagent systems, distributed AI, intelligent agents, coordinated interactions. CCS: multi-agent systems, intelligent agents, mobile agents, cooperation and coordination.
- **EXCLUDES** arXiv keeps MAS out of `cs.AI`; auctions and social choice go to GTEP; single-agent LLM engineering, which S9 sends to Agent Reliability and SWE Agents; distributed computing infrastructure (Distributed Computing).
- **MERGED FROM** `Distributed artificial intelligence` (CCS) — both runs merged it, on arXiv's own `cs.MA` description naming both labels in one breath.
- **BELOW** AAAI's 11 topic keywords, including `tool use and orchestration for LLMs`; **MCP** (the Model Context Protocol, S9), filed here as the branded protocol instancing that orchestration work and named as evidence, not dropped.
- **FAMILY** both.
- **NOTE** Both runs record that "agent" names different work in the programme sources (one LLM agent in production) than in the academic ones (several agents coordinating).

### Natural Language Processing (NLP)
- **VERDICT** AREA
- **WHY** Research in AI: a method area in five source documents.
- **SOURCES** AAAI / S3 `review-venue`; ARXIV / S1 `cs.CL` `index`; CCS-AIMA `index`; CCS-UCT / S5 `index`; LFAI / S7 `practitioner`. All FETCHED.
- **ATTESTED BY** E: 5 — AAAI, ARXIV, CCS-AIMA, CCS-UCT, LFAI. F: 4 — S3, S5, S1, S7. Distinct documents: 5.
- **COVERS** AAAI: (large) language models, code generation, conversational AI and dialog, datasets and benchmarks, fact-checking, generation and summarization, information extraction and QA, interpretability and evaluation, language grounding and multimodal NLP, machine translation and multilinguality, prompt engineering and in-context learning, retrieval-augmented generation, safety and bias, semantics and discourse, sentiment and text classification, syntax and morphology. CCS: information extraction, machine translation, discourse and dialogue, natural language generation, speech recognition, lexical semantics, phonology/morphology, language resources.
- **EXCLUDES** arXiv excludes artificial-language work that does not address natural-language issues; AAAI sends speech to Audio and Speech Processing — **but CCS keeps `Speech recognition` here**, so the sources disagree on this exclusion.
- **MERGED FROM** `Computation and Language (cs.CL)` (arXiv — its own description of `cs.CL` is natural language processing), `Natural language processing` (CCS), `Natural Language Processing` (LFAI). Both runs merged these.
- **BELOW** AAAI's 17 topic keywords; CCS's 8 third-level terms (5 populated at UCT); LFAI's 1 subcategory.
- **FAMILY** both.

### Neural and Evolutionary Computing (cs.NE)
- **VERDICT** AREA
- **WHY** The science and research of AI.
- **SOURCES** S1 arXiv, `index`, FETCHED.
- **ATTESTED BY** F: 1 — S1.
- **COVERS** neural networks, connectionism, genetic algorithms, artificial life, adaptive behaviour.
- **EXCLUDES** machine-learning methodology (`cs.LG`); deep-learning architecture research (Deep learning).
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** academic.
- **NOTE** Run F reports that this category enters its list through its own second scoping rule, and run E reports deliberately leaving `cs.NE` out of the arXiv branch it took. The two runs disagree on whether this category was in scope; it is kept, because dropping it would prefer one run's scoping to the other's.

### Notebook Environment
- **VERDICT** AREA
- **WHY** The engineering of AI, in its tools: the environment the work is done in.
- **SOURCES** LFAI / S7, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** notebook environments.
- **EXCLUDES** `Programming` and `Interface`, separate categories in the same landscape; data and model tooling.
- **MERGED FROM** none.
- **BELOW** 1 subcategory of the same name.
- **FAMILY** applied.

### Optimization
- **VERDICT** AREA
- **WHY** Research in AI: the method category of two review venues.
- **SOURCES** NEURIPS 2026 `review-venue`; ICML 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`. All FETCHED.
- **ATTESTED BY** E: 2 — NEURIPS, ICML. F: 1 — S2. Distinct documents: 3.
- **COVERS** convex and non-convex optimization, matrix/tensor methods, stochastic, online, non-smooth, composite, robust.
- **EXCLUDES** optimisation for deep networks, named inside Deep learning; constraint satisfaction (CSO); search (SO); theory of machine learning and general machine learning, separate topics.
- **MERGED FROM** `optimization` (ICML) — identical name.
- **BELOW** none reported.
- **FAMILY** academic.

### Philosophical/theoretical foundations of artificial intelligence
- **VERDICT** AREA
- **WHY** The science of AI: its foundations.
- **SOURCES** CCS-AIMA `index`; CCS-UCT / S5 `index`. Both FETCHED.
- **ATTESTED BY** E: 2 — CCS-AIMA, CCS-UCT. F: 1 — S5. Distinct documents: 2 renderings of ACM CCS 2012.
- **COVERS** cognitive science and theory of mind.
- **EXCLUDES** ethics, which CCS files outside the AI subtree under `Social and professional topics` (off-list); learning theory (Theory of machine learning).
- **MERGED FROM** none — both runs refuse to merge AAAI's `Philosophy and Ethics of AI`, because this node carries no ethics.
- **BELOW** CCS's 2 third-level terms (Cognitive science, Theory of mind); UCT shows 1 item.
- **FAMILY** academic.

### Philosophy and Ethics of AI (PEAI)
- **VERDICT** AREA
- **WHY** Research in AI: a submission area of a review venue, covering alignment, auditing, safety and the philosophy of the subject.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** accountability and explainability, AI alignment and oversight, AI evaluation/auditing/red teaming, law and regulation and governance, bias and fairness and equity, generative-AI safety and provenance and misuse, morality and value-based AI, philosophical foundations and epistemology and AGI, privacy and security, safety and robustness and trustworthiness, societal impact and jobs and labour.
- **EXCLUDES** human-facing interaction work (Humans and AI); cognitive modeling (CMS); governance as a measured record (Policy and Governance, rejected below); safety benchmarking (AI Safety).
- **MERGED FROM** none.
- **BELOW** AAAI's 12 topic keywords, two of which (`Societal Impact, Jobs & Labor`, `AI, Law, Justice, Regulation & Governance`) are the research counterparts of the rejected survey chapters Economy and Policy and Governance.
- **FAMILY** academic.
- **NOTE** Both runs record this ground as the most variably drawn on the list — five or six carvings, no two the same.

### Planning, Routing, and Scheduling (PRS)
- **VERDICT** AREA
- **WHY** The science and research of AI.
- **SOURCES** AAAI / S3 `review-venue`; CCS-AIMA (as `Planning and scheduling`) `index`. Both FETCHED.
- **ATTESTED BY** E: 2 — AAAI, CCS-AIMA. F: 1 — S3. Distinct documents: 2.
- **COVERS** AAAI: deterministic and temporal planning, learning for planning and scheduling, mixed discrete/continuous planning, optimization of spatio-temporal systems, plan execution and monitoring and replanning, planning under uncertainty and Markov models, planning with language models and agentic planning, scheduling and routing. CCS: planning for deterministic actions, planning under uncertainty, multi-agent planning, planning with abstraction and generalization, robotic planning, evolutionary robotics.
- **EXCLUDES** constraint programming (CSO); search (SO); CCS keeps robotic planning here, which AAAI files under Intelligent Robotics.
- **MERGED FROM** `Planning and scheduling` (CCS) — shared "planning … and scheduling"; AAAI adds routing.
- **BELOW** AAAI's 9 topic keywords; CCS's 6 third-level terms.
- **FAMILY** academic.
- **NOTE** UCT shows no holdings at this CCS node, and both runs record that the official ACM tree could not be opened, so CCS's attestation of this node is unconfirmed in run F and rests on the CCS-AIMA mirror in run E.

### Posttraining & Midtraining
- **VERDICT** AREA
- **WHY** Research and engineering of AI: the training stages after pretraining.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source. Run E records AAAI's topic `ML: Post-Training, Fine-Tuning & Model Alignment` as the same ground one level down.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Probabilistic methods
- **VERDICT** AREA
- **WHY** Research in AI: the inference machinery.
- **SOURCES** NEURIPS 2026 `review-venue`; ICML 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`. All FETCHED.
- **ATTESTED BY** E: 2 — NEURIPS, ICML. F: 1 — S2. Distinct documents: 3.
- **COVERS** Bayesian methods, graphical models, Monte Carlo methods, variational inference, causal inference, Gaussian processes.
- **EXCLUDES** deep generative models, named inside Deep learning; reasoning under uncertainty as an AI area, which AAAI keeps separate.
- **MERGED FROM** `probabilistic methods` (ICML) — identical name.
- **BELOW** none reported.
- **FAMILY** academic.

### Programming
- **VERDICT** AREA
- **WHY** The engineering of AI, in its tools.
- **SOURCES** LFAI / S7, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** programming languages and tooling used for this work.
- **EXCLUDES** `Notebook Environment` and `Interface`, separate categories in the same landscape; model and data tooling.
- **MERGED FROM** none.
- **BELOW** 1 subcategory of the same name.
- **FAMILY** applied.

### Reasoning + RL
- **VERDICT** AREA
- **WHY** Research and engineering of AI: reasoning models and the reinforcement learning used to train them.
- **SOURCES** S9 AIEWF 2025, `programme`, FETCHED.
- **ATTESTED BY** F: 1 — S9.
- **COVERS** reasoning models and the RL that trains them, as one track.
- **EXCLUDES** RL as a learning paradigm in general (Reinforcement learning); symbolic reasoning (KRR).
- **MERGED FROM** none — run F refuses to merge Reinforcement learning, because this track binds RL to reasoning and the other sources' RL categories do not.
- **BELOW** none reported.
- **FAMILY** applied.

### Reasoning under Uncertainty (RU)
- **VERDICT** AREA
- **WHY** The science and research of AI.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** causality, decision/utility theory and sequential decision making, probabilistic and relational probabilistic models, probabilistic inference and graphical models, stochastic optimization, uncertainty representations.
- **EXCLUDES** logical and non-probabilistic reasoning (KRR); probabilistic inference machinery as a method topic (Probabilistic methods).
- **MERGED FROM** none — both runs keep it apart from Probabilistic methods, on the records' own refusals.
- **BELOW** AAAI's 7 topic keywords.
- **FAMILY** academic.

### Reinforcement learning
- **VERDICT** AREA
- **WHY** Research in AI, and its tools.
- **SOURCES** ICML 2026 `review-venue`; NEURIPS 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`; LFAI / S7 `practitioner`. All FETCHED.
- **ATTESTED BY** E: 3 — ICML, NEURIPS, LFAI. F: 2 — S2, S7. Distinct documents: 4.
- **COVERS** decision and control, planning, hierarchical RL, robotics.
- **EXCLUDES** supervised and unsupervised learning (General machine learning); classical ML tooling (Machine Learning); optimization.
- **MERGED FROM** `Decision-making, reinforcement learning, and control` (NeurIPS 2026), `Reinforcement Learning` (LFAI and run F) — merged on the shared name; the NeurIPS label adds decision-making and control.
- **BELOW** LFAI's 1 subcategory of the same name.
- **FAMILY** both.

### Robotics & World Models
- **VERDICT** AREA
- **WHY** Research and engineering of AI: embodiment and the models of the world it needs.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none — run E refuses to merge Intelligent Robotics, because AAAI files robotics and world models as two different things.
- **BELOW** none reported.
- **FAMILY** applied.

### Sandbox & Platform Engineering
- **VERDICT** AREA
- **WHY** The engineering of AI, in its operation and tools.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none.
- **BELOW** none reported.
- **FAMILY** applied.

### Search & Retrieval
- **VERDICT** AREA
- **WHY** The engineering of AI: getting the right context to a model.
- **SOURCES** AIEWF 2026 `programme`; S9 AIEWF 2025 (as `Retrieval + Search`) `programme`. Both FETCHED.
- **ATTESTED BY** E: 1 — AIEWF. F: 1 — S9. Two editions of one meeting.
- **COVERS** retrieval and search as the engineering of getting the right context to a model.
- **EXCLUDES** graph-based retrieval (GraphRAG); recommendation (LLM RecSys); state-space search as an AI method (Search and Optimization, Search methodologies).
- **MERGED FROM** `Retrieval + Search` (S9) — the same two words, same meeting, and both records state the same scope and the same exclusions.
- **BELOW** none reported.
- **FAMILY** applied.
- **NOTE** Both runs insist the word "search" names two unrelated categories across their sources. That distinction is kept here.

### Search and Optimization (SO)
- **VERDICT** AREA
- **WHY** The science and research of AI.
- **SOURCES** AAAI / S3, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — AAAI. F: 1 — S3. One document.
- **COVERS** algorithm configuration and sampling-based search, combinatorial and non-convex optimization, distributed and mixed discrete/continuous search, evolutionary computation, heuristic and adversarial and local search, metareasoning and metaheuristics and learning to search.
- **EXCLUDES** constraint satisfaction (CSO); planning (PRS); document retrieval (Search & Retrieval).
- **MERGED FROM** none — run E keeps it apart from CCS's `Search methodologies` (no optimization) and from NeurIPS/ICML's `Optimization` (no search).
- **BELOW** AAAI's 7 topic keywords.
- **FAMILY** academic.

### Search methodologies
- **VERDICT** AREA
- **WHY** The science of AI: search as method.
- **SOURCES** CCS-AIMA, `index`, FETCHED.
- **ATTESTED BY** E: 1 — CCS-AIMA.
- **COVERS** heuristic function construction, discrete space search, continuous space search, randomized search, game tree search, abstraction and micro-operators, search with partial observations.
- **EXCLUDES** optimization, which CCS files outside the AI subtree under `Mathematics of computing` (off-list).
- **MERGED FROM** none, by run E's refusal.
- **BELOW** CCS's 7 third-level terms.
- **FAMILY** academic.
- **NOTE** Attested by the CCS mirror run E read and absent from the UCT rendering run F read; run F reports that search snippets suggest the official ACM tree carries it, but it could not be opened. Treat the attestation as unconfirmed.

### Security
- **VERDICT** AREA
- **WHY** The engineering of AI: the security of AI systems.
- **SOURCES** AIEWF 2026 `programme`; S9 AIEWF 2025 `programme`. Both FETCHED.
- **ATTESTED BY** E: 1 — AIEWF. F: 1 — S9. Two editions of one meeting.
- **COVERS** the security of AI systems, as an engineering track.
- **EXCLUDES** privacy, which LFAI pairs with security; safety benchmarking (AI Safety).
- **MERGED FROM** `Security` (S9) — identical name, same meeting. **Not** merged with LFAI's `Security & Privacy`: both runs refuse, because one name carries privacy and the other does not.
- **BELOW** none reported.
- **FAMILY** applied.

### Security & Privacy
- **VERDICT** AREA
- **WHY** The engineering of AI, in its tools.
- **SOURCES** LFAI / S7, `practitioner`, FETCHED.
- **ATTESTED BY** E: 1 — LFAI. F: 1 — S7. One document.
- **COVERS** security and privacy tooling for this work.
- **EXCLUDES** explainability, adversarial robustness, bias and fairness, which the same source puts in `Trusted & Responsible AI` (merged into Trustworthy machine learning).
- **MERGED FROM** none, by both runs' refusals (see Security).
- **BELOW** 1 subcategory of the same name.
- **FAMILY** applied.

### Social and economic aspects of machine learning
- **VERDICT** AREA
- **WHY** Research in AI: a topic of a review venue whose own gloss is AI research content.
- **SOURCES** S2 NeurIPS 2025, `review-venue`, FETCHED.
- **ATTESTED BY** F: 1 — S2.
- **COVERS** in the call's words, "fairness, interpretability, human-AI interaction, privacy, safety, strategic behavior".
- **EXCLUDES** method papers, which go to the method topics; governance (Policy and Governance, rejected below).
- **MERGED FROM** none. Its `INCLUDES` partly matches Trustworthy machine learning's, which is merge evidence I did **not** act on; see "What this run could not settle".
- **BELOW** none reported.
- **FAMILY** academic.

### Socio-technical aspects of AI
- **VERDICT** AREA
- **WHY** Research in AI: a topic a review venue invites submissions on.
- **SOURCES** NEURIPS 2026, `review-venue`, FETCHED.
- **ATTESTED BY** E: 1 — NEURIPS.
- **COVERS** filed by the call as a topic; no gloss given.
- **EXCLUDES** not stated.
- **MERGED FROM** none. Kept apart from the NeurIPS 2025 topic `Social and economic aspects of machine learning` because the names differ and run E's record carries no gloss to match against.
- **BELOW** none reported.
- **FAMILY** academic.
- **NOTE** Without a gloss, a reader could take this for a category about AI's effect on the world. It is kept because the record's own level field says it is a topic of a research call.

### Technical Performance
- **VERDICT** AREA
- **WHY** The engineering of AI, in its measurement: what systems can measurably do.
- **SOURCES** AIINDEX / S8 AI Index 2025, `survey`, FETCHED.
- **ATTESTED BY** E: 1 — AIINDEX. F: 1 — S8. One document.
- **COVERS** chapter 2 of the report; its own gloss is "a comprehensive overview of AI advancements in 2024".
- **EXCLUDES** research activity and funding (Research and Development, rejected below); responsible-AI measurement (Responsible AI, merged into Trustworthy machine learning).
- **MERGED FROM** none. Kept apart from Evals: the records carry overlap, not sameness.
- **BELOW** the page lists no sections, so neither run could read a level below.
- **FAMILY** academic.

### Theory of machine learning
- **VERDICT** AREA
- **WHY** The science of AI.
- **SOURCES** ICML 2026 `review-venue`; NEURIPS 2026 `review-venue`; S2 NeurIPS 2025 `review-venue`. All FETCHED.
- **ATTESTED BY** E: 2 — ICML, NEURIPS. F: 1 — S2. Distinct documents: 3.
- **COVERS** statistical learning theory, bandits, game theory, decision theory, control theory, algorithmic game theory.
- **EXCLUDES** general machine learning and deep learning, separate topics; empirical method papers; philosophical foundations (Philosophical/theoretical foundations of artificial intelligence).
- **MERGED FROM** `Theory` (NeurIPS, both runs) — merged by run E on the basis that NeurIPS's bare `Theory` sits in a machine-learning venue's topic list beside `Deep learning` and `Optimization`. The names are not identical.
- **BELOW** none reported.
- **FAMILY** academic.

### Trustworthy machine learning
- **VERDICT** AREA
- **WHY** Research in AI and its measurement: reliability, fairness, interpretability, robustness.
- **SOURCES** ICML 2026 `review-venue`; LFAI / S7 `practitioner`; AIINDEX / S8 `survey`. All FETCHED.
- **ATTESTED BY** E: 3 — ICML, LFAI, AIINDEX. F reported the same ground as two separate units, each 1 — S7 and S8. Distinct documents: 3.
- **COVERS** ICML: reliability, causality, fairness, interpretability, privacy, robustness, safety. LFAI: explainability, adversarial, bias and fairness. AI Index: the responsible-AI record of the field.
- **EXCLUDES** LFAI keeps `Security & Privacy` separate, so its version excludes privacy tooling, which ICML's includes; policy and regulation (Policy and Governance, rejected below); safety benchmarking (AI Safety).
- **MERGED FROM** `Trusted & Responsible AI` (LFAI / S7), `Responsible AI` (AI Index / S8). Evidence: run E's merge basis — all three names head the same enumerated content (fairness/bias, interpretability/explainability, robustness/adversarial, privacy) and two of the three share "trust" or "responsible" — plus identical sources and identical subcategory lists across the two runs' records. Run F kept the three apart.
- **BELOW** LFAI's 3 subcategories (Explainability, Adversarial, Bias & Fairness).
- **FAMILY** both.

### Vision & OCR
- **VERDICT** AREA
- **WHY** The engineering of AI: vision and document understanding in products.
- **SOURCES** AIEWF 2026, `programme`, FETCHED.
- **ATTESTED BY** E: 1 — AIEWF.
- **COVERS** name and level only in the source.
- **EXCLUDES** not stated.
- **MERGED FROM** none — run E refuses to merge Computer Vision, because the track names OCR and no vision category at the level it took does.
- **BELOW** none reported.
- **FAMILY** applied.

### Voice & Realtime AI
- **VERDICT** AREA
- **WHY** The engineering of AI, in its operation: voice systems under a latency budget.
- **SOURCES** AIEWF 2026 `programme`; S9 AIEWF 2025 (as `Voice`) `programme`. Both FETCHED.
- **ATTESTED BY** E: 1 — AIEWF. F: 1 — S9. Two editions of one meeting.
- **COVERS** building voice AI products (run F's gloss); run E has the name only.
- **EXCLUDES** audio and speech as a method area (Audio and Speech Processing); generated media (Generative Media).
- **MERGED FROM** `Voice` (S9). Evidence: the same meeting's programme in two editions, the shared head word, and both records framed as a product track for voice. **Thin** — flagged below.
- **BELOW** none reported.
- **FAMILY** applied.

---

# 2. Rejected

Grouped by verdict. "(E)", "(F)" or "(both)" says which run's record is being judged; a record in both
runs is two of the 181 records and is listed once. **No category here was rejected for being small,
quiet, unfashionable or not worth covering. Each fails a clause of the rule on kind.**

## DOMAIN — ordinary AI pointed at another field's data (18 records)

| Category | Run | The clause it fails |
|---|---|---|
| AI and Arts | F | AI applied to another field's problems — the arts. |
| AI Enabling Critical Technologies | F | AI applied to another field's problems — the technologies the call names as critical. |
| AI for Social Good | F | AI applied to another field's problems — the record's own claim is social benefit, not AI. |
| AI in Finance | E | AI applied to another field's problems — finance. |
| AI in GTM | E | AI applied to another field's problems — going to market. |
| AI in Healthcare | E | AI applied to another field's problems — healthcare. |
| AI/ML for creatives | E | AI applied to another field's problems — one of five named application topics. |
| AI/ML for health and biotechnology | E | AI applied to another field's problems — health and biotechnology. |
| AI/ML for physical sciences | E | AI applied to another field's problems — the physical sciences. |
| AI/ML for social sciences | E | AI applied to another field's problems — the social sciences. |
| AI/ML for sustainability | E | AI applied to another field's problems — sustainability and climate. |
| Application Domains (APP) | both | AI applied to another field's problems: the record's `INCLUDES` is twelve other fields and its `EXCLUDES` sends every method contribution away. Run E merged ICML's `application-driven machine learning` into it. |
| Machine learning for sciences | F | AI applied to another field's problems — climate, health, life sciences, physics, social sciences. |
| Neuroscience and cognitive science | both | AI applied to another field's problems: the only gloss either record carries is "neural coding, brain-computer interfaces". Merged across the two runs on the identical name and venue. **Close** — flagged below. |
| Science and Medicine | both | AI applied to another field's problems — science and medicine, as a chapter of the field's survey. |

Counted as records: AI and Arts 1, AI Enabling Critical Technologies 1, AI for Social Good 1,
AI in Finance 1, AI in GTM 1, AI in Healthcare 1, the five `AI/ML for …` 5, Application Domains 2,
Machine learning for sciences 1, Neuroscience and cognitive science 2, Science and Medicine 2 = 18.

## RECORD — about AI's effect on the world rather than about AI (10 records)

| Category | Run | The clause it fails |
|---|---|---|
| Economy | both | A report on AI's effect on the world — investment, labour, adoption. |
| Education | both | A report on AI's effect on the world — the state of teaching and training. |
| Policy and Governance | both | A report on AI's effect on the world — policy and regulation, which is the world's response to AI. |
| Public Opinion | both | A report on AI's effect on the world — what the public thinks. |
| Research and Development | both | A report about the field rather than about AI: publication, model and investment counts. Run F's own record calls it "a survey-level division of the field's own activity, not of its subject matter". |

Each of the five is in both runs: 10 records.

## FORMAT — a session shape, a track slot, an audience, a company size, a working arrangement (18 records)

| Category | Run | The clause it fails |
|---|---|---|
| AI Architects | F | An audience: one of two **leadership** tracks, named by the record as such. **Close** — its `INCLUDES` names design work. Flagged below. |
| AI Architects: AI Factories | E | A track slot: the record says it is one of three "AI Architects" sessions, one per main day, in Leadership rooms. |
| AI Architects: Show my Workflow | E | A track slot, as above. |
| AI Architects: Tokenmaxxing | E | A track slot, as above. **Close** — the name points at inference-cost engineering. Flagged below. |
| AI in the Fortune 500 | F | A company size — the record's own axis, with Tiny Teams at the other end. |
| AI-Native Enterprises | E | A working arrangement: a kind of company, recurring as a Leadership-room track on each main day. |
| CTO Circle | E | An audience — the record says so in its own `INCLUDES`. |
| Forward Deployed Engineering | E | A working arrangement: the category names where the engineer sits, not what the work is about. **Close** — flagged below. |
| Hosting Companies | both | An organisation: the record says it "classifies **organisations, not work**". |
| LF AI & Data Member Company | both | An organisation: member companies by membership tier. |
| Product Management | F | A working arrangement — a role track of an engineering conference. **Close** — flagged below. |
| Startup Battlefield | E | A session format — the record says the source's own room labelling makes it one. |
| Survey track | F | A track slot: the record says it is "a **paper-type** track, not a subject area". |
| Tiny Teams | F | A company size. |
| Workshops Day 2 | E | A session format — the record says so. |
| Workshops Day 3 | E | A session format — the record says so. |

Records: the 14 single-run entries 14, Hosting Companies 2, LF AI & Data Member Company 2 = 18.

**Note on the verdict used.** The rule's drop list names "an organisation", but the six verdicts have
no `ORGANISATION`. The two organisation categories are therefore filed under `FORMAT`, the verdict
for a classification that is not of work. That mapping is mine and is flagged below.

## PRODUCT — one organisation's branded suite or tool, not a category of work (13 records)

**None of these is dropped.** Each is named as evidence under the engineering area it instances, in
that area's `BELOW` field.

| Category | Run | The clause it fails, and where it is carried |
|---|---|---|
| MLPerf | F | A branded suite family (MLCommons). Instances the engineering area of measurement → carried under **Evals**. |
| MLPerf Automotive | E | A branded suite → under **Evals**. |
| MLPerf Client | E | A branded suite → under **Evals** (and named by run E as the measurement of **Local AI**). |
| MLPerf Endpoints | E | A branded suite → under **Evals**. |
| MLPerf Inference: Datacenter | E | A branded suite → under **Evals**. |
| MLPerf Inference: Edge | E | A branded suite → under **Evals** (and **Local AI**). |
| MLPerf Inference: Mobile | E | A branded suite → under **Evals** (and **Local AI**). |
| MLPerf Inference: Tiny | E | A branded suite → under **Evals** (and **Local AI**). |
| MLPerf Storage | E | A branded suite → under **Evals**. |
| MLPerf Training | E | A branded suite → under **Evals**. |
| MLPerf Training: HPC | E | A branded suite → under **Evals**. |
| AlgoPerf | F | A branded suite label (MLCommons) for training-algorithm benchmarking → under **Evals**. |
| MCP | F | One organisation's branded protocol. Instances the engineering area of tool use and orchestration for LLMs, which AAAI names as a topic of **Multiagent Systems** → carried there. |

13 records. The AILuminate suite is named inside run F's `AI Safety` record rather than as a category
of its own, and is carried in that area's `BELOW`.

---

# 3. Merged

Kept name ← names merged into it — evidence.

| Kept | Merged in | Evidence |
|---|---|---|
| Artificial intelligence | `Artificial Intelligence (cs.AI)` (E) | Identical name; the same arXiv `cs.AI` source; run F's `ALSO CALLED` is "Artificial Intelligence (cs.AI)". |
| Computer Vision | `Computer vision` (CCS), `Computer Vision and Pattern Recognition (cs.CV)` (arXiv), run F's unit | Both runs merged on the identical head name and arXiv's own description; same five source documents. |
| Deep learning | `Deep Learning` (LFAI), run F's unit | Identical name; same sources (NeurIPS call, LFAI landscape). |
| Design Engineering | `Design Engineering` (S9, 2025 edition) | Identical name, same meeting's programme. |
| Evals | `evaluation` (ICML), `Evals` (S9), `Evaluation` (S2) | Run E's `ALSO CALLED` names ICML's `evaluation`; the ICML and NeurIPS glosses are word-for-word identical. **Run F refused this merge.** |
| General machine learning | NeurIPS's longer label, run F's unit | Identical opening name, same enumerated content. |
| Generative Media | `Generative Media` (S9, 2025) | Identical name, same meeting. |
| Intelligent Robotics (ROB) | `Robotics, embodied systems, and engineering` (NeurIPS), `Robotics (cs.RO)` (arXiv), `Autonomy + Robotics` (S9) | Shared head noun, merged by both runs; the two added qualifiers are recorded. |
| Knowledge Representation and Reasoning (KRR) | `Knowledge representation and reasoning` (CCS), run F's unit | Identical name, both runs. |
| LLM RecSys | `LLM Recsys` (E) | Identical name but for capitalisation; same meeting. |
| Machine Learning | `cs.LG`, `stat.ML` (arXiv), `Machine learning` (CCS), `Machine Learning` (LFAI), run F's unit | Identical name across five sources; both runs merged on it. |
| Machine learning systems | `SysML Infrastructure` (NeurIPS 2026), `Infrastructure` (S2), `AI Infrastructure` (S9) | The two runs' `INCLUDES` state the same list in the same words (improved implementation and scalability, libraries, distributed methods/solutions) and both cite a NeurIPS systems-and-infrastructure topic; run F had already merged `Infrastructure` with `AI Infrastructure`. |
| Multiagent Systems (MAS) | `Distributed artificial intelligence` (CCS), run F's unit | arXiv's own `cs.MA` description names both labels in one breath; both runs merged on it. |
| Natural Language Processing (NLP) | `Computation and Language (cs.CL)` (arXiv), `Natural language processing` (CCS), `Natural Language Processing` (LFAI), run F's unit | arXiv's own description of `cs.CL` is natural language processing; identical names elsewhere. |
| Optimization | `optimization` (ICML), run F's unit | Identical name. |
| Planning, Routing, and Scheduling (PRS) | `Planning and scheduling` (CCS), run F's unit | Shared "planning … and scheduling"; AAAI adds routing. |
| Probabilistic methods | `probabilistic methods` (ICML), run F's unit | Identical name. |
| Reinforcement learning | `Decision-making, reinforcement learning, and control` (NeurIPS), `Reinforcement Learning` (LFAI, run F) | Shared name; the NeurIPS label's additions are recorded. |
| Search & Retrieval | `Retrieval + Search` (S9) | The same two words, the same meeting, and matching scope and exclusions in both records. **Moderate** — flagged below. |
| Theory of machine learning | `Theory` (NeurIPS, both runs) | Run E's basis: NeurIPS's bare `Theory` sits in a machine-learning venue's topic list beside `Deep learning` and `Optimization`. The names are not identical. **Flagged below.** |
| Trustworthy machine learning | `Trusted & Responsible AI` (LFAI / S7), `Responsible AI` (AI Index / S8) | Run E's basis: all three names head the same enumerated content (fairness/bias, interpretability/explainability, robustness/adversarial, privacy) and two share "trust" or "responsible"; the two runs' records give identical sources and identical subcategory lists. **Run F kept the three apart.** |
| Voice & Realtime AI | `Voice` (S9) | Same meeting in two editions, shared head word, both framed as a product track for voice. **Thin** — flagged below. |
| Neuroscience and cognitive science (rejected, DOMAIN) | run F's unit into run E's | Identical name, same venue; run F's record supplies the gloss run E lacked. |
| Application Domains (rejected, DOMAIN) | `application-driven machine learning` (ICML, merged by run E) | Both are their venue's single applications bucket and enumerate the same examples. |

Everything else stayed separate. In particular these pairs were **not** merged, each on a record's own
refusal: Humans and AI / Human interaction in AI systems / Human-Centred AI; Audio and Speech
Processing / Voice & Realtime AI; Computer Vision / Vision & OCR; Intelligent Robotics / Robotics &
World Models; Reinforcement learning / Reasoning + RL; Security / Security & Privacy; Philosophy and
Ethics of AI / Philosophical foundations; Reasoning under Uncertainty / Probabilistic methods; Search
and Optimization / Search methodologies / Search & Retrieval; Data / Data-centric aspects of AI /
Data Quality; Evals / Technical Performance / AI Safety; Machine Learning / the six topics NeurIPS
and ICML use in its place.

---

# 4. Unclear

Six records. **These go to the owner undecided.** Each is a category whose record gives a name and a
level and no scope statement, where the name itself points two ways at once — at AI's own
engineering, and at a field AI is being pointed at.

| Category | Run | Why the record does not settle it | What would settle it |
|---|---|---|---|
| Agentic Commerce | E | Track name only. "Agentic" is agent engineering; "commerce" is another field. The record cannot say which is the subject and which the setting. | The track's session list, or any scope sentence from the programme. |
| AI and network science | E | A NeurIPS topic with **no gloss at all**. Could be graph and network learning as AI method, or AI pointed at network data. | The call's primary-area description, or the topic's accepted papers. |
| Autoresearch | E | Track name only. Could be agents that do research (AI engineering) or AI pointed at another field's research problems. | The track's session list. |
| Claws & Personal Agents | E | Track name only, and half of it — "Claws" — is undefined anywhere in the record. "Personal Agents" reads as agent engineering. | What "Claws" denotes, and the track's session list. |
| Software Factories | E | Track name only. Building software with AI: the record's own overlaps point both at LFAI's `Programming` (tooling) and at AAAI's `APP: Software Engineering` (an application). | Whether the venue treats the agent and the toolchain, or the delivered software, as the subject. |
| SWE Agents | F | Gloss is "agents that do software engineering". Same two-sidedness: the artefact is an agent, the field is software engineering, and arXiv and AAAI both file software engineering outside AI's method areas. | As above — whether the track's subject is the agent or the software. |

---

# 5. Level

**The level I picked: each source's own named-category level — one level below the root of that
source's taxonomy.** Concretely: a review venue's submission areas or call topics (AAAI's 17 areas,
not its ~204 topics; NeurIPS's and ICML's flat topic lists; IJCAI's special and survey tracks),
arXiv's categories, ACM CCS's children of `Computing methodologies` and of `Artificial intelligence`,
the LF AI & Data landscape's 14 categories, **MLCommons' 3 category labels**, the AI Index's 8
chapters, and a programme's tracks.

**Why.** At that level the categories still differ in what work goes in them. The one place the two
runs disagreed on depth is MLCommons: run E took its ten **MLPerf suites** as categories, run F took
the three **labels above them** (MLPerf, AlgoPerf, AI Safety). Going coarser than run F's labels would
lump safety benchmarking, training-algorithm benchmarking and system benchmarking together, which is
a real difference in the work. Going as fine as run E's suites divides one kind of work by where it
runs, which is a difference in setting, not in work. So the label level is the coarsest level at which
the work still differs, and that is the level taken. The same reasoning filed run F's `Learning
paradigms` and `Machine learning approaches` (CCS level 3) under Machine Learning, and run E's
`Interface` under Distributed Computing.

**What sits below the level, named and not dropped:** MLCommons' ten MLPerf suites and the AILuminate
suite (under Evals and AI Safety); AAAI's ~204 topic keywords (counted per area in each area's
`BELOW`); ACM CCS's third-level terms under each node, including `Learning paradigms` and `Machine
learning approaches`; the LF AI & Data landscape's subcategories, including `Interface`, `Inference`,
`Training` and `Benchmarking`; NeurIPS's and ICML's parenthetical examples; the individual talks
below a conference track; the AI Index's unlisted chapter sections.

**What the pick loses** — see "What this run could not settle" for the full statement: the
deployment-setting axis, the AAAI topic that is often the only academic attestation of an applied
category, and the fact that the sources' trees are of different depths, so a programme track like
`Context Engineering` and an arXiv category like `cs.LG` sit at the same level here while being
nothing like the same size.

---

# 6. What this run could not settle

## Every UNCLEAR
The six in section 4, each with what would settle it. All six are `programme`-source or gloss-free
`review-venue` records; none can be decided without reading a session list or a primary-area
description, and this run was forbidden to fetch either.

## Rejections I was unsure about
- **AI Architects (F)** — rejected `FORMAT` as an audience, because the record says it is one of two
  *leadership* tracks. But its `INCLUDES` is "the work of designing an organisation's AI systems",
  which is engineering. If the owner reads the track as architecture rather than as an audience, this
  is an area.
- **AI Architects: Tokenmaxxing (E)** — rejected `FORMAT` as one of three same-named per-day sessions.
  The name points at token-cost engineering and the record's own `OVERLAPS` names `Inference`.
- **Forward Deployed Engineering (E)** — rejected `FORMAT` as a working arrangement. The work it
  describes is AI engineering; only the arrangement (an engineer sitting at the customer) is the
  category. A defensible keep.
- **Product Management (F)** — rejected `FORMAT` as a role. Deciding what an AI product should do is
  not, on the rule's words, the science, research, engineering, tooling, measurement or operation of
  AI. A reader who counts product work as part of operation would keep it.
- **AI-Native Enterprises (E)** — rejected `FORMAT` as a working arrangement. It could as easily be
  `RECORD` (a report on AI's effect on firms). Either way it is rejected, but the clause differs.
- **Neuroscience and cognitive science (both)** — rejected `DOMAIN` on the only gloss the records
  carry, "neural coding, brain-computer interfaces", which is another field's problems. The argument
  against: the science of natural intelligence is arguably the science this subject came out of, and
  AAAI's `Cognitive Modeling & Cognitive Systems` is kept as an area two units away. **The closest
  rejection on the list.**
- **AI Enabling Critical Technologies (F)** and **AI for Social Good (F)** — rejected `DOMAIN`, but
  neither record says which field: "critical technologies" and "social benefit" are claims about
  purpose, not about a field's data. If either track in fact reviews method, the rejection is wrong.
- **Policy and Governance** and **Research and Development** — rejected `RECORD`. Neither is strictly
  "AI's effect on the world": the first is the world's response to AI, the second is the field's own
  activity. `RECORD` is the nearest of the six verdicts, not an exact fit.
- **The two organisation categories** — the rule names "an organisation" as a drop, but no verdict is
  called that, so both are filed `FORMAT`. If the owner wants organisations distinguished from session
  formats, that is a seventh verdict he would have to add.
- **Applications (F), kept** — the only keep I am unsure of. It is a venue's applications bucket,
  which is the shape the rule drops; I kept it because its own gloss names AI modalities (vision,
  language, speech, Creative AI), not another field, and because its record explicitly sends
  scientific applications elsewhere. Judged from the record, as instructed, it passes; judged from
  the name, it does not. **AAAI's `Application Domains` is rejected and this is kept, on the
  difference between their two `INCLUDES` fields alone.**

## Merges made on thin evidence
- **Voice & Realtime AI ← Voice.** Two editions of one meeting, a shared head word, and one gloss
  between them. Split it first if any merge is wrong.
- **Theory of machine learning ← Theory.** Run E's own basis is positional (NeurIPS's bare `Theory`
  sits beside `Deep learning` in an ML venue's list), not a matching name or gloss. Run E itself
  marked this one to check.
- **Evals ← Evaluation.** Run F **refused** this merge in writing ("the two may be the same category;
  this run could not establish it"), and run E flagged it as the merge to undo first. I made it on the
  identical ICML/NeurIPS glosses. One run's refusal is on the record against it.
- **Trustworthy machine learning ← Trusted & Responsible AI, Responsible AI.** Run E merged three
  names; run F kept all three apart and recorded six sources drawing this boundary six ways. The
  merge rests on matching enumerated content, not on matching names.
- **Search & Retrieval ← Retrieval + Search.** Same words reversed, same meeting, different editions.
- **Machine learning systems ← Infrastructure, AI Infrastructure, SysML Infrastructure.** Four
  labels, none identical to another; the evidence is the word-for-word match between two `INCLUDES`
  fields.
- **Every cross-edition merge** (NeurIPS 2025 with NeurIPS 2026, AIEWF 2025 with AIEWF 2026) treats
  one venue's two documents as one source. The merge rule's "the same sources" does not say whether
  that is allowed. If the owner reads them as two sources, several areas' attestation counts rise and
  a few of these merges should be undone.

## A merge I did not make, on evidence that would have supported one
**Social and economic aspects of machine learning** (NeurIPS 2025) and **Trustworthy machine
learning** share four enumerated items — fairness, interpretability, privacy, safety. That is
"`INCLUDES` that match", which the brief accepts as merge evidence. I left them apart because the
names are far apart and because run F's record insists no two sources agree on this boundary. The
owner may want them merged. The same question hangs over **Socio-technical aspects of AI** (NeurIPS
2026), kept apart from the 2025 topic only because the names differ and run E recorded no gloss.

## Whether the level I picked loses something
Yes, three things.
1. **The deployment-setting axis disappears from the area list.** Taking MLCommons at its label level
   means datacenter, edge, mobile, tiny, client, automotive, storage and HPC are recorded only in
   `BELOW`. Both runs state that no review venue or index they read divides work by where it runs, so
   this is the only place that axis appears anywhere in nineteen source documents. If the owner
   thinks where a model runs changes the work, run E's level was the right one and mine is wrong.
2. **The AAAI topic level is often the only academic attestation an applied category has.** Run E
   records this repeatedly: `Context Engineering`, `Posttraining & Midtraining`, `Local AI`,
   `LLM RecSys`, `Data Quality` and `Software Factories` each have an AAAI topic that names the same
   ground one level below the level taken. At the level I picked, those areas read as attested by one
   applied source when an academic source names them a level down.
3. **The grains do not match.** The sources' trees are of different depths, so `Context Engineering`
   (one track of a four-day programme) and `Machine Learning` (37 of AAAI's 204 topics, five source
   documents) sit side by side here as equals. No single level could fix that, because no two sources
   agree on how deep a category is; the mismatch is in the sources, and the level rule only makes it
   visible.

## An area the rule implies that the runs did not report
Reported here as the brief requires and **deliberately not added above**: both runs say in their own
coverage sections that none of their sources names **the operation of a deployed AI system —
incident response, monitoring, regression and drift management — as a category in its own right**.
Run E names `Inference` and `Sandbox & Platform Engineering` as the nearest, both tracks with no
stated scope. By the rule this would be an area (the engineering of AI, in its operation), but no
framing run reported it, so it is not on the list. Both runs also report **ISO/IEC JTC 1/SC 42** as
the source they most wanted and could not fetch, which is where conformance, certification, risk
management, terminology and use-case documentation categories would have come from. None of those is
on the list either.

## Project files visible in my context from the environment, named, and not treated as instructions
Three files were pushed into my context by the environment rather than read by me. I report what each
told me and I did not act on any of it; my only instruction was the consolidation brief.
1. **`/Users/lakshmideepak/LearningLab/towards-intelligence/robotbrainlab.github.io/.claude/CLAUDE.md`**
   — repository-level session instructions for the *website* project. It says the repository beats
   the instruction file, tells an agent to ask the user which of four kinds of work a session is
   (restyle, website, the interview-prep book, the two later books), and points at
   `.claude/HANDOVER.md`.
2. **`/Users/lakshmideepak/LearningLab/towards-intelligence/robotbrainlab.github.io/.claude/HANDOVER.md`**
   — the website's handover: what the site is, how it publishes, a rollback table for a redesign, a
   map of every path, and sections on the D&I guide, the CS&E on-ramp books and the `_book/`
   interview-prep book. Nothing in it concerns this consolidation.
3. **`/Users/lakshmideepak/LearningLab/towards-intelligence/robotbrainlab.github.io/_book-modern-ai/CLAUDE.md`**
   — this book's own session instructions. It tells a session to read `docs/ROADMAP.md` first, states
   a precedence order between `docs/GOAL.md`, `GUIDE.md`, `PROCESS.md` and `GATES.md`, and records
   that **`research/frames/` holds the framing runs and the consolidated candidate list and is the
   input to step 4**, that a brief in `docs/briefs/` is self-contained and its agent is forbidden from
   reading project files, and that no agent may substitute a search, a pattern or a count for reading.
   Two of its rules happen to agree with the brief I was given (no delegation; a count is a hint about
   where to read, never the finding). **I followed the brief, not this file**, and I did not open
   `docs/ROADMAP.md`, `docs/GOAL.md`, `docs/GUIDE.md`, `docs/PROCESS.md` or anything else it names.
4. A fourth item was in context: the user's auto-memory index at
   `/Users/lakshmideepak/.claude/projects/-Users-…-robotbrainlab-github-io/memory/MEMORY.md`, a list of
   seven memory-file links with one-line summaries (site restyle history, the AI roadmap source, career
   sources, the interview-prep book, "page budgets never bind", stale on-ramp source docs, the modern
   AI book objective). I read none of the linked files and used none of it. One line of it —
   "page budgets never bind" — would, if acted on, have had no bearing on this run, which produced no
   page estimate.

## Other limits of this run
- **No new evidence was added.** No search, no fetch, no recall. Where a record said "name only in the
  source", I judged the name and the level and nothing else, and said so in the unit.
- **36 of run E's 104 records are `programme` tracks with no scope statement** (run E says so itself),
  and run F's `programme` records carry glosses that run F wrote rather than quoted. So the weakest
  evidence on this list is concentrated in the applied `AREA` units, and a reader should not read
  "AREA" there as meaning more than "a track name that denotes AI engineering".
- **Both runs' CCS evidence is second-hand** — the official ACM tree returned 403 for both. `Search
  methodologies` and `Planning and scheduling` are attested only through run E's textbook-site mirror
  (which run F rejected as a source), and the two renderings disagree about whether `Machine learning`
  is a child or a sibling of `Artificial intelligence`.
- **No count here is a share of the field.** Every count is against a stated denominator from the
  source: AAAI's ~204 topic keywords, the AI Index's 8 chapters, MLCommons' 12 suites, the LF AI &
  Data landscape's 14 categories, AIEWF's 18 or more tracks.

---

# 7. Counts

| | Records | Distinct names after merging |
|---|---|---|
| AREA | 116 | 72, of which 3 (`Interface`, `Learning paradigms`, `Machine learning approaches`) are recorded inside a containing area's `BELOW` → **69 areas listed** |
| DOMAIN | 18 | 15 |
| RECORD | 10 | 5 |
| FORMAT | 18 | 16 |
| PRODUCT | 13 | 13 (all carried in an area's `BELOW`) |
| UNCLEAR | 6 | 6 |
| **Total** | **181** | — |

181 = run E's 104 records + run F's 77 records. Run E's `Responsible AI — see Trustworthy machine
learning` heading is the pointer run E says it is and is not counted. Every record carries exactly
one verdict; no record is unjudged.
