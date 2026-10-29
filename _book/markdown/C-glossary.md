# Glossary

Every term the book defines, with the chapter that owns it. A term is defined in exactly one
chapter; every other chapter refers to it rather than redefining it.

| Term | Meaning | Ch |
|---|---|---|
| **429** | *Too many requests.* The provider's rate limit, on requests per minute and on tokens per minute. Retryable when you are going too fast; the same status comes back when the account is out of credit, which no wait fixes | 19 |
| **Accountability** | Somebody who can be asked to answer for a decision, and who bears a consequence for it. A property of people and organisations, never of a component | 3 |
| **Activation function** | The step in the feed-forward block that is not a matrix multiplication, such as keeping positives and zeroing negatives. Without it the block's two matrices would collapse into one | 12 |
| **Active parameters** | The parameters that actually run for a given token, as against the total the model holds. Cost follows the active figure; the name usually quotes the total | 15 |
| **Agent** | A system in which the model decides what to do next, repeatedly, rather than your code deciding the sequence | 4 |
| **Answer key** | Which document each of your queries is actually about. The only input in the procedure that has to come from you | 24 |
| **Answer relevance** | Whether the answer addresses what was asked. Independent of groundedness, and not a yes or no once the question has parts | 32 |
| **Approval point** | A step the loop cannot pass without a person, enforced in your code rather than requested in the instructions | 4 |
| **Approximate nearest neighbour index** | A structure that answers which vectors are closest without comparing against all of them, accepting that the answer may be wrong. Shortened to ANN | 29 |
| **Assistant message** | What the model said earlier in the conversation, sent back to it by your code. The model does not remember saying it | 18 |
| **Attention (self-attention)** | The step in which each position takes a weighted blend of information from the others, in amounts computed from the content rather than fixed in advance | 11 |
| **Attention block** | The half of a layer that moves information between positions — Chapter 11's formula in full. The only part of a model that does | 12 |
| **Attention head** | One complete set of query, key and value matrices and the weights they produce. A layer runs several in parallel over slices of the width, and a final matrix mixes their outputs | 11 |
| **Attention weights** | One row of the grid after scaling, masking and softmax: positive numbers adding to 1, saying how much of each position to take | 11 |
| **Attribution** | The claim that the cited text supports the statement it is attached to. No string comparison reaches it; Chapters 32 and 33 are where it gets checked by other means | 28 |
| **Autoregressive** | Producing output one token at a time, with each token appended to the input before the next pass | 9 |
| **Backpropagation** | The procedure that computes a derivative for every parameter in one backward sweep through the model. How the gradient of Chapter 14's update rule is obtained. Not taught in this book | 17 |
| **Base model** | A model that has had only pretraining. It continues text rather than answering, which is what the later stages change | 14 |
| **Baseline** | What a judge that always says pass would score on your set. Every agreement figure has to be read against it, and on a working application it is high | 31 |
| **Batch endpoint** | Upload requests, collect results hours later, pay substantially less. For work nobody is waiting on | 19 |
| **Batching** | Running many requests through the same forward pass, so one read of the parameters serves all of them. Close to free up to a point — each request still reads its own cache and does its own arithmetic — which is why the price per token is low and why your neighbours affect your output | 15 |
| **Bi-encoder** | Query and document encoded separately and compared by a cosine, so document vectors are precomputable. With one shared model the score is symmetric | 26 |
| **Big-O** | How a cost grows as an input grows, with constants and smaller terms deliberately discarded. Not a measurement of time | 8 |
| **BM25** | The standard lexical scoring function, combining term frequency, inverse document frequency and document length, with a saturating term-frequency curve | 26 |
| **Bootstrap** | Estimating how much a statistic would move by resampling your own cases with replacement. One procedure for every statistic you score, where a closed form is a different formula each time | 20 |
| **Byte-pair encoding (BPE)** | Building a vocabulary by starting from the 256 single bytes and repeatedly merging the commonest adjacent pair in a corpus until the vocabulary is the size wanted. Starting from bytes is what makes any text at all representable | 10 |
| **Candidate set** | The documents the first stage passes to the second. A reranker can only permute it, so it is a ceiling | 26 |
| **Capability set** | Tasks at the edge of what the system can do, scored well below 1.0 on purpose. At 1.0 it has stopped measuring, and the fix is harder tasks | 38 |
| **Case** | One input plus whatever marks the answer right or wrong. The unit the statistics count — and they count rows, so forty rephrasings of one question are worth nearer one case than forty | 20 |
| **Causal mask** | Setting every score for a later position to minus infinity before softmax, so it gets exactly zero weight. It makes a position's output depend only on itself and what precedes it, so the arithmetic is the same whether or not the rest of the sentence exists | 11 |
| **Check** | Anything that verifies the output before it is used, from a required shape through to a second model's opinion | 2 |
| **Chunk** | One piece of a split document: the unit that is embedded, stored in the index and returned by retrieval | 27 |
| **Chunk size** | How much text a chunk holds. A floor on it is set by taking the *shortest* passage that answers each of your questions and keeping the longest of those | 27 |
| **Citation** | A pointer from something a reply says to the text it came from. Checkable only if it carries a document id, a locator and the quoted span | 28 |
| **Claim-level check** | Decomposing an answer into its claims and giving each one a verdict against the retrieved passages. The verdicts are what tell you which sentence to fix | 32 |
| **Compaction** | Replacing the record of a run with a shorter one that keeps the facts later steps need. Chapter 18's summarise strategy applied to a loop, where nothing reading the record *while the run is still going* can notice an omission | 35 |
| **Compound system** | A system of several parts with the model as one of them, rather than as the whole product | 2 |
| **Compounding error** | Two things at once across a run: each step's chance of being right multiplies against the others, so a high per-step figure becomes a low whole-run one; and a wrong step's result is carried into the next step as though it were true | 4 |
| **Compute-bound** | A step whose speed is set by the arithmetic it has to do rather than by how fast its numbers arrive. Prefill is; a large enough batch becomes so | 15 |
| **Concept owner** | The single chapter that teaches a given concept. Every other chapter refers to it by number rather than re-teaching it, so the reader never meets three partial explanations of one thing | 7 |
| **Confidence interval** | The range a measurement would fall in most of the time if you repeated it. Here, the 2.5th to 97.5th percentiles of the resampled scores | 20 |
| **Constrained decoding** | Restricting each token choice to what the format allows, by editing the scores before the pick. The model is unchanged | 22 |
| **Content stream** | A PDF page's list of drawing instructions, each placing a string at a position. Its order is the order the marks were made, not a reading order | 27 |
| **Context** | Everything sent to the model on one call: the instructions, any added material, and the request | 2 |
| **Context assembly** | Turning retrieved passages, an instruction and a question into the request the model is given — spread across Chapter 18's message list, and counting against one window | 28 |
| **Context budget** | How much of the window is left for passages once the instruction and the question are counted. Not the same number as Chapter 26's candidate set, and set by a different thing | 28 |
| **Context engineering** | Deciding what occupies the context at each step of a run. Distinct from writing a prompt (Chapter 18), because a prompt is written once and a run's context is rebuilt every step, mostly out of material you did not write | 35 |
| **Context window** | The maximum number of tokens a model will accept at once. A cost limit rather than a memory, counting the reply as well as the request. The whole conversation is re-sent every call, and something is dropped — or the call refused — when it fills | 16 |
| **Cosine similarity** | The dot product divided by both lengths, which removes magnitude and keeps direction. Always between −1 and 1 | 8 |
| **Coupled task** | One whose pieces each need the one before, so the chain is the whole task. Given several agents it pays for all of them and finishes no sooner | 37 |
| **Criteria drift** | Your own standard moving as you see more output, measured by re-labelling old outputs blind and counting the flips | 33 |
| **Critical path** | The longest chain of pieces that must happen in order. The shortest a task can take however many agents you have, so pieces divided by it is the most parallelism the work contains | 37 |
| **Cross-encoder** | Query and document passed through one model together, giving one score for the ordered pair. Not precomputable; free to be asymmetric | 26 |
| **Cross-entropy** | The training objective: the average of `\(-\log p\)`{=latex} over every position, where `\(p\)`{=latex} is the probability given to the token that actually came next. Zero for a perfect prediction, unbounded for a confident mistake | 14 |
| **Current convention** | How competent engineers work at the moment: true, load-bearing and replaceable. It usually names a technique rather than a reason, and usually has a predecessor you can remember | 6 |
| **Dated detail** | A fact with a date on it — a name, a number, a version. It stops being true when somebody ships something or changes a price | 6 |
| **Dead state** | A grammar state with no legal token. It does not raise — the mask stops meaning anything and the decoder emits whatever was first | 22 |
| **Decode** | One forward pass per output token. Does almost no arithmetic and is limited by reading every parameter the pass uses out of memory once per token | 15 |
| **Delta** | One streamed piece: what to add to what you have, not the whole answer again | 19 |
| **Dense retrieval** | Embedding every document once, embedding the query at search time with the *same* model, and ranking by cosine | 24 |
| **Depth** | The number of layers in the stack. The last of the three numbers — vocabulary, width, depth — that describe most of a model's shape | 9 |
| **Dimension** | One slot in a vector. A position in a list, not a direction in space, and usually not nameable on its own | 8 |
| **Direct preference optimisation (DPO)** | The preference objective written as one formula: raise the preferred reply's probability relative to the rejected one, both measured against the model as it was before this stage. Stated in this book, not derived | 14 |
| **Discounted cumulative gain** | The sum of each result's grade divided by a discount that grows with position | 26 |
| **Dispatcher** | The code that takes a proposal, validates it, decides, and runs the function or refuses. The only participant that can refuse | 23 |
| **Document frequency** | How many documents in the collection contain a term at all | 26 |
| **Document length** | How many terms a document holds, compared with the collection average. BM25's third input, and the reason a long document is not automatically more relevant | 26 |
| **Dot product** | Multiply two vectors slot by slot and add the results. Large when both are large in the same slots — and also larger when either is simply longer | 8 |
| **Elicitation** | The one thing a client offers a server: a way for the server to ask the user for something it needs. The only client feature the 2026-07-28 revision lists, now that roots and sampling are deprecated | 36 |
| **Embedding** | The vector an embedding model returns for a given text. Its width is the model's, and it is the same for a word, a sentence and a page | 24 |
| **Embedding model** | A model whose whole job is to turn one piece of text into one vector of fixed width. No output tokens, nothing to continue | 24 |
| **Embedding table** | A matrix with one row per vocabulary entry. Looking a token up in it is how that token enters the model; the rows are called embeddings | 9 |
| **Error analysis** | The part of evaluation that means reading real outputs, sorting the failures into kinds, and working on the largest kind | 5 |
| **Evaluation** | Building and using something that tells you whether a system works: a set of cases, a way to judge each answer, and a number you can compare over time | 5 |
| **Evaluator–optimiser** | Produce, judge, revise, until the judge passes or your code gives up. Fixed in shape, not in length | 34 |
| **Evidence strength** | How much a claim is supported: announcement, demonstration, one study, practitioner report, settled practice — or a derivation, which stands outside the ladder because you can check it yourself | 6 |
| **Examples** | What a good answer looks like, shown rather than described. Part of the specification | 18 |
| **Exhaustive search** | Comparing the query against every vector. Exact, and linear in the size of the collection | 29 |
| **Exponential backoff** | Doubling the wait after each failed attempt, up to a cap, so a struggling system is not hammered | 19 |
| **Failure mode** | A named kind of wrong output, named after what went wrong rather than after the part of the system suspected of causing it | 30 |
| **Faithfulness** | The same property under the name an interviewer may use: the answer is faithful to the passages it was given | 32 |
| **Feed-forward block** | The half of a layer that works on each position alone: two matrices with an activation between them, the middle between about two and a half and four times the width of the ends. Holds more of a layer's parameters than attention does | 12 |
| **Few-shot** | A prompt that carries examples of a good answer. The *shot* is an example, so the word counts them and says nothing else | 18 |
| **Final state** | What the world looks like when the run ends. The cheapest thing to grade and the easiest to pass for the wrong reason, which is why it is a claim about the *starting* state too | 38 |
| **Finish reason** | The response's own statement of why generation stopped. What distinguishes a truncated reply from a malformed one | 21 |
| **Fixed path** | A design in which the sequence lives in your code: your code runs every step, whatever selected it, and the order is written down rather than decided as the run goes. Five shapes: chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser | 34 |
| **Forward pass** | One journey through the model — lookup, the stack once, one distribution out. It produces exactly one distribution | 9 |
| **Foundation model** | A model trained once on general material, then used for many tasks it was not specifically built for | 1 |
| **Function calling** | The provider's name for the whole five-step convention, also sold as tool calling. The model does step 2 of it and nothing else | 23 |
| **Generalisation theory** | Why a model fitted to one body of text works on text it never saw — the bias–variance trade-off, and what learning theory proves about it | 17 |
| **Graded relevance** | A relevance judgement on a small scale rather than yes-or-no, so a partial answer and a full one can be told apart | 26 |
| **Grader** | What decides whether one trial succeeded. Code, then a judge, then a person — in that order, because the order is the cost | 38 |
| **Gradient** | For each parameter, how much the loss would rise if that parameter rose. The update rule moves every parameter a small step against it. How it is computed is outside this book | 14 |
| **Greedy decoding** | Always taking the highest-scoring token. What "temperature zero" does in practice, since dividing by zero is not defined | 13 |
| **Greedy fill** | Keeping any passage that fits in the room remaining. Silently promotes short passages over higher-ranked long ones | 28 |
| **Grounded** | Every claim the answer makes is supported by a passage that was retrieved. Says nothing about whether the passages were right or the answer useful | 32 |
| **Hallucination** | Output that is fluent, plausible and not true. Not a malfunction: no step in the computation checks anything, so a plausible continuation is all the mechanism can produce | 16 |
| **Hybrid retrieval** | Running lexical and dense retrieval and combining their rankings | 26 |
| **Idempotency** | Doing an operation twice has the same effect as doing it once. What makes a retry after a timeout safe | 19 |
| **Inductive bias** | What a design assumes about the world before it sees any data | 17 |
| **Inference** | Running a finished model to get a reply. This is what "using a model" means | 1 |
| **Initialisation** | What the parameters are set to before training begins, and why the choice matters | 17 |
| **Input tokens** | Everything you send on a call — instructions, attached material and the request. Countable exactly before you send | 10 |
| **Instructions** | What to do, what not to do and who to be. Part of the specification, so it changes rarely and is paid for on every call | 18 |
| **Inter-agent misalignment** | One agent's output not being what the next one needed. The middle of the three failure categories, and Chapter 35's summary problem with no shared context to catch it | 37 |
| **Intermediate reasoning (chain-of-thought)** | Emitting the steps of a problem as tokens so that later passes can condition on them. The only way to carry partial work forward, because one pass runs its layers once however hard the question is, and nothing persists between passes | 16 |
| **Interview depth** | Knowing something well enough to give the mechanism, the trade-off, and how you would check it, in about a minute of speech. Not exhaustive, and more than a summary | 7 |
| **Inverse document frequency** | A weight that rises as a term gets rarer, so a term almost every document holds barely moves a score | 26 |
| **Irreversible action** | Something a tool does that cannot be undone once it has happened — a refund, a message, a deletion. The reason a tool's reach is decided before it is offered | 3 |
| **Jitter** | Waiting a random amount up to the backoff rather than exactly it, so many workers do not retry in step | 19 |
| **Judge (LLM-as-a-judge)** | A model asked to return a verdict on one named thing about one output. Pass or fail on a named failure mode, never a score out of five. The field's name is used wherever a model scores output, whatever it returns, so it is wider than this chapter's version | 31 |
| **Just-in-time retrieval** | Opening a document when a step needs it rather than loading the library before the run starts. Needs a catalogue of what exists — one line a document, not one of Chapter 29's indexes; beats loading up front unless a task reads nearly all of it | 35 |
| **Kappa** | An agreement coefficient running to 1.0, used to say how far two labellers agree. Not a correctness figure: the study's 0.88 is three people agreeing with each other, and its 0.77 is a model agreeing with those people | 37 |
| **Key** | The vector saying what a position offers to others, made with `\(W_K\)`{=latex}. Scored against every query | 11 |
| **Key–value cache (KV cache)** | The stored keys and values for every position in every layer, so decode attends to earlier positions without recomputing them. Costs `\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} | 15 |
| **Large language model (LLM)** | The field's full name for the kind of model this book means by *model*: text in, generated text out. Shortened to LLM almost everywhere it is used | 1 |
| **Lasting principle** | A reason for doing something, or a shape that does not move, which outlives the technique it was first attached to. It stops being true only if the reason itself is wrong | 6 |
| **Latency** | The delay between sending a request and receiving the reply, felt as a wait before the first word and a pace after it | 1 |
| **Layer** | A block of arithmetic taking one vector per position and returning one per position, same width in as out. Every layer has the same shape and its own numbers | 9 |
| **Layout analysis** | Inferring a page's structure — columns, tables, headings — from where its marks sit. Always approximate; the chapter's version turns on one threshold fitted to one page | 27 |
| **Length** | What a ruler would measure if the slots were coordinates: square every slot, add them, take the square root | 8 |
| **Lexical retrieval** | Scoring a document by the query terms it contains. Not a filter: every document gets a number and the list is sorted | 26 |
| **Logarithm** | The inverse of raising `\(e\)`{=latex} to a power. It turns multiplication into addition, which is why it appears wherever many probabilities are combined | 8 |
| **Logits** | The raw scores from the final matrix multiplication, one per vocabulary entry, before softmax. Can be negative; only the differences between them matter | 13 |
| **Long context** | A large maximum input. Buys a looser budget and whole documents; does not remove the need to select, and is not free | 28 |
| **Lost in the middle** | The field's name for a measured effect: one relevant passage in a long input is used less reliably in the middle than near either end. A finding about particular models, not a rule of the design | 16 |
| **Masked mass** | How much probability the constraint deleted at a step. Small means the constraint was free; large means it overruled the model | 22 |
| **Masking** | Setting a forbidden token's score to `\(-\infty\)`{=latex}, which makes its probability exactly zero after the softmax — as long as one token survives. Mask them all and you get `nan`, not zero | 22 |
| **Matrix** | A grid of numbers, read as rows or as columns depending on what you are doing | 8 |
| **MCP client** | The connector inside the host, one per server, so "a client per connection" and "a client per server" are the same sentence. It is what makes the calls; the model never sees it | 36 |
| **MCP host** | The application holding the model. It opens the connections, holds one client per server, and is where consent for a tool call lives | 36 |
| **MCP server** | A service offering tools, resources and prompts to a client. Its tool descriptions are input to your prompt, so they are untrusted unless you run the server | 36 |
| **Mean reciprocal rank** | The average of the reciprocal rank over a set of queries | 26 |
| **Memory-bound** | A step whose speed is set by how fast numbers arrive from memory rather than by the arithmetic done with them. At two bytes per parameter, decode does about one operation for every byte it reads, on hardware built for hundreds | 15 |
| **Merge list** | The merges, in the order they were made. Kept with the model and replayed in that order to tokenise any later text | 10 |
| **Metadata filter** | Restricting a search to documents with some property — an owner, a date, a department | 29 |
| **Mixture of experts (MoE)** | Replacing one feed-forward block per layer with several and routing each token through a few of them. The model holds all of them and runs some | 15 |
| **Model** | A service that takes text and returns generated text, charged by the amount of text | 1 |
| **Model Context Protocol (MCP)** | A documented wire format between an application holding a model and a service offering tools, resources and prompts. Collapses per-integration glue. Adds no step to Chapter 23's five and moves no decision; step 4 becomes a call into another process. The model is not a participant | 36 |
| **Multi-agent system** | A design in which several agents run on one task, each with its own context and stopping condition, coordinated by your code or by one of them. Chapter 4 owns the agent and Chapter 35 the sub-agent; this is the arrangement of several | 37 |
| **Multi-head attention (MHA)** | Several attention heads run in parallel over slices of the width, their outputs joined by one further matrix. What this chapter's one head is a simplification of. Chapter 15's Note is what real systems do to the keys and values from here | 11 |
| **Multi-tenant retrieval** | Retrieval where each user may see only their own documents, so the filter is a correctness requirement rather than an optimisation | 29 |
| **Must-keep list** | The facts the rest of the task depends on, named before the summary is written and checked against it after. Written afterwards it is written from the summary and tests nothing | 35 |
| **Namespaced name** | A tool name carrying its area before its verb, as in `orders.look_up`. The one part of a tool that appears again in every proposal and every result, and the cheapest edit available: renaming touches the registry key and nothing inside the function | 36 |
| **Neighbour expansion** | Fetching the rows adjacent to a retrieved row in the original document and supplying them together. Needs some recorded locator — an offset, or an ordinal in the id; costs budget; does not know what is relevant | 28 |
| **Next-token distribution** | One probability for every entry in the vocabulary, adding to 1, saying how likely each is to come next. The entire output of one call | 9 |
| **Normalisation** | Rescaling the stream to a predictable range before each block reads it, so the numbers do not grow out of hand as layer after layer adds to them | 12 |
| **Normalised discounted cumulative gain** | A DCG divided by the DCG of the best possible ranking of the same documents, making it comparable across queries | 26 |
| **Numerical stability** | How quantities behave through long chains of arithmetic, and what keeps them in a usable range. The subject behind Chapter 12's one sentence on normalisation. Not taught in this book | 17 |
| **Objective design** | Why one expression rather than another is the right thing for a model to minimise. The question Chapter 14 states its preference objective without answering. Not taught in this book | 17 |
| **OCR** | Recognising characters in an image, for pages that have no text layer at all. Imperfect, and a separate step before parsing can begin | 27 |
| **Optimisation theory** | The study of when a procedure like the update rule converges, to what, and how fast. Not taught in this book | 17 |
| **Optimiser design** | Choosing and adapting the step size and the form of the update. Not taught in this book | 17 |
| **Orchestrator–workers** | Parallelisation where a model decides what the pieces are, so the call count is settled at run time | 34 |
| **Output format** | The shape the answer must take, stated rather than hoped for. Part of the specification | 18 |
| **Output tokens** | Everything that comes back. Priced several times higher than input, one forward pass each, and not knowable in advance | 10 |
| **Overlap** | Starting each chunk a little before the last one ended, so a passage cut by one boundary survives whole in a neighbour. Costs storage and returns near-duplicates | 27 |
| **Page furniture** | Headers, footers, page numbers and watermarks: text on the page that is not part of the document | 27 |
| **Paired comparison** | Running both versions on the same cases and keeping the results together, so the part of case-to-case variation the two versions share cancels when you subtract | 20 |
| **Parallel width** | The most pieces that can be in flight at once, and therefore the number of agents that earn their place. Chapter 9's *width* is a different thing — the size of a model's vectors | 37 |
| **Parallelisation** | One call per piece, the pieces coming from the input, then one call to combine. Independent, so they can run at once | 34 |
| **Parameter** | One number inside the model, set by training and unchanged by inference. The count is what "a 7B model" reports | 9 |
| **Parsing** | Turning a file into text a program can work on. For a document format this means reconstructing something the file does not record | 27 |
| **Partition** | Every failure in exactly one mode, nothing dropped and nothing counted twice. Checkable, and worth checking | 30 |
| **pass@k** | The chance at least one of *k* trials succeeds, `\(1-(1-p)^k\)`{=latex}. Rises with *k*. Only a capability when something can tell a good attempt from a bad one | 38 |
| **pass\^k** | The chance all *k* trials succeed, `\(p^k\)`{=latex}. Falls with *k*, and it is the one to worry about | 38 |
| **People** | The reviewers and approvers who handle the consequential cases and carry responsibility for them | 2 |
| **Perplexity** | The exponential of the cross-entropy. Reads as the number of equally likely options the model is effectively choosing between; a uniform choice among `\(V\)`{=latex} options has perplexity `\(V\)`{=latex} | 14 |
| **Position bias** | A judge preferring an answer for where it was printed rather than for what it says. Measured by showing each pair both ways and counting the flips | 31 |
| **Positional encoding** | How a token's position is put into the arithmetic, since the attention formula carries no notion of order. Added to the embedding before the stack, or applied as a rotation to queries and keys, or added to the scores themselves | 11 |
| **Post-filtering** | Searching everything, then discarding what the user may not see. Returns about `f × s` of a tenant's documents from a fetch of `f` at share `s` | 29 |
| **Practitioner report** | A survey or a set of accounts of what people say they do. It is a practitioner report however it was published, and it supports what people *do* far better than whether it works | 6 |
| **Pre-filtering** | Restricting the pool before searching. Exact when the restricted pool is then scanned exhaustively; an index that restricts as it walks is also pre-filtering and is not exact | 29 |
| **Preference optimisation** | Training on pairs of replies with a preference between them, to make the preferred kind more likely relative to the other. Changes which of its existing behaviours come out; nothing in its objective rewards adding knowledge | 14 |
| **Prefill** | The pass that processes the whole prompt, every position at once. Limited by arithmetic, whose attention part grows with the square of the prompt length and overtakes the rest on a long one. What you wait for before the first word | 15 |
| **Pretraining** | Running the loop on an enormous quantity of general text. Where essentially all of a model's knowledge comes from, and nearly all of the computation | 14 |
| **Probe** | One group the index looks inside at query time. More probes always mean more work, and never less recall — but once recall is exact, further probes buy nothing | 29 |
| **Prompt chaining** | Stages in sequence, each call's output the next one's input. Used when the work has nameable stages that are easier asked separately | 34 |
| **Prompt template** | A templated message or workflow an MCP server offers to users. Not a tool, and not something the model selects | 36 |
| **Proposal** | What the model emits — tokens your code reads as a request to run something. Nothing has happened yet | 23 |
| **Provenance** | A note's two extra fields: where it came from — read, inferred or told — and when it was written. They do not make a note true; they say which notes expire and which were never checked | 35 |
| **Purposeful tool** | A tool written for a task somebody asks for rather than for an endpoint that exists. Does the joining your code would have done, and costs less in total than the endpoints it replaces even though its description is longer | 36 |
| **Quantisation** | Storing each parameter in fewer bits. Halving the bits halves the memory and roughly halves the time spent reading, at a cost in precision that has to be measured | 15 |
| **Query** | The vector saying what a position is looking for, made by multiplying its vector by `\(W_Q\)`{=latex} | 11 |
| **Reading order** | The order a person reads a page in. A human fact about a layout, and not something a page description like PDF records — some formats do store an order, which is why the problem is format-specific | 27 |
| **Recall@k** | The fraction of all relevant documents appearing in the top k. Blind to their order | 26 |
| **Reciprocal rank** | One divided by the position of the first relevant result, for a single query | 26 |
| **Reciprocal rank fusion** | Combining rankings by summing one over a constant plus each rank, using positions only and never the scores | 26 |
| **Registry** | The map from a name to a function your code is willing to run. The lookup that refuses a name the model invented | 23 |
| **Regression** | A case that passed before the change and fails after it — established over repeated runs, not from one | 33 |
| **Regression set** | The cases you run on every change. Past failures are the minimum and cannot catch a case that has never failed, so it carries passing cases too | 33 |
| **Regularisation** | The techniques that stop a model fitting its training data too closely | 17 |
| **Relevance** | Whether this document answers that question, for this asker. A directed judgement, not a distance | 25 |
| **Relevance judgement** | One recorded decision that a given document does or does not answer a given query. The unit an answer key is made of | 25 |
| **Repair** | Editing a reply so it parses, restricted to things that were never part of the data: a code fence, text outside the braces, a comma JSON disallows | 21 |
| **Representation learning** | Why fitting a model to predict text arranges its vectors so that the arrangement is useful for other things. The question Chapter 9 refused. Not taught in this book | 17 |
| **Reranker** | The model that does the rescoring in the second stage — in current practice usually a cross-encoder | 26 |
| **Reranking** | Rescoring a small candidate set with a more expensive method than the one that produced it | 26 |
| **Residual connection** | Adding a block's output to the vector that went into it, rather than replacing it. What lets a layer contribute nothing and pass its input through | 12 |
| **Residual stream** | The running vector passing up through the stack, which every block adds into. By the end it is a sum of every contribution made along the way, with nothing marking which is which | 12 |
| **Resource** | Context and data an MCP server offers for the user or the model to use, as against a function for the model to execute | 36 |
| **Retrieval** | Searching your own collection for the passages that bear on a request, so they can be put into the context | 2 |
| **Retrieval-augmented generation (RAG)** | The arrangement where your code searches your own material, puts what it found into the context, and the model answers out of that. Names the whole arrangement rather than any one part of it | 2 |
| **Routing** | One call picks a branch from a menu your code wrote; your code runs the branch. The model sees the labels and never the code behind them. Chapter 52's routing is a different thing — choosing between models for one request | 34 |
| **Rubber-stamping** | Approval given without real attention, usually because the volume is too high for any. It costs what review costs and delivers none of its value | 3 |
| **Rule of three** | With no failures in `\(n\)`{=latex} tries, the rate can still be about `\(3/n\)`{=latex}. What to use when a bootstrap has no failure to resample | 21 |
| **Scaling laws** | The relationships between model size, data, compute and loss, and their derivation | 17 |
| **Schema** | The list of claims your code makes about a reply — fields, types, allowed values, ranges — and enforces on every one. A contract you check, not a request you hope was honoured | 21 |
| **Self-agreement** | How often a judge gives the same verdict on the same answer shown twice. Every point of flipping is a point any other figure could have landed elsewhere, and measuring it needs no labels | 31 |
| **Semantic search** | What dense retrieval is usually called. The same thing, in the words people use when they complain about it | 25 |
| **Semaphore** | A counter that bounds how many jobs run at once. Three words of code, and the difference between concurrency and attacking your own account | 19 |
| **Server-sent events** | A long-lived HTTP response carrying one small event per line as the server produces them. How a streamed reply arrives | 19 |
| **Softmax** | Turns a list of scores into positive numbers that sum to 1, preserving their order and turning each gap between scores into a multiple between shares | 8 |
| **State machine** | What a schema compiles into: a set of states, each with the tokens allowed next. Engines call it an automaton | 22 |
| **Step** | One pass through the loop: the model decides, something runs, the result comes back | 4 |
| **Stop condition** | A string you nominate that halts generation when it appears. Providers call it a stop sequence; it is not Chapter 4's stopping condition. One of the ordinary ways a reply ends, alongside the model's own stop token and your maximum | 13 |
| **Stop token** | An entry in the vocabulary meaning *finished*, scored and sampled like any other token. Often called an end-of-sequence token. A model stops talking by predicting that it has stopped | 13 |
| **Stopping condition** | The set of rules that end a run — the model finishing, a step limit, or your code refusing | 4 |
| **Strict mode (JSON mode, structured outputs)** | A provider's facility for enforcing a schema during generation, as against asking for it in the prompt. Providers use all three names and they do not all promise the same thing — one may undertake only that the reply parses | 22 |
| **Structured note** | A fact the agent writes outside the context window as a key and a value, and reads back later. Model output, so it is untrusted input however plainly it is phrased | 35 |
| **Sub-agent** | A nested run with its own context and stopping condition, returning only its answer. Keeps what it read out of the parent's context, and cannot be consulted once it has returned | 35 |
| **Subword** | A token that is part of a word rather than a whole one. What makes it possible to represent a word the vocabulary has never seen | 10 |
| **Supervised fine-tuning (SFT)** | Running the same loop with the same objective on curated request–response pairs. Turns a model that continues text into one that answers | 14 |
| **Supplied information** | The part of a prompt that is different on every call. The only one of the four parts that is data rather than specification | 18 |
| **System message** | The message holding your instructions and usually the output format. Your specification, set once per conversation and never the thing to drop when the history will not fit — nor are the example turns, if that is where your examples live | 18 |
| **Task** | An agent's unit, as a case is a single call's: a starting state, a goal, and a condition that can be checked when the run ends. If you cannot write the condition you do not have one | 38 |
| **Temperature** | A number the logits are divided by before softmax. Below 1 sharpens the distribution, above 1 flattens it, and it never changes the order | 13 |
| **Term** | The unit a lexical index counts — usually a lower-cased word, sometimes stemmed. Not the model's token from chapter 10 | 26 |
| **Term frequency** | How often a term appears in one document | 26 |
| **Token** | One entry in a model's vocabulary — usually a piece text is cut into. Beyond the single bytes, which are always there, which pieces earned an entry is a matter of frequency in the corpus the vocabulary was built from — not of meaning or length | 10 |
| **Token bucket** | A limiter on the *rate* rather than on how many run at once, for when the requests-per-minute limit is the one that hurts | 19 |
| **Token multiplication** | What several agents cost when they *duplicate* the work rather than divide it, which is simply their number: six agents each doing the whole task cost 6.03 times one. Dividing the work costs less than one agent, because the re-send cost falls with the length of a run. Neither the instruction block nor the shared material rises with the number of agents while the work is divided | 37 |
| **Tokeniser** | The program that cuts text into tokens and maps them to indexes, using one model's vocabulary and merge list. A count does not carry from one model's tokeniser to another's | 10 |
| **Tool** | An action the model may ask for. The model proposes it; your code decides whether to run it | 2 |
| **Tool defect** | A failure the tool or its description could have prevented. Distinct from a refusal your code made correctly, which is the system working, and from a service being down, which is Chapter 19's. Rank tools by this, not by failure rate | 36 |
| **Tool description** | The text your code sends about one function: a name, a sentence and the parameter names and types. Not the function, and not your constraints | 23 |
| **Tool message** | A result your code returns after the model asked for something. Chapter 23 | 18 |
| **Top-k** | Keeping only the `\(k\)`{=latex} highest-scoring tokens and renormalising. Keeps the same number of options however confident the model is | 13 |
| **Top-p** | Also called nucleus sampling. Keeping the smallest set of tokens whose probabilities add to at least `\(p\)`{=latex}, then renormalising. Narrow where the model is confident, wide where it is not, at the cost of not knowing in advance how many survive | 13 |
| **Total timeout** | The cap on a whole call, as distinct from the gap between chunks that most libraries call the read timeout. Derived from the token cap | 19 |
| **Trace** | The record of one request: input, retrieval and its candidates, model and version, tool calls, output, tokens and per-stage timings | 33 |
| **Training** | The one-time process that produced the model's numbers. Not something you do on a request | 1 |
| **Training cut-off** | The point in time after which no text reached the model's training. It knows nothing later, and cannot tell that it does not | 1 |
| **Transcript** | The ordered record of one trial's steps — what the model asked for, what ran, what came back. Not Chapter 33's trace, which is the per-request production record that holds one | 38 |
| **Transformer** | A stack of identical layers, each adding an attention block's output and a feed-forward block's output into the residual stream. *Decoder-only* adds that every position may look only backwards | 12 |
| **Trials** | Repeated runs of the same case, which measure the model's own variation. Averaged within the case, never counted as extra cases | 20 |
| **Turn** | One exchange — the user's message and the model's reply to it. A conversation is a list of turns, and the whole list is re-sent on each one | 18 |
| **Two-tower** | A bi-encoder with separate query and document encoders, so the score is `\(\cos(f(q), g(d))\)`{=latex} with `\(f \neq g\)`{=latex}: still precomputable, no longer symmetric | 26 |
| **User message** | The request and the material it is about, from the person or from your code on their behalf | 18 |
| **Validation layers** | Parses / right shape / values possible / values true. The first three are mechanical; the fourth needs a judgement and belongs elsewhere | 21 |
| **Value** | The vector a position hands over when it is attended to, made with `\(W_V\)`{=latex}. What the weights are spent on | 11 |
| **Vector** | An ordered list of numbers. Two vectors can be compared only if they have the same number of slots | 8 |
| **Vector database** | A product that wraps an index like this one and serves it over a network, also called a vector store. The index is the data structure; the database is a deployment choice around it | 29 |
| **Vocabulary** | The fixed, numbered list of every entry a model can read or produce — nearly all pieces of text, and a few that are not. Built once, before training, and fixed while you use the model | 9 |
| **Width** | The number of slots in the vectors moving from layer to layer, the same all the way through. Written `\(d\)`{=latex} in formulas | 9 |
| **Zero-shot** | A prompt that carries no examples: instructions, output format and the request only | 18 |
