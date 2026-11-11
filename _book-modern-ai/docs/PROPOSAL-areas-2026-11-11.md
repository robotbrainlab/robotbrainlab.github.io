# Proposed areas for the book — 12, from the 63 candidates

**`[I RECOMMEND] 2026-11-11`. This is a proposal, not a decision.** `GOAL.md` §3.3 gives the owner
"approves, redraws or rejects **the proposed list**". Until today nobody made the proposal: the
framing run reports and does not decide, and the consolidation run is forbidden from rejecting
anything for being unimportant. So what reached him was an inventory of 63 and no recommendation,
and cutting an inventory with no recommendation is originating the argument from nothing — the
exact thing §3.3 retracts. **The missing step is mine. This is it.**

**What I judged against**, because §3.3 names it: *"An argument needs a purpose and reasons; it does
not need a particular author. The purpose is already written down: §1.1's career goal and §3.1's
five questions."*

- **§1.1 `[STATED]`** — become a strong candidate for **AI Researcher, Research Engineer, AI
  Engineer, Machine Learning Engineer**. Not staying informed. The identity is a **research-oriented
  engineer**, and four capabilities are wanted *together*: theoretical depth, research awareness,
  experimentation skill, hands-on engineering.
- **§3.1 `[STATED]`** — every area must answer five questions, among them **ongoing research**,
  **engineering developments**, **established scientific knowledge** and the **transition between
  them**.

**The operative test.** An area is kept when it has **live research and live engineering at the same
time**, and lies on the path to those four roles. An area with only one of the two cannot answer all
five questions on its own. It is not deleted from the record — it is either folded inside a kept
area or named in the cut list with its reason, and it comes back if you say so.

**What I did not do.** I did not invent a category. Every name below comes from the 63, which come
from what the field itself files. No area is cut here for being small, quiet or unfashionable.

---

## The proposal, in one table

| # | Area | Sources | What it is for |
|---|---|---|---|
| 1 | **Machine learning** | 8 | the theory under everything else |
| 2 | **Deep learning and representations** | 3 | architectures, and what a model learns |
| 3 | **Reinforcement learning** | 4 | learning from interaction; how reasoning models are trained |
| 4 | **Language models** | 8 | the model class the named roles are built around |
| 5 | **Training and post-training** | 1 | how a research result becomes a shipped model |
| 6 | **Computer vision** | 8 | the second mature modality |
| 7 | **Generative models and media** | 2 | images, audio, video, voice — one research base, one practice |
| 8 | **AI infrastructure and inference** | 5 | serving, compute, hardware, cost |
| 9 | **Agentic systems** | 2 | the engineering the AI Engineer role is defined by |
| 10 | **Retrieval and data** | 3 | what you give a model, and where it comes from |
| 11 | **Evaluation and measurement** | 4 | how anyone knows whether it works |
| 12 | **Safety, security and trustworthy ML** | 6 | interpretability, robustness, attack and defence |

**12 kept · 27 folded into a kept area · 24 cut. 12 + 27 + 24 = 63.**

---

## The twelve, with the reason for each

### 1. Machine learning — 8 sources

**Folds in:** general machine learning (3), theory of machine learning (3), Optimization (3),
probabilistic methods (3), Generalization and multi-task learning (2).

**Why these are one area.** Each is a topic line on an ICML, ICLR or NeurIPS call. They are slices of
one body of theory, cut differently by each venue. Taught apart they become five short chapters that
keep referring to each other; taught together they are the **theoretical depth** capability §1.1
names first.

**Why it is kept.** It is the only area that answers §3.1 question 3 — established scientific
knowledge — for everything downstream. Without it the book is a tour of tools.

### 2. Deep learning and representations — 3 sources

**Folds in:** representation learning for computer vision, audio, language and other modalities (1);
unsupervised, self-supervised, semi-supervised and supervised representation learning (1); learning
on graphs and other geometries & topologies (1); visualization or interpretation of learned
representations (1).

**Why.** Architectures and representations are where research reaches engineering fastest, which is
question 4. The interpretability topic sits here rather than under safety because what it
interprets is a representation.

### 3. Reinforcement learning — 4 sources

**Folds in:** Reasoning + RL (1).

**Why.** Four venues give it its own topic. It is also how current reasoning models are trained,
which puts it directly on the role path rather than in the history of the field.

### 4. Language models — 8 sources

**Folds in:** Natural Language Processing is the kept record; Language and multimodal language
models (1) merges into it. ACL's 29 remaining topics already sit below it.

**Why.** The four roles in §1.1 are, as advertised today, largely language-model roles. Eight sources
name this boundary — joint highest in the register.

### 5. Training and post-training — 1 source

**Why, on one source.** It is the stage where a research result becomes a model somebody ships —
§3.1 question 4 in its purest form, and the part of the pipeline a Research Engineer owns. The
framing run records that **no 2026 venue track names pre-training at all**, so this is the only
registered boundary covering training stages.

**This is the weakest keep in the list** and the first one to challenge. It rests on one applied
source and on my reading of the role, not on agreement between sources.

### 6. Computer vision — 8 sources

**Folds in:** nothing. CVPR's 32 subject areas already sit below it.

**Why.** Eight sources, and the second modality with a complete research-to-production stack. It is
also where many methods are proved before they reach language.

### 7. Generative models and media — 2 sources on the kept name

**Folds in:** Generative Media (2), Voice & Realtime AI (2), Audio and Speech Processing (1).

**Why these are one area.** Diffusion and flow methods, audio generation and speech are one research
base and one production practice. Separately they are four thin areas; together they carry both a
science side and an engineering side.

### 8. AI infrastructure and inference — 5 sources

**Folds in:** Inference (1), Local AI (1), Model (1).

**Why.** The systems layer: serving, compute, hardware, distributed methods, latency and cost. This
is the **hands-on engineering** capability, and it is where the Machine Learning Engineer role
mostly lives.

### 9. Agentic systems — 2 sources on the kept name

**Folds in:** Harness Engineering (1), Context Engineering (1), Memory & Continual Learning (1).

**Why, on thin attestation.** The academic sources barely name it — ACL files it as `AI/LLM Agents`
and nothing else does. That is a fact about publishing lag, not about the work: this is the practice
the **AI Engineer** title currently denotes. **Three of its four parts are ⚠ areas** whose scope the
framing run wrote itself, because the source programme carries no track descriptions. So this area is
real and its boundary is the least evidenced in the list.

### 10. Retrieval and data — 3 sources on the kept name

**Folds in:** Search & Retrieval (2), Data (1), Graphs (2), Data Mining & Knowledge Management (4).

**Why.** Retrieval, data quality, pipelines and labelling are one subject from the point of view of
somebody building a system: what you give the model, and where it came from. DMKM brings the
academic half that the applied sources do not have.

### 11. Evaluation and measurement — 4 sources

**Folds in:** datasets and benchmarks (2). 25 MLCommons suites and groups already sit below it.

**Why.** This is §1.1's **experimentation skill** capability — reproduce, test, evaluate — and the
one area that gives the rest of the book its evidence standard. The framing run notes that `Power`
is the only energy category in the whole register, and it sits here.

### 12. Safety, security and trustworthy ML — 6 sources

**Folds in:** Safety (2), Security (4).

**Why.** Six sources on trustworthy ML alone, academic and applied. Interpretability, robustness,
red-teaming and privacy are simultaneously live research and shipped engineering, which is the
clearest pass of the five-question test in the whole list.

---

## What I cut, and why — 24

### Classical symbolic AI — 10

Knowledge Representation and Reasoning (6), Planning Routing and Scheduling (5), Search and
Optimization (4), Game Theory and Economic Paradigms (4), Constraint Satisfaction and Optimization
(3), Reasoning under Uncertainty (3), Cognitive Modeling & Cognitive Systems (2), causal reasoning
(1), neurosymbolic & hybrid AI systems (1), Neural and Evolutionary Computing (1).

**Why.** These are well attested — AAAI and IJCAI organise the whole classical field, so their
calls name every one. **Attestation measures how the field files its conferences, not what the four
roles in §1.1 require.** The research here is largely mature, which means question 1 (ongoing
research) and question 4 (research-to-engineering transition) have thin answers today.

**What this costs, said plainly.** Cutting KRR and PRS removes most of the symbolic tradition from
the book. If the goal were "AI Researcher" in the academic sense, several of these would belong.
**`causal reasoning` and `neurosymbolic` are the two I am least sure of** — both are live, both are
thin, and both overlap what Deep learning and Trustworthy ML already carry.

### Separate career tracks — 2

**Intelligent Robotics (10 sources)** and **Multiagent Systems (5)**.

**Robotics is the most-attested boundary in the entire register**, so this is the cut that most
needs its reason stated: it is a field with its own hardware, control theory, simulation and safety
stack, and none of the four roles in §1.1 is a robotics role. Multiagent Systems is coordination
theory; the agent work the roles ask for is in area 9, which is a different subject under a similar
name.

**This is the single most reversible cut in the list.** If robotics is in your target, say so and it
comes back as area 13.

### The surrounding trade, not the science or engineering of AI — 5

Design Engineering (2), Software Factories (2), Sandbox & Platform Engineering (1), Notebook
Environment (1), Programming (1).

**Why.** These are how software is built around AI, not how AI is built. Two of them are ⚠ areas
whose scope the framing run wrote itself. They would teach you tooling you already have.

### Standards and conformance — 3

Foundational standards (1), Functional safety and AI systems (1), Computational approaches and
characteristics of AI systems (1).

**Why.** ISO/IEC SC 42 working groups. They standardise terminology and conformance process. That is
real work, but it is neither research nor building, and it answers question 1 with nothing.
**Relevant if you target a regulated industry** — say so and they come back.

### Philosophy, and human interaction — 2

**Philosophy and Ethics of AI (5)** — tagged science only, with no engineering side at all. The parts
that touch practice are already inside area 12.

**Humans and AI (5)** — a genuine research area. Cut because for the four named roles it is
secondary, and its engineering half is interface work. **The second cut I am least sure of.**

### The two umbrellas — 2

**Artificial intelligence (ACM CCS)** and **Artificial Intelligence (cs.AI)**. The consolidation run
says both sit outside the level and that reading the list flat would double-count their contents.
They are index nodes, not areas.

---

## What this proposal does not settle

- **The order of the twelve, and which become parts of the book.** That is step 7 and needs the
  research first.
- **Whether twelve is the right number.** I did not aim at a count. It is what the test yielded. You
  earlier said "roughly ten"; this is twelve, and areas 5, 9 and 10 are where it would shrink.
- **The three gaps no source reported**: pre-training, role- and job-shaped categories, and anything
  named only in a non-English venue. Area 5 covers part of the first. The other two stay open.
- **Area 9's boundary** rests on scope the framing run wrote itself for three of its four parts. It
  is the one area where I would expect the first scout to come back and redraw the edges.

## What happens when you approve it

Each approved area gets one scout — `briefs/TEMPLATE-area-research.md` — which finds the subjects
inside it and returns them with sources. That is step 5. The scopes and exclusions each scout is
given are written from this list in the same sitting, and writing them is mine as well, by the same
argument as this proposal.
