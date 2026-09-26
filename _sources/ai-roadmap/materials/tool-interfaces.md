<div align="justify">

# A Tool Is an Interface

| | |
| --- | --- |
| **Type** | Conceptual note — the durable idea underneath whichever protocol is current |
| **For** | [11. Compound AI Systems: Tools, Retrieval and Verification](../LEARNING-GUIDE.md#11-compound-ai-systems-tools-retrieval-and-verification) |
| **You should already have** | Structured outputs and tool use from *AI Engineering* chapters 2 and 6, and [an agent loop with tools of your own](agent-loop-exercise.md) |
| **Its counterpart in the other track** | [Agents, Tools and Context](../LEARNING-GUIDE.md#agents-tools-and-context) teaches the interoperability specification practitioners use now. This note is what stays true when that specification is replaced |
| **Sources** | *AI Engineering* chs 2 and 6 · Kambhampati et al., LLM-Modulo |

When a model calls a tool, two systems that were designed independently have to agree about something. That is an interface problem, and interface problems have a century of accumulated engineering wisdom behind them — almost all of which applies here, with one twist that changes the design: **the caller is a language model, and the only documentation it has is what you wrote in the description.**

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [What the Contract Contains](#1-what-the-contract-contains)
2. [The Twist: Your Documentation Is the Implementation](#2-the-twist-your-documentation-is-the-implementation)
3. [Least Privilege, Stated as a Design Rule](#3-least-privilege-stated-as-a-design-rule)
4. [Rewrite a Bad Tool](#4-rewrite-a-bad-tool)

</details>

---

## 1. What the Contract Contains

Every tool interface, under any protocol, has to settle the same six things. If your design does not answer one of them, the model will answer it for you at runtime.

| Element | The question it settles | What goes wrong when it is vague |
| --- | --- | --- |
| **Name** | Which capability is this | Two tools with overlapping names get confused under pressure |
| **Description** | When should it be used, and when not | The model calls it for tasks it was never meant for |
| **Inputs** | What must be supplied, in what types and units | Silent unit errors: days for dates, cents for dollars |
| **Output** | What comes back, in what shape | Your parser breaks when a field is renamed upstream |
| **Errors** | What failure looks like, distinguishably | A failure is read as an answer and reasoned onwards from |
| **Effects and privileges** | What changes in the world, and what the tool may touch | A read tool that can write; a scoped credential that is not scoped |

The list is unremarkable — which is the point. The discipline here is ordinary interface design, applied where teams often improvise because the caller is a model.

[⬆ Back to Contents](#contents)

---

## 2. The Twist: Your Documentation Is the Implementation

A human developer reading an unclear API can open the source, ask a colleague or experiment. A model has the description and the schema you gave it, and nothing else. This inverts the usual priority: with tools for models, the description *is* part of the implementation, and vague wording is a defect in the same sense as a race condition.

Four rules follow, each of which you can test on the loop you built.

- **Name the capability, not the endpoint.** `find_order_by_customer_email` beats `orders_get_v2`. The model matches on meaning.
- **Say when *not* to use it.** A description that ends "use this only for orders placed in the last 90 days; for older orders use the archive tool" prevents a whole class of wrong calls.
- **Make the arguments hard to get wrong.** Enumerated values instead of free text, explicit units in the field name (`amount_cents`, `date_iso`), and required fields that really are required.
- **Return something the model can use and your code can check.** A structured result with a status, so success and failure are distinguishable without reading prose — and so your orchestration code can branch on it before the model ever sees it.

Fewer, well-described tools beat many thin ones. Every additional tool is another choice the model makes on each step, and the failure modes of [the fault-injection lab](fault-injection-lab.md) compound with the number of choices.

[⬆ Back to Contents](#contents)

---

## 3. Least Privilege, Stated as a Design Rule

A tool is a permission you have granted to a system that sometimes decides wrongly. Two rules keep that bounded, and step 15 turns both into security requirements.

1. **Grant the narrowest capability that does the job.** Not "database access" but "look up an order by id, returning these four fields". The narrow version is also the one with the clearer contract, which is why security and reliability pull in the same direction here.
2. **Separate the untrusted from the powerful.** A tool that reads content you do not control and a tool that acts on the world should not be reachable within the same unchecked step. That combination — untrusted input, sensitive access, external action — is exactly what step 15's containment design exists to break up.

A useful test before adding any tool: *if the model called this at the worst possible moment with the worst plausible arguments, what would happen, and who would find out?* If the answer is uncomfortable, the fix is the interface, not a better prompt.

[⬆ Back to Contents](#contents)

---

## 4. Rewrite a Bad Tool

Here is a tool as teams often first write it:

```text
name: query
description: Runs a query against the system and returns the result.
inputs:  { "q": "string" }
output:  free text
errors:  returns the string "error" on failure
effects: unspecified
```

Rewrite it as a proper contract, for one real capability in your own system. Then answer:

1. **What did you have to decide** that the original left open? List each item — those were the decisions the model was making for you.
2. **Which of your six elements is weakest**, and what would it cost to strengthen it?
3. **Give the description to a colleague who does not know your system**, with the goal but not the code, and ask them when they would call the tool. Their answer is a cheap approximation of what the model will do.
4. **What would this look like under the current interoperability specification** taught in the Modern track — and which parts of your contract would survive a switch to a different one? Those parts are the design; the rest is plumbing.

**Completion criterion.** Every tool in your compound system has a name, a description that says when not to use it, typed inputs with units, a checkable output, distinguishable errors, and a privilege you could defend in a security review.

[⬆ Back to Contents](#contents)

</div>
