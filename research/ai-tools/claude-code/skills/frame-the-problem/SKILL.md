---
name: frame-the-problem
description: >-
  Run structured product discovery before building anything. Use this skill
  whenever the user wants to build something new but hasn't pinned down the
  problem — "I want to build X", "should I build this?", a vague feature idea, or
  any moment where jumping straight to code would risk building the wrong thing.
  It separates the real problem from the proposed solution, identifies the user
  and the value, names the riskiest assumption, and proposes the smallest test to
  validate before committing engineering effort.
---

# Frame the Problem

The most expensive mistake in software is building the wrong thing *well*. Before code or
planning, make sure the problem is real and worth solving.

## Workflow

1. **Resist the solution.** The user almost always arrives with a solution ("build a dashboard").
   Treat it as a hypothesis, not a spec — your job is the *problem* underneath it.
2. **Clarify the essentials** (ask only what you can't infer):
   - *Who* is this for, and what are they actually trying to get done (the job)?
   - *What* real problem does it solve — stated as a problem, not a feature?
   - How *often* and how *painful* is it? Would they change behavior / pay to fix it?
   - What *outcome* would mean success (observable, not "make it better")?
3. **Dig past the stated solution** with the five whys until you reach the underlying need.
4. **Name the four risks and the riskiest assumption:** value (will anyone want it?),
   usability (can they use it?), feasibility (can we build it?), viability (does it work for the
   business?). Identify the single assumption that, if false, kills the idea.
5. **Propose the smallest test** to retire that assumption cheaply (a conversation, a fake-door,
   a prototype) — before building.

## Output

```
## Discovery — <idea>
**Real problem:** <the need beneath the request>
**User & job:** <who, what progress they want>
**Success looks like:** <observable outcome>
**Riskiest assumption:** <the one that could kill it>
**Cheapest test:** <how to validate before building>
**Recommendation:** build / refine / stop — <one line why>
```

Be willing to recommend *not* building it. That's the whole point of the skill.
