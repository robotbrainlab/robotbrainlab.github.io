# Interview Bank

A hundred questions of the kind this book prepares you to answer, each keyed to the chapter
that holds the answer.

**The questions come first, and they came before the chapters — from question 14 onward.**
They were written from the contents, so they are not a summary of what got written: they are
the standard it has to meet. A chapter is not finished until its questions can be answered
from it, and if one cannot, the chapter is short of something rather than the question being
unfair.

**Questions 1 to 13 are the exception, and they are weaker for it.** They cover chapters 1 to
7, which were finished on 23 October; this bank was written on 27 October, by somebody who had
read them. Questions 3, 7, 9, 11 and 13 land close to a review question their chapter already
asks. **A question reverse-engineered from an answer cannot test whether the answer is
there.** Part I was checked against these thirteen and came through — twelve answerable, one
needing a second chapter in its key — but that is not a clean pass and should not be read as
one. From chapter 8 on, the bank genuinely precedes the chapter, and the test means what it
says.

**The answers arrive as the chapters do.** Each will be 150 to 180 words, which is about what
sixty seconds of speech holds: the mechanism, the trade-off, and how you would check it. An
answer written before its chapter would be written from memory, which is the one way this book
is not allowed to be written. Where the *Ch* column points at a chapter that does not exist
yet, the question is still the right question.

**Eight chapters carry no question, on purpose.** Chapter 7 is this book's own map, and
chapter 57 is advice about what to leave out — neither is something anybody will ask you.
Labs 40, 42, 43, 44, 46 and 48 are tested through the chapters they rest on: lab 44 is
covered by the retrieval questions on chapter 26, lab 46 by those on chapters 30 and 31, and
so on. Every other chapter in the book has at least one question, and the six labs that do
appear here are the ones you would be asked to describe rather than explain.

## Part I · Mental Model

| # | Question | Ch |
|---|---|---|
| 1 | What is a language model, described as a component in a system rather than as a product? | 1 |
| 2 | What can a model not know, and why does a better model not fix it? | 1 |
| 3 | What do you choose when you use a model, and what do you not choose? | 1 |
| 4 | Name the parts a contemporary AI application combines, say what each is for, and say what each one costs you. | 2–3 |
| 5 | What is in the context of a single request, and what decides what goes in it? | 2 |
| 6 | Why does retrieval exist? Name the failure it removes. | 3 |
| 7 | Every part you add removes one failure and introduces another. Give two examples. | 3 |
| 8 | What is an agent, and what is it not? | 4 |
| 9 | Each step of your agent is right nine times in ten and the task needs ten steps. What is your success rate, and what does that tell you about a demonstration that worked? | 4 |
| 10 | Where does the time actually go on a project like this? | 5 |
| 11 | A user reports a wrong answer. Name the things that could have caused it, and say what you would need in order to tell them apart. | 5 |
| 12 | Of everything you have learned about this field, what would you bother memorising and what would you look up? Why that split? | 6 |
| 13 | A provider announces a model thirty per cent better at coding. What do you want to know before you repeat that? | 6 |

## Part I · Inside the Model

| # | Question | Ch |
|---|---|---|
| 14 | What does a dot product measure, and why does that make it the basis of similarity? | 8 |
| 15 | What does one forward pass of a model actually produce? | 9 |
| 16 | What is in the embedding table, and what does a single dimension of it mean? | 9 |
| 17 | Why is text turned into tokens rather than words or characters? | 10 |
| 18 | Why does code cost more tokens than ordinary English? | 10 |
| 19 | Why does a model miscount the letters in a word? | 10 |
| 20 | Walk me through attention on a short sentence. | 11 |
| 21 | Why is the attention score divided by the square root of the key dimension? | 11 |
| 22 | Why does attention cost grow with the square of the input length, and what follows from that in practice? | 11 |
| 23 | What do several attention heads give you that one does not? | 11 |
| 24 | What is the residual stream, and what does a layer do to it? | 12 |
| 25 | Why does "where is that fact stored in the model" have no clean answer? | 12 |
| 26 | What does temperature do to the numbers? | 13 |
| 27 | Why is temperature zero still not a guarantee of the same output twice? | 13 |
| 28 | Name the training stages and say what each one changes. | 14 |
| 29 | Why is the first token slow and every token after it fast? | 15 |
| 30 | Your prompt doubles in length. Why does the work more than double? | 15 |
| 31 | What is the key–value cache, and how big is it? | 15 |
| 32 | Why can a very large model be cheap per token? | 15 |
| 33 | Why is hallucination the default behaviour rather than a defect? | 16 |
| 34 | Why does asking a model to work step by step improve accuracy, and why is the visible reasoning not a reliable account of how it answered? | 16 |
| 35 | An interviewer asks why depth helps. You have not studied that. What do you say? | 17 |

## Part II · Use

| # | Question | Ch |
|---|---|---|
| 36 | What are the separable parts of a prompt, and why does separating them matter? | 18 |
| 37 | Your conversation history will not fit in the context. What do you drop, and how do you decide? | 18 |
| 38 | Why does current practice weight what the model receives over how the instruction is worded? | 18 |
| 39 | Your script works on ten documents and dies on a 429 at document four thousand of ten thousand. What do you do? | 19 |
| 40 | Why can you not stream a response that you have to validate? | 19 |
| 41 | What is idempotency, and where does it matter in a pipeline like this? | 19 |
| 42 | A multi-step pipeline fails half way. How do you resume it? | 19 |
| 43 | How do you decide whether prompt B is better than prompt A? | 20 |
| 44 | What is a bootstrap interval, and why use one here rather than a named distribution? | 20 |
| 45 | How many cases and how many trials are enough? | 20 |
| 46 | Why must a program never trust prose? | 21 |
| 47 | You are asking for JSON. How do you measure how often you do not get it, and what do you do with the failures? | 21 |
| 48 | How is a format constraint actually enforced while the model generates? | 22 |
| 49 | When can a strict output format make the answer worse? | 22 |
| 50 | Walk me through a tool call. Who decides what runs? | 23 |
| 51 | Where does validation of a tool call belong, and why not in the instructions? | 23 |
| 52 | How would you choose an embedding model for your own data? | 24 |
| 53 | Why is a public benchmark score a starting point rather than a verdict? | 24 |
| 54 | Give me a query that meaning-based search gets wrong, and say why. | 25 |
| 55 | Why is similarity not the same thing as relevance? | 25 |
| 56 | What is BM25 doing, roughly? | 26 |
| 57 | What is the difference between a bi-encoder and a cross-encoder, and where does each belong? | 26 |
| 58 | What is nDCG, and why is there a logarithm in it? | 26 |
| 59 | You have two rankings of the same documents. How do you combine them? | 26 |
| 60 | Why is document parsing the upstream bottleneck for everything downstream? | 27 |
| 61 | What does a chunk boundary decide? | 27 |
| 62 | Long context or retrieval? | 28 |
| 63 | What must a citation actually support, and how would you check that it does? | 28 |
| 64 | What does an approximate index buy you, and what does it cost? | 29 |
| 65 | Each user may see only their own documents. How does that change your retrieval? | 29 |
| 66 | You have forty bad outputs and no metrics. What do you do first? | 30 |
| 67 | Why let the failure modes choose the metrics rather than measuring what is conventional? | 30 |
| 68 | When do you use a model as a judge rather than code? | 31 |
| 69 | How do you establish that a judge can be trusted? | 31 |
| 70 | What is position bias, and what does it do to your numbers? | 31 |
| 71 | Why measure retrieval and generation separately? | 32 |
| 72 | What is a claim-level check on a grounded answer? | 32 |
| 73 | Where do your labelled evaluation cases come from? | 32 |
| 74 | What goes into a regression set, and when does it run? | 33 |
| 75 | What is criteria drift, and how do you notice it? | 33 |
| 76 | What do you record in a trace, and what do you deliberately not record? | 33 |
| 77 | When is an agent warranted instead of a path your code controls? | 34 |
| 78 | Name the fixed-path patterns and say what each is for. | 34 |
| 79 | What is compaction, and how do you prove nothing important was dropped? | 35 |
| 80 | Why treat an agent's own memory as untrusted input? | 35 |
| 81 | What makes a tool good for a model to use rather than good for a programmer to call? | 36 |
| 82 | What is the Model Context Protocol, and what problem does it solve? | 36 |
| 83 | When do several agents help, and how do multi-agent systems fail? | 37 |
| 84 | What is pass@k, how does it differ from pass^k, and which one should worry you? | 38 |
| 85 | Prompt, retrieve or tune? How do you choose? | 39 |
| 86 | What does owning a fine-tuned model cost you that prompting does not? | 39 |

## Part III · Apply

| # | Question | Ch |
|---|---|---|
| 87 | Walk me through something you built end to end, and tell me the numbers you got. | 45 |
| 88 | How did you compare two prompts in a way you could defend? | 41 |
| 89 | You measured a fixed path against an agent on the same task. What did you find? | 47 |
| 90 | How did you reduce cost per request, and what did it cost you in quality? | 49 |
| 91 | You attacked your own system. What did you try, and what happened? | 50 |

## Part IV · What Next

| # | Question | Ch |
|---|---|---|
| 92 | Why can a model not reliably tell an instruction from data? | 51 |
| 93 | A web page your agent reads tells it to send your customer list somewhere. What happens, and what would have stopped it? | 51 |
| 94 | What is the rule about combining untrusted input, sensitive access and external action? | 51 |
| 95 | Where does model output reach a shell, a query or a page, and what do you do about it? | 51 |
| 96 | Your system is correct and nobody will wait for it. What do you measure, and which lever do you pull? | 52 |
| 97 | The bill arrived and you cannot account for it. How do you find out where it went? | 53 |
| 98 | It worked last week and nothing in your code changed. What do you investigate, and what should have been in place? | 54 |
| 99 | What do you not know yet, and how would you go about learning it? | 56 |
| 100 | Design a support assistant that answers from a company's own documents. Talk me through it. | 55 |
