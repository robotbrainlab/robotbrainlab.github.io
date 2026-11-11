# Consolidated candidate areas — union of framing runs `h` and `i`

Written 2026-11-12. Input: `2026-11-11-h.md` (172 candidate areas, 9 sources across 5 kinds) and
`2026-11-11-i.md` (135 candidate areas, 10 sources across 5 kinds). Nothing else in the repository
was read, and no new evidence was gathered: no searches, no fetches.

## The rule applied

The book's own title gives the rule. *Research, Science and Engineering* are three modes.

> Keep a category if it belongs to the science of AI, the research in AI, or the engineering of AI
> — and engineering includes its tools, its measurement and its operation.
> Drop it if it belongs to none of the three: AI applied to another field's problems, a report on
> AI's effect on the world, a meeting format or audience, or an organisation.
> A product or tool name is not dropped. It is reported as the engineering area it instances, with
> the product named as evidence.
> Tag every surviving area with the mode or modes it serves.

Nothing was added to this rule, and no category was rejected for being small, quiet or unfashionable.

## Two reading policies I had to fix, because the rule does not state them

Both are stated here so the owner can overturn either one.

**P1 — scope.** A record whose `INCLUDES` says the source gave a name and a level and nothing more
cannot be an `AREA`; the verdict is `UNCLEAR` and what would settle it is a scope statement from the
source. I treated **an enumerated child list as scope**: the ACM CCS nodes name their child concepts
and the AAAI-26 areas name their keywords, and those lists say what work goes in the box. I did
**not** treat a bare name as scope, however unambiguous it looks — so *Graphs*, *Harness
Engineering*, *Evals*, *Security*, *Vision* and *Language* are all `UNCLEAR`.

**P2 — rejecting without a scope statement.** Where the record states the label's *kind* on the
source's own evidence ("names a leadership room", "a container label", "an audience label", "a
company-size label", "a job-function label", "a day of workshops", "an ad hoc group named for the
committee's own procedure"), I rejected on that stated kind. Where the record states nothing about
kind, I did not reject; the verdict is `UNCLEAR`.

**One verdict has no bucket in the brief.** Thirty-odd arXiv `cs` categories and six ACM CCS
siblings are *not AI at all* — operating systems, networking, numerical analysis, computer graphics.
They fail the keep clause ("belongs to none of the three"), but none of `DOMAIN`, `RECORD`, `FORMAT`
or `PRODUCT` names that case. I filed them as `DOMAIN` and said so on every line. Run `i` recorded
the same thing about its own list: taking all 40 arXiv categories "brings in thirty-odd categories
that nobody would call AI … a reader should treat their presence as a property of the instrument."

## Level

**Chosen level: the subject-area level** — the level at which a source's own filer picks a primary
box. That is: an arXiv `cs` subject category (40), an AAAI-26 keyword area (16), a NeurIPS or ICML
topic (12 / 10), a child of "Artificial intelligence" in the ACM CCS (8), an SC 42 working group
(14), an MLCommons suite (12), a conference programme track (36 / 18), a CRFM report subsection (26).

Two adjustments, in opposite directions:

- **Finer than the chosen level, recorded under `BELOW`, never dropped.** ACL Rolling Review's 31
  tracks sit inside Natural Language Processing (run `h`'s own `cs.CL` record: "arXiv carries natural
  language processing as one category; ACL Rolling Review splits the same ground into 31 tracks").
  The ACM CCS level-4 nodes sit inside their level-3 parents. AAAI-26's 296 keywords sit inside its
  16 areas; they are item evidence in run `i`, not units, so they carry no verdict.
- **Coarser than the chosen level.** ACM CCS level 2 wraps eight of the boxes at my level inside one
  node, "Artificial intelligence". I kept that node as an area but marked it as sitting above the
  chosen level, with its eight children named in `BELOW`. I did **not** take CCS level 2 as the
  chosen level, because at that level Computer Vision, Natural Language Processing, Planning and
  Search stop differing in what work goes in them — they become one box.

**What the level loses.** The 31 ACL tracks are distinctions the language community treats as
different work — machine translation is not syntax, and neither is summarization. At the chosen
level they are not areas; they are `BELOW` Natural Language Processing. If the owner wants the book's
language chapters to follow ACL's cut rather than arXiv's, the level has to be re-picked there.
It also loses nothing on the applied side: the programme tracks and the MLCommons suites are already
at their sources' own primary level.

---

## Areas

47 areas. Alphabetical. No other ordering.

| Area | Sources | Named by | Covers, in one clause |
|---|---|---|---|
| AILuminate | 1 | applied | safety assessment of general chatbot generative-AI systems |
| AlgoPerf: Training Algorithms Benchmark Results | 1 | applied | how much faster a changed training algorithm reaches a target |
| Applications | 1 | academic | work filed by modality — vision, language, speech and audio, Creative AI |
| Artificial intelligence (ACM CCS, above the chosen level) | 1 | academic | the whole subject as one index node, split into eight children |
| Cognitive Modeling & Cognitive Systems | 1 | academic | cognitive architectures, analogy, simulating human behaviour |
| Computer Vision | 4 | academic | image processing, pattern recognition, scene understanding |
| Constraint Satisfaction and Optimization | 1 | academic | constraint programming, satisfiability, solvers |
| Control methods | 1 | academic | robotic planning, computational control theory, motion path planning |
| cs.AI (Artificial Intelligence) | 1 | academic | AI minus vision, robotics, ML, multiagent and language |
| cs.NE (Neural and Evolutionary Computing) | 1 | academic | neural networks, connectionism, genetic algorithms, adaptive behaviour |
| Data Mining & Knowledge Management | 2 | academic | mining, knowledge graphs, recommendation, semantic web |
| Deep Learning | 2 | academic | architectures, generative models, foundation models, LLMs |
| Evaluation | 3 | academic | methodology, meta studies, replicability and validity, human-in-the-loop |
| Game Theory and Economic Paradigms | 1 | academic | auctions, mechanism design, equilibrium, social choice |
| General Machine Learning | 2 | academic | supervised, unsupervised, online, active, ranking, time series |
| Humans and AI | 2 | academic | interaction, teaming, human computation, accessibility, explainability |
| Infrastructure | 2 | academic | libraries, implementation and scalability, hardware, distributed methods |
| Intelligent Robots | 2 | academic | manipulation, navigation, human-robot interaction, embodied AI |
| Knowledge Representation and Reasoning | 4 | academic | description logics, nonmonotonic reasoning, ontologies, causal and temporal reasoning |
| Machine Learning | 4 | academic | all aspects of ML research, including robustness, explanation, fairness, methodology |
| MLPerf Automotive | 1 | applied | measuring AI computers for driving assistance and in-vehicle systems |
| MLPerf Client | 1 | applied | measuring LLM and other AI workloads on personal computers |
| MLPerf Endpoints | 1 | applied | measuring how fast a system turns inputs into results |
| MLPerf Inference: Datacenter | 1 | applied | measuring inference speed on datacenter systems |
| MLPerf Inference: Edge | 1 | applied | measuring inference speed on edge systems |
| MLPerf Inference: Mobile | 1 | applied | measuring inference on consumer mobile chips and stacks |
| MLPerf Inference: Tiny | 1 | applied | measuring inference on ultra-low-power systems |
| MLPerf Storage | 1 | applied | measuring how fast storage supplies training data |
| MLPerf Training | 1 | applied | measuring time to train a model to a target quality |
| MLPerf Training: HPC | 1 | applied | the same measurement on large-scale supercomputers |
| Multiagent Systems | 4 | academic | multiagent systems, intelligent agents, coordination, distributed AI |
| Natural Language Processing | 4 | academic | extraction, translation, dialogue, generation, speech, lexical semantics |
| Optimization | 2 | academic | convex and non-convex, stochastic, robust, online, matrix and tensor methods |
| Philosophical/theoretical foundations of artificial intelligence | 1 | academic | cognitive science and theory of mind as foundations of the field |
| Philosophy and Ethics of AI | 2 | academic | philosophical foundations, epistemology, morality, safety, accountability |
| Planning and scheduling | 3 | academic | deterministic planning, planning under uncertainty, multi-agent and robotic planning |
| Planning, Routing, and Scheduling | 1 | academic | the same plus routing, plan recognition, planning with language models |
| Probabilistic Methods | 2 | academic | variational and causal inference, Bayesian methods, graphical models, Monte Carlo |
| Reasoning under Uncertainty | 2 | academic | probabilistic inference, graphical models, decision theory, causality |
| Reinforcement Learning | 2 | academic | decision and control, planning, hierarchical RL, robotics |
| Retrieval + Search | 1 | applied | embedding-based retrieval from internal data and agentic search over web and docs |
| Robotics | 3 | academic | robotics as its own category, carved out of cs.AI |
| Search and Optimization | 2 | academic | heuristic, local, adversarial and distributed search, evolutionary computation |
| Search methodologies | 2 | academic | heuristic functions, discrete and continuous search, game tree search |
| Social and economic aspects of machine learning | 1 | academic | fairness, interpretability, human-AI interaction, privacy, safety, strategic behaviour |
| Theory | 3 | academic | control theory, learning theory, algorithmic game theory, bandits, decision theory |
| Trustworthy Machine Learning | 1 | academic | causality, fairness, interpretability, privacy, robustness, safety |

**13 of the 47 were named by applied sources; the other 34 by academic sources only; none by both.**
That is a finding about the framing runs, not about the field: see *What this run could not settle*.

---

## Full unit records

Alphabetical. Source kinds are carried forward from the framing runs: `review-venue`, `index`,
`programme`, `survey`, `practitioner`. `h` and `i` identify the framing run a line came from.

```
NAME            AILuminate
VERDICT         AREA
WHY             A branded suite reported as the engineering area it instances — the measurement of
                an AI system's safety — with the product named as evidence (engineering includes
                its measurement).
SOURCES         MLCommons Benchmark Suites, https://mlcommons.org/benchmarks/ — practitioner — h, i
ATTESTED BY     h: 1 — MLCommons Benchmark Suites listing. i: 1 of 10 — S7.
COVERS          "assesses the safety of general chatbot gen AI systems" "to help guide development,
                inform purchasers and consumers, and support standards bodies and policymakers".
EXCLUDES        Speed and throughput, which the MLPerf suites measure.
MERGED FROM     AILuminate (h) and AILuminate (i) — same source, same label.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            AlgoPerf: Training Algorithms Benchmark Results
VERDICT         AREA
WHY             A branded suite reported as the engineering area it instances — measuring what a
                change of training algorithm buys.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1 — MLCommons. i: 1 of 10 — S7.
COVERS          "Measures how much faster we can train neural network models to a given target
                performance" "by changing the underlying training algorithm."
EXCLUDES        Inference, which the MLPerf Inference suites cover.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            Applications
VERDICT         AREA
WHY             Its quoted contents are AI's own modalities, not another field's problems, so it is
                research in AI.
SOURCES         NeurIPS 2025 Call for Papers — review-venue — h, i
ATTESTED BY     h: 1 — NeurIPS 2025 CFP. i: 1 of 10 — S1.
COVERS          "Applications (e.g., vision, language, speech and audio, Creative AI)".
EXCLUDES        Science applications, which NeurIPS files under Machine learning for sciences;
                theory-first work, which has its own topic.
MERGED FROM     the two runs' identical records.
BELOW           none reported; its examples are Computer Vision, Natural Language Processing and the
                speech material that sits under them.
FAMILY          academic
MODE            research
```

```
NAME            Artificial intelligence (ACM CCS, above the chosen level)
VERDICT         AREA
WHY             It is the science and research of AI as one index node; kept, but flagged, because
                it wraps eight areas that are themselves at the chosen level.
SOURCES         ACM Computing Classification System 2012, SKOS/RDF release — index — h
ATTESTED BY     h: 1 — ACM CCS 2012.
COVERS          No scope note; the source files eight child concepts here: Natural language
                processing; Knowledge representation and reasoning; Planning and scheduling; Search
                methodologies; Control methods; Philosophical/theoretical foundations of AI;
                Distributed artificial intelligence; Computer vision.
EXCLUDES        Machine learning, which the CCS files as a sibling, not here.
MERGED FROM     none.
BELOW           all eight children above — each of which is an area in its own right in this list.
FAMILY          academic
MODE            science, research
```

```
NAME            Cognitive Modeling & Cognitive Systems
VERDICT         AREA
WHY             The science of intelligence as an AI venue files it: architectures and simulations
                of cognition.
SOURCES         AAAI-26 keywords page — review-venue — i
ATTESTED BY     i: 1 of 10 — S3.
COVERS          13 keywords, named in the record: Adaptive Behavior; Affective Computing; Agent
                Architectures; Analogy; Applications; (Computational) Cognitive Architectures;
                Computational Creativity; Conceptual Inference and Reasoning; Neural Spike Coding;
                Other Foundations; Simulating Human Behavior; Social Cognition And Interaction;
                Symbolic Representations.
EXCLUDES        Human-facing interaction work, which AAAI files under Humans and AI.
MERGED FROM     none.
BELOW           the 13 keywords above.
FAMILY          academic
MODE            science, research
```

```
NAME            Computer Vision
VERDICT         AREA
WHY             A research area of AI by every source that files it.
SOURCES         AAAI-26 keywords ("Computer Vision (CV)") — review-venue — i; arXiv taxonomy
                ("cs.CV (Computer Vision and Pattern Recognition)") — index — h, i; ACM CCS 2012
                ("Computer vision") — index — i; AAAI-26 main-track call scope sentence — review-venue — i
ATTESTED BY     i: 4 of 10 — S3, S5, S6, S4. h: 1 — arXiv taxonomy (as cs.CV).
COVERS          "Covers image processing, computer vision, pattern recognition, and scene
                understanding. Roughly includes material in ACM Subject Classes I.2.10, I.4, I.5."
EXCLUDES        Multimedia (cs.MM) and graphics (cs.GR); cs.AI excludes Vision from itself.
MERGED FROM     cs.CV (Computer Vision and Pattern Recognition) [h]; Computer Vision [i, already a
                three-source merge]. Evidence: same source (arXiv cs.CV) and run i's own merge note.
BELOW           CCS's 4 nodes (Computer vision tasks; Image and video acquisition; Computer vision
                representations; Computer vision problems) and AAAI's 26 CV keywords, among them 3D
                Computer Vision, Diffusion Models for Vision, Large Vision Models, Remote Sensing /
                Geospatial AI, Vision for Robotics & Autonomous Driving.
FAMILY          academic
MODE            science, research
```

```
NAME            Constraint Satisfaction and Optimization
VERDICT         AREA
WHY             Research in AI: solver methods, filed as an area by a general-AI venue.
SOURCES         AAAI-26 keywords page — review-venue — i
ATTESTED BY     i: 1 of 10 — S3.
COVERS          12 keywords: Applications; Constraint Learning and Acquisition; Constraint
                Optimization; Constraint Programming; Constraint Satisfaction; Distributed
                CSP/Optimization; Mixed Discrete/Continuous Optimization; Other Foundations;
                Satisfiability; Satisfiability Modulo Theories; Search; Solvers and Tools.
EXCLUDES        Heuristic and adversarial search, which AAAI files under Search and Optimization.
MERGED FROM     none.
BELOW           the 12 keywords above.
FAMILY          academic
MODE            research
```

```
NAME            Control methods
VERDICT         AREA
WHY             A child of "Artificial intelligence" in the index that subdivides AI: the research
                and engineering of acting in the world.
SOURCES         ACM CCS 2012 SKOS release (id 10010147.10010178.10010213) — index — i
ATTESTED BY     i: 1 of 10 — S6.
COVERS          3 child nodes: Robotic planning; Computational control theory; Motion path planning.
EXCLUDES        Task-level planning, which CCS files under Planning and scheduling — the two share
                the node "Robotic planning".
MERGED FROM     none.
BELOW           the 3 nodes above.
FAMILY          academic
MODE            research, engineering
```

```
NAME            cs.AI (Artificial Intelligence)
VERDICT         AREA
WHY             Research in AI, defined by the archive almost all of this work is deposited in.
SOURCES         arXiv category taxonomy — index — h, i
ATTESTED BY     h: 1 — arXiv. i: 1 of 10 — S5.
COVERS          "Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent
                Systems, and Computation and Language … In particular, includes Expert Systems,
                Theorem Proving …, Knowledge Representation, Planning, and Uncertainty in AI."
EXCLUDES        Vision (cs.CV), Robotics (cs.RO), Machine Learning (cs.LG), Multiagent Systems
                (cs.MA), Computation and Language (cs.CL) — named in the source.
MERGED FROM     the two runs' identical records.
BELOW           none reported; the source names Knowledge Representation, Planning and Uncertainty
                in AI as contents, and all three are areas in their own right here.
FAMILY          academic
MODE            research
```

```
NAME            cs.NE (Neural and Evolutionary Computing)
VERDICT         AREA
WHY             The science of the mechanisms modern AI is built from.
SOURCES         arXiv category taxonomy — index — h, i
ATTESTED BY     h: 1 — arXiv. i: 1 of 10 — S5.
COVERS          "Covers neural networks, connectionism, genetic algorithms, artificial life,
                adaptive behavior. Roughly includes some material in ACM Subject Class C.1.3,
                I.2.6, I.5."
EXCLUDES        Nothing in the source's own words; cs.AI does not carve cs.NE out of itself.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          academic
MODE            science, research
```

```
NAME            Data Mining & Knowledge Management
VERDICT         AREA
WHY             Research in AI and its tools, filed as one of a general-AI venue's 16 areas.
SOURCES         AAAI-26 keywords page — review-venue — i; AAAI-26 main-track call ("data mining") — review-venue — i
ATTESTED BY     i: 2 of 10 — S3, S4.
COVERS          19 keywords, including Anomaly/Outlier Detection; Data Stream Mining; Graph Mining
                and Social Network Analysis; Intelligent Query Processing; Knowledge Acquisition
                from the Web; Linked Open Data and Knowledge Graphs; Recommender Systems; Rule and
                Pattern Mining; Scalability, Parallel & Distributed Systems; Semantic Web; Web.
EXCLUDES        Language-model work (AAAI files it under NLP); knowledge representation proper.
MERGED FROM     none.
BELOW           the 19 keywords above.
FAMILY          academic
MODE            research, engineering
```

```
NAME            Deep Learning
VERDICT         AREA
WHY             The science and research of the model class modern AI runs on.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML 2025/2026 CFP — review-venue — h, i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 2 of 10 — S1, S2, plus S3 at keyword level.
COVERS          "Deep learning (e.g., architectures, generative models, optimization for deep
                networks, foundation models, LLMs)"; ICML: "(architectures, generative models,
                theory, etc.)".
EXCLUDES        General method work (General Machine Learning); at NeurIPS, optimization theory,
                which is its own topic — the call does not say where that boundary falls.
MERGED FROM     Deep learning [h] + Deep Learning [i] — same sources, same label up to case.
BELOW           AAAI's keywords Deep Learning Algorithms; Deep Learning Theory; Deep Neural
                Architectures and Foundation Models, which sit inside Machine Learning there.
FAMILY          academic
MODE            science, research
```

```
NAME            Evaluation
VERDICT         AREA
WHY             Engineering includes its measurement; here it is measurement as a method question.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML CFP — review-venue — h, i; Stanford
                CRFM foundation-models report — survey — i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 3 of 10 — S1, S2, S10, plus S3 at keyword level.
COVERS          "Evaluation (e.g., methodology, meta studies, replicability and validity,
                human-in-the-loop)".
EXCLUDES        Applications, which are a separate topic at both venues.
MERGED FROM     Evaluation [h] + Evaluation [i, itself a three-source merge].
BELOW           none reported. Not merged with Evals (programme) or with the MLCommons suites: both
                runs kept those apart, and run i says so in the record.
FAMILY          academic
MODE            research, engineering
```

```
NAME            Game Theory and Economic Paradigms
VERDICT         AREA
WHY             Research in AI as a general-AI venue files it; the methods are the venue's own.
SOURCES         AAAI-26 keywords page — review-venue — i
ATTESTED BY     i: 2 of 10 — S3, and S5 as cs.GT (reported separately there because the label differs).
COVERS          13 keywords: Adversarial Learning; Applications; Auctions and Market-Based Systems;
                Behavioral Game Theory; Cooperative Game Theory; Coordination and Collaboration;
                Equilibrium; Fair Division; Game Theory; Imperfect Information; Mechanism Design;
                Other Foundations; Social Choice / Voting.
EXCLUDES        Multi-agent coordination papers, which AAAI also offers under Multiagent Systems.
MERGED FROM     none — cs.GT was left separate and rejected; see the rejection note.
BELOW           the 13 keywords above.
FAMILY          academic
MODE            research
```

```
NAME            General Machine Learning
VERDICT         AREA
WHY             The science and research of learning, as the two ML venues' residual method topic.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML CFP — review-venue — h, i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 2 of 10 — S1, S2.
COVERS          "General machine learning (supervised, unsupervised, online, active, etc.)"; ICML
                adds clustering, ranking, semi- and self-supervised learning, time series analysis.
EXCLUDES        Deep architectures, which both venues file under Deep Learning.
MERGED FROM     General machine learning [h] + General Machine Learning [i].
BELOW           none reported. Deliberately not merged with Machine Learning: run i's record says
                the qualifier "General" marks it as the residual topic at venues that are all ML.
FAMILY          academic
MODE            science, research
```

```
NAME            Humans and AI
VERDICT         AREA
WHY             Research in AI: how systems and people work together, filed as one of 16 areas.
SOURCES         AAAI-26 keywords page — review-venue — i; AAAI-26 main-track call
                ("human-in-the-loop AI") — review-venue — i
ATTESTED BY     i: 2 of 10 — S3, S4.
COVERS          21 keywords, including Crowd Sourcing and Human Computation; Human-Aware Planning;
                Human-Computer Interaction; Human-in-the-loop Machine Learning; Intelligent User
                Interfaces; Learning Human Values and Preferences; Human-AI Teaming; Explainable AI
                (XAI) for Human Understanding; AI for Accessibility.
EXCLUDES        Cognitive modelling, which AAAI files under CMS.
MERGED FROM     none.
BELOW           the 21 keywords above.
FAMILY          academic
MODE            research
```

```
NAME            Infrastructure
VERDICT         AREA
WHY             The engineering of AI — its tools and its operation — as both ML venues file it.
SOURCES         NeurIPS 2025 CFP ("Infrastructure") — review-venue — h, i; ICML CFP ("Machine
                Learning Systems") — review-venue — h, i
ATTESTED BY     h: 2 — NeurIPS, ICML (merged there). i: 1 of 10 under each label — S1, S2.
COVERS          "Infrastructure (e.g., libraries, improved implementation and scalability,
                distributed solutions)"; ICML: "improved implementation and scalability, hardware,
                libraries, distributed methods".
EXCLUDES        Model research (Deep Learning); at ICML, optimization theory.
MERGED FROM     Machine Learning Systems [i]. Evidence: run h's ALSO CALLED names it —
                "ICML calls it 'machine learning systems'" — and the two parentheticals are near
                identical. Run i declined this merge on the label difference; it is listed under
                thin-evidence merges so the owner can split it again.
BELOW           none reported. AI Infrastructure (programme) was NOT merged in — see Unclear.
FAMILY          academic
MODE            engineering
```

```
NAME            Intelligent Robots
VERDICT         AREA
WHY             Research and engineering in AI: an AI venue's own robotics area.
SOURCES         AAAI-26 keywords page — review-venue — i; AAAI-26 main-track call
                ("robotics and perception") — review-venue — i
ATTESTED BY     i: 2 of 10 — S3, S4.
COVERS          12 keywords: Behavior Learning & Control; Cognitive Robotics; Human-Robot
                Interaction; Learning & Optimization for ROB; Localization, Mapping, and Navigation;
                Manipulation; Motion and Path Planning; Multi-Robot Systems; Multimodal Perception &
                Sensor Fusion; Other Foundations and Applications; State Estimation; Embodied AI.
EXCLUDES        Vision-for-robotics papers, also offered under Computer Vision.
MERGED FROM     none — run i declined to merge it with Robotics (different head noun), and I kept
                that decision.
BELOW           the 12 keywords above.
FAMILY          academic
MODE            research, engineering
```

```
NAME            Knowledge Representation and Reasoning
VERDICT         AREA
WHY             The science and research of representing and inferring, in both an AI venue and the
                index that subdivides AI.
SOURCES         AAAI-26 keywords ("KRR") — review-venue — i; ACM CCS 2012 ("Knowledge
                representation and reasoning") — index — i; AAAI-26 main-track call — review-venue — i;
                named inside arXiv's cs.AI description — index — i
ATTESTED BY     i: 4 of 10 — S3, S6, S4, S5's cs.AI description.
COVERS          CCS's 12 nodes: Description logics; Semantic networks; Nonmonotonic, default
                reasoning and belief revision; Probabilistic reasoning; Vagueness and fuzzy logic;
                Causal reasoning and diagnostics; Temporal reasoning; Cognitive robotics; Ontology
                engineering; Logic programming and answer set programming; Spatial and physical
                reasoning; Reasoning about belief and knowledge. AAAI adds 19 keywords including
                Argumentation, Automated Reasoning and Theorem Proving, Common-Sense Reasoning.
EXCLUDES        At AAAI, probabilistic inference, which goes to Reasoning under Uncertainty — but
                the CCS files "Probabilistic reasoning" inside KRR. A live boundary disagreement.
MERGED FROM     the AAAI area and the CCS node, merged by run i on an identical label up to case.
BELOW           the 12 CCS nodes and the 19 AAAI keywords.
FAMILY          academic
MODE            science, research
```

```
NAME            Machine Learning
VERDICT         AREA
WHY             The science, research and engineering of learning systems — the largest area in
                every source that carries it.
SOURCES         AAAI-26 keywords ("Machine Learning (ML)") — review-venue — i; arXiv ("cs.LG") —
                index — h, i; ACM CCS 2012 ("Machine learning", a sibling of Artificial
                intelligence) — index — h, i; AAAI-26 main-track call — review-venue — i
ATTESTED BY     i: 4 of 10 — S3, S5, S4, S6. h: 2 — arXiv (cs.LG), ACM CCS (Machine learning).
COVERS          "Papers on all aspects of machine learning research (supervised, unsupervised,
                reinforcement learning, bandit problems, and so on) including also robustness,
                explanation, fairness, and methodology." CCS files 5 children here: Learning
                paradigms; Learning settings; Machine learning approaches; Machine learning
                algorithms; Cross-validation.
EXCLUDES        At arXiv, what cs.AI carves out in the other direction; the CCS files vision,
                language, planning and knowledge representation under Artificial intelligence, not
                here.
MERGED FROM     cs.LG (Machine Learning) [h]; Machine learning [h, ACM CCS]; Machine Learning [i,
                already an S3+S5 merge]. Evidence: same sources and identical labels; run i's own
                ATTESTED BY counts the CCS node as attesting this area.
BELOW           AAAI's 55 ML keywords — the largest keyword set on its page — including Deep
                Learning Algorithms, Deep Neural Architectures and Foundation Models, Reinforcement
                Learning, Large Multimodal Models, Mixture of Experts, Neuro-Symbolic Learning,
                Quantum Machine Learning, Efficient ML / Green AI, Hardware-aware ML; and the CCS's
                5 children above. Note that several of those keywords are areas in their own right
                here, because the ML venues file them at the top level.
FAMILY          academic
MODE            science, research, engineering
```

```
NAME            MLPerf Automotive
VERDICT         AREA
WHY             A branded suite reported as the engineering area it instances: measuring AI
                computers for a deployment class.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1 — MLCommons. i: 1 of 10 — S7.
COVERS          "Measures the performance of computers intended for automotive, both for Advanced
                Driving Assistance System/Autonomous Driving (ADAS/AD) and In-Vehicle Infotainment
                (IVI)" "embedded systems."
EXCLUDES        Datacenter serving, which MLPerf Inference: Datacenter measures.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Client
VERDICT         AREA
WHY             As above: measurement of AI workloads on a deployment class.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Evaluates the performance of large language models (LLMs) and other AI workloads on
                personal computers" "from laptops and desktops to workstations." The only suite
                whose description names LLMs.
EXCLUDES        Phones (MLPerf Inference: Mobile) and datacenter systems.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Endpoints
VERDICT         AREA
WHY             As above: measurement of inference serving.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast systems can process inputs and produce results using a trained
                model." Both runs record that this is word for word the description the same page
                gives MLPerf Inference: Datacenter.
EXCLUDES        Training, which the MLPerf Training suites cover.
MERGED FROM     the two runs' identical records. NOT merged with MLPerf Inference: Datacenter —
                see the declined merge in What this run could not settle.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Inference: Datacenter
VERDICT         AREA
WHY             As above: measurement of inference serving.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast systems can process inputs and produce results using a trained model."
EXCLUDES        Training; edge, mobile and tiny systems, which have their own suites.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Inference: Edge
VERDICT         AREA
WHY             As above.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast systems can process inputs and produce results using a trained
                model on edge systems."
EXCLUDES        Datacenter systems.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Inference: Mobile
VERDICT         AREA
WHY             As above.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast consumer mobile devices with different AI chips and software
                stacks can process inputs" "and produce results using a trained model."
EXCLUDES        PCs, which MLPerf Client covers.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Inference: Tiny
VERDICT         AREA
WHY             As above.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast systems can process inputs and produce results using a trained
                model on ultra-low-power systems." (Run h's copy was truncated at fetch; run i's is
                whole.)
EXCLUDES        Mobile and edge class systems.
MERGED FROM     the two runs' records — i's supplies the sentence h's truncated.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Storage
VERDICT         AREA
WHY             Measurement of an operational part of AI systems that no academic source files.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast storage systems can supply training data when a model is being
                trained."
EXCLUDES        The training computation itself, which MLPerf Training measures.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Training
VERDICT         AREA
WHY             Measurement of training systems.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast systems can train models to a target quality metric."
EXCLUDES        Inference, which the five MLPerf Inference suites cover.
MERGED FROM     the two runs' identical records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            MLPerf Training: HPC
VERDICT         AREA
WHY             Measurement of training at supercomputer scale.
SOURCES         MLCommons Benchmark Suites — practitioner — h, i
ATTESTED BY     h: 1. i: 1 of 10 — S7.
COVERS          "Measures how fast systems can train models to a target quality metric running on
                large-scale supercomputers." (h's copy truncated; i's whole.)
EXCLUDES        Ordinary-scale training, which MLPerf Training covers.
MERGED FROM     the two runs' records.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            Multiagent Systems
VERDICT         AREA
WHY             Research in AI: agents acting together, filed by a venue, an archive and an index.
SOURCES         AAAI-26 keywords ("Multiagent Systems (MAS)") — review-venue — i; arXiv ("cs.MA") —
                index — h, i; ACM CCS 2012 ("Distributed artificial intelligence") — index — i;
                AAAI-26 main-track call — review-venue — i
ATTESTED BY     i: 4 of 10 — S3, S5, S4, S6. h: 1 — arXiv (cs.MA).
COVERS          "Covers multiagent systems, distributed artificial intelligence, intelligent agents,
                coordinated interactions. and practical applications. Roughly covers ACM Subject
                Class I.2.11." CCS files 4 nodes under its own name for this: Multi-agent systems;
                Intelligent agents; Mobile agents; Cooperation and coordination.
EXCLUDES        At arXiv, what cs.AI carves out; at CCS, single-agent planning.
MERGED FROM     cs.MA [h]; Multiagent Systems [i, S3+S5]; Distributed artificial intelligence [i,
                S6]. Evidence for the last: cs.MA's quoted INCLUDES names "distributed artificial
                intelligence, intelligent agents, coordinated interactions", which is the CCS node's
                own child list. Run i kept them apart as parent and child; listed under
                thin-evidence merges.
BELOW           AAAI's 15 MAS keywords (Adversarial Agents; Agent Communication; Agent-Based
                Simulation; Agent/AI Theories and Architectures; Agreement, Argumentation &
                Negotiation; Applications; Coordination and Collaboration; Distributed Problem
                Solving; Mechanism Design; Modeling other Agents; Multiagent Learning; Multiagent
                Planning; MAS under Uncertainty; Other Foundations; Teamwork) and the CCS's 4 nodes.
FAMILY          academic
MODE            research
```

```
NAME            Natural Language Processing
VERDICT         AREA
WHY             Research, science and engineering of language systems; the one area every kind of
                source in both runs files.
SOURCES         AAAI-26 keywords ("Natural Language Processing (NLP)") — review-venue — i; ACM CCS
                2012 ("Natural language processing") — index — i; arXiv ("cs.CL (Computation and
                Language)") — index — h, i; AAAI-26 main-track call — review-venue — i
ATTESTED BY     i: 4 of 10 — S3, S6, S4, S5's gloss on cs.CL. h: 1 — arXiv (cs.CL).
COVERS          arXiv: "Covers natural language processing. Roughly includes material in ACM Subject
                Class I.2.7." CCS files 8 nodes: Information extraction; Machine translation;
                Discourse, dialogue and pragmatics; Natural language generation; Speech recognition;
                Lexical semantics; Phonology / morphology; Language resources.
EXCLUDES        "work on artificial languages (programming languages, logics, formal systems) that
                does not explicitly address natural-language issues" — it goes to cs.PL or cs.LO.
MERGED FROM     cs.CL (Computation and Language) [h, i]. Evidence: run i's ALSO CALLED records that
                arXiv itself glosses cs.CL, inside the cs.AI description, as "Computation and
                Language (Natural Language Processing)", and run i's ATTESTED BY counts that gloss
                as an attestation of this area. Both runs declined the merge on the label
                difference; listed under thin-evidence merges.
BELOW           The 31 ACL Rolling Review tracks (run h): Clinical and Biomedical Applications;
                Computational Social Science and Cultural Analytics; Dialogue and Interactive
                Systems; Discourse and Pragmatics; Efficient Methods for NLP; Ethics, Bias, and
                Fairness; Generation; Human-Centered NLP and Human-AI Interaction; Information
                Extraction; Information Retrieval and Text Mining; Interpretability and Analysis of
                Models for NLP; Language Diversity and NLP for Low-resourced Languages; Language
                Modeling; Linguistic Theories, Cognitive Modeling, and Psycholinguistics; LLM Agents
                for NLP; Machine Learning for NLP; Machine Translation; Multilingualism and
                Cross-Lingual NLP; Multimodality and Language Grounding to Vision, Robotics and
                Beyond; NLP and Code Models; NLP and Symbolic Reasoning; NLP Applications; Phonology,
                Morphology, and Word Segmentation; Question Answering; Resources and Evaluation;
                Semantics: Lexical and Sentence-Level; Sentiment Analysis, Stylistic Analysis, and
                Argument Mining; Speech Recognition, Text-to-Speech and Spoken Language
                Understanding; Summarization; Syntax: Tagging, Chunking and Parsing; Theme tracks.
                Also the CCS's 8 nodes above and AAAI's 24 NLP keywords, among them (Large) Language
                Models; Conversational AI/Dialog Systems; Prompt Engineering / Prompting; Code
                Generation / Program Synthesis from Natural Language; Speech; Machine Translation,
                Multilinguality, Cross-Lingual NLP.
FAMILY          academic
MODE            science, research, engineering
```

```
NAME            Optimization
VERDICT         AREA
WHY             Research in AI: how models are fitted.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML CFP — review-venue — h, i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 2 of 10 — S1, S2, plus S3 at keyword level.
COVERS          "Optimization (e.g., convex and non-convex, stochastic, robust)"; ICML adds
                matrix/tensor methods, online, non-smooth, composite.
EXCLUDES        Learning theory, which both venues file under their theory topic.
MERGED FROM     the two runs' identical records.
BELOW           AAAI's keyword "ML: Optimization".
FAMILY          academic
MODE            research
```

```
NAME            Philosophical/theoretical foundations of artificial intelligence
VERDICT         AREA
WHY             The science of AI at its foundations, as the only index that subdivides AI files it.
SOURCES         ACM CCS 2012 SKOS release (id 10010147.10010178.10010216) — index — i
ATTESTED BY     i: 1 of 10 — S6.
COVERS          2 child nodes: Cognitive science; Theory of mind. The smallest of the eight AI children.
EXCLUDES        The applied reasoning methods, which are the other seven CCS AI children. The node
                contains no ethics at all.
MERGED FROM     none.
BELOW           the 2 nodes above.
FAMILY          academic
MODE            science
```

```
NAME            Philosophy and Ethics of AI
VERDICT         AREA
WHY             A submission area of an AI research venue whose enumerated keywords include the
                philosophical foundations of the field and the safety and accountability of its
                systems — research in AI, not only a report on its effects.
SOURCES         AAAI-26 keywords page — review-venue — i; AAAI-26 main-track call ("ethics") —
                review-venue — i
ATTESTED BY     i: 2 of 10 — S3, S4.
COVERS          12 keywords: Accountability, Interpretability & Explainability; AI & Epistemology;
                AI & Jobs/Labor; AI & Law, Justice, Regulation & Governance; Applications;
                Artificial General Intelligence; Bias, Fairness & Equity; Morality & Value-based AI;
                Philosophical Foundations of AI; Privacy & Security; Safety, Robustness &
                Trustworthiness; Societal Impact of AI.
EXCLUDES        Technical fairness and privacy methods, also offered inside Machine Learning and
                Computer Vision.
MERGED FROM     none.
BELOW           the 12 keywords above. Four of them (Jobs/Labor, Law and Governance, Societal
                Impact, and parts of Bias and Equity) are effect-on-the-world material that the rule
                would drop if they stood alone; they are recorded here, not dropped.
FAMILY          academic
MODE            science, research
```

```
NAME            Planning and scheduling
VERDICT         AREA
WHY             Research in AI: deciding what to do, as a child of "Artificial intelligence".
SOURCES         ACM CCS 2012 (id 10010147.10010178.10010199) — index — i; AAAI-26 main-track call
                ("planning") — review-venue — i; named inside arXiv's cs.AI description — index — i
ATTESTED BY     i: 3 of 10 — S6, S4, S5's cs.AI description.
COVERS          5 child nodes: Planning for deterministic actions; Planning under uncertainty;
                Multi-agent planning; Planning with abstraction and generalization; Robotic planning.
EXCLUDES        Search methods, which CCS files under Search methodologies.
MERGED FROM     none — run i declined to merge it with AAAI's PRS, which adds routing.
BELOW           the 5 nodes above.
FAMILY          academic
MODE            research
```

```
NAME            Planning, Routing, and Scheduling
VERDICT         AREA
WHY             Research in AI; the same ground as the CCS node plus routing, as an AI venue's area.
SOURCES         AAAI-26 keywords page — review-venue — i
ATTESTED BY     i: 1 of 10 under this label — S3.
COVERS          18 keywords: Activity and Plan Recognition; Applications; Deterministic Planning;
                Learning for Planning and Scheduling; Mixed Discrete/Continuous Planning;
                Model-Based Reasoning; Optimization of Spatio-temporal Systems; Other Foundations;
                Plan Execution and Monitoring; Planning under Uncertainty; Planning with Language
                Models; Planning with Markov Models; Planning/Scheduling and Learning; Replanning
                and Plan Repair; Routing; Scheduling; Scheduling under Uncertainty; Temporal Planning.
EXCLUDES        Search heuristics, which AAAI files under Search and Optimization.
MERGED FROM     none.
BELOW           the 18 keywords above.
FAMILY          academic
MODE            research
```

```
NAME            Probabilistic Methods
VERDICT         AREA
WHY             The science and research of inference under uncertainty.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML CFP — review-venue — h, i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 2 of 10 — S1, S2.
COVERS          "Probabilistic methods (e.g., variational inference, causal inference, Gaussian
                processes)"; ICML: "Bayesian methods, graphical models, Monte Carlo methods".
EXCLUDES        Deep generative models, which both venues file under Deep Learning.
MERGED FROM     the two runs' identical records.
BELOW           AAAI's keywords Bayesian Learning; Probabilistic Circuits and Graphical Models.
FAMILY          academic
MODE            science, research
```

```
NAME            Reasoning under Uncertainty
VERDICT         AREA
WHY             Research in AI; an AI venue's own area for inference, decision and causality.
SOURCES         AAAI-26 keywords page — review-venue — i; named inside arXiv's cs.AI description
                ("Uncertainty in AI") — index — i
ATTESTED BY     i: 2 of 10 — S3, S5's cs.AI description.
COVERS          11 keywords: Applications; Causality; Decision/Utility Theory; Graphical Models;
                Other Foundations; Probabilistic Programming; Relational Probabilistic Models;
                Sequential Decision Making; Probabilistic Inference; Stochastic Optimization;
                Uncertainty Representations.
EXCLUDES        Symbolic reasoning, which AAAI files under KRR — while the CCS files probabilistic
                reasoning inside KRR instead.
MERGED FROM     none.
BELOW           the 11 keywords above.
FAMILY          academic
MODE            research
```

```
NAME            Reinforcement Learning
VERDICT         AREA
WHY             Research in AI: learning to act.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML CFP — review-venue — h, i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 2 of 10 — S1, S2, plus S3 at keyword level and S5 inside
                the cs.LG and cs.SY descriptions.
COVERS          "Reinforcement learning (e.g., decision and control, planning, hierarchical RL,
                robotics)" — the two venues' example lists are the same.
EXCLUDES        Supervised and unsupervised learning, which both venues file under General Machine
                Learning.
MERGED FROM     the two runs' identical records.
BELOW           AAAI's keyword "ML: Reinforcement Learning".
FAMILY          academic
MODE            research
```

```
NAME            Retrieval + Search
VERDICT         AREA
WHY             The engineering of AI systems: how a deployed model reaches the data it answers
                from. One of only two programme tracks in either run with a scope statement.
SOURCES         AI Engineer World's Fair 2025 programme — programme — i
ATTESTED BY     i: 1 of 10 — S9.
COVERS          "core retrieval problems, including embedding-based retrieval from internal data and
                agentic search over web and docs", as a complement to RecSys.
EXCLUDES        Recommendation, which the programme gives to LLM RecSys; graph-structured retrieval,
                which it gives to GraphRAG.
MERGED FROM     none. Search & Retrieval (run h, 2026 programme) was NOT merged in: that record
                carries no scope and no ALSO CALLED, so the merge has no evidence. It is UNCLEAR.
BELOW           none reported.
FAMILY          applied
MODE            engineering
```

```
NAME            Robotics
VERDICT         AREA
WHY             Research and engineering in AI: a category the archive carves out of cs.AI by name.
SOURCES         arXiv ("cs.RO (Robotics)") — index — h, i; Stanford CRFM report ("Robotics", a
                Capabilities subsection) — survey — i; AAAI-26 main-track call ("robotics and
                perception") — review-venue — i
ATTESTED BY     i: 3 of 10 — S5, S10, S4. h: 1 — arXiv (cs.RO).
COVERS          "Roughly includes material in ACM Subject Class I.2.9."
EXCLUDES        cs.AI carves Robotics out of itself; arXiv keeps control in cs.SY.
MERGED FROM     cs.RO [h]; Robotics [i, S5+S10].
BELOW           none reported here; AAAI's Intelligent Robots area and the programme tracks
                Robotics & World Models and Autonomy + Robotics were deliberately not merged in.
FAMILY          academic
MODE            research, engineering
```

```
NAME            Search and Optimization
VERDICT         AREA
WHY             Research in AI: an AI venue's own area for search and combinatorial optimization.
SOURCES         AAAI-26 keywords page — review-venue — i; AAAI-26 main-track call ("search") —
                review-venue — i
ATTESTED BY     i: 2 of 10 — S3, S4.
COVERS          15 keywords: Adversarial Search; Algorithm Configuration; Applications;
                Combinatorial Optimization; Distributed Search; Evaluation and Analysis;
                Evolutionary Computation; Heuristic Search; Learning to Search; Local Search;
                Metareasoning and Metaheuristics; Mixed Discrete/Continuous Search; Non-convex
                Optimization; Other Foundations; Sampling/Simulation-based Search.
EXCLUDES        Constraint solvers, which AAAI files under CSO.
MERGED FROM     none.
BELOW           the 15 keywords above.
FAMILY          academic
MODE            research
```

```
NAME            Search methodologies
VERDICT         AREA
WHY             Research in AI, as a child of "Artificial intelligence" in the index that
                subdivides AI.
SOURCES         ACM CCS 2012 (id 10010147.10010178.10010205) — index — i; AAAI-26 main-track call
                ("search") — review-venue — i
ATTESTED BY     i: 2 of 10 — S6, S4.
COVERS          7 child nodes: Heuristic function construction; Discrete space search; Continuous
                space search; Randomized search; Game tree search; Abstraction and micro-operators;
                Search with partial observations.
EXCLUDES        Planning, which CCS files under Planning and scheduling.
MERGED FROM     none. Note that "search" here is state-space search, not retrieval; run i records
                that both senses are live at the same level in different sources.
BELOW           the 7 nodes above.
FAMILY          academic
MODE            research
```

```
NAME            Social and economic aspects of machine learning
VERDICT         AREA
WHY             Judged from the record, not the name: its quoted contents are properties of systems
                that are studied and engineered — fairness, interpretability, privacy, safety.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i
ATTESTED BY     h: 1 — NeurIPS. i: 1 of 10 — S1.
COVERS          "Social and economic aspects of machine learning (e.g., fairness, interpretability,
                human-AI interaction, privacy, safety, strategic behavior)".
EXCLUDES        Evaluation methodology, which NeurIPS files as its own topic.
MERGED FROM     the two runs' identical records. Not merged with Trustworthy Machine Learning: both
                runs declined, and run i says the labels differ in kind.
BELOW           none reported.
FAMILY          academic
MODE            research
```

```
NAME            Theory
VERDICT         AREA
WHY             The science of AI: what can be learned, controlled and decided, and at what cost.
SOURCES         NeurIPS 2025 CFP — review-venue — h, i; ICML CFP ("Theory of Machine Learning") —
                review-venue — h, i; Stanford CRFM report — survey — i
ATTESTED BY     h: 2 — NeurIPS, ICML. i: 2 of 10 — S1, S10, plus S2 under the qualified label and
                S3 at keyword level.
COVERS          "Theory (e.g., control theory, learning theory, algorithmic game theory)"; ICML:
                "statistical learning theory, bandits, game theory, decision theory".
EXCLUDES        Optimization, which both venues file as its own topic.
MERGED FROM     Theory of Machine Learning [i, S2]. Evidence: run h's ALSO CALLED names it — "ICML
                calls it 'theory of machine learning'" — and both occupy the theory slot of two
                otherwise matching lists. Run i declined on the qualifier; listed under
                thin-evidence merges.
BELOW           AAAI's keywords Learning Theory; Deep Learning Theory.
FAMILY          academic
MODE            science, research
```

```
NAME            Trustworthy Machine Learning
VERDICT         AREA
WHY             Research and engineering in AI: the properties a deployed system must hold.
SOURCES         ICML Call for Papers — review-venue — h, i
ATTESTED BY     h: 1 — ICML 2026 CFP. i: 2 of 10 — S2, and S8 whose WG 3 is named "Trustworthiness".
COVERS          "Trustworthy Machine Learning (causality, fairness, interpretability, privacy,
                robustness, safety, etc.)" — ICML 2026's wording adds reliability.
EXCLUDES        Evaluation methodology, which ICML files separately; causal inference, which NeurIPS
                places under Probabilistic methods instead.
MERGED FROM     the two runs' records (h "trustworthy machine learning", i "Trustworthy Machine
                Learning") — same source, same label up to case.
BELOW           none reported. SC 42's WG 3: Trustworthiness is a separate unit and is UNCLEAR, for
                want of a scope statement.
FAMILY          academic
MODE            research, engineering
```

---

## Rejected

77 categories, grouped by verdict. Each line gives the clause of the rule it fails.

### DOMAIN — 51

Two kinds sit here, because the brief's six verdicts have no bucket for the second.
**(a) AI pointed at another field's problems or data.** **(b) Not AI at all** — a neighbouring field
of computer science, which fails the keep clause ("belongs to none of the three") but matches no
rejection label; marked *(not AI)*.

- Application Domains (APP) — (a) AAAI's own guide says "typically the application is NOT the primary keyword"; the 11 keywords are sectors.
- Application-Driven Machine Learning — (a) "driven by the needs of end-users in applications such as healthcare, physical sciences, biosciences, social sciences, sustainability and climate".
- Machine learning for sciences — (a) "climate, health, life sciences, physics, social sciences".
- Neuroscience and cognitive science — (a) "neural coding, brain-computer interfaces": AI methods pointed at another science's data. **Close.**
- AI in Finance (programme) — (a) AI carried into financial services; no scope statement, name and overlaps only. **Close.**
- AI in GTM (programme) — (a) AI carried into sales and marketing; no scope statement. **Close.**
- AI in Healthcare (programme) — (a) AI carried into medicine; no scope statement. **Close.**
- AI for Scientific Discovery (AAAI panel) — (a) AI pointed at the sciences; no scope statement. **Close.**
- AI for Social Good (AAAI panel) — (a) AI pointed at social problems; no scope statement. **Close.**
- Clinical and Biomedical Applications (ARR) — (a) NLP pointed at medicine; no scope statement. **Close.**
- Education (CRFM) — (a) filed by the report under "Applications".
- Healthcare and biomedicine (CRFM) — (a) filed under "Applications".
- Law (CRFM) — (a) filed under "Applications"; law as a field AI is applied to.
- JWG 3: AI enabled health informatics (SC 42) — (a) a standards group for AI in health. **Close.**
- Joint Working Group SC 42 – ISO/TC 68: Artificial intelligence — (a) TC 68 is the financial-services committee. **Close.**
- cs.CE (Computational Engineering, Finance, and Science) — (a) "applications of computer science to the mathematical modeling of complex systems in … science, engineering, and finance".
- cs.AR (Hardware Architecture) — (b) not AI *(not AI)*. **Close:** AI hardware is engineering of AI, but this record is general systems organisation.
- cs.CC (Computational Complexity) — (b) *(not AI)*.
- cs.CG (Computational Geometry) — (b) *(not AI)*.
- cs.CR (Cryptography and Security) — (b) *(not AI)*. **Close:** security of AI systems is engineering of AI; this record is general cryptography and security.
- cs.DB (Databases) — (b) *(not AI)*. **Close:** it is where arXiv files data mining.
- cs.DC (Distributed, Parallel, and Cluster Computing) — (b) *(not AI)*. **Close:** it is the substrate large training runs use.
- cs.DL (Digital Libraries) — (b) *(not AI)*.
- cs.DM (Discrete Mathematics) — (b) *(not AI)*.
- cs.DS (Data Structures and Algorithms) — (b) *(not AI)*.
- cs.ET (Emerging Technologies) — (b) *(not AI)*.
- cs.FL (Formal Languages and Automata Theory) — (b) *(not AI)*.
- cs.GR (Graphics) — (b) *(not AI)*.
- cs.GT (Computer Science and Game Theory) — (b) *(not AI)*. **Close:** its own scope names learning in games and agent modelling, and AAAI files the same ground as an area (kept).
- cs.HC (Human-Computer Interaction) — (b) *(not AI)*. **Close:** AAAI's Humans and AI covers the AI-specific part (kept).
- cs.IR (Information Retrieval) — (b) *(not AI)*. **Close:** retrieval is central to deployed AI; Retrieval + Search and Data Mining & Knowledge Management carry it (both kept).
- cs.IT (Information Theory) — (b) *(not AI)*.
- cs.LO (Logic in Computer Science) — (b) *(not AI)*. **Close:** KRR covers the AI-specific part (kept).
- cs.MM (Multimedia) — (b) *(not AI)*.
- cs.MS (Mathematical Software) — (b) *(not AI)*.
- cs.NA (Numerical Analysis) — (b) *(not AI)*; the source says it is an alias for math.NA.
- cs.NI (Networking and Internet Architecture) — (b) *(not AI)*.
- cs.OS (Operating Systems) — (b) *(not AI)*.
- cs.PF (Performance) — (b) *(not AI)*. **Close:** engineering includes measurement, but this measures computing systems generally; the MLPerf suites are the AI-specific ones (kept).
- cs.PL (Programming Languages) — (b) *(not AI)*.
- cs.SC (Symbolic Computation) — (b) *(not AI)*. **Close:** neuro-symbolic work.
- cs.SD (Sound) — (b) *(not AI)*. **Close:** speech is a modality of AI; the CCS files "Speech recognition" inside NLP, which keeps it in the list.
- cs.SE (Software Engineering) — (b) *(not AI)*. **Close:** AI for code and the testing of AI systems; NLP's keyword "Code Generation / Program Synthesis" keeps that ground.
- cs.SI (Social and Information Networks) — (b) *(not AI)*.
- cs.SY (Systems and Control) — (b) *(not AI)*; an alias for eess.SY. **Close:** the CCS files Control methods inside AI (kept).
- Computer graphics (ACM CCS) — (b) *(not AI)*; a sibling of Artificial intelligence in the index.
- Concurrent computing methodologies (ACM CCS) — (b) *(not AI)*.
- Distributed computing methodologies (ACM CCS) — (b) *(not AI)*. **Close:** same ground as Infrastructure.
- Parallel computing methodologies (ACM CCS) — (b) *(not AI)*.
- Modeling and simulation (ACM CCS) — (b) *(not AI)*. **Close:** world models.
- Symbolic and algebraic manipulation (ACM CCS) — (b) *(not AI)*. **Close:** computer algebra and theorem proving.

### RECORD — 9

- cs.CY (Computers and Society) — "impact of computers on society, computer ethics, information technology and public policy, legal aspects of computing": a report on the effect, not on AI.
- Economics (CRFM) — the economic effects of foundation models; the report files it under "Society".
- Environment (CRFM) — the environmental cost of foundation models; under "Society".
- Ethics of scale (CRFM) — ethical questions arising from scale; under "Society". **Close:** ethics is also research in AI, and AAAI's PEAI area (kept) carries that.
- Inequity and fairness (CRFM) — unequal effects of foundation models; under "Society". **Close:** fairness is a technical research property, carried by Trustworthy Machine Learning and Social and economic aspects (both kept).
- Legality (CRFM) — the law as it bears on foundation models; under "Society".
- Misuse (CRFM) — deliberate harmful use; under "Society". **Close:** misuse mitigation is engineering.
- Geopolitical Aspects & Implications of AI (AAAI panel) — AI's effect on states and policy. **Close:** rejected without a scope statement, on the name alone.
- Role of Academia (AAAI panel) — about the institutions that do the research, not about AI. **Close:** rejected without a scope statement.

### FORMAT — 17

- Theme tracks (proposed by participating publication venues…) (ARR) — the record calls it a container label; the only descriptive text is "proposed by participating publication venues and specific to those venues": a track slot.
- cs.GL (General Literature) — a document-type category: "introductory material, survey material, predictions of future trends, biographies"; run i calls it "a document-type category, not a subject".
- cs.OH (Other Computer Science) — "the classification to use for documents that do not fit anywhere else": a residual filing slot.
- AI Architects: AI Factories (programme) — "names a leadership room, an audience grouping by job role rather than a subject area".
- AI Architects: Show my Workflow (programme) — same.
- AI Architects: Tokenmaxxing (programme) — same.
- AI-Native Enterprises (programme) — same.
- CTO Circle (programme) — same.
- L1: AI Architects (programme) — "an exclusive, invite-only track for VPs and executives": an audience.
- L2: AI in the Fortune 500 (programme) — an audience-and-company-size label.
- Tiny Teams (programme) — a company-size label: "small, highly profitable teams with more ARR and customers than employees".
- Product Management (programme) — "a job-function label, not a subject".
- Startup Battlefield (programme) — "names a networking room, a session format".
- Workshops Day 2 (programme) — "names a day of workshops, a session format".
- Workshops Day 3 (programme) — same.
- Liaison with SC 27 (SC 42 AHG 4) — "an ad hoc group named for a liaison with another subcommittee, not a subject area": a working arrangement.
- Best practices for new proposals (SC 42 AHG 8) — "an ad hoc group named for the committee's own procedure, not a subject area".

### PRODUCT — 0

No category was rejected as a product. The rule says a product or tool name is not dropped but
reported as the engineering area it instances: that is what the twelve MLCommons suites are, and
they are areas. The one branded label with no scope at all — **MCP** — is `UNCLEAR`, not `PRODUCT`,
because without a scope statement the record does not say what engineering area it instances.

---

## Merged

**Substantive merges — different names, same area.**

| Kept | Merged in | Evidence |
|---|---|---|
| Machine Learning | cs.LG (Machine Learning) [h]; Machine learning (ACM CCS) [h]; Machine Learning (AAAI area + cs.LG) [i] | Same sources and identical labels; run i's ATTESTED BY counts the CCS node as attesting this area |
| Computer Vision | cs.CV [h]; Computer Vision (AAAI + CCS + cs.CV) [i] | Same source (arXiv cs.CV); run i's own merge, on labels identical up to case and a matching opening sentence |
| Natural Language Processing | Natural language processing (CCS) + NLP (AAAI) [i]; cs.CL (Computation and Language) [h, i] | arXiv itself glosses cs.CL as "Computation and Language (Natural Language Processing)" (ALSO CALLED naming the other); run i's ATTESTED BY counts that gloss |
| Multiagent Systems | cs.MA [h]; Multiagent Systems (AAAI + cs.MA) [i]; Distributed artificial intelligence (CCS) [i] | cs.MA's quoted INCLUDES names "distributed artificial intelligence, intelligent agents, coordinated interactions" — the CCS node's own child list |
| Robotics | cs.RO [h]; Robotics (cs.RO + CRFM) [i] | Same source, identical label |
| Knowledge Representation and Reasoning | KRR (AAAI) + Knowledge representation and reasoning (CCS) [i] | Identical label up to case (run i's merge) |
| Infrastructure | Machine Learning Systems (ICML) [i]; Infrastructure [h, i] | Run h's ALSO CALLED: "ICML calls it 'machine learning systems'", with near-identical parentheticals |
| Theory | Theory of Machine Learning (ICML) [i]; Theory [h, i] | Run h's ALSO CALLED: "ICML calls it 'theory of machine learning'"; both occupy the theory slot of two matching lists |
| Data / WG 2 (SC 42) | Data [h] + WG 2: Big Data [i] | Run i's ALSO CALLED: "An earlier ISO listing names the same group simply 'Data'; the route gives 'Big Data'"; same body, same group reference |
| WG 5 (SC 42) | Computational approaches and computational characteristics of AI systems [h] + WG 5: Computational approaches and characteristics of artificial intelligence systems [i] | Run i's ALSO CALLED records both titles for the same group |
| JWG 2 (SC 42) | Joint Working Group SC 42 – SC 7 [h] + JWG 2: Testing of AI-based systems [i] | Same body, same group reference; run i's route gives the subject title h's listing lacked |
| JWG 3 (SC 42) | Joint Working Group SC 42 – ISO/TC 215: AI enabled health informatics [h] + JWG 3 [i] | Same body, same group reference |
| JWG 4 (SC 42) | Joint Working Group SC 42 – IEC TC 65/SC 65A: Functional safety [h] + JWG 4 [i] | Same body, same group reference |

**Identity merges across the two runs — same source, same label.** 70 further pairs, carrying no
judgement: the 36 remaining arXiv `cs` categories; the 12 MLCommons suites; the NeurIPS/ICML topics
Applications, Application-Driven Machine Learning, Deep Learning, Evaluation, General Machine
Learning, Machine learning for sciences, Neuroscience and cognitive science, Optimization,
Probabilistic Methods, Reinforcement Learning, Social and economic aspects of machine learning,
Trustworthy Machine Learning; the AI Engineer World's Fair tracks Design Engineering, Evals,
Generative Media, Security and LLM RecSys (the two runs read the 2025 and 2026 programmes); and
SC 42's WG 1, WG 3 and WG 4.

---

## Unclear

99 categories. **These leave this run undecided.** For all but one, what would settle it is the same
thing: **a scope statement from the source** saying what work the category holds. They are listed by
source, so the next step can go to one page per block.

**AI Engineer World's Fair programme — 33.** The programme page carries no per-track description for
any of these; the label is all there is. Run h's 2026 tracks: Agentic Commerce; Agentic Engineering;
Autoresearch *(h adds: names a keynote slot)*; Claws & Personal Agents; Computer Use; Context
Engineering; Data Quality; Design Engineering; Evals; Forward Deployed Engineering; Generative Media;
Graphs; Harness Engineering *(a keynote slot)*; Inference; LLM RecSys; Local AI; Memory & Continual
Learning; Posttraining & Midtraining; Robotics & World Models; Sandbox & Platform Engineering;
Search & Retrieval; Security; Software Factories *(a keynote slot)*; Vision & OCR; Voice & Realtime
AI. Run i's 2025 tracks: Agent Reliability; AI Infrastructure; Autonomy + Robotics; GraphRAG; MCP;
Reasoning + RL; SWE Agents; Voice.
*MCP additionally:* what would settle it is a scope statement saying what work the track covers, not
what the protocol is; without one the record cannot say which engineering area the product instances.

**ACL Rolling Review tracks — 29.** ARR's call lists track names only and points authors to a
separate page for help choosing an area. Computational Social Science and Cultural Analytics;
Dialogue and Interactive Systems; Discourse and Pragmatics; Efficient Methods for NLP; Ethics, Bias,
and Fairness; Generation; Human-Centered NLP and Human-AI Interaction; Information Extraction;
Information Retrieval and Text Mining; Interpretability and Analysis of Models for NLP; Language
Diversity and NLP for Low-resourced Languages; Language Modeling; Linguistic Theories, Cognitive
Modeling, and Psycholinguistics; LLM Agents for NLP; Machine Learning for NLP; Machine Translation;
Multilingualism and Cross-Lingual NLP; Multimodality and Language Grounding to Vision, Robotics and
Beyond; NLP and Code Models; NLP and Symbolic Reasoning; NLP Applications; Phonology, Morphology,
and Word Segmentation; Question Answering; Resources and Evaluation; Semantics: Lexical and
Sentence-Level; Sentiment Analysis, Stylistic Analysis, and Argument Mining; Speech Recognition,
Text-to-Speech and Spoken Language Understanding; Summarization; Syntax: Tagging, Chunking and
Parsing. **All 31 ARR tracks (these 29, plus Clinical and Biomedical Applications and Theme tracks,
which carry verdicts) are recorded under Natural Language Processing's `BELOW`.** What would settle
them: ARR's separate area-guide page, which neither run opened.

**Stanford CRFM foundation-models report subsections — 14.** The contents page gives a name and a
level and no scope statement for any subsection. Adaptation; AI safety and alignment; Data;
Interaction; Interpretability; Language; Modeling; Philosophy of understanding; Reasoning and search;
Robustness to distribution shifts; Security and privacy; Systems; Training; Vision. What would settle
them: the report's own section text, which run i did not open.

**AAAI 2025 Presidential Panel chapters — 13.** The report describes all 17 chapters at once and
gives no per-chapter scope; run h could not open the report itself. AI & Cognitive Science; AI &
Sustainability *(what would settle it: whether the chapter is about AI applied to sustainability or
about the environmental cost of AI — the two fall on opposite sides of the rule)*; AI Agents; AI
Ethics & Safety; AI Evaluation; AI Factuality & Trustworthiness; AI Perception vs. Reality; AI
Reasoning; Artificial General Intelligence (AGI); Diversity of AI Research Approaches; Embodied AI;
Hardware & AI; Research Beyond the AI Research Community.

**ISO/IEC JTC 1/SC 42 groups — 10.** The only scope either run could quote is the subcommittee's own,
"Standardization in the area of Artificial Intelligence"; no group has a published scope in either
route. WG 1: Foundational standards; WG 2: Data / Big Data; WG 3: Trustworthiness; WG 4: Use cases
and applications; WG 5: Computational approaches and characteristics of AI systems; JWG 2: Testing of
AI-based systems; JWG 4: Functional safety and AI systems; JWG 5 (ISO/TC 37): Natural language
processing; JWG 6 (ISO/CASCO): Conformity assessment schemes for AI systems; Joint Advisory Group on
AI and sustainability *(what would settle it: whether the group studies AI applied to sustainability
or the environmental cost of AI)*. What would settle the rest: ISO's own committee page, which
returned HTTP 403 to both runs.

---

## What this run could not settle

**Every `UNCLEAR` is above, with what would settle it.** 99 of 223 categories — 44% — are undecided
for want of a scope statement. The next step must say what it did with each one before the owner sees
the proposal.

**The applied vocabulary is almost all in the `UNCLEAR` pile, and that is the largest single risk in
this run.** Of the 47 areas, 13 were named by applied sources and 12 of those 13 are MLCommons
measurement suites; the thirteenth is one retrieval track. Every other area comes from academic
sources alone, and **no area is named by both families**. The reason is mechanical: academic sources
publish scope sentences and practitioner programmes do not. So *Evals*, *Inference*, *Context
Engineering*, *Agent Reliability*, *AI Infrastructure*, *SWE Agents*, *Posttraining & Midtraining*,
*Memory & Continual Learning*, *Local AI*, *GraphRAG*, *Computer Use* and *Agentic Engineering* —
the whole working vocabulary of deployed AI — are undecided here, not rejected. **A book on the
engineering of AI that took only this run's `AREA` list would have almost no engineering in it.**

**Rejections I was unsure about.** Each is marked **Close** in the Rejected list; they are, in short:
the ten arXiv categories that carry AI-adjacent ground under a general computer-science scope
(cs.AR, cs.CR, cs.DB, cs.DC, cs.GT, cs.HC, cs.IR, cs.LO, cs.PF, cs.SC, cs.SD, cs.SE, cs.SY); the five
ACM CCS siblings with the same problem (Distributed, Parallel and Concurrent computing
methodologies, Modeling and simulation, Symbolic and algebraic manipulation); the six
no-scope domain labels rejected on their names and overlaps alone (AI in Finance, AI in GTM, AI in
Healthcare, AI for Scientific Discovery, AI for Social Good, Clinical and Biomedical Applications);
the two AAAI panel chapters rejected without a scope statement (Geopolitical Aspects, Role of
Academia); the four CRFM Society subsections where the technical and the societal reading both fit
(Ethics of scale, Inequity and fairness, Misuse, and — for the opposite reason — Neuroscience and
cognitive science); and the two SC 42 joint groups rejected on the identity of the partner committee
(JWG 3 health, JWG 7 finance). **In each case the loss, if I am wrong, is named beside the line**, so
the ground can be recovered from the area that still carries it.

**Merges made on thin evidence, so they can be split again.**
1. **Infrastructure ← Machine Learning Systems.** Run h merged them on its ALSO CALLED; run i
   deliberately kept them apart on the label difference. The two example lists differ: ICML names
   hardware, NeurIPS does not.
2. **Theory ← Theory of Machine Learning.** Same split decision between the runs. NeurIPS's examples
   name control theory; ICML's name bandits and decision theory instead.
3. **Natural Language Processing ← cs.CL.** Both runs kept these apart on the label; I merged on
   arXiv's own gloss. If the owner wants arXiv's "Computation and Language" treated as a different
   cut from AAAI's "Natural Language Processing", this is the merge to undo.
4. **Multiagent Systems ← Distributed artificial intelligence.** The CCS makes DAI the *parent* of
   multi-agent systems; cs.MA makes multiagent systems the category and names DAI inside it. I merged
   on the matching contents; the parent/child direction is the reason to doubt it.
5. **Machine Learning ← Machine learning (ACM CCS).** The CCS node is a sibling of "Artificial
   intelligence", not a child, so merging it into the AAAI/arXiv area imports a different
   containment claim along with the name.

**A merge I considered and declined.** `MLPerf Endpoints` and `MLPerf Inference: Datacenter` carry
**word-for-word the same scope sentence** on the MLCommons page. That is "INCLUDES that match", which
the brief names as merge evidence — but both runs report it as a defect of the page rather than as
identity, and neither opened the suites' own pages. Merging two separately published suites on a
copy-paste would be a wrong finding, so they stand as two areas. What would settle it: the two
suites' own pages.

**What the level loses** is stated in full under *Level* above: ACL's 31 tracks stop being areas and
become `BELOW` Natural Language Processing, and the ACM CCS's level-2 node "Artificial intelligence"
is kept but sits above the chosen level, wrapping eight areas that are also listed separately. The
owner may want that node struck as a container.

**An area the rule implies that no framing run reported — recorded here, not added to the list.**
Run h says it plainly in its own coverage section: "no source I read has a category for the work of
running a trained model as a product under load — MLCommons measures it, the AI Engineer World's Fair
schedules talks about it, but neither files it as a named subject." Run i says the same of agents and
of language models: "No index and no refereed venue in the set carries a top-level category named
after agents or language models." Both gaps survive consolidation. Nothing has been added for them.

**What both runs' source sets miss, carried forward.** Neither run has a source that files AI work by
job or role (both tried a job board and failed), so roles and occupations are absent except as three
or four conference audience labels — all of which this run rejected as `FORMAT`. All 19 sources are
English-language and US- or Europe-based: no Chinese, Japanese, Korean, French or German filing
system was read. Work done inside companies and never submitted anywhere appears only where a
practitioner meeting gave it a track. Nothing newer than mid-2026 is in either run; run i's `survey`
kind rests on a 2021 report, and both runs' `index` evidence rests on an ACM classification from 2012.

**Project files visible in my context, and what they told me.** Three were attached automatically and
I read them as context, not as instruction, and opened no file in the repository except the two
framing files and this output:
- `.claude/CLAUDE.md` (repository root) — session instructions for the *website*: which kind of work
  a session is, the restyle rules, publishing. It told me nothing about this task and governs nothing
  here.
- `.claude/HANDOVER.md` — the website handover: the site map, the D&I guide build, the on-ramp books.
  Nothing about this task.
- `books/modern-ai/CLAUDE.md` — the book's own session instructions. Relevant, and it told me four
  things I obeyed: that research output goes to a file and not only into the conversation, and that
  "the consolidator must put its coverage section in its file, not only in its reply"; that no agent
  and no session may substitute a search, a pattern or a count for reading; that a stage which
  reduces its input must close its arithmetic over the input's own total; and that the owner is never
  handed an unrecommended list, which is why this run decides nothing about which areas the book
  covers — it only applies the rule it was given. It also says the two framing runs are "not yet
  consolidated", which matches what I found.
- The user-level memory file listed `[Never hand an unrecommended list]` and `[Page budgets never
  bind]`; neither changed anything here.

**My arithmetic.**

| | Count |
|---|---|
| Categories run `h` carried | 172 |
| Categories run `i` carried | 135 |
| Union before merges | 307 |
| Merges (records folded into another unit) | 84 |
| **Distinct categories after merges** | **223** |
| `AREA` | 47 |
| `DOMAIN` | 51 |
| `RECORD` | 9 |
| `FORMAT` | 17 |
| `PRODUCT` | 0 |
| `UNCLEAR` | 99 |
| **Sum of verdicts** | **223** |

A merge folds one record into another unit, so a unit built from *n* records counts *n* − 1 merges.
Merges made **inside** a single run are already reflected in that run's own total and are not counted
again here. The 84 are:

| Merges | What |
|---|---|
| 35 | arXiv `cs` categories, run to run, under identical labels (`cs.CL` is counted on its own line below) |
| 12 | MLCommons suites, run to run, under identical labels |
| 12 | NeurIPS / ICML topics, run to run, under identical labels |
| 8 | SC 42 groups — WG 1 to WG 5 and JWG 2 to JWG 4 — three of them under titles that differ between the runs |
| 5 | AI Engineer World's Fair tracks, run to run, under identical labels |
| 2 | Machine Learning absorbs run h's `cs.LG` and run h's ACM CCS "Machine learning" |
| 2 | Natural Language Processing absorbs both runs' `cs.CL` records |
| 2 | Multiagent Systems absorbs run h's `cs.MA` and run i's "Distributed artificial intelligence" |
| 2 | Infrastructure absorbs run i's "Infrastructure" and run i's "Machine Learning Systems" |
| 2 | Theory absorbs run i's "Theory" and run i's "Theory of Machine Learning" |
| 1 | Computer Vision absorbs run h's `cs.CV` |
| 1 | Robotics absorbs run h's `cs.RO` |
| **84** | 307 − 84 = **223** |

**Nothing was dropped.** Every one of the 307 records from the two runs is either a unit above, a
line in Rejected, a line in Unclear, or named inside a `MERGED FROM` or a `BELOW` field.

## Written to

`/Users/lakshmideepak/LearningLab/towards-intelligence/robotbrainlab.github.io/books/modern-ai/research/frames/CONSOLIDATED-2026-11-12.md`
— **223 distinct categories** from a 307-record union: 47 `AREA`, 51 `DOMAIN`, 9 `RECORD`, 17
`FORMAT`, 0 `PRODUCT`, 99 `UNCLEAR`.
