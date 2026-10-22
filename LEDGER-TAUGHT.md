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

## Per-chapter record

One row per finished chapter. Fill it when the chapter is closed, before the next one
is begun.

| Ch | Title | What the reader can now do | Anything a later chapter must not claim is new |
|---|---|---|---|
| 1 | What a Model Is, and What You Get From It | Say what a model is as a component: text in, text out, charged by the amount, answered after a noticeable wait. Tell training from inference. Say what the model knows, what it cannot know, and what the caller chooses | **Do not** introduce as new: that a model is a service you call; that training and inference are different; that the model has a knowledge cut-off; that it has not seen the reader's private material; that the model itself cannot look anything up; that cost grows with the amount of text moved; that the wait has two phases. **Do not** write that the book has not yet mentioned latency, cost, or the fact that replies vary — chapter 1 states all three. Verified by grep: the chapter uses **none** of the words *token*, *context*, *retrieval*, *tool*, *agent*. It points forward to chapter 10 for "the unit text is measured in" and to chapter 2 for "machinery around the model" without naming either concept, so chapters 2, 4 and 10 may introduce all five words as genuinely new. **Two exceptions.** *Latency* is used and defined in Key Terms, so chapters 15 and 52 must not present it as new. And the worked exchange labels the three parts of a request — **instructions**, **added material**, **the request** — which are three of chapter 2's five parts. Chapter 2 owns *context* as the term and may teach it, but it must not present those three labels as though the reader has never seen them split out |
| 2 | The Parts Around the Model | Name the five parts of a compound system and say what each is for; look at an AI feature and say what it retrieves, what it may do, what it checks and who approves | **Do not** introduce as new: *context*, *retrieval*, *tool*, *check*, *compound system*, or *people* as a part — all six are defined here and are in Key Terms. **Do not** re-explain that the model proposes and your code decides (ch 23 owns the mechanism, not the principle), that a tool can be asked for and refused, that a person approves the consequential cases, or that cost lives in the context. **Do not** say the book has not yet shown a system diagram. The chapter maps chapter 1's four gaps onto four of the five parts — retrieval, tools, checks, people, in that order — so **chapter 3 must use that same pairing and the same order**, and must not present the mapping as new. Chapter 3 owns *why* each gap is real and *what each part costs in return*; neither is taught here |
