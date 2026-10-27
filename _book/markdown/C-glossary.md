# Glossary

Every term the book defines, with the chapter that owns it. A term is defined in exactly one
chapter; every other chapter refers to it rather than redefining it.

| Term | Meaning | Ch |
|---|---|---|
| **Accountability** | Somebody who can be asked to answer for a decision, and who bears a consequence for it. A property of people and organisations, never of a component | 3 |
| **Agent** | A system in which the model decides what to do next, repeatedly, rather than your code deciding the sequence | 4 |
| **Approval point** | A step the loop cannot pass without a person, enforced in your code rather than requested in the instructions | 4 |
| **Check** | Anything that verifies the output before it is used, from a required shape through to a second model's opinion | 2 |
| **Compound system** | A system of several parts with the model as one of them, rather than as the whole product | 2 |
| **Compounding error** | Two things at once across a run: each step's chance of being right multiplies against the others, so a high per-step figure becomes a low whole-run one; and a wrong step's result is carried into the next step as though it were true | 4 |
| **Concept owner** | The single chapter that teaches a given concept. Every other chapter refers to it by number rather than re-teaching it, so the reader never meets three partial explanations of one thing | 7 |
| **Context** | Everything sent to the model on one call: the instructions, any added material, and the request | 2 |
| **Current convention** | How competent engineers work at the moment: true, load-bearing and replaceable. It usually names a technique rather than a reason, and usually has a predecessor you can remember | 6 |
| **Dated detail** | A fact with a date on it — a name, a number, a version. It stops being true when somebody ships something or changes a price | 6 |
| **Error analysis** | The part of evaluation that means reading real outputs, sorting the failures into kinds, and working on the largest kind | 5 |
| **Evaluation** | Building and using something that tells you whether a system works: a set of cases, a way to judge each answer, and a number you can compare over time | 5 |
| **Evidence strength** | How much a claim is supported: announcement, demonstration, one study, practitioner report, settled practice — or a derivation, which stands outside the ladder because you can check it yourself | 6 |
| **Foundation model** | A model trained once on general material, then used for many tasks it was not specifically built for | 1 |
| **Inference** | Running a finished model to get a reply. This is what "using a model" means | 1 |
| **Interview depth** | Knowing something well enough to give the mechanism, the trade-off, and how you would check it, in about a minute of speech. Not exhaustive, and more than a summary | 7 |
| **Irreversible action** | Something a tool does that cannot be undone once it has happened — a refund, a message, a deletion. The reason a tool's reach is decided before it is offered | 3 |
| **Lasting principle** | A reason for doing something, or a shape that does not move, which outlives the technique it was first attached to. It stops being true only if the reason itself is wrong | 6 |
| **Latency** | The delay between sending a request and receiving the reply, felt as a wait before the first word and a pace after it | 1 |
| **Model** | A service that takes text and returns generated text, charged by the amount of text | 1 |
| **People** | The reviewers and approvers who handle the consequential cases and carry responsibility for them | 2 |
| **Practitioner report** | A survey or a set of accounts of what people say they do. It is a practitioner report however it was published, and it supports what people *do* far better than whether it works | 6 |
| **Retrieval** | Searching your own collection for the passages that bear on a request, so they can be put into the context | 2 |
| **Rubber-stamping** | Approval given without real attention, usually because the volume is too high for any. It costs what review costs and delivers none of its value | 3 |
| **Step** | One pass through the loop: the model decides, something runs, the result comes back | 4 |
| **Stopping condition** | The set of rules that end a run — the model finishing, a step limit, or your code refusing | 4 |
| **Tool** | An action the model may ask for. The model proposes it; your code decides whether to run it | 2 |
| **Training** | The one-time process that produced the model's numbers. Not something you do on a request | 1 |
| **Training cut-off** | The point in time after which no text reached the model's training. It knows nothing later, and cannot tell that it does not | 1 |
