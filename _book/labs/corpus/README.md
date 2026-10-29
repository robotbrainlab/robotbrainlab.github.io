# The corpus the labs run on

Every lab in Part III runs on the files in this directory. `BOOK-GUIDE.md` §9 and chapter 7 both
promise the reader the same three things, and this is them: about forty short public-domain
documents, eight queries with a hand-made judgement of how well each document answers each one,
and one deliberately awkward PDF with a table and a scanned page.

## Where it came from, and why not from somewhere else

**These documents were written for this book and dedicated to the public domain** under CC0 1.0
(`LICENCE.txt`). That is a change of plan, recorded here because the reasoning matters more than
the decision.

The first plan was to assemble the corpus from existing public-domain text — Project Gutenberg, or
United States federal works, which are public domain by statute. Three things argued against it:

1. **The provenance claim would have been mine.** Putting forty fetched documents into a public
   repository means asserting, document by document, that each one is free of encumbrance. That is
   a claim about somebody else's rights, made on the owner's behalf, and a CC0 dedication of
   original text removes the question rather than answering it.
2. **The labs need planted properties, and found text supplies them by luck.** Chapter 43 needs a
   query where an exact string beats similarity. Chapter 27 needs an answer that straddles a chunk
   boundary. Chapter 32 needs two documents that disagree about a number. Chapter 50 needs a
   document it is safe to inject an instruction into. In found prose those are things you hope for;
   here they are designed, and the next section lists every one so no lab can claim to have
   discovered what was put there for it.
3. **Continuity.** Thirty-nine chapters use one running example — a retailer, its orders, its
   refund and delivery policies. A corpus in that domain means Part III continues Part II rather
   than starting again on unrelated material.

**"Public domain" is satisfied literally and not by redefinition.** A CC0 dedication places these
documents in the public domain; the reader may do anything with them. That is what chapter 7
promises and what this is.

## What was deliberately planted

Listed so that no lab reports as a finding something the corpus was built to contain. This is
`LEDGER-DEFECTS.md` entry 34's lesson applied to data rather than to a claim: when the author of
the evidence is also the author of the conclusion, the evidence has to be declared.

| Planted | Where | Which lab needs it |
|---|---|---|
| Identifiers that similarity cannot match — SKU codes, policy section numbers, a plan name | throughout | 43: one query where an exact string beats a dense ranking |
| An answer split across two documents, neither holding all of it | delivery-fees, delivery-exceptions | 27, 28: reassembly, and the retrieval ceiling |
| Two documents that disagree on a figure | refunds-policy, refunds-faq | 32: a claim no single passage supports |
| A near-duplicate pair differing in one clause | returns-standard, returns-clearance | 26, 44: fusion and reranking on near-ties |
| Page furniture repeated on every document of one set | the policy set | 27: what stripping furniture does to BM25 |
| One document far longer than the rest | warranty-full | 27: chunk size against document length |
| One document that answers no query at all | about-us | 26: recall's denominator, and a distractor |
| A document whose text invites an instruction | shipping-partners | 50: an injected instruction in retrieved context |
| A table that misparses into wrong figures, and a page with no text layer | awkward.pdf | 27, 45: parsing, and what a silent skip costs |

## The files

- `docs/` — the forty documents, one `.md` each, with a short YAML header giving an id and a title.
- `queries.tsv` — eight queries.
- `judgements.tsv` — one row per query and document, with a grade of 0, 1 or 2.
- `awkward.pdf` — two pages, and both are awkward on purpose. Its sources are beside it
  (`awkward.tex`, `awkward-page2-source.tex`, `awkward-page2.png`) so the file can be rebuilt
  rather than trusted.

### What is wrong with `awkward.pdf`, exactly

**Page 1 is a surcharge table drawn as three side-by-side blocks**, so the content stream emits
every cell of the first column before any cell of the second. It reads correctly on the page and
wrongly through `pdftotext`, and **the failure is not a reordering — it is a misalignment that
produces confident wrong answers.** From a real extraction:

```
Scottish Highlands and islands
Northern Ireland

AB36-38, IV, KW, PA20-9.50
80
6.50
```

The 9.50 has been spliced into the middle of a wrapped postcode range, and everything after it
has shifted up by one, so Northern Ireland lands against 6.50 only by luck and the Isle of Man
lands against 11.00 when the table says 11.00 belongs to it and 14.00 to the Scillies. A reader
of the page gets the right answer. A pipeline that parses this gets a wrong surcharge and no
error. That is chapter 27's subject and chapter 45's end-to-end case, and it is why the table is
built this way rather than as a `tabular`.

**Page 2 is an image of text with no text layer.** `pdftotext -f 2 -l 2` returns one character.
The page carries two facts that are nowhere else in the corpus — that the Northern Ireland
surcharge rose from 5.50 to 6.50, and that the Scillies moved carrier — so a pipeline that
silently skips the page loses information rather than merely losing a page, which is the honest
version of why a scan matters.

**The table's figures agree with `docs/delivery-exceptions.md` on purpose.** The PDF is a third
source for query 3, so a lab can ask whether its answer came from the document, the PDF, or a
misparse of the PDF — and the three are distinguishable.
- `LICENCE.txt` — the CC0 dedication.

## How the judgements were made

By hand, by one person, in one sitting, against a written rule — which is the weakest part of any
retrieval evaluation and is the part chapters 25 and 26 are most careful about. The rule:

- **2** — this document answers the query on its own. A reader with only this document is done.
- **1** — this document bears on the query and does not answer it. It names the right policy
  without the figure, or holds half of a two-part answer.
- **0** — nothing in this document helps.

Two consequences the labs rely on and should say out loud. **The grades are one person's**, so
chapter 31's question about a judge's self-agreement applies to this file too. And **recall
computed against this file is recall against this file**, not against the corpus — chapter 26 owns
that distinction and `judgements.tsv` cannot settle it.
