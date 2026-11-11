<div align="justify">

# Fault Injection: Find the Component That Failed

| | |
| --- | --- |
| **Type** | Lab — break the system on purpose, diagnose from evidence, then check |
| **For** | [11. Compound AI Systems: Tools, Retrieval and Verification](../LEARNING-GUIDE.md#11-compound-ai-systems-tools-retrieval-and-verification) |
| **You should already have** | [the agent loop you built](agent-loop-exercise.md), your step 9 retriever, and an evaluation you trust from step 6 |
| **Needs** | Python, standard library only. The harness runs offline |
| **Sources** | Kapoor et al., "AI Agents That Matter" · Kambhampati et al., LLM-Modulo · Liu et al., "Lost in the Middle" |

A compound system gives you one symptom — a wrong answer — and five candidate causes: retrieval, context, the tool, the model's decision, or your own orchestration code. The skill this lab builds is not knowing which it *usually* is. It is producing evidence that distinguishes them, quickly, before you start changing things.

The method is the one you already use for data: create the failure yourself, under control, so you learn what each failure *looks like* from the outside. Then when one arrives uninvited, you recognize its signature.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Faults](#1-the-faults)
2. [The Harness](#2-the-harness)
3. [Run It Blind](#3-run-it-blind)
4. [Signatures](#4-signatures)
5. [Do It To Your Own System](#5-do-it-to-your-own-system)

</details>

---

## 1. The Faults

Six faults, each a plausible thing that happens in production rather than an invention for the lab.

| # | Fault | What actually happens in production |
| --- | --- | --- |
| 1 | Retrieval returns nothing | An index rebuild fails; a filter excludes everything |
| 2 | Retrieval returns confidently wrong passages | Embedding model swapped; a near-duplicate outranks the right passage |
| 3 | A tool raises an error | A dependency times out, a credential expires |
| 4 | A tool returns malformed output | An upstream API changes a field name or a unit |
| 5 | The context is truncated | The history outgrows the budget and the middle is dropped |
| 6 | The model's step does not parse | A model update changes the output format |

Faults 1, 2 and 5 produce *fluent, plausible, wrong* answers — the ones that are dangerous because nothing looks broken.

[⬆ Back to Contents](#contents)

---

## 2. The Harness

```python
"""Inject one fault at a time into a retrieve-then-answer pipeline and read the trace."""
import random

random.seed(7)

DOCS = {
    "refund-policy": "Refunds are issued within 14 days of purchase, minus shipping.",
    "returns-policy": "Items may be returned unopened within 30 days for store credit.",
    "shipping": "Standard shipping takes 3-5 working days.",
}

def retrieve(query: str, fault: str | None) -> list[str]:
    if fault == "empty":
        return []
    if fault == "wrong":
        return [DOCS["shipping"]]                      # plausible, unrelated
    hits = [text for key, text in DOCS.items() if key.split("-")[0] in query.lower()]
    return hits or [DOCS["refund-policy"]]

def call_tool(name: str, fault: str | None) -> str:
    if fault == "tool_error":
        raise TimeoutError("order-service did not respond")
    if fault == "tool_malformed":
        return '{"purchase_date": "01/09/2026"}'        # day-first, undeclared
    return '{"purchase_date": "2026-09-01"}'

def build_context(goal: str, passages: list[str], tool_output: str, fault: str | None) -> str:
    parts = [f"GOAL: {goal}", *passages, f"TOOL: {tool_output}"]
    context = "\n".join(parts)
    if fault == "truncated":
        context = context[: len(context) // 2]         # the middle and end are gone
    return context

def answer(context: str, fault: str | None) -> str:
    """A stand-in model: answers from what it was given, and never says 'I don't know'."""
    if fault == "unparsable":
        return '<tool_call name="order_service"'          # truncated, unparsable
    has_refund_rule = "14 days" in context
    has_date = "2026-09-01" in context
    if has_refund_rule and has_date:
        return "Not refundable: 20 days have passed, past the 14-day window. Offer a return."
    if has_refund_rule:
        return "Refunds are available within 14 days of purchase."
    return "This purchase is eligible for a refund; please process it."  # confident, wrong

def run(fault: str | None = None) -> dict:
    goal = "Is this refund request within policy?"
    passages = retrieve("refund window", fault)
    try:
        tool_output = call_tool("order_service", fault)
    except Exception as exc:
        tool_output = f"ERROR: {exc}"
    context = build_context(goal, passages, tool_output, fault)
    return {"fault": fault or "none",
            "passages": len(passages),
            "context_chars": len(context),
            "tool_output": tool_output[:40],
            "answer": answer(context, fault)}

FAULTS = (None, "empty", "wrong", "tool_error", "tool_malformed", "truncated", "unparsable")
for fault in FAULTS:
    r = run(fault)
    print(f"{r['fault']:14s} passages={r['passages']}  ctx={r['context_chars']:3d}  "
          f"tool={r['tool_output']:34s} answer={r['answer'][:58]}")
```

[⬆ Back to Contents](#contents)

---

## 3. Run It Blind

Do this before reading section 4, and do it with a colleague if you can.

1. Have someone else (or a script) pick one fault at random and run only that line, showing you **the answer alone**.
2. From the answer, write down your hypothesis and the *single* piece of evidence you would ask for next.
3. Ask for that evidence — one field of the trace, nothing more — and revise.
4. Record how many pieces of evidence you needed to be sure.

The count is the point. An engineer who needs the whole trace to diagnose anything will not be able to diagnose a system whose trace is ten thousand tokens long.

[⬆ Back to Contents](#contents)

---

## 4. Signatures

After running all seven rows, fill in this table from what you saw, then compare with your hypotheses.

| Fault | What the answer looks like | Which field of the trace settles it in one look |
| --- | --- | --- |
| none | | |
| empty | | |
| wrong | | |
| tool_error | | |
| tool_malformed | | |
| truncated | | |
| unparsable | | |

Then answer the four questions that matter more than the table:

1. **Three of the faults produce the same answer, word for word.** Which three, and what is the smallest piece of evidence that separates each from the others? (They are the reason a trace records retrieval results and context size, not just the final text.)
2. **Which fault produces an answer that is confidently wrong with no error anywhere?** What would have to be true of your evaluation for you to notice it in production?
3. **The malformed tool output is a date in another format.** Nothing raised. Where should that have been caught — the tool, the parser, or a check on the answer — and what does your choice cost?
4. **Truncation removed the middle of the context.** Relate what you saw to the "lost in the middle" result you read in step 11: what does that imply about long-context systems that look fine in testing?

[⬆ Back to Contents](#contents)

---

## 5. Do It To Your Own System

Take the compound system from your step 11 practice and inject the same six faults, one at a time, with a flag rather than by editing code.

- Write the **diagnosis you would make from the output alone**, before looking at the trace.
- Note which faults your evaluation catches automatically and which pass it silently. The silent ones are your next tests, in the sense of [the testing checklist](ml-testing-checklist.md).
- Add one check that turns the most dangerous silent failure into a loud one — a grounding check, a schema assertion, a retrieval-quality floor — and prove it works by re-injecting the fault.

**Completion criterion.** Given a bad output from your own system, you can name the component responsible with evidence rather than intuition, and you have at least one automatic check that fires for a failure that used to be silent. Step 12 then asks the harder question: whether the measurement that told you it was working deserves to be believed.

[⬆ Back to Contents](#contents)

</div>
