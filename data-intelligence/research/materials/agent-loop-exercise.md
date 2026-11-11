<div align="justify">

# Build the Loop Yourself

| | |
| --- | --- |
| **Type** | Exercise — implement the mechanism, then watch it work and fail |
| **For** | [11. Compound AI Systems: Tools, Retrieval and Verification](../LEARNING-GUIDE.md#11-compound-ai-systems-tools-retrieval-and-verification) |
| **You should already have** | Kambhampati et al. on generate-and-verify, Kapoor et al. on agent evaluation, *AI Engineering* chapter 6 on agents and memory, and a retriever of your own from step 9 |
| **Needs** | Python, standard library only for the skeleton. A model call is optional and the exercise works without one |
| **Sources** | Kambhampati et al., LLM-Modulo · Kapoor et al., "AI Agents That Matter" · *AI Engineering* ch 6 |

An agent framework will give you a working loop in ten lines and leave you unable to say what happened when it misbehaves. The loop itself is small — small enough that you should write it once, by hand, before you ever adopt one. Then the frameworks become a convenience rather than a mystery, and the questions this roadmap keeps asking — which component failed, how much freedom does this task need, what did the model actually see — become answerable.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Loop in One Paragraph](#1-the-loop-in-one-paragraph)
2. [The Skeleton](#2-the-skeleton)
3. [What to Build](#3-what-to-build)
4. [Questions the Loop Forces You to Answer](#4-questions-the-loop-forces-you-to-answer)
5. [Connect It to Your Own System](#5-connect-it-to-your-own-system)

</details>

---

## 1. The Loop in One Paragraph

The model receives a context: the goal, the tools it may call and what has happened so far. It emits one step — either a tool call or a final answer. Your code, not the model, executes the tool, observes the result, appends it to the context, and calls the model again. That repeats until the model answers, or until a limit you set stops it.

Everything that makes agents hard is in the words *your code*: what you put in the context, which tools exist, what happens when one fails, when you stop, and what you do with a step that does not parse.

[⬆ Back to Contents](#contents)

---

## 2. The Skeleton

This runs as it stands, with a stand-in for the model so the mechanism is visible without an API key. The stand-in is deliberately crude: replacing it with a real model call is the second half of the exercise.

```python
"""A minimal agent loop: decide, act, observe, repeat — with the state visible."""
from dataclasses import dataclass, field

# ---- tools: ordinary functions, with the description the model will rely on ----------

def search_policy(query: str) -> str:
    """Search the policy archive. Returns the best matching passage."""
    archive = {
        "refund": "Refunds are issued within 14 days of purchase, minus shipping.",
        "returns": "Items may be returned unopened within 30 days.",
    }
    for key, passage in archive.items():
        if key in query.lower():
            return passage
    return "NO MATCH"

def days_between(a: str, b: str) -> str:
    """Whole days between two ISO dates, as a string."""
    from datetime import date
    return str((date.fromisoformat(b) - date.fromisoformat(a)).days)

TOOLS = {"search_policy": search_policy, "days_between": days_between}

# ---- the loop's state: what the model sees, and what you keep -------------------------

@dataclass
class Trace:
    goal: str
    steps: list[dict] = field(default_factory=list)

    def context(self) -> str:
        """Everything the model is given. Nothing else is in scope."""
        lines = [f"GOAL: {self.goal}", f"TOOLS: {', '.join(TOOLS)}"]
        for i, step in enumerate(self.steps, start=1):
            lines.append(f"[{i}] {step['action']} -> {step['observation']}")
        return "\n".join(lines)

# ---- the model: replace this function, and only this function -------------------------

def decide(context: str) -> dict:
    """Return the next step: {'tool': name, 'args': {...}} or {'answer': text}.

    This stand-in follows a fixed script so the loop can be watched. A real
    implementation sends `context` to a model and parses what comes back — and
    then the parsing, not the model, is where your first bugs will be.
    """
    if "[1]" not in context:                   # nothing done yet: read the policy
        return {"tool": "search_policy", "args": {"query": "refund window"}}
    if "[2]" not in context:                   # policy in hand: work out the days
        return {"tool": "days_between", "args": {"a": "2026-09-01", "b": "2026-09-21"}}
    return {"answer": "Outside the 14-day refund window by 6 days; offer a return instead."}

# ---- the loop -------------------------------------------------------------------------

def run(goal: str, max_steps: int = 6) -> Trace:
    trace = Trace(goal=goal)
    for _ in range(max_steps):
        step = decide(trace.context())
        if "answer" in step:
            trace.steps.append({"action": "ANSWER", "observation": step["answer"]})
            return trace
        name, args = step["tool"], step.get("args", {})
        if name not in TOOLS:                  # a tool the model invented
            trace.steps.append({"action": name, "observation": "ERROR: no such tool"})
            continue
        try:
            observation = TOOLS[name](**args)
        except Exception as exc:               # a tool can fail; the loop must not
            observation = f"ERROR: {type(exc).__name__}: {exc}"
        trace.steps.append({"action": f"{name}({args})", "observation": observation})
    trace.steps.append({"action": "STOP", "observation": "step budget exhausted"})
    return trace

if __name__ == "__main__":
    result = run("Is this purchase still refundable, and what should we offer?")
    print(result.context())
```

[⬆ Back to Contents](#contents)

---

## 3. What to Build

Run the skeleton, then make these five changes in order. Each one is a decision, not a feature.

1. **Replace `decide` with a real model call.** Send the context, ask for one step in a fixed format, and parse it. Count how many of your first twenty runs produce something you cannot parse. That number is your first reliability measurement and it is usually not zero.
2. **Give the model a real tool of your own** — the retriever you built in step 9. Write its description as if the model were a new colleague who can read one sentence about it and nothing else.
3. **Decide what the model sees.** The skeleton appends every observation forever. Choose a policy — full history, last k steps, a summary — and measure what it does to cost and to answers. This is the context budget of step 11, met as an implementation choice.
4. **Handle the three failure paths explicitly**: the model asks for a tool that does not exist, the arguments do not fit, the tool raises. The skeleton does something for each; decide whether it is the right thing.
5. **Choose a stopping rule.** A step budget is the crudest. Add one more: no progress, repeated identical calls, cost ceiling, or a verifier that says the answer is good enough.

[⬆ Back to Contents](#contents)

---

## 4. Questions the Loop Forces You to Answer

Write your answers next to the code.

- **Who decides?** List every decision in your loop and mark whether the model or your code makes it. Most reliability problems are decisions that drifted into the first column.
- **What is the trace for?** Yours records actions and observations. What would you need in it to explain a bad answer a week later — and what would you need to *not* record for privacy reasons?
- **Where would a framework have hidden this?** Name the two decisions above that a framework would have made for you, and say whether its default matches what you chose.
- **What makes a run correct?** Not "it answered" — a criterion you could evaluate over repeated trials, in the sense of [the repeated-trial simulation](repeated-trial-simulation.md).

[⬆ Back to Contents](#contents)

---

## 5. Connect It to Your Own System

Your step 11 practice extends the evolving system into a compound system. Use this loop as its controller, and keep the trace: [the fault-injection lab](fault-injection-lab.md) breaks this exact system on purpose, and [the autonomy rubric](autonomy-rubric.md) decides how much of it should be allowed to act without you.

**Completion criterion.** You can run a task end to end, show the trace, point at the step where the model decided something, and say what your code would have done if that decision had been wrong.

[⬆ Back to Contents](#contents)

</div>
