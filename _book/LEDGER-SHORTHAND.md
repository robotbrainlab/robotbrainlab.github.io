# What an interviewer calls it

The book teaches a concept under its formal name. An interview asks for it by its shorthand.
Both have to be in the book, or a reader searching for the word they will actually hear finds
nothing — which is what happened: "RAG" appeared in no chapter, no glossary row and no bank
question, while the thing itself ran across chapters 2 and 24 to 29 and 32.

**The rule.** The chapter that *owns* a concept names the field's word for it once, where it
explains the formal name, in the shape chapter 14 uses for DPO: a sentence in the body, and the
shorthand carried in the Key Terms row's term. Every later chapter may then use the shorthand
and must not re-explain it. A chapter must never use a shorthand earlier than the chapter that
names it — `tools/verify-inputs.py` is the gate on that, and it reads the Key Terms table.

**Where a shorthand is only a spoken name for a practice, or names something wider than the
chapter builds, it is named in the body and left out of the Key Terms table.** That is marked
*body* below. The index entry still exists, because a bold span of four words or fewer is
indexed automatically.

## Named

| Shorthand | What the book calls it | Home | State |
|---|---|---|---|
| LLM, large language model | *model* | 1 | Named. Key Terms row added |
| RAG, retrieval-augmented generation | retrieval, taken as the whole arrangement | 2 | Named. Key Terms row added |
| agentic | agent | 4 | Named, *body*. An adjective about degree, not a thing |
| BPE | byte-pair encoding | 10 | Named. Row extended |
| self-attention | attention | 11 | Named. Row extended |
| MHA, multi-head attention | several attention heads | 11 | Named. Key Terms row added |
| transformer, decoder-only | the stack: attention block, feed-forward block, residual, normalisation | 12 | Named. Key Terms row added for *transformer*; *decoder-only* is *body* |
| SFT | supervised fine-tuning | 14 | Named. Row extended |
| RLHF | — | 14 | Was already named, in a Note, with no row of its own |
| KV cache | key–value cache | 15 | Named. Row extended |
| MoE | mixture of experts | 15 | Named. Row extended |
| TTFT, time to first token; time per token | why the first token is slow, and the pace after it | 15 | Named, *body*. Chapter 52 owns the two metrics in production and should carry their rows |
| CoT, chain-of-thought | intermediate reasoning | 16 | Named. Row extended |
| lost in the middle | long inputs are not used evenly | 16 | Named. Key Terms row added |
| prompt engineering | the prompt as a specification | 18 | Named, *body* |
| few-shot | examples | 18 | Named. Key Terms row added |
| zero-shot | a prompt with no examples | 18 | Named. Key Terms row added |
| evals | evaluation, and the evaluation set | 20 | Named, *body*. A plural noun for a practice spread over 20 and 30 to 33 |
| A/B test | paired comparison | 20 | Named, *body*, and **distinguished rather than equated**: an A/B test splits live traffic, which is not what chapter 20 does |
| JSON mode, structured outputs | strict mode | 22 | Named. Row extended, with the warning that the three names do not all promise the same thing |
| function calling, tool calling | the five steps of a tool call | 23 | Named. Key Terms row added |
| ANN | approximate nearest neighbour index | 29 | Was already named, in the Key Terms row |
| vector database, vector store | — | 29 | Named. Key Terms row added, and **kept apart** from the index: the index is a data structure, the database a product around it |
| LLM-as-a-judge | judge | 31 | Named. Row extended, noting the field's name is wider than the chapter's version |
| observability | trace, tracing | 33 | Named, *body* |
| top-k, top-p | — | 13 | Was already named |
| BM25, RRF, nDCG, MRR, recall@k | — | 26 | Already in the chapter. The Key Terms rows for reciprocal rank fusion, mean reciprocal rank and normalised discounted cumulative gain carry the long form only, so a reader scanning Appendix C for *nDCG* has to know the expansion. Worth extending; not done here |

## Waiting on a chapter that is not written

Name each one as its chapter lands, in the same shape.

| Shorthand | What it will be called | Home |
|---|---|---|
| MCP | the Model Context Protocol | 36 |
| multi-agent, orchestrator–workers | — | 37 |
| pass@k, pass^k | — | 38 |
| LoRA, PEFT, QLoRA, distillation | parameter-efficient fine-tuning | 39 |
| prompt injection, jailbreak, guardrails | — | 51 |
| prompt caching, prefix caching | prompt-prefix caching | 52 |
| speculative decoding, continuous batching, paged KV cache | — | 52 |
| re-embedding, index migration | — | 54 |

## Deliberately not adopted

Each of these was checked with a word-boundary grep and left out on purpose. Do not add them
without reopening the reason.

- **HNSW, IVF, product quantisation.** Chapter 29's own Note says the specific index structures
  are a current convention and tells the reader not to carry the parameter names anywhere.
  `ivf.py` is a lab filename, not a term.
- **MTEB and other benchmark names.** Chapter 24 treats a public score as a starting point, and
  a product name is the most perishable thing a chapter can hold.
- **In-context learning, ICL.** The book teaches examples as part of a specification, not as
  learning that happens at inference. Naming it would assert a mechanism no chapter gives.
- **p-value, statistical significance.** Chapter 20 uses the bootstrap precisely because it will
  not assume a distribution it cannot justify. Naming significance would import a test the
  chapter does not run.
- **Golden set, golden dataset.** The phrase is used both for an evaluation set (20, 32) and for
  a regression set (33). Naming it would have to pick one, and nothing needs it.
- **Hybrid search.** Chapter 26 says *hybrid retrieval*; the two differ by one ordinary word and
  any search for *hybrid* lands on it.
- **ReAct.** It is not one of chapter 34's five fixed-path patterns, and chapter 4's loop is not
  presented as it. Naming it would add a pattern the book does not teach.

## The abbreviations are in the index too

Each naming sentence follows chapter 14's DPO shape, so the formal name is bolded and the
abbreviation is not — which means the automatic index carried *retrieval-augmented generation*
and not *RAG*. A reader looking up the word they will actually hear found nothing, which is the
original complaint arriving in Appendix D instead of in a chapter.

Closed on 2026-10-29 with an empty index span beside each abbreviation, which prints nothing:

```
RAG[]{idx="RAG"}
```

Appendix D now carries ANN, BPE, CoT, DPO, KV cache, LLM, MHA, MoE, MRR, nDCG, RAG, RLHF, RRF,
SFT and TTFT, each pointing at the page where its chapter names it. **Any shorthand named from
here on needs the same span** — the Key Terms row and the bolded long form do not produce it.
