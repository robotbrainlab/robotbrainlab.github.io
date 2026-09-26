<div align="justify">

# The Reinforcement-Learning Arc Behind Post-Training

| | |
| --- | --- |
| **Type** | Conceptual note — a bridge between two things the assigned reading treats separately |
| **For** | [10. How Foundation Models Are Made and Adapted](../LEARNING-GUIDE.md#10-how-foundation-models-are-made-and-adapted) |
| **You should already have** | The gradient reasoning of step 2, a model you trained in step 3, the language-model mechanism you built in step 8, and *Hands-On ML* chapter 19 on Markov decision processes and policy gradients |
| **What it is not** | A reinforcement-learning course. It explains why RL vocabulary appears in post-training and what each borrowed term does there; the algorithms themselves belong to the extension path |
| **Sources** | *Hands-On ML with Scikit-Learn and PyTorch* ch 19 · Huyen, *AI Engineering* ch 2, post-training |

The assigned reading leaves a gap you will notice immediately. *Hands-On ML* teaches reinforcement learning with agents, states and rewards. *AI Engineering* describes post-training with prompts, responses and preferences, and uses words like *policy*, *reward model* and *KL penalty* as if you already knew why they were there. Nothing in between says why a method built for an agent walking through a maze ends up training a model that answers questions. That sentence is what this note supplies.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Shape of the Problem](#1-the-shape-of-the-problem)
2. [What Each Borrowed Term Becomes](#2-what-each-borrowed-term-becomes)
3. [Why There Is a KL Term](#3-why-there-is-a-kl-term)
4. [What Changes When the Reward Is a Program](#4-what-changes-when-the-reward-is-a-program)
5. [Check Yourself](#5-check-yourself)

</details>

---

## 1. The Shape of the Problem

Supervised training needs a right answer for every input. That is exactly what you do not have for most of what you want a model to do. Nobody can write the single correct reply to *"explain this error message to a junior colleague"*, and asking annotators to write one produces a narrow target that rewards imitation of the annotator rather than usefulness to the reader.

But something weaker is available: given two replies, a person can usually say which is better. That is a *comparison*, not a label, and it is the reason reinforcement learning enters the picture. Reinforcement learning is the branch of machine learning built for the case where you cannot say what the right action was, only how good the outcome turned out to be. It is the only well-developed body of method for learning from a signal of that shape.

So post-training is not RL because language modelling is secretly a maze. It is RL because the supervision has the shape RL was invented for: a score on what the model did, not a target for what it should have done.

[⬆ Back to Contents](#contents)

---

## 2. What Each Borrowed Term Becomes

Every term you met in chapter 19 has a counterpart here, and the counterparts are unusually simple because this problem is a degenerate case of the one RL usually solves.

| In chapter 19 | In post-training | Why it collapses |
| --- | --- | --- |
| Policy — what the agent does in a state | The model itself: given a prompt, a distribution over next tokens | The model *is* the policy; training the policy means changing the weights you have been studying since step 7 |
| State | The prompt plus the tokens generated so far | The state is just the context window you built in step 8 |
| Action | The next token | The action space is the vocabulary |
| Episode | One complete response | Episodes are short and always terminate |
| Reward | A score for the finished response | Usually one number at the end, not a reward at each step |
| Value function, discounting, exploration over long horizons | Mostly absent or simplified | With one reward at the end of a short episode, the long-horizon machinery RL needs for mazes has little to do |

Read that table twice. It is the whole translation. The reason post-training papers look intimidating is that they keep the RL notation while discarding most of the RL difficulty.

The one genuinely new part is where the reward comes from. In a maze the environment supplies it. Here, someone has to. Three answers are in use, and step 10's reading covers them: a **reward model** trained on human comparisons to predict which response a person would prefer; **direct preference methods**, which skip the separate reward model and optimize the comparisons directly; and **programmatic checks**, treated in [4](#4-what-changes-when-the-reward-is-a-program).

[⬆ Back to Contents](#contents)

---

## 3. Why There Is a KL Term

Here is the failure the KL term exists to prevent, and it is worth predicting before you read the answer: what would a model do if you optimized nothing but a learned reward?

It would find the reward model's mistakes. A reward model is a model: it is accurate on the kind of responses it was trained on and unreliable elsewhere. Optimize against it hard enough and the policy drifts into regions where the reward model is confidently wrong — producing text that scores highly and reads like nothing a person would want. This is Goodhart's law (step 6) wearing a different hat, and it is the reason the objective carries a second term.

That second term measures how far the model being trained has moved from the model it started as. **KL divergence** — named after Kullback and Leibler — is the standard measure of how different two probability distributions are; applied here, it compares the trained model's distribution over next tokens with the original's. Adding it to the objective says: improve the reward, *and stay recognizably the model you were*.

The trade-off is visible from both ends:

- **Too weak a penalty.** The model wanders, the reward keeps rising, and the outputs get worse. If a system's scores improve while its users complain, suspect this.
- **Too strong a penalty.** The model barely moves, and training achieves nothing.

This is also why post-training is described as *steering* a model rather than *teaching* it. The KL term is the leash, and choosing its strength is an engineering decision made on measurements, not a constant handed down.

[⬆ Back to Contents](#contents)

---

## 4. What Changes When the Reward Is a Program

For some tasks the reward does not need a model or a person at all: a unit test passes or fails, a solution matches a known answer, a program compiles. Training against that kind of automatic check is what recent work calls reinforcement learning from verifiable rewards, and the [lifecycle brief](foundation-model-lifecycle.md) covers its current status and the claims around it.

Conceptually it changes one thing and leaves the rest: the reward is now exact, cheap and unfakeable *within its domain*, so the Goodhart pressure of [3](#3-why-there-is-a-kl-term) moves rather than disappears. A model optimized against tests does not learn to deceive a reward model; it learns to satisfy tests, which is the same thing one level down — and whether satisfying tests generalizes to the capability you cared about is exactly the construct-validity question step 12 makes rigorous.

[⬆ Back to Contents](#contents)

---

## 5. Check Yourself

You have what this note exists to give you if you can answer these without looking back. Write the answers down; two of them come back in step 12 and step 15.

1. Why is post-training posed as reinforcement learning rather than as supervised learning? Answer in terms of the supervision available, not the algorithms.
2. What is the policy, and what does one episode consist of?
3. A team reports that their reward model's scores rose steadily during post-training and that human raters now prefer the *older* model. What single hypothesis explains this, and what would you measure to test it?
4. A colleague proposes raising the KL penalty until scores stop rising. Why is that a bad rule, and what would you measure instead?
5. A model is trained against an automatic checker. Name one capability claim that this training would support and one that it would not.

[⬆ Back to Contents](#contents)

</div>
