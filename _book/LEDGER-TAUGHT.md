# What each chapter already taught

**Consult this before writing any chapter's opening paragraph, and grep it for "Do not"
before writing the chapter at all.**

It exists because the two worst defects a long book produces are both a chapter not
knowing what came before it. In the French book, one chapter opened by claiming to
introduce endings that an earlier chapter had taught in full; another opened with
"every sentence in this book so far has been positive" when an earlier chapter teaches
negation completely, including the exact example it then built on. **No gate looks at
sequence.** This file is the only defence.

## How to read it

There are two kinds of row and they answer different questions.

| Kind | Answers | How it is used |
|---|---|---|
| **Owns** | *Who teaches this?* | A question you are asking |
| **Do not** | *What must I not say about it?* | A question you did not think to ask |

A "Do not" row is the one that gets skimmed past. In the French book a chapter ran this
check, cited it in its record, and still wrote the exact sentence the row forbade —
because the row was read for its ownership half and the warning half was not noticed.
**Grep for "Do not" and read every hit.**

## Concept ownership

Seeded from `TOC.md`'s *Who owns what*. The owner teaches it; every other chapter refers
to it by chapter number and does not re-teach it.

| Concept | Owns | Also touches it | Do not |
|---|---|---|---|
| Softmax | 8 (as a formula) | 11, 13 | Do not re-derive it in 11 or 13. Chapter 8 has the formula; 11 applies it to scores, 13 to logits |
| Prefill and decode | 15 | 52 | Do not explain the mechanism again in 52. Chapter 15 owns *why*, 52 owns *what you measure and which lever you pull* |
| Quantisation | 15 | 52 | Do not restate the bits-per-parameter arithmetic in 52 |
| The training stages, and what each does | 14 | 39 | Do not define SFT or preference optimisation in 39 — it owns *when you would do it and what it costs you* |
| Sub-agents | 35 | 37 | Do not introduce sub-agents in 37 as if they were new |
| Tool descriptions as untrusted input | 36 | 50, 51 | Do not treat this as a security-chapter idea. Chapter 36 teaches it as tool design; 51 generalises it |
| Prompt-prefix caching | 52 | 53 | Do not teach the mechanism in 53 — it owns the economics |
| Routing and cascades | 52 | 53 | Same split |
| Tracing a request | 33 | 45, 54 | Do not introduce tracing in 54. Chapter 33 owns what a trace holds and what to capture |
| Citation and attribution | 28 | 32, 33 | Do not re-teach how citations are assembled in 32 — it owns whether the citation *supports the claim* |

## Claims in their corrected form

Claims the book makes more than once, written here the way they are true, because the
false version is the one that comes to mind. Grep this list before writing a chapter that
touches the subject.

| Say this | Not this | Why |
|---|---|---|
| A rule gives **the same verdict** every time, for nothing | A rule is **right** every time / gives certainty | Deterministic is not correct. A rule is only as right as whoever wrote it, and a shape check says nothing about whether the answer is true |
| A second answer stands in the same relation to the truth as the first — usually right, sometimes confidently wrong | A model's answer has **no** relation to the truth | Models are useful because their answers do correlate with truth. The point is that a self-check is not independent, not that it is worthless |
| The model itself cannot look anything up | The model cannot look anything up | Products with search do look things up, with machinery around the model |
| The model can only **use** tools you described | The model can only **ask for** tools you described | It will ask for functions that do not exist; your code refuses them |
| Accountability stays with the operator; people are **how it is discharged** on the cases that need defending | Adding human review means **somebody is answerable** | The organisation is answerable whether or not anyone looked. Review buys defensibility, not accountability. This one survived into a summary table and an answer key after the body was fixed |
| A self-check **tends to** fail in the same places | A self-check **fails** in the same places | A different model is not independent, but it does not fail identically either |

## Per-chapter record

One row per finished chapter. Fill it when the chapter is closed, before the next one
is begun.

| Ch | Title | What the reader can now do | Anything a later chapter must not claim is new |
|---|---|---|---|
| 1 | What a Model Is, and What You Get From It | Say what a model is as a component: text in, text out, charged by the amount, answered after a noticeable wait. Tell training from inference. Say what the model knows, what it cannot know, and what the caller chooses | **Do not** introduce as new: that a model is a service you call; that training and inference are different; that the model has a knowledge cut-off; that it has not seen the reader's private material; that the model itself cannot look anything up; that cost grows with the amount of text moved; that the wait has two phases. **Do not** write that the book has not yet mentioned latency, cost, or the fact that replies vary — chapter 1 states all three. Verified by grep: the chapter uses **none** of the words *token*, *context*, *retrieval*, *tool*, *agent*. It points forward to chapter 10 for "the unit text is measured in" and to chapter 2 for "machinery around the model" without naming either concept, so chapters 2, 4 and 10 may introduce all five words as genuinely new. **Two exceptions.** *Latency* is used and defined in Key Terms, so chapters 15 and 52 must not present it as new. And the worked exchange labels the three parts of a request — **instructions**, **added material**, **the request** — which are three of chapter 2's five parts. Chapter 2 owns *context* as the term and may teach it, but it must not present those three labels as though the reader has never seen them split out |
| 2 | The Parts Around the Model | Name the five parts of a compound system and say what each is for; look at an AI feature and say what it retrieves, what it may do, what it checks and who approves | **Do not** introduce as new: *context*, *retrieval*, *tool*, *check*, *compound system*, or *people* as a part — all six are defined here and are in Key Terms. **Do not** re-explain that the model proposes and your code decides (ch 23 owns the mechanism, not the principle), that a tool can be asked for and refused, that a person approves the consequential cases, or that cost lives in the context. **Do not** say the book has not yet shown a system diagram. The chapter maps chapter 1's four gaps onto four of the five parts — retrieval, tools, checks, people, in that order — so **chapter 3 must use that same pairing and the same order**, and must not present the mapping as new. Chapter 3 owns *why* each gap is real and *what each part costs in return*; neither is taught here |
| 3 | Why It Is Assembled This Way | Say, for any part of an AI system, what failure it removes and what failure it introduces; argue why each of the four gaps is real and what closing it costs | **Do not** introduce as new: the four gaps, the gap-to-part pairing, or *compound system*. **Do not** write that accountability is created by adding a reviewer — the chapter's central correction is that it never moves. **Do not** say a rule is *right* or *certain*; it gives the same verdict every time. **Do not** present *accountability*, *irreversible action* or *rubber-stamping* as new terms; all three are bolded and in Key Terms here. The chapter establishes that **every part removes one failure and introduces another**, and that the simplest arrangement that works is usually right — chapter 4 may lean on both, and chapter 5 owns how much of the real work telling failures apart turns out to be |
| 4 | The Agent Loop, and How Much Freedom It Actually Gets | Say what an agent is and what it is not; explain why a run of many steps is a worse bet than a single call; name the three ways a loop ends | **Do not** introduce as new: *agent*, *step*, *stopping condition*, *approval point* or *compounding error* — all five are bolded and in Key Terms here. **Do not** say an agent is a new kind of model or a new component; the chapter's headline claim is that no new component is added and the loop is new *code*. **Do not** re-teach that an approval point belongs in code rather than in the instructions. **Chapter 34 may refer to compounding error by name** and should; it owns the named patterns and when an agent is warranted, neither of which is taught here. **Chapter 38 owns pass@k and pass^k and the 0.95-over-20 figure** — this chapter deliberately uses 0.9 and 0.99 so the boundary stays visible, and ch 38 should not present the compounding arithmetic as new |
| 5 | Where the Work Actually Goes | Name the four activities an AI application is actually built out of, say which one decides the other three, and say why nothing in a wrong answer tells you which part produced it | **Do not** introduce as new: **evaluation** or **error analysis** — both are bolded and in Key Terms here. **Chapter 30 owns the method** of error analysis and may teach all of it, but must not present the *name* as new; chapters 31–33 own the rest of evaluation, **chapter 32** owns measuring retrieval and generation separately, **chapter 33** owns the per-request record, and **chapter 53** owns cost as a method. **Do not** restate the share claim more strongly than *a substantial part*, and never as a measurement: the source is a practitioner report, and the chapter says so on purpose. **Do not** present the four activities as chapter 2's five parts — the chapter states outright that the two lists differ and that the activities cut across the parts, and that writing the instructions is *part of* the first activity rather than one of the four. **Do not** claim the model cannot ask for an undescribed tool; it can, and your code has nothing to run (chapter 2's corrected form). The five causes of a wrong answer map one-for-one onto chapter 2's five diagnostic questions, in order, and are *common* rather than exhaustive — a later chapter may add a tool returning a wrong result without contradicting this. **Chapter 18 may teach prompt writing in full**; this chapter only says it is the part you finish first |
| 6 | What Changes Fast, and What Changes Slowly | Sort any claim into a lasting principle, a current convention or a dated detail by asking what would have to change for it to stop being true; name the evidence behind a claim and say its strength out loud; read a release announcement for the four things in it | **Do not** introduce as new: **lasting principle**, **current convention**, **dated detail**, **practitioner report** or **evidence strength** - all five are bolded and in Key Terms here, and **chapter 7** uses the three-way sort to explain the book's own shape. **A lasting principle here is a reason OR a shape that does not move**, which is what gives chapters 8-17's mechanism a place in the taxonomy; do not narrow it back to reasons only. The chapter puts **a derivation outside the evidence ladder**, not on top of it, because the ladder measures how far somebody else's reporting can be trusted - keep it off the ladder. **Do not** write that a vendor's material is worthless or an announcement 'whatever it contains': the rule is that it is an announcement *until you can see what it was measured on*, and a score on a named public test anybody can re-run is more than one. **Do not** write that adoption tells you nothing about whether something works; it becomes evidence once a practice has survived years and its failure modes are written down. The chapter uses practices owned elsewhere purely as specimens and teaches none of them: **chapters 26 and 28** own search re-ordering (and it is a *current convention* here, not settled practice), **chapter 20** owns telling a real difference from noise, **chapters 30-33** own building a measurement, **chapter 4** owns the ten-step arithmetic the chapter calls a derivation. Its lab's announcement, model, test and prices are all **invented on purpose** so nothing in the chapter can date - do not replace them with real ones |
| 7 | A Map of This Book | Say what each of the four parts answers, which half of Part I they have finished, what the labs build and what the book leaves out | **Do not** introduce as new: **interview depth** or **concept owner** - both are bolded and in Key Terms here. **This is where the book first states its purpose**: chapters 1-6 never mention an interview, and chapter 7 says plainly that the book is for the situation where you explain this material out loud. Later chapters may assume the reader knows that. **The four threads are Security (51), Speed (52), Cost (53) and Failure (54)** - name all four whenever Part IV is described, in the body AND in any summary. **Do not restate which chapters an interview reaches first as a measured fact**: the chapter calls its weight ranking a judgement and says nobody has surveyed it, which is chapter 6's discipline applied to itself; the one concrete claim it makes is that chapters 18-29 are the half of **Part II** a conversation reaches first - not half of the book. The lab's eight questions and their key live inside the chapter and need nothing external, per BOOK-GUIDE §9. **Part I is now complete**, so a later chapter may rely on anything in chapters 1-7 and on nothing in 8-17 until it is written |
