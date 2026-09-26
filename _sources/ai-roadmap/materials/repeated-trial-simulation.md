<div align="justify">

# Repeated Trials: What One Run Cannot Tell You

| | |
| --- | --- |
| **Type** | Simulation — an experiment you run, predict and interpret |
| **For** | [4. Statistics: Is the Difference Real?](../LEARNING-GUIDE.md#4-statistics-is-the-difference-real), and again as the testing counterpart in [6. Evaluation and Testing](../LEARNING-GUIDE.md#6-evaluation-and-testing) |
| **You should already have** | Sampling variability, intervals and the bootstrap (*Computational and Inferential Thinking* chs 10–13) |
| **Needs** | Python, standard library only. Runs in a second |
| **Sources** | Miller, "Adding Error Bars to Evals" · *Computational and Inferential Thinking* chs 10–13 |

Everything you have measured so far behaved the same way twice: run the same model on the same data and you get the same score. The systems you are about to build do not. The same prompt, the same input and the same model can give a different answer each time, and that changes what a measurement means — including what it means to say that a system "can" do something.

This simulation gives you that experience on a system whose truth you control, so that when you meet it in a system whose truth you do not, you recognize it.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Predict First](#1-predict-first)
2. [The Simulation](#2-the-simulation)
3. [What to Look For](#3-what-to-look-for)
4. [Capability and Reliability Are Different Claims](#4-capability-and-reliability-are-different-claims)
5. [Carry It Into Your Own System](#5-carry-it-into-your-own-system)

</details>

---

## 1. Predict First

Write your answers down before running anything. The value of this exercise is mostly in the gap between these predictions and what happens.

1. A stochastic system succeeds on a given task with probability 0.7, independently each attempt. You evaluate it once on 50 tasks. How far from 70% do you expect the score to be? Give a range you would be surprised to fall outside.
2. Two systems have true success rates of 0.70 and 0.75. You evaluate each once on 50 tasks. How often do you think the *worse* system will score higher?
3. A system succeeds 70% of the time per attempt. If a user may retry up to three times, what fraction of tasks will succeed at least once? If instead the task requires three steps that must *all* succeed, what fraction of tasks will complete?

[⬆ Back to Contents](#contents)

---

## 2. The Simulation

```python
"""Repeated trials: one run, many runs, and two different claims."""
import random
import statistics

random.seed(20260921)          # reproducible; change it and rerun to see what is stable

def run_eval(p: float, n_tasks: int) -> float:
    """One evaluation: n_tasks independent attempts at success probability p."""
    return sum(random.random() < p for _ in range(n_tasks)) / n_tasks

def spread(p: float, n_tasks: int, repeats: int = 2000) -> tuple[float, float, float]:
    """What a single evaluation of this system could report."""
    scores = [run_eval(p, n_tasks) for _ in range(repeats)]
    scores.sort()
    return scores[int(0.025 * repeats)], statistics.mean(scores), scores[int(0.975 * repeats)]

# 1. How much does one evaluation move?
for n in (20, 50, 200, 1000):
    lo, mean, hi = spread(0.70, n)
    print(f"n={n:5d}  single-run score usually between {lo:.2f} and {hi:.2f}  (mean {mean:.2f})")

# 2. How often does the worse system win a single head-to-head?
def worse_wins(p_a: float, p_b: float, n_tasks: int, repeats: int = 2000) -> float:
    return sum(run_eval(p_a, n_tasks) > run_eval(p_b, n_tasks) for _ in range(repeats)) / repeats

for n in (20, 50, 200, 1000):
    print(f"n={n:5d}  the 0.70 system beats the 0.75 system in "
          f"{worse_wins(0.70, 0.75, n):.0%} of evaluations")

# 3. Two claims about the same system: succeed once in k, or succeed k times running
def at_least_once(p: float, k: int, trials: int = 20000) -> float:
    return sum(any(random.random() < p for _ in range(k)) for _ in range(trials)) / trials

def all_of(p: float, k: int, trials: int = 20000) -> float:
    return sum(all(random.random() < p for _ in range(k)) for _ in range(trials)) / trials

print()
print("per-attempt success 0.70")
for k in (1, 3, 5, 10):
    print(f"  k={k:2d}  at least one succeeds: {at_least_once(0.70, k):.2f}"
          f"   every one succeeds: {all_of(0.70, k):.2f}")
```

[⬆ Back to Contents](#contents)

---

## 3. What to Look For

Compare the output against your predictions, then answer these in writing.

- **The interval at n = 50.** A system whose true rate is 0.70 routinely reports scores from roughly 0.58 to 0.82 on fifty tasks. If you had read one of those numbers in a report, what would you have concluded? What does this imply about the benchmark tables you will meet in step 13?
- **The head-to-head.** At n = 50 the worse system wins a surprising share of comparisons. This is not a bug in the simulation; it is what "the difference is not significant" means, felt rather than stated. Which of the two methods you learned in step 4 — an interval on the difference, or a paired comparison — reduces this, and why does pairing help here?
- **The two k columns.** They move in opposite directions. Write the sentence that explains why, without using the word "probability" twice.
- **Change one thing.** Set the two rates to 0.70 and 0.71 and find, by bisection, the n at which the better system wins 90% of the time. Was it what you expected? Is that n affordable for a system where each attempt costs a model call?

[⬆ Back to Contents](#contents)

---

## 4. Capability and Reliability Are Different Claims

The last block is the one that matters most in the rest of the roadmap.

> **"At least once in k attempts"** is a *capability* claim: the system can do this.
> **"Every attempt in k"** is a *reliability* claim: the system can be depended on to do this.

They are computed from the same per-attempt rate and they diverge fast. At 0.70 per attempt, a system that "can" do something in three tries almost always (0.97) completes a three-step task less than half the time (0.34). A demonstration shows you the first number. A user experiences the second.

This is why step 11 insists on evaluating whole trajectories over repeated trials, why step 6's tests for stochastic systems use tolerances rather than exact assertions, and why "it worked when I tried it" is not evidence. When you read a claim about an agent, your first question is now which of the two numbers is being quoted.

[⬆ Back to Contents](#contents)

---

## 5. Carry It Into Your Own System

On your evolving system, take one task type that is not deterministic — anything that involves a model call — and:

1. Run the same evaluation set three times without changing anything. Record the three scores.
2. Report your system's quality as an interval rather than a number, and write one sentence saying what produced the width.
3. If the system has any multi-step path, estimate both numbers: how often at least one attempt succeeds, and how often a whole run completes.

**Completion criterion.** You can state your system's quality as a range with a reason, and you can say which of your claims about it are capability claims and which are reliability claims. Step 12 makes both harder by asking whether the measurement itself deserves trust.

[⬆ Back to Contents](#contents)

</div>
