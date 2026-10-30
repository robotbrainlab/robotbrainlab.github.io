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

**The answers are at the end, and they are written to be said.** Each is about what sixty seconds
of speech holds: the mechanism, the trade-off, and how you would check it. Each was written from
its own chapter, read immediately before — an answer written from memory is the one way this book
is not allowed to be written — and each was written after every chapter was finished, which is why
they are here rather than beside the questions.

**There are no chapter numbers inside an answer**, because an answer is a thing you say and nobody
says a chapter number out loud. The *Ch* column is where to go when an answer raises something you
cannot yet defend.

**Eight chapters carry no question, on purpose.** Chapter 7 is this book's own map, and
chapter 57 is advice about what to leave out — neither is something anybody will ask you.
Labs 40, 42, 43, 44, 46 and 48 are tested through the chapters they rest on: lab 44 is
covered by the retrieval questions on chapter 26, lab 46 by those on chapters 30 and 31, and
so on. Every other chapter in the book has at least one question, and the six labs that do
appear here are the ones you would be asked to describe rather than explain.

## Part I · Mental Model

| # | Question | Ch |
|---|---|---|
| 1 | What is a language model (an LLM), described as a component in a system rather than as a product? | 1 |
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
| 20 | Walk me through attention (self-attention) on a short sentence. | 11 |
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
| 31 | What is the key–value cache (the KV cache), and how big is it? | 15 |
| 32 | Why can a very large model be cheap per token? | 15 |
| 33 | Why is hallucination the default behaviour rather than a defect? | 16 |
| 34 | Why does asking a model to work step by step (chain-of-thought) improve accuracy, and why is the visible reasoning not a reliable account of how it answered? | 16 |
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
| 50 | Walk me through a tool call (function calling). Who decides what runs? | 23 |
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
| 68 | When do you use a model as a judge (LLM-as-a-judge) rather than code? | 31 |
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

## The Answers

### Answers 1–13 · Mental Model

**1.** A service you call over a network: your program sends text, it returns generated text, you
are charged for the amount of text moving in both directions, and you wait — a noticeable pause
before the first word, then a pace as the rest arrives. Its numbers were fixed by somebody else
before you ever called it, and nothing you send changes them, so it carries nothing from one call
to the next; products that seem to remember you are storing your earlier messages and sending them
again. Four properties, and each one creates a gap that something else has to fill: it cannot see
your data, it cannot act in the world, it cannot reliably check itself, and it is not accountable
for anything. That is why real systems are several parts with a model as one of them. The way to
see this in any product is to ask what text must have been sent on your behalf for the answer to
come out as it did.

**2.** Three things, and only one of them is about capability. It knows nothing after its training
cut-off, because no later text reached it. It knows nothing of yours — your data is private, it
changes, and it differs per reader, so it was never in the training material and could not have
been. And it cannot tell you that it is out of its depth, so instead of refusing it produces
something plausible. A better model moves the cut-off forward and widens what it knows in general,
which makes the first gap smaller and later. It does nothing at all to the second, because that is
not a weakness to be improved — the material is not the provider's to train on. And it does not fix
the third either; the failure is that a missing-information signal does not exist, not that the
model is not clever enough to send one. The way to see all three in a minute is to ask about last
week and then about your own account.

**3.** You choose four things: which model you call, the text you send it, the handful of settings
that change how the reply is produced, and what your code does with the reply once it arrives. Of
those, the text you send is the one that matters most and is where almost all of the engineering
goes. What you do not choose is what the model knows and how it behaves — those were decided by
somebody else, before you arrived, and they are the same tomorrow as today unless the provider
replaces the model underneath you. So when it does something you do not want, you have exactly
three moves: change what you send, change which model you call, or check the reply and handle the
bad cases in code. There is no fourth. Reaching for a fourth — asking the instructions more firmly
to be reliable — is the commonest wasted afternoon in this work.

**4.** Five, and the useful way to hold them is one vehicle, then four gaps with a part and a
price against each. The context is
everything you send on a call — instructions, added material, the request — assembled fresh every
time, limited in size, and responsible for most of the cost. Retrieval searches your own collection
and puts what it found into the context; it closes the model's ignorance of your data, and you pay
with a second system that can be wrong on its own. Tools are actions the model may ask for, where
it proposes and your code decides and runs; they close the fact that it only produces text, and you
pay with every surface a tool can reach, including actions that cannot be undone. Checks verify
output before anybody uses it, and you pay for what they were not built to catch and for the good
answers a strict one rejects. People handle the consequential cases and carry the result; you pay in
delay, cost, and the risk of approval without attention.

**5.** Three things: the instructions, any added material, and the request itself. It is assembled
fresh on every single call — nothing persists in the model between calls, so anything the model is
to take into account has to be in the text you send this time. It has a ceiling on how much it will
accept, and it is where most of your bill comes from, because cost scales with the amount of text
moved rather than with the difficulty of the question. What decides what goes in it is your code,
which is the whole point: the model does not fetch anything, so every passage, every earlier
message and every instruction is there because something you wrote put it there. That makes the
size of the context an engineering decision rather than a detail, and it is the reason the design
rule is worth saying plainly — what is not in the context does not exist.

**6.** Because the model does not know your data, and that gap is permanent rather than temporary.
Your material is private, so it was not in the training text; it changes, so a model trained on a
snapshot of it would be stale; and it differs per reader, so there is no single version of it to
have learned. No better model closes any of that. The specific failure retrieval removes is the
confident wrong answer about something the model could not possibly know — not a refusal, which
would at least be honest, but a plausible answer produced because nothing in the machinery signals
missing information. Retrieval finds the passages that bear on the request and puts them in the
context, so the model is answering from material rather than from recall. What you pay for it is a
second system with failures of its own: it can return nothing useful, or the wrong passage
confidently, and then the answer is wrong for a new reason.

**7.** Retrieval is the first. It removes the model's ignorance of your data, and it introduces a
search system that can fail on its own terms — finding nothing relevant, or finding something
plausible and wrong — so a wrong answer now has two possible homes instead of one, and telling them
apart becomes work you have to do deliberately. Tools are the second. They remove the fact that the
model only produces text, and they introduce every surface the tool can reach: a tool that can
refund, send or delete can do those things wrongly, and some of them cannot be undone, which is why
a tool's reach is decided before it is offered rather than after something goes wrong. Checks are a
third if you want one: they catch failures, and they introduce both the failures they were not built
for and the good answers a strict check rejects. The pattern is the lesson — which is why the
simplest arrangement that works is usually the right one.

**8.** It is the same arrangement as a system where your code controls the sequence, with exactly one
change: the model decides what happens next, repeatedly, instead of your code deciding. No new
component appears. What moves is control flow, and what you write is a loop plus the rules that end
it. Three consequences follow immediately. You cannot read the program and know the sequence it will
run, because the sequence is decided at run time. Two runs of the same input can differ. And a
mistake made early is not corrected later — it is built on, because the record of what happened is
what the model reads to decide the next step. What an agent is *not* is a smarter model or an extra
part; the model is the same one. So the question to ask of any agent is never whether the model is
good enough, but how much freedom it has been given and what ends the loop.

**9.** About a third. Nine in ten per step, ten steps, is nine tenths to the power ten, which is
0.349 — so roughly two runs in three fail somewhere. That arithmetic is the governing fact about
loops, and it is worth having at two points: at seven steps the same reliability is already worse
than a coin toss, and raising per-step reliability to ninety-nine in a hundred takes the same ten
steps to 0.904, which is the difference between a demonstration and a system. What it tells you
about a demonstration that worked is the useful half. A system succeeding a third of the time shows
you a good run about every third attempt, so somebody running it three or four times before
recording a video is not being dishonest and has told you nothing about reliability. The test is
never whether it can work; it is how often it does, measured over runs you did not choose.

**10.** Not in the instructions, which are the visible part and the part you finish first. The work
is four activities, plus one that cuts across them. Choosing what reaches the model. Deciding what
it may do. Finding out whether it works. Controlling what it costs. And then, across all four,
telling which part failed when an answer is wrong. Finding out whether it works is the one that
takes longest, and practitioners report it taking a substantial part of building an application —
which is an account of what people do rather than a measurement of what it should be, and worth
saying at that strength. Two reasons it takes long: it decides most of the other questions, so
getting it wrong is expensive everywhere; and its failures do not announce themselves the way a
crash does, so the ones nobody anticipated only reach you if somebody reads output that nobody
complained about. The practical consequence is an estimate — put the measuring in the plan.

**11.** One symptom, five common causes. Retrieval may have found nothing useful. The context may
have been assembled badly, or been too full. The model may have ignored material that was right
there in front of it. A check may have passed something it should have caught. Or the case needed a
person and never reached one. The difficulty is that nothing in the output tells you which: the
answer looks the same in every one of those five worlds, and the natural response — change the
instructions and try it again — is the move that tells you least about which one you are in. So to
tell them apart you need two things, and both are work you do before the failure rather than after.
A record of what actually happened on each request, so a failure can be traced rather than argued
about: what was retrieved, what was sent, what came back. And retrieval measured separately from
generation, so you can say which half of the system failed.

**12.** Memorise the reasons, the shapes, the arithmetic and the failure modes. Look up everything
with a date on it. The split follows from a question you can ask of any claim: what would have to
change in the world for this to stop being true? If the answer is that a company would have to ship
something or change a price, it is a dated detail and belongs in documentation you read on the day
you depend on it. If the answer is that the field would have to find a better way, it is a current
convention — true, load-bearing and replaceable, worth knowing and not worth attaching yourself to.
And if the answer is that the reason itself would have to be wrong, it is a lasting principle and
that is what is worth carrying. The hard case is a convention that has been true long enough to look
like a principle, and the tell is that it names a technique rather than a reason, and has a
predecessor you can remember.

**13.** Four things, and none of them is the number. What is the precise claim — thirty per cent
better at what, measured how, because "better at coding" is not a claim anybody can check. What was
it measured on, and is that anything like my work. What was it compared with: the previous version
of the same model, a competitor, or a weaker setting of itself. And what changed about the price and
the limits at the same time, because a model that is better and three times dearer is a different
proposition. Until I can see what it was measured on, a provider's own material is an announcement,
which is the weakest kind of evidence there is — below a demonstration, a single study, a report of
what practitioners do, and settled practice. The thing I would actually do before repeating it is
run my own cases against it, because a result on my own traffic is the only measurement that is
about my case, and it needs nobody's reporting.

### Answers 14–35 · Inside the Model

**14.** A dot product multiplies two vectors slot by slot and adds the results, so it is large
when both put their weight in the same slots. That is what makes it read as agreement: the two
lists are big in the same places. The catch is that it also grows when either vector is simply
longer, so a long vector scores well against everything. That is why similarity is normally
cosine similarity — the dot product divided by both lengths — which divides magnitude out and
keeps direction alone, landing between −1 and 1. The trade-off is exactly what the division
throws away: cosine cannot tell a strong signal from a weak one pointing the same way, and
sometimes magnitude was the thing you wanted. Checking it is arithmetic you can do by hand. Score
two vectors, then multiply one of them by ten — the dot product goes up tenfold and the cosine
does not move. And a cosine outside −1 to 1 is a bug in your code rather than a surprising
result.

**15.** One probability for every entry in the vocabulary, adding to 1 — the next-token
distribution, and nothing else. The last position's vector is multiplied by a matrix with one
column per vocabulary entry to give one score per entry, and softmax turns those scores into the
distribution. It is not a word and it certainly is not a sentence: picking from that distribution
happens outside the model, which is where temperature and the cuts live. So a hundred-token reply
is a hundred passes, each over an input one token longer, which is what autoregressive means. Two
things follow that matter in practice. The cost of output is a forward pass per token, which is
why the dear half is dear. And the only thing a single call gives you is one draw from one
distribution, so a good output is not evidence of anything. You can see it directly: ask a
provider for the log-probabilities and you get a ranked list per position, not a sentence.

**16.** A matrix with one row per vocabulary entry, each row as wide as the model is — looking a
token's index up in it is how that token enters the model at all. Its size is vocabulary times
width, so 128,000 by 4,096 is 524,288,000 numbers before a single layer. A single dimension means
nothing nameable. Those coordinates were chosen by nobody: they are whatever made next-token
prediction work during training, so there is no slot for tense or for plurality, and asking what
dimension 412 holds is a question with no answer. What carries meaning is the arrangement —
directions and distances between rows — not any one slot. The consequence is that you cannot read
an embedding, only compare it, which is why every use of one is a similarity and never an
inspection. Check it both ways: nearest neighbours by cosine give you related words, and sorting
the vocabulary by one dimension gives you no coherent category at all.

**17.** Because both ends are worse. Words make the vocabulary hundreds of thousands of entries
before you count names, typos and product codes, which makes the embedding table and the output
step enormous while still leaving text that cannot be represented at all. Characters fix that hole
and create another: an English word runs about five characters, so the sequence gets several times
longer, and length is what you pay for twice, since each output token is a forward pass and the
attention grid grows with the square of the input. Subwords sit between them — a common word earns
one entry, a rare one is spelled out of several — and the base vocabulary is the 256 bytes, which
is why nothing is ever unrepresentable and why the worst case is one token per byte. The trade-off
is that which pieces earned an entry is a matter of frequency in somebody else's corpus, not
meaning or length. Check it by tokenising the same text with two models' tokenisers: the counts
differ.

**18.** The merges that built the vocabulary were bought with a corpus that is mostly prose, so
the entries went mostly to prose, and code then pays in three ways at once. Its punctuation is
dense, and each mark that did not earn a merge is a token on its own. Its indentation is runs of
spaces, which are often several tokens of nothing. And its identifiers are made-up compounds —
get_user_by_id, maxRetryCount — that no corpus saw often enough to merge, so each is cut into
several pieces. The honest way to put it is that you are not charged for difficulty but
for how well your text matches the corpus somebody else compressed — the same reason a language
written in another script costs more. How much more is a dated and
vendor-specific detail that moves with every new vocabulary, so measure rather than quote. Run a
file of code and a page of prose through the tokeniser: the prose lands near four characters a
token, and the same quantity of code costs more tokens than that.

**19.** Because a token's spelling is not in the input. The word arrives as one index or a few, the
index is looked up in the embedding table, and from there every step works on the vector and never
on the token. Nothing in that input says this piece is ten characters of which three are the same,
because an index is not spelled. So the model is not counting badly — it is answering a question
about something it was never given, out of whatever it absorbed about the word's spelling during
training, which is recall rather than counting. Two things follow. It is not a bug, and a better
model does not necessarily fix it, because the input representation has not changed. And the fix
is not to ask more firmly: a check that code can do belongs in code, so have the model write the
program that counts or count in your own. You can see the split in one sitting — ask for the count
and ask for the code, and the code is right.

**20.** Take five positions, one per token. Three fitted matrices turn each position's vector into
three others: a query, what that position is looking for; a key, what it offers; and a value,
what it hands over when attended to. Every query is dotted
with every key, giving a square grid of scores, and that dot product is the whole definition of
relevance here. The scores are divided by the square root of the key width, every later position
is set to minus infinity so a position can see only itself and what precedes it, and softmax turns
each row into weights that are positive and add to 1. The output for a position is the weighted sum
of the value vectors. In a worked case the last position put about seven tenths of its weight on
one earlier token, so it went in standing for a pronoun and came out standing largely for the noun.
Nothing told it to. Check a row by hand: the weights must sum to 1 and a masked position must be
exactly zero.

**21.** Because a dot product grows with the width it is taken over — more slots, more products
added — and softmax turns each gap between scores into a multiple between shares. Put those
together and unscaled scores at a realistic width saturate the softmax: nearly all the weight
lands on one position and attention stops blending, which is the opposite of what it is for.
Dividing holds the scores in a range where softmax still spreads them. The reason it is the square
root of the width rather than the width itself is that the slot-by-slot products partly cancel,
some positive and some negative, so the total grows like the square root; dividing by the width
would over-correct and flatten the weights towards uniform, which is just as useless in the other
direction. You can check the scaling empirically. Generate random query and key vectors at two
widths, score them, and look at the spread of the results — it tracks the square root of the
width, not the width.

**22.** The grid has one entry per pair of positions, so it has the square of the length in it, and
each entry is a dot product over the key width. The reason every pair has to be computed is the
circular one: which positions matter depends on the content, and the scores are what you are
computing to find that out, so there is nothing to prune on until you already have the number you
were trying to avoid. Three things follow. Long inputs are superlinearly expensive. There is a
length past which this stops being affordable, which is much of why there is a limit on what you
may send at all. And recomputing the grid on every output token would be ruinous, which is what
the stored keys and values exist to prevent. One caveat worth saying out loud: squared is true of
attention and not of a whole layer, and at a thousand tokens attention is about a twentieth of the
arithmetic. Check it by timing the first token at two prompt lengths.

**23.** A head is one complete set of query, key and value matrices, one grid and one set of
weights — so it has exactly one opinion about what is relevant to each position. Several heads run
in parallel over slices of the width, each with its own matrices, and a final matrix mixes their
outputs. The point is that the opinions differ. In a worked pair of heads differing only in the key
matrix, one put most of its weight on an earlier noun and the other on the position itself;
neither is right, they are two questions asked of the same tokens. The cost is not what you would
guess: the total arithmetic is unchanged, because each head works over a slice only as wide as the
width divided by their number. That is the real trade-off — sixteen heads
at a width of 4,096 leaves each one 256 dimensions to work in. Check it by pulling the weights per
head on one input: two heads that agree everywhere are a layer paying for one.

**24.** The stream is the running vector that passes up through the stack, and what a layer does to
it is add. A layer does not replace the vector it is given; it computes a change and adds it, which
is what a residual connection means and what lets a layer contribute nothing and pass its input
through untouched. Each layer writes twice: an attention block, which is the only part of a model
that moves information between positions, and a feed-forward block, which works on each position
alone and holds the larger share of the parameters — about 57 per cent of a layer at a common
shape. The stream is normalised before each block reads it, which keeps the numbers in range as
layer after layer adds into them. The consequence to carry is that by the end the stream is a sum
of every contribution with nothing marking which is which. Check the shape: same width in as out
at every layer, which is the property that makes stacking possible.

**25.** Three reasons, and they compound. Contributions are added into the same numbers — every
block adds into one running vector — and a sum cannot be taken apart afterwards, so nothing marks
which contribution came from where. A parameter is used again on input after input rather than
belonging to anything, so there is no sense in which it is that fact's parameter. And what the
model holds is numbers that make likely continuations likely, not facts at addresses, so there is
no row to go and read. The engineering consequence is the useful half of the answer: you cannot
delete a fact, and changing one is a research subject rather than an operation, so anything that
has to be correctable belongs outside the model in something you can query and edit. Check it by
asking what you would actually do to remove one claim, and watching the answer have nowhere to
point — with about nine parameters in ten sitting in the layers, and none of them labelled.

**26.** It divides the logits before softmax. Below 1 that sharpens the distribution, because
dividing by a small number spreads the scores apart and softmax turns a wider gap into a bigger
share for the leader; above 1 it flattens them the same way in reverse. What it never does is
change the order, because dividing every score by the same positive number cannot change which is
largest. Two consequences are worth having ready. It has no effect whatsoever on greedy decoding,
which takes the largest logit either way, so setting a low temperature and setting zero are not
the same claim about determinism. And the order of operations is temperature first, then the cut —
whether that is a fixed count of tokens or the smallest set reaching a probability — then the draw,
which means temperature changes which tokens survive the cut. Check it by pulling the
log-probabilities at two temperatures on one prompt: the ranking is identical and the spread is
not.

**27.** Because zero means greedy — take the largest score — and which score is largest can move.
Floating-point addition is not associative, so changing the order of a sum changes its last digits;
batching changes that order, and who else is calling at the same moment decides your batch. In a
model that routes each token through a few of many blocks, the routing can depend on your
neighbours. And what the provider runs underneath you can change without the name you call
changing. Some of those move only the last digits of a score, which matters just where two tokens
are nearly tied — and there the reply can diverge from that token onward; where nothing is close,
the greedy path is identical. The engineering consequence is that determinism is not a property you
can claim, so a regression suite demanding identical strings will fail on its own schedule. Check
it by sending one call a hundred times and counting distinct outputs.

**28.** Three, and they all run the same loop: forward pass, compute the loss, move every parameter
a little in the direction that reduces it. Pretraining runs it on an enormous quantity of general
text, which is where essentially all of a model's knowledge comes from and nearly all of the
computation goes; the objective is the average of minus the log of the probability it gave to the
token that actually came next, so the text supplies its own answers. Supervised fine-tuning runs
the same loop with the same objective on curated request and response pairs, which turns a model
that continues text into one that answers. Preference optimisation trains on pairs of replies with
a preference between them and raises the preferred one relative to the rejected; it changes which
existing behaviours come out, and nothing in its objective rewards adding knowledge. What follows:
no stage gives the model a way to look anything up, and nothing in it tests whether anything is
true. Check it by prompting a base model — it continues rather than answers.

**29.** They are two different computations. The first is one pass over the whole prompt with every
position computed together, and it is limited by arithmetic, so it is where a long prompt is paid
for. Every token after it is one pass of its own, which does almost no arithmetic and is limited by
having to read every parameter it uses out of memory once per token — at two bytes a parameter that
is roughly one operation for every byte read, on hardware built for hundreds. So the first token
pays for the prompt and each later one pays for a single pass. Two things follow. A long prompt
moves the first wait and barely touches the rate after it, so the two complaints have different
fixes. And later tokens are not free of growth either, because each pass attends over everything
stored so far, so a long reply gets slower as it goes. Check it by measuring time to first token
and tokens a second as two numbers.

**30.** Three costs rise at once and one of them faster than proportionally. The arithmetic of that
first pass has a part growing with the length and an attention part growing with its square, so
doubling multiplies it by more than two — though at a thousand tokens the squared part is about one
twentieth of the work, so the real multiplier is nearer 2.1 than 4; the two halves are equal around
nineteen thousand tokens, and only past that does the square run the show. The stored keys and
values grow with the length, so the memory you are holding doubles, and that is usually what
decides how many conversations fit on a machine. And every pass that produces a token attends over
all of it, so each token of the reply costs more than it did. The slogan that this is quadratic is
true of attention and not of the pass. Check it by timing that first pass at both lengths and
comparing the ratio with 2.1 at your own shape.

**31.** It is the stored keys and values for every position in every layer, kept so that producing
each new token does not recompute them — all but the last row and column of the grid are unchanged
from the previous pass, so recomputing is the obvious waste. Its size is two, for keys and values,
times the layer count, times the width, times the tokens, times the bytes a number takes. At a
common shape — thirty-two layers, a width of 4,096, two bytes — that is 512 KiB a token, so 3.91
GiB for an eight-thousand-token conversation and 39 GiB for ten of them. Two consequences: the
cache rather than the weights usually decides how many conversations fit, so doubling your traffic
is a memory problem and not an arithmetic one, and it is why running many requests together saves
less at long contexts, since the parameters are shared and each request's cache is not. Check it by
putting your own layer count and width into the formula.

**32.** Two reasons. The first is about what actually runs: a model can hold many feed-forward
blocks per layer and route each token through only a few, so the parameters that run for a given
token are a fraction of the total the model holds — under a third in a worked case. Cost follows
that active figure, while the name quotes the total, which is why the headline size misleads. The
second is that producing a token is limited by reading parameters out of memory, and one read
serves every request running together in the same pass, so the cost of the read is divided among
them. That is most of why the price per token is as low as it is. The trade-offs are real: the
machine still has to hold every parameter, so memory follows the total rather than the active
count, and sharing a pass with strangers is exactly why your output can depend on who else was
calling. Check it by comparing a model's quoted size with its active parameter count.

**33.** Because no step in the computation consults anything or checks anything. The pass turns the
input into one distribution over the vocabulary using only its own fitted numbers; there is no
lookup, no source and no verification anywhere in it. So a fabricated citation that reads exactly
like a real one is the most ordinary thing the mechanism can produce — a plausible continuation is
the only kind of output there is. Two consequences follow. Asking the model to be careful cannot
fix it, because carefulness is not a step in the arithmetic; it shifts the distribution, which is
not the same as adding a check. And the checking therefore lives outside the model, in retrieval
that supplies a source or in code that verifies the claim against one. Check it by taking a claim
type you care about and verifying a sample against the source: the rate is a measurement you can
have, and it is never zero.

**34.** Those are two claims and only one of them is mechanism. The mechanism is that one pass runs
its layers once however hard the question is, and nothing persists between passes, so writing the
steps out as tokens is the only place a partial result can go — the model's only scratchpad is its
own output, which is why intermediate steps can carry work forward at all. That the working also
makes the answer better is a separate and weaker claim; the mechanism does not reach it, it sits as
demonstrated and studied rather than settled, and how much it buys on your task is therefore a
measurement rather than a fact. As for the trace, it is generated text and not a record: those
tokens do real work and are not an account of how the answer was produced, so reading them as an
explanation is a mistake. It also costs output tokens, the dear half. Check it by running your own
set both ways and putting an interval on the difference.

**35.** Name the thing, say what you know that borders it, say what you would do if you needed it.
So: honestly, nobody has a clean account of that. The mechanism I can give you is that more layers
means more rounds of gathering from other positions and computing at each one, and a result
assembled at layer twenty can be gathered from at layer twenty-one. Why that buys what it buys —
why thirty-two layers beats sixteen by more than it costs, where the returns stop — is an open
research question, and I have not studied the attempts at it. What I can tell you is what a layer
does, which half of it holds the parameters, and what depth costs at inference. If I needed the
theory, I would start with the standard text rather than a blog post, because this is settled
material and not a moving target. The failure here is not saying I do not know. It is stopping
there, or producing a confident derivation instead.

### Answers 36–51 · Use

**36.** Four: instructions, examples, output format and supplied information. The first three are
a specification that changes rarely; the fourth is data that changes on every call. Separating
them buys three things. You can change one block and measure it, which you cannot do if a prompt
is one lump of text, because then you have changed a prompt and do not know which part moved the
result. It shows you where your bill is, since the specification is paid for on every single call
whether or not it did any work that time. And it puts the unchanging part at the front, where it
can be cached, and the data last. It also tells you what must survive when the conversation stops
fitting, which is the specification and nothing else. Checking it is counting: tokenise each block
separately and look at the shares. The usual surprise is how much of the bill is the part that
never changes.

**37.** The one rule that comes closest to not being a trade-off: the specification never goes.
That means the system message, and the example turns too if that is where the examples live. It is
a small share of a long list, and dropping any of it changes the behaviour of everything after, so
pin it and truncate around it. Then four strategies, each losing something different. Drop the
oldest turns from the front; keep a fixed window of the last few, always; replace old turns with a
summary; or start again and carry nothing. The real difference between the first two is
predictability — dropping oldest keeps as much as fits, so cost per turn keeps rising, while a
fixed window makes every turn cost the same. The one that catches people is summarising: a summary
is itself model output, and nothing tells you what it left out. Check it by logging what you
removed each turn, so the loss stops being silent.

**38.** Because if the information is not in the request, no wording fixes it — and that half is a
derivation rather than a survey. The model has only what you sent it, and no step in the
computation looks anything up, so a rewrite cannot supply a fact. The ordering practitioners
converge on follows: is the information there at all; is the task clearly specified with the output
shape stated; are there examples, since showing beats describing for anything with a format; and
only then, is the wording good — a real lever and the smallest of the four. The uncomfortable
corollary is that a prompt failing for want of information can be rewritten for a week without
improving, and you will feel busy the whole time. On strength, the ordering is a current
convention resting on what practitioners report, short of settled practice, because nobody has
written down where it stops holding. Check it by printing what the model actually received before
touching the wording.

**39.** First, read the error's body and not only its status. Too many requests means you are going
too fast and is retryable, but the same status comes back when the account is out of credit, and no
wait fixes that. Then four things. Retry with exponential backoff, so a struggling system is not
hammered, and with jitter, so your workers do not retry in step. Bound how many run at once with a
semaphore — rate times duration, so a hundred and twenty a minute at two seconds each is four — and
leave a margin, because a semaphore bounds concurrency and not rate; if the requests-per-minute
limit is the one that hurts, use a token bucket. Check that one raised exception is not discarding
your three thousand nine hundred and ninety-nine good results, which it does unless you ask for
exceptions to be returned. And the reason document four thousand hurts at all is that nothing
recorded the first three thousand nine hundred and ninety-nine. Check it by killing the job and
restarting it.

**40.** Because the check needs all of it. A streamed reply arrives as small pieces your code
appends, and validation asks a question about the finished object — does it parse, is it the right
shape, are the values possible — which you cannot answer from a prefix that is going to be fine in
a moment. So the rule is to stream when the consumer can use a piece, and not when it needs the
whole. A sequence of independent units is the case where it does work, because each unit can be
validated as it completes, and that is worth designing for deliberately. The thing people forget
is that streaming also buys a cancellation point, which is the saving nobody builds: you can stop
paying for output you already know is wrong. The trade-off is plain — a shorter wait before the
first word, against validating anything as a whole. Check it by handing your validator a prefix of
a reply you know is good and watching it fail.

**41.** Doing an operation twice has the same effect as doing it once. It matters because a
timed-out call may have succeeded: the result never reached you, so your retry is a second request
for work that is already done, and the timeout cannot tell you which case you are in. Where it
bites is anything with an effect outside your own process — a charge, a message sent, a row
inserted, a file written. The mechanism is a key derived from the content of the request, a record
of which keys have completed, and a check against that record before you act. The trap is the one
that looks like safety: a content-derived key will also defeat a re-run you meant to make, so you
need a deliberate way to say this is a new run over the same input. Check it by sending one request
twice on purpose and counting the effects. One, or the key is not doing its job.

**42.** From a file you wrote as you went, not by starting over. The shape depends on the job: one
flushed line per item for a single job over many items, and one line per item and stage for a
pipeline, keyed by the input and holding that stage's result. On restart you read it, skip what is
finished, and do the rest. Two details carry the whole thing. Flushed, because a line sitting in a
buffer is lost in exactly the crash you are protecting against. And keyed by the input rather than
by position, so the file survives a reordering or a changed input set — a position-keyed file
quietly matches the wrong rows. The trade-off is that each stage's result has to be storable, so a
pipeline passing rich objects around needs them serialised at every boundary. Check it by killing
the job halfway and restarting: redone work or skipped work means the key is wrong.

**43.** Not by comparing two scores, because one run is not a score. Forty cases at a true 0.70
have a standard deviation of 0.072, so a span of two of those is about fourteen points, and five
seeded runs of one unchanged prompt gave 0.625 and 0.875 among them. Nor by computing an interval
for each and looking at whether they overlap, which is not the test. Put the interval on the
difference, and compute it paired: both prompts on the same cases, resampling the cases rather than
the results, which cancels the part of the case-to-case variation the two share. Here that took the
width from 0.400 to 0.250. Then read what is actually carrying the comparison, which is only the
cases where the two disagree — 33 agreed and 7 disagreed, five to two, which is why the interval
still contained zero. Cannot tell is then the answer. Check it by writing the prediction down
first and changing exactly one thing.

**44.** Resample your cases with replacement, compute your statistic on each resample, and take the
2.5th and 97.5th percentiles of those. That is the whole procedure — three lines, and no
distribution to assume or formula to derive. A proportion has a perfectly good closed form, so the
reason to prefer this is not that it is more correct: it is that the same three lines also give you
an interval on a paired difference, on an average of per-case marks, and on a ranking measure,
where a closed form is a fresh derivation each time and a fresh chance to pick the wrong one. Two
limits to say out loud. The interval is anchored on the score you measured, so it recovers the
right width and says nothing about being in the right place. And it cannot see a failure it never
observed. Check it on a statistic whose closed form you know, and compare the widths.

**45.** They buy different things, so neither fixes the other. Cases buy resolution on the range of
inputs; trials, meaning repeats of the same case, buy it on the model's own variation. Averaging
several judgements of one case divides that case's own variance by the number of them, which
diminishes steeply, so two or three and stop — and they are averaged within the case, never
recorded as extra rows, because the statistics count rows. For cases, width shrinks with the square
root, so each halving costs four times as many. Concretely, at the shape measured here, two hundred
cases is where a difference of seven and a half points starts to be visible, but a real draw of two
hundred clears zero only 72 times in a hundred, and four hundred manages 95. That gap is the
difference between a typical interval and a detection rate. Check it by computing the interval your
own case count would give before collecting anything.

**46.** Because prose has no contract. Your code would have to guess what the words mean, and a
guess that is right ninety-five times in a hundred is a defect five times in a hundred. The reason
a reply was clean JSON ninety-nine times is that clean JSON was the likeliest continuation, not
that anything enforced it, so the hundredth reply is not bad luck — it is the same mechanism
working normally. So ask for a fixed format: show the exact shape rather than describing it, say
what to do when a value is unavailable, and ask for nothing but the format. Then enforce it in
code, because a schema is a contract your code checks rather than a request you hope was honoured.
The limit is worth stating in the same breath: a schema check tells you the answer is shaped like
an answer and not that the answer is right. Check it by running eleven realistic replies through
your validator.

**47.** Measure it on a set and put an interval on the rate. One failure in forty gives an interval
of 0.000 to 0.075, and that lower end is an artefact of resampling a single failure rather than
evidence the rate might be zero; two thousand replies place it between 0.011 and 0.021. If you see
no failures at all, resampling has nothing to resample and reports zero to zero, so use the rule of
three instead: none in forty tries is still consistent with one reply in thirteen. Then the
failures have four options, and the one never to choose is a silent default. Reject by default.
Retry, feeding the validator's own message back. Repair the envelope and never the contents —
needing to know what the model meant makes it a retry. And record every failure with its input.
Check the finish reason too: an unterminated string usually means the token cap rather than a
formatting slip.

**48.** By masking. Before each pick, every token the format forbids has its score set to minus
infinity, so the softmax gives it a probability of exactly zero and no decoding rule can choose
it — as long as one token survives, since masking them all gives you a nan rather than a zero. The
model computes what it would have computed anyway; the constraint edits the numbers on the way out.
The format itself compiles into a state machine over the tokens allowed next. The reason engines
differ in what they support is that your schema is written over characters while generation happens
over tokens, so the honest check runs the whole grammar over every character a candidate token
would contribute, in every state, asking whether what is left is still satisfiable. Engines
precompute that, which is why features keeping the machine small are supported and recursion and
length bounds often are not. Check it by reading the deleted probability mass per step.

**49.** Two ways, at very different strengths. The first is a derivation: the schema forbids
intermediate tokens, and the model's only scratchpad is its own output, so a format with nowhere to
think in deletes the thinking. How large that effect is, though, is a handful of studies, each in
one setting, with nobody having written down where it stops holding — so give the mechanism
confidently and the magnitude carefully. The fix follows from the mechanism: a reasoning field
before the answer field, in that order, because tokens condition only on what came before them, and
it works only if the engine holds you to your field order, which the format itself does not. The
second way is commoner and arithmetic rather than subtle — a schema too narrow to express the right
answer deletes that answer, because you forbade it. Check it by treating strict mode as a change to
measure: paired, same cases, an interval on the difference.

**50.** Five steps, and four of them are yours. You send the tool descriptions, as text, in the
input. The model emits a proposal — tokens your code reads as a request to run something, and
nothing has happened yet. Your code parses it, validates it and decides. Your code runs the
function. Your code sends the result back as a tool message. So there are two decisions and only
one of them can refuse: the model decides what to propose, your code decides what runs, and the
second one is invisible precisely because it happens in code you wrote. What the model never sees
is the function itself, or any constraint you kept on your side — a description is a name, a
sentence, and the parameter names and types, at around two hundred characters each. That is input
on every call, so thirty tools is of the order of fifteen hundred tokens before the conversation
starts. Check it by logging every proposal beside what actually ran.

**51.** In your code, and the reason is mechanical rather than a matter of taste. Nothing in the
loop compares a proposal's values against your instructions except code you wrote. Your instruction
is competing with every other piece of text in the input, because nothing in the input marks one
part of it as the instruction. A strict mode can hold a proposal to a shape, and to an enumerated
set of values, and neither of those is a limit on a number or a check against the world. So a year
of compliance is a correlation rather than a limit, and it tells you nothing about the proposal
that arrives tomorrow. A proposal can be anything the model can emit: a tool you never described,
an argument of the wrong type, a refund of nine thousand pounds, or a sentence where a proposal
should be. Your code is the only participant that can refuse. Check it by feeding those four
straight to your dispatcher.

### Answers 52–65 · Retrieval

**52.** By measuring, because the best model is a property of your data — through its language,
its domain and its document length. Length first, since it is the one that gets forgotten: every
embedding model has a maximum input length, and past it your text is cut off with no error at all.
Then build the one input no benchmark can supply, which is the answer key — which document each of
your queries is actually about. Shortlist three models from public results, run them over your own
queries, and score. The trap is that an overall figure hides the thing you are choosing on. Two
candidates both scored three of four overall, while one went two of two on short documents and one
of two on long, and the other the reverse; grouped by language the two were identical. So a
breakdown helps only when you group by the property that matters for your corpus, and picking that
property is a judgement you make before running anything.

**53.** Because it is one study: it worked there, on somebody else's corpus, with somebody else's
queries and document lengths — and those are the properties that decide which model wins on yours.
It also cannot supply the input the whole measurement turns on, which is which document each of
your queries is actually about. That has to come from you, and it is the step people skip. There is
a second reason not to read a leaderboard number as a quantity: a raw similarity score has no
meaning on its own, not across models, not across queries and not across corpora, so you can rank
by it and you cannot carry it anywhere or threshold on it. The right use of a benchmark is to
shortlist three models in an afternoon; the wrong use is to pick one. Check it by running your
shortlist against your own answer key, paired, with an interval on the difference.

**54.** Anything keyed on an identifier. Two maintenance notes differing in one token out of ten
sat 0.99983 from each other, and the right one won by 0.00050 — which is the difference of two
distances from the query rather than a distance between any pair, so there is no margin to work
with. Names, invoice numbers, error codes, stock codes and version strings are all that same case.
The reason is a sketch rather than a calculation: one vector has to hold the whole text at a fixed
width, so a string that appears once is competing for that room with everything else in the
passage. Tokenisation compounds it, because a rare code is cut into pieces that are mostly common
fragments, so little of what survives is specific to that code. And that dense retrieval loses to
lexical scoring on such queries is an observation, not a derivation. Check it by scoring your own
identifier queries both ways.

**55.** Because one is symmetric and the other is directed. The cosine of a and b equals the cosine
of b and a, which falls straight out of the formula. Relevance is a judgement that depends on who
is asking: a glossary entry answers what does idempotent mean, and the question does not answer the
entry. A better model narrows that gap and cannot close it, because the two are not the same kind
of object. The sharpest illustration is negation. A sentence and its negation sat 0.99976 from each
other — closer to each other than either was to the question — so whatever separates them is a
residual, and that residual reaches you as one number carrying everything else as well. You cannot
tune it, threshold it, or tell from the score which of the two you are holding. Check it by
building an answer key and scoring the ranking against it, rather than inspecting distances.

**56.** It scores a document by the query terms it contains, and it answers three objections in
order. Term frequency: a document mentioning a term often is more about it. Inverse document
frequency: a term held by few documents is worth more than one held by many, since otherwise the
commonest words would dominate every score. And document length: a long document mentions
everything more often without being more about any of it. Two properties are worth carrying and
the tuned constants are not among them. Term frequency saturates — a hundred mentions reach about
98.5 per cent of the ceiling — which is why a document saying refund six times lost to one matching
two query terms once each. And the classic inverse weight goes negative for a term held by more
than half the collection, which is why the modern form adds one inside the logarithm. Check it by
scoring a document that repeats one term and watching the curve flatten.

**57.** A bi-encoder puts query and document through an encoder separately and compares the results
with a cosine, so every document vector is computed before any query arrives and query time costs
one forward pass. A cross-encoder puts the pair through one model together, so nothing is
precomputable, a million documents cost a million passes, and the score is free to be asymmetric.
Hence two stages: retrieve cheaply over everything, then rescore a candidate set of about a
hundred. One correction worth making, because it is commonly got wrong: a bi-encoder is not by
itself an escape from the symmetry problem. What forces symmetry is putting both sides through the
same function, so separate query and document encoders — or one model told which side it is
encoding by a marker — keep the precomputation and give up the symmetry. Check the ceiling:
reordering a candidate set cannot add anything to it, so the first stage bounds the second.

**58.** Discounted cumulative gain sums each result's relevance grade divided by a discount that
grows with position; normalising divides that by the gain of the best possible ordering of the same
documents, which is what makes it comparable across queries. The logarithm is a convention and not
a derivation: the discount has to decrease with position, and a logarithm decays slowly, which
roughly matches how people read a list. What is derivable is that the base cancels — base 2, 10 and
e gave three different gains, 3.9307, 13.0574 and 5.6708, and an identical normalised figure of
0.621602, because changing the base scales the measure and its ideal by the same constant. The gain
convention does not cancel: the grade directly gave 0.6216 and two to the grade less one gave
0.5193 on the same ranking. So two tools' numbers are not comparable until you know both
conventions. Check it by recomputing at a second base and confirming the normalised figure does not
move.

**59.** Not by adding the scores, because neither has a unit: the lexical scores ran from 0 to
5.5089 and the similarities from 0.6198 to 0.9891, so a sum is whatever weighting you implied
without stating it. Reciprocal rank fusion throws the scores away and sums one over a constant plus
each rank, which needs nothing from either system except an ordering. What it pays for that is
ties: a document at ranks one and two and a document at ranks two and one are indistinguishable to
it, so the right answer can score exactly the same as the wrong one, and your tie-break then
decides the measurement. Its constant, usually sixty, sets what a first place is worth — the gap
between rank one and rank two is 0.5 at zero and 0.000264 at sixty. And fusion is not bounded by
its inputs in either direction. Check it the paired way, with an interval, and declare your
tie-break.

**60.** The claim has two halves and only one of them is derivable. The derivable half: every later
stage consumes the parser's output and none of them reconsults the file, so a dropped word is
absent from the chunker, the embedding, the index and the reranker alike, and no stage can correct
an error upstream of it. The observed half — that it is in practice the commonest cause of bad
answers — is an observation nobody can put a rate on from here. Why it goes wrong is that a page is
not text: a document format's page is a list of instructions placing strings at positions, with no
sentence, no column and no reading order recorded in it, so reading order is reconstructed by
approximate rules. Two files placing the same eight strings at the same positions, differing only
in the order they were drawn, read correctly one way and weld two separate policies into one
paragraph the other. Check it by printing the extracted text for a document you know.

**61.** Three things: what shares one vector, what can be returned together, and which questions
are answerable at all. Then the derivation worth carrying. Retrieval scores rows and returns some
of them, so if no row holds a whole answer, no method, model or reranker can return a single
passage that answers the question — and that was fixed when the parser and the cuts were chosen.
State it no wider than that, though: where the cuts tile the document the information is still
there across two adjacent rows, so reassembling an answer moves downstream rather than becoming
impossible, and a chunker that discards text is a different matter. Two failures are distinct too.
When the chunk is smaller than the answer, no amount of overlap helps — sixty-character chunks
never held a sixty-five-character answer. When the chunk is big enough and the cut falls inside the
answer, overlap is exactly the fix. Check it by writing five real questions and sizing the chunk
above the longest answering passage.

**62.** They are not alternatives, because they answer different questions: retrieval answers which
text is relevant, and the window answers how much of it you can afford to show. The arithmetic says
why selection arrives early. A hundred documents of two thousand tokens is two hundred thousand
tokens against a hundred and twenty-eight thousand, about 1.6 times over, and filling a window that
size costs 62.5 GiB of stored keys and values on a common shape, against 13 GiB of weights. The
observed half cuts against the obvious conclusion: more in the window is not reliably more used. So
a long window buys a looser budget, a large document handled whole, and the removal of the worst
small-window failures. What it does not buy is an end to choosing, because a window is finite at
any size and a corpus is not. Check it by computing the cache cost of the window you propose to
fill.

**63.** That the quoted text entails the statement it is attached to — not that the quote exists.
Three checks are mechanical and each catches a different failure: does the document exist, is the
quote in it, and is it at the offset claimed. One case shows why the first earns its place on its
own, a genuine quote filed under a filename that does not exist. But a citation can pass all three
and still be wrong: real text, at the exact offset claimed, attaching a cancellation fee to a
refund. So the three are necessary and not sufficient, and what they buy is a much smaller set of
survivors — the wrong-claim case, a statement cited nowhere at all, which the checks never look at
because there is nothing to look at, and a quote undone by the document's next sentence. Then a
person reads a sample of what survived. Check it by running the three in code and sampling the rest
by hand.

**64.** It buys work. Instead of comparing the query against every vector, it groups them once and
searches only some of the groups, so one query took 120 comparisons against 2,000 and returned the
same ten documents. What it costs is exactness, and the honest way to put that is that an index
whose recall you have never measured is a speedup of unknown cost. Measure it against the
exhaustive search you installed it to avoid — once, offline, on a sample. Then read the worst query
and not the mean: one probe gave a mean recall of 0.925 over twenty queries while the worst query
scored 0.4, and only six of the twenty lost anything, so that mean is fourteen perfect queries
averaged with six partial ones. Two more things. Comparing against the group centres never goes
away, so probing every group costs more than no index at all. And recall against brute force is not
the same as returning the right documents.

**65.** The filter stops being an optimisation and becomes a correctness requirement, because
returning another tenant's document is a disclosure. That rules out the arrangement people reach
for first. Searching everything and then discarding what the user may not see returns about the
fetch size times that tenant's share of the corpus — a tenant owning one per cent asked for ten
results and got one. Nothing reports a failure, and a short list is indistinguishable from a tenant
who genuinely has little. Raising the fetch does not rescue it either, because an approximate
search returns at most what it examined, so a larger fetch means more probes and more probes means
the exhaustive search the index existed to avoid. Restricting the pool before searching was both
exact and cheaper for that tenant, twenty comparisons against two hundred and twenty. Check it by
writing down the smallest tenant's share: that is the number the whole design turns on.

### Answers 66–76 · Measurement

**66.** Read them, beside their inputs — not a dashboard, not a metric. Write one short note per
failure in your own words before you have any categories at all, because the categories you start
with tend to be the ones you already believe, and escaping those is what the exercise is for. Then
group the notes and count. Then let the modes choose what you measure. One warning about the
grouping: it is a judgement about the outputs and not about the notes' wording. Grouping forty
notes by their opening verb gave ten groups against eight real modes and failed in both directions
at once — five of the ten held more than one real mode, and six of the eight were split across
groups, because the same kind of wrong gets written down three ways. And name a mode after what
went wrong, never after the part of the system you suspect, or every count afterwards is a count
of your guess. Check it by confirming every note was used exactly once.

**67.** Because a conventional metric measures what was conventional for somebody else's
application, while a check derived from your own modes is guaranteed to be about a real failure,
with its coverage known before you build it. Worked on forty failures in eight modes, the best
actionable check caught twenty — perfect it and twenty failures are untouched, which is what
choosing the metric before knowing the failures costs you. Coverage is not the test either: exact
match against a reference answer catches all forty and closes all eight modes and is useless,
because every failure differs from the reference and so does every correct answer worded
differently. Read the other way, the modes say what to build — a claim-support check was twenty
failures for one piece of work, and a refusal detector seven more and nearly free. All three usable
checks together reached 28 of 40, leaving twelve in five modes and one mode untouched, which you
write down rather than inventing a metric for. Check it by marking checks failure by failure.

**68.** When the check needs a decision about what the text means, and not before. Sorted by what
each one needs in order to decide, nine of sixteen checks need only a comparison between things
that are both literally present — a filename, a substring, an offset, a digit — and seven need a
judgement about meaning. That is the line, and it is the whole answer. The second thing to say is
that a failure mode is not a code mode or a judge mode: six of eight split, and seven of the eight
have a part that code can decide, so run the cheap part first and leave the judge less to be wrong
about. And whatever you do use a model for, have it return pass or fail on one named mode rather
than a score out of five, because a score has to be interpreted before anybody can act on it and
the interpretation is yours. Check it by writing the code check first and seeing what is left over.

**69.** Three measurements, in order, and the first two need no labels at all. Self-agreement:
show it twenty of the same answers twice and count the flips. One judge held its verdict on 17 of
20, and one of the three flips was a failure it had caught, so a reported five of twelve could
have printed as four of twelve — which bounds how much of every other figure you can rely on. Then
a flip count under an arbitrary change, such as printing a pair the other way round. Then the
baseline: what a judge that passes everything would score, which was 48 of 60, eighty per cent,
finding nothing — so eighty-five per cent is five points of value. Then split that agreement into
the two numbers that matter: of the real failures how many it caught, and of its alarms how many
were real. Check it by labelling enough failures rather than enough cases: the catch rate uses the
failures alone.

**70.** A judge preferring an answer for where it was printed rather than for what it says. The
same judge on the same forty pairs reported a seventy per cent win rate with the new answer printed
first and thirty per cent with it printed second — a forty-point swing with nothing changed but
the order, and whichever order you happened to run is what you would have reported. The
measurement is the flip count rather than either rate: sixteen of forty, every one of them to
whichever answer came first, and that is exactly what a single ordering cannot show you. Both
repairs cost something. Discarding the flipped pairs throws away forty per cent of your data and
assumes the rest are not systematically different; scoring them half each dilutes every real
result towards a tie. The honest report is two numbers: it agreed with me on twenty of the
twenty-four pairs where it held a verdict, and held none on the other sixteen.

**71.** Because one verdict on the answer cannot say which half failed, and the two halves have
different fixes. Scoring every case twice turned a single 62.5 per cent into four cells:
twenty-two fine; eight where an answer was in the context and the system got it wrong, which
finding more passages fixes none of; seven where no answer was there at all, which belongs to
retrieval and no prompt work touches; and three where no passage held an answer and the answer was
right anyway. Eight against seven says both stages, in almost equal measure, and the headline said
none of it. The cell people miss is the last one: the end-to-end figure counts those three as
successes, and for a grounded system they are failures, because the answer did not come from the
passages, so nothing can show where it did come from and nothing will notice when the document
changes. Check it by building that table before proposing any fix.

**72.** Decomposing the answer into the claims it makes and giving each claim a verdict against the
retrieved passages. Grounded means every claim is supported, which is the citation principle — the
quote must entail the statement — applied to every claim rather than only to the cited ones. The
unit is the whole point. One answer scored three of six claims supported against three of four
sentences: two figures twenty-five points apart from the same text, and the difference is that a
sentence carrying one supported claim and one invented one lets the first vouch for the second. In
that answer the claim that actually answered the question was the unsupported one, built on a real
passage read as saying something it does not say. Had it cited the two passages it leaned on, both
citations would have passed all three mechanical checks. The trade-off: decomposing is itself a
judgement, so the figure is comparable only against itself under one rule held still.

**73.** Two places, and neither is enough on its own. Real failures give you the questions people
actually ask. Generated questions give you an answer key for free, because you know which passage
each one came from, and they cover corners nobody has asked about yet. The trap is that a generated
set is easy by construction: a word-overlap retriever ranked the right passage first on eight of
eight generated questions and two of eight asked ones over the same passages, because a generated
question shares three to six words with its source and a real one shares none or one. A question
built from a passage is a question about your own vocabulary. So generate, then rewrite the
questions away from the passage's wording and keep the key — and keep the two sets apart, because
averaging them gives a number that means neither. Check it by counting the words each question
shares with its source passage.

**74.** Everything, or every case that has ever failed — not the failures only, which is the
mistake almost everybody makes. A set of past failures cannot catch a case that has never failed:
run one against the next version and it reports four fixes and no regressions when there were
three, because all three passed the previous version and so were never in the set. The ever-failed
set reports those three as standing failures rather than as regressions, since a before-and-after
comparison cannot report an already-failing case as one; what it buys you is the change after that
one. It runs on every change. And running it once is not running it: four of twenty cases were
unstable in both versions, and a single-run comparison reported two regressions and two fixes where
a five-run majority reported one fix. Check it by the rule that a case is not a regression until it
fails more often than it passed.

**75.** Your own standard moving as you see more output. The same forty outputs, unchanged, scored
eighty-five per cent in week one and 72.5 in week five, with seven labels changed and six of them
from pass to fail. That destroys any comparison across time, because a version scored in week one
against one scored in week five differs by a change you made and a change you underwent — 12.5
points of it here. You notice it by keeping the old labels and re-labelling a sample blind. Looking
at the old label first measures nothing, because you will agree with yourself. When the flips go
one way you have learned a criterion, so write it down and re-label the whole set, or you are
running two standards inside one set. And drift itself is not a mistake to eliminate, since it
belongs to a person's judgement. Silent drift is, including a code check whose documents changed
under it.

**76.** The record of one request: the input, the retrieval query and its candidates with their
scores, the model and its version, the tool calls, the output, the tokens and the per-stage
timings. It is where your cases come from. The content decision is the interesting one, and it is
not all-or-nothing. Four of sixteen fields hold text; drop them and five of eight questions still
survive — including whether retrieval returned the right passage, which a document id answers with
no text at all. What is lost is everything needing the text, and a case needs an input and an
output to be a case, so a content-free trace cannot feed a regression set. So: ids, counts and
timings on everything, and content on a sample of the failures, with a deletion window. Three
fields to think twice about are the whole source document, anything sent as a credential, and
anything you cannot delete on request.

### Answers 77–86 · Agents and Adaptation

**77.** Four columns, and two of them are not what people expect. Can you enumerate the paths,
which is the only column that can make an agent necessary. Is there a cheap check on the result — a
veto rather than a reason, since nothing makes an agent safe except being able to tell when it was
wrong. Can a wrong step be undone, which decides whether a person has to approve each step rather
than whether to build the thing at all. And the shape: paths you cannot enumerate still get a
pattern when you know the work splits and only a model can say into what, which is an orchestrator.
What is not a column: how hard the task is, how good the model is, whether anybody would be
impressed. On nine tasks the rule gave six patterns, two agents and one that belongs to a person.
The order to try is one call, chain, router, parallelise, orchestrator, evaluator, loop — climbing
only when the evaluation set fails.

**78.** Five of them. Prompt chaining is stages in sequence, each call's output the next one's
input, for work with nameable stages that are easier asked separately. Routing is one call picking
a branch from a menu your code wrote, so adding a branch is a reviewable code change rather than a
sentence in an instruction. Parallelisation is one call per piece, with the pieces coming from the
input, and then one call to combine. Orchestrator and workers is that same shape with a model
deciding what the pieces are. Evaluator and optimiser is produce, judge, revise, until the judge
passes or your code gives up. The distinction worth more than the names is which of them have a
call count you can work out before you run: four of six do, and the last two do not, because a
model decides how many pieces there are and a judge decides when to stop. So fixed in shape is not
fixed in length, and controlling the path is a different property from knowing the bill.

**79.** Replacing the record of a run with a shorter one that keeps the facts later steps need —
summarising applied to a loop, where nothing reading that record while the run is still going can
notice an omission. The proof is a must-keep list: the facts the rest of the task depends on, named
before the summary is written and checked against it afterwards. A list written afterwards is
written from the summary and tests nothing at all. What goes into it first is the negative
results — what was tried and did not work — because a kept negative result is what stops a later
step repeating a step already taken, and putting them first costs one line. That ordering claim is
a demonstration and no higher, since two dropped facts are the whole sample. The trigger is set by
the largest single result your tools can return: on a window of 128,000 tokens with an 8,400-token
result, that is 93 per cent and not 95.

**80.** Because a note is model output read back as established fact. Whatever wrote it had every
property any other generated text has — no step in producing it checked anything — so a plainly
phrased note saying an account is closed may simply never have been true, and by the time a later
step reads it nothing distinguishes it from something you put there yourself. The repair is
provenance: two extra fields, where the fact came from, meaning read or inferred or told, and when
it was written. Those do not make a note true. What they do is separate a note that went stale
from one that was never right, and only the first is caught by a date. The same argument covers a
tool description from a server you do not run, which is text sitting in your input beside your own
instructions — so the limit stays in your registry and your dispatcher, neither of which reads a
description. Check it by sampling your notes and verifying each against its source.

**81.** It is named for a task somebody asks for rather than for an endpoint that happens to
exist, and it does the joining your code would otherwise have done. Twelve endpoints rewritten as
four purposeful tools took five tasks from fourteen calls to nine and cut the plausible first
moves from 5.4 to 2.0 — with each description 130 characters longer, and the set still costing 46
per cent less. The output matters as much, because an output is the next call's input: of
twenty-six fields on one order object, seven were read and the other nineteen were 78 per cent of
the characters. So high signal in few tokens means dropping what the task does not read and adding
what the model would otherwise need a second call to work out. Never truncate silently, because a
list cut to three items looks exactly like a list of three items. And an error should say what to
do next: a bare status code let the next step recover from none of eight failures.

**82.** A documented wire format between a host, which is the application holding the model, one
client per server inside that host, and a server offering tools, resources and prompt templates.
What it does not do is the important half. It adds no step to the five steps of a tool call and it
moves no decision: step three stays wholly yours, the model still only emits a proposal, and step
four becomes asking another process to run the function, which is the same step with a network call
in it. The model is not a participant in the protocol at all. So what it solves is integration work
rather than capability, and the lasting principle underneath is that a model can only be given
tools as text, and fetching that text is the same work in every application. One caution: a
description from a server you do not run is untrusted text in your input, so the limit stays in
your dispatcher.

**83.** Ask first whether the work comes apart, because that answer is arithmetic. Write the task
as pieces and what each one needs; the critical path is the longest chain through them, and it is
the shortest the task can take however many agents you buy. Pieces divided by the critical path is
the most parallelism the work contains — twenty for a queue of tickets, 1.0 for planning a trip —
and the number worth buying is the parallel width, the most pieces that can be in flight at once,
not one per piece. A coupled task pays for every agent and finishes no sooner. The cost runs the
other way from the story: dividing the work cost 0.61 times a single agent, because the re-send
cost falls with the length of a run, while six agents each doing the whole task cost 6.03 times,
which is what token multiplication actually names. The failures are three kinds — system design,
misalignment between agents, and task verification — and the evidence is one study.

**84.** The first is the chance that at least one of k trials succeeds, one minus the failure rate
raised to the k, and it rises with k. The second is the chance that all k succeed, the rate raised
to the k, and it falls. At a trial rate of 0.65 and five trials they are 0.995 and 0.116 — a factor
of 8.6 out of one underlying number, which is why four out of five means nothing until you say
which you mean. The second is the one that should worry you, because the first is only a capability
when something can tell a good attempt from a bad one. Two details worth carrying: estimate the
first from n trials with c passes by the without-replacement form and never by raising the observed
failure rate to the k, which understates it every time, and a 1.000 means k exceeded your failures
rather than that the task never fails.

**85.** Sort the ask by what it needs — facts the model has not seen, a behaviour, or neither — and
most cases decide themselves. Of twelve real asks, four needed facts, which is retrieval's job;
two were not a model's job at all; and six were behaviour, four of those reached by an instruction
in the request. That leaves two of twelve where tuning is even a candidate, and both had a prompt
that already worked, so the question was cost rather than capability — and the cost argument loses,
because a nine-hundred-token guide over a hundred thousand calls is ninety million tokens against a
hundred and fifty million for the tune, and a fixed prefix is the most cacheable thing a request
contains. The case that does justify a tune is a behaviour a prompt reaches unreliably. The order
is prompt, then retrieval, then tuning, because the first two are reversible in an afternoon.

**86.** Five standing obligations, and none of them is about accuracy: the training set still
exists and is licensed, the old weights still exist, something still serves them, somebody owns the
re-tune, and every base-model change needs its own gate. Three changes at eighty per cent leaves
you having passed every one only 51.2 per cent of the time — though being merely current at the end
needs only the latest tune, which stays at 0.80. Then the asymmetry people misremember: a low-rank
adapter cuts the trainable count 1,325-fold and the memory only 8.0-fold, because the frozen
weights still have to be in memory. So it makes a tune fit on hardware you have and makes no single
request cheaper to serve — it does make serving several variants cheap, at 8.4 MB a file. And a tune
moves what you did not train on: target 0.55 to 0.85 and general 0.90 to 0.775 here. Size that
general set by the smallest regression you would refuse to ship.

### Answers 87–91 · Apply

**87.** A retrieval system over forty documents and one PDF: parse, chunk, index, retrieve, rerank,
assemble one traced request, check the citations. Eight queries, with the shortest answering
passage written down first, which turns did-retrieval-work into a substring test instead of an
opinion. The numbers: 176 chunks cut on structure, nine of them under twenty characters, and one of
those stubs took rank one on a common word alone. Dense beat lexical by +0.311 recall at five, and
fusion lost to dense by −0.120, both intervals clearing zero. The reranker's gain straddled zero,
so it is not in the pipeline — measuring a stage is permission to delete one. End to end, four of
eight right: an answer was sent on five, right on four of those five, three failures retrieval's
and one generation's. And 612 input tokens to 75 output, 8.2 to one, so 67 per cent of the bill is
the input. The result I would lead with is the reply that was grounded, cited and wrong.

**88.** Thirty extraction cases from the corpus — a question, the document that answers it, and the
exact value — with a program asserting that every expected answer appears in its own document,
because a case whose answer is not in its source is a case about nothing. Two prompts differing in
one sentence, graded in code by exact match after a declared normalisation, so no judge was needed.
Then the step that mattered: read the failures, and read the union of all three graders' lists
rather than one, because they rejected nine, five and four and the loosest saw fewest. The nine
were three different defects — four were the key's notation, one was the key dropping a qualifier,
and four were the prompt being ignored, which the headline hid because the fairest grader stripped
the trailing unit that would have caught it. The paired bootstrap then gave +0.967 on one grader,
which measures format; on accuracy the set cannot separate the two at all.

**89.** That the comparison as I first set it up was confounded, and finding that was the result.
Twelve tasks each asserted to need two documents, three trials, three designs, 108 runs. The agent
searched once on 29 of 36 runs, so the smaller budget I had given it was never a trade — it was a
handicap, and a handicap is a confound. So I added the same loop at the fixed path's budget, which
makes the two questions separable. The agent against the fixed path is −0.444 and clears zero; the
wide agent against the fixed path, which isolates the design, is −0.167 and cannot tell; the wide
agent against the agent, which isolates the budget, is +0.278 and cannot tell. So forty-four points
split into twenty-eight of budget and seventeen of design, and the only comparison with a verdict
is the one that confounds them. The diagnosis is what I would act on: both loops wrote narrower
queries than the question they were handed.

**90.** Three levers measured on real traffic, and the honest answer is that two of them had
nothing to give. The baseline was eleven cents a thousand requests at a median latency of 1.31
seconds — the mean of 1.74 is one call in twenty-four that took 11.01, which is the sharpest
evidence that the wait is a queue. Reordering the prompt so the stable part comes first brought
back 2,432 of 2,458 input tokens cached against zero the other way round, worth nineteen cents a
thousand — but only on the shape that costs 3.4 times the baseline before the lever and 1.8 after
it, so taking both still costs more than not. The retrieved shapes got no cached tokens in either
order, their prompts being about 612 tokens against the provider's 1,024 minimum. And routing had
nothing to route to: both models answered twelve of twelve, a paired difference of zero, and the
cascade escalated three cases, all three correct answers.

**91.** Four payloads over three channels — a retrieved passage, a tool output's title, and the
notes store — on four questions, three trials, with a clean arm alongside. One cell of twelve fired,
and it fired on everything: an instruction appended once to the last retrieved chunk suspended the
citation rule on four of four questions, across all twelve runs. Nothing else fired, and no run
ever proposed the tool one payload named, so the registry was never asked and that defence was
never exercised. What generalises is the row rather than the column. The payloads asking the system
to add something got nothing, the one asking it to call something got nothing, and the one asking
it to stop doing something got everything — because your code can refuse an action, and an omission
is not a request, so there is nothing to refuse. It was invisible because what is missing is not
visible in what is there: correct prose, right figures, empty citation list.

### Answers 92–100 · What Next

**92.** Because your instruction is text in the input and so is the page it reads, and nothing in
one sequence of tokens marks which part is yours. A model's input has no channel for metadata — it
is one list of tokens — so this is a property of the component and not a defect a better model
closes. Two things follow, and the second is the one to act on. What injected text cannot do is
act: only your code acts, and only through a name its registry holds. What it can do is take away a
rule that exists only as an instruction — an instruction appended once to a retrieved passage
suspended a citation rule on four of four questions, across all twelve runs. So the boundary is
what your code can refuse, and any rule you actually care about needs a line of code at the end
rather than a sentence in a prompt. Check it by attacking your own system and seeing which rules
survive.

**93.** What happens depends on whether all three things are in that one session. The page is
input, like every other channel the model reads — the request, a retrieved passage, a tool result, a
tool description, a note the agent wrote, a sub-agent's return, a compaction summary. If the session
has access to the list and a tool that can send, then the injected text has something worth asking
for and a way to send it; the model proposes, and whether anything happens is your dispatcher's
decision, since that is the only participant that can refuse. What would have stopped it: removing
one of the three, shrinking one — the tool sends only to an allow-list, the retrieval is scoped to
the caller — or an approval. Approval is the weakest of those wherever the action is frequent,
because volume turns review into rubber-stamping. And an outbound URL the model composes is an
external action with no tool attached.

**94.** Never combine untrusted input, sensitive access and external action in one session without
approval. The reason is that any two of the three are ordinarily survivable. Untrusted input and sensitive access with no way out is a leak with no
channel. Untrusted input and an action with nothing worth sending is noise. Access and an action
with nobody injecting is your system working. The three together give injected text something worth asking for and a way to send
it. There are four fixes, and the first two are the strong ones, because they remove a capability
and so nothing has to work at the moment of the attack: have no such tool, and do not read the
untrusted thing. Then scope the access to the caller. Then have a person approve — the weakest of
the four wherever the action is frequent, because volume turns review into rubber-stamping, which
is worth saying since it is the fix people reach for first. Check it by writing down every
channel the model reads, then naming the sessions that hold all three.

**95.** Wherever you forgot that it was output rather than a value. That is insecure output
handling, and the fix is not novel: the escaping and parameterising that web and database
engineering settled long ago, applied at every place generated text reaches something that renders
or executes it — a template, a query, a shell, a file path. Two cases are easy to miss. Code the
model wrote needs sandboxing rather than inspection, because a validator reading generated code for
safety is a judgement about text standing where a limit should be: no network, no credentials in
the environment, nothing of production, and thrown away afterwards. And a URL the model composes is
an outbound request, which is an external action with no tool attached, so it needs a decision of
its own rather than falling under whatever the tools are allowed to reach. Check it by listing every
sink in your system and saying what escapes at each one.

**96.** First find out which complaint it is, because slow is at least four and almost none of them
shares a lever: nothing appears for seconds, the words crawl once they start, it is usually fine and
sometimes awful, or every call is quick and the whole thing is slow. So measure the first-token wait
and the per-token time separately, record the total, the token counts, the cached count, the model
and the sequence number, and report a middle and a tail rather than a mean — on one arm the median
was 1.31 seconds, the mean 1.74, only three of twenty-four were slower than the mean, and the
slowest was 8.4 times the median. Then attribute, because in a built system most of the latency is
your own design. Then one lever: streaming leaves the total alone and moves the first wait down to
prefill, and sending less helps both waits without handing you a different model to re-measure.

**97.** Not from the provider's breakdown: over a hundred and forty-four requests it was one row
with one number on it, and every split that mattered was inside a single feature. So there are two
routes. A separate key or project per feature costs nothing and cannot split finer than a key.
Recording the counts yourself answers questions nobody asked in advance, and cannot be done
retrospectively — so record the three token counts, the reasoning count, the model with its version,
and the row everybody omits, which is what the request was for. Then look for multipliers rather
than increments, because that is what the expensive features are: duplicated agents at 6.03 times
one, agents running on to a twenty-step limit at 13.79, a doubled loop limit at 3.4 times the
tokens, a reranker at about thirteen extra calls a request. They compose. And watch reasoning
tokens, which are charged at the output rate and not returned.

**98.** That sentence is almost always true and almost never relevant, because four other things
move: the model behind the name you call, your documents, the service's behaviour under load, and
your own standard — and only one of the four announces itself. So I would investigate in that order.
What should have been in place is three things. A pinned snapshot rather than a floating name,
because a floating name is not necessarily the newest, and a retirement is loud, specific and timed
by you where a repointed name is none of those. A gated upgrade: hold the prompt, the cases, the
grader and the temperature, change only the snapshot, and report the cases that moved rather than
the score — three of thirty moved while a difference of −0.100 could not be told from zero, and all
three of the newer model's answers were correct. And one versioned artefact holding the prompt, the
configuration, the index and the model version.

**99.** I can name the gaps, which is the point of having drawn the line where I did. Thirteen of
them: why the embedding geometry carries meaning, how the gradient is computed, what step size to
use, initialisation, regularisation, numerical stability, why gradient descent arrives anywhere,
why one objective rather than another, inductive bias, generalisation theory, why depth helps, why
models got better at producing useful intermediate steps, and scaling laws. Not one of them is
needed to follow the arithmetic of a single reply, which is the line I built on. As for learning
them: eight are one general text, two more are a learning-theory text, and three have no book —
two are open research questions and one lives in the literature. But the first thing I would read
is not on that list at all. It is the bootstrap, because it is a method I have used on real data a
dozen times and cannot derive.

**100.** Seven moves, and the architecture is only the third of them. One: clarify the requirement
in questions, the highest-value one being what it should do when it does not know, because the
default is a plausible answer rather than a refusal and the trade against refusing when the answer
is there is somebody else's decision. Two, deliberately before the architecture: thirty cases of
question, document and answer, with the grader written before any reply is seen, paired comparisons,
and the two verdicts kept apart. Three: dense retrieval, measured rather than asserted — dense beat
lexical by +0.311 recall over chunks and fusion lost to dense — with a lexical lookup kept for
identifier queries and the routing itself declared unmeasured. Four: the four prompt blocks in
order, a context budget rather than a window, and citations with their limit named. Five: eleven
cents a thousand requests, so six thousand a day is $19.80 a month. Six: the failure modes named.
Seven: four fields to watch, and what I would not build yet.
