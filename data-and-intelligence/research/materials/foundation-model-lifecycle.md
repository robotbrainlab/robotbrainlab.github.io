<div align="justify">

# Reading the Foundation-Model Lifecycle: What Is Settled, What Is Current, What Is Contested

| | |
| --- | --- |
| **Type** | Conceptual brief — how to hold claims about post-training, verifiable rewards and distillation with the confidence each deserves |
| **For** | [10. How Foundation Models Are Made and Adapted](../LEARNING-GUIDE.md#10-how-foundation-models-are-made-and-adapted), and again at [15. Trustworthy AI and Security](../LEARNING-GUIDE.md#15-trustworthy-ai-and-security) for fine-tuning side effects |
| **You should already have** | *AI Engineering* chapter 2 on pretraining and post-training, and [the reinforcement-learning arc](reinforcement-learning-arc.md) |
| **Evidence** | Every status below comes from this project's [landscape research](../research/2026-09-17-data-intelligence-landscape.md) and, where a practice is contemporary, from the [current-practice register](../reviews/modern-practice-register.md) that the four-week scan maintains. Where the evidence is thin or the field disagrees, this brief says so rather than choosing a side |

This part of AI moves faster than any book can follow, which is why the roadmap writes this page itself and rewrites it on a schedule. Its purpose is not to list techniques — *AI Engineering* does that — but to teach you the habit the rest of your career depends on here: sorting what you read into **settled**, **current practice** and **contested**, and acting differently on each.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Three Confidences](#1-the-three-confidences)
2. [The Lifecycle, Claim by Claim](#2-the-lifecycle-claim-by-claim)
3. [Two Claims Worth Holding Loosely](#3-two-claims-worth-holding-loosely)
4. [What an Adaptation Changes That You Did Not Ask For](#4-what-an-adaptation-changes-that-you-did-not-ask-for)
5. [Use It](#5-use-it)

</details>

---

## 1. The Three Confidences

| Confidence | What it means | What you are entitled to do with it |
| --- | --- | --- |
| **Settled** | Reproduced widely, stable for years, and not seriously disputed | Build on it; explain it as fact; expect it to still be true next year |
| **Current practice** | What competent engineers do now, with real evidence behind it, but shaped by tools and costs that change | Use it, and say *when* you learned it; expect the details to move and the reasons to stay |
| **Contested** | The field disagrees, or the evidence is thin, or the result has not been reproduced independently | Quote it as a claim with an author attached, never as background; design so that being wrong about it is survivable |

The failure this prevents is not believing something false. It is believing something true *with the wrong strength* — planning a system around a result that three months later turns out to have been one lab's benchmark.

[⬆ Back to Contents](#contents)

---

## 2. The Lifecycle, Claim by Claim

| Stage | The claim | Confidence | What to do about it |
| --- | --- | --- | --- |
| Pretraining | Capability comes mostly from scale and data curation; the model learns to predict the next token on very large general corpora | Settled | Treat the base model as a fixed input you did not make |
| Supervised fine-tuning | Training on demonstrations turns a next-token predictor into something that follows instructions; it is now one stage among several rather than the whole of alignment | Settled as a technique; its *place in the pipeline* is current practice | Expect SFT → preference → RL as the usual order, and expect the order to be revised |
| Preference optimization | Human comparisons are turned into a training signal, through a reward model with reinforcement learning, or directly through closed-form objectives | RLHF settled; direct preference methods current practice, often as an intermediate stage | Know both exist; do not assume a given model used either |
| Reinforcement learning from verifiable rewards | For tasks with programmatic checks — tests, exact answers — the reward is computed, not modelled, and this is how reasoning models are produced | Current practice for reasoning models; the algorithmic details are active research | Understand the idea; treat specific recipes as this season's |
| Distillation | A smaller student trained on a larger teacher's outputs, or on its own outputs graded by the teacher, retains much of the capability at lower cost, and can restore capability lost to fine-tuning | Current practice; on-policy variants emerging | A live option whenever cost is the constraint; verify the retained capability yourself |
| Test-time compute | Spending inference on intermediate reasoning, sampling several answers, or verifying them buys accuracy you did not train for | Current practice | Remember that it moves cost from training to every request — which is step 16's problem |

Notice what the table does not contain: any number. Benchmark figures age faster than the practices do, and a number you memorize today is a claim you will repeat wrongly in a year.

[⬆ Back to Contents](#contents)

---

## 3. Two Claims Worth Holding Loosely

**Does reinforcement learning add capability, or surface it?** When a model trained with verifiable rewards solves problems the base model failed, the natural reading is that training taught it something new. The alternative reading is that the base model could already produce the right answer sometimes, and training re-weighted it towards doing so reliably. The field has not settled this, and the roadmap's evidence marks it as an **active debate**. It matters to you practically: on the first reading, more RL is a path to new capability; on the second, it is a path to reliability, and the ceiling is set by the base model you started from.

**Does a visible chain of thought explain the answer?** A model that writes out its reasoning is not thereby showing you the computation that produced its answer. Studies find models omitting influences that demonstrably changed their output, and the evidence on when reasoning traces can be trusted is **contested**. Treat a chain of thought as an artefact the model produced, not as an explanation — a distinction step 12 sharpens and step 15 relies on.

For both: if a design decision depends on which way the question resolves, that dependency is a risk to write down, not a detail.

[⬆ Back to Contents](#contents)

---

## 4. What an Adaptation Changes That You Did Not Ask For

Fine-tuning has a property that makes it unlike other engineering changes: **its effects are not confined to the behaviour you tuned.** Training on a narrow task can move behaviour far outside that task, including in directions nobody intended. Narrow fine-tuning producing broad behavioural change — the literature calls the alarming end of this *emergent misalignment* — is an **active research** area whose mechanism is not settled, and the evidence is strong enough that the practical rule does not depend on the mechanism:

> **Never evaluate an adapted model only on the task you adapted it for.**

Your step 10 practice applies this directly, and step 15 returns to it as a security property. Keep a held-out slice of general behaviour — instruction following, refusals, tone, a few capabilities you did not touch — and measure it before and after every adaptation. If the target metric improves and something else falls, you have found the trade you were about to ship without knowing.

[⬆ Back to Contents](#contents)

---

## 5. Use It

Take one claim about the foundation-model lifecycle from anywhere you like — a paper you have read, a vendor's post, a conference talk, a colleague's assertion — and write four lines:

1. The claim, stated precisely enough to be wrong.
2. Its confidence: settled, current practice, or contested — and the evidence you are relying on for that judgment.
3. What you would do differently if it were false.
4. What evidence would change your mind, and whether anyone is in a position to produce it.

Keep the note. Step 13 turns this into a repeatable method for reading research, and it will be a good deal easier there for having done it here.

[⬆ Back to Contents](#contents)

</div>
