# Lab: The Pipeline End to End

Eleven chapters of Part II described a retrieval system a piece at a time, and five labs built
pieces of one. This chapter builds the whole thing on the corpus the book ships, traces one
request through every stage, and then measures the two halves apart until the numbers say where
to work. It is the longest lab in the book, because a pipeline you were shown in parts is not a
pipeline you have built.

*The problem.* I want a system that answers questions about my own documents and shows where
each answer came from.

*The question.* When it gets an answer wrong, which stage was it, and what is the cheapest thing
that would have fixed it?

**What this lab does not do.** It teaches no measure and no failure mode, and the only new piece
of arithmetic in it is one line of elementary probability in step 3. Chapter 26
owns the retrieval measures, Chapter 20 the interval, Chapter 28 the citation checks, Chapter 32
the two-verdict scoring, Chapter 33 the trace, and Chapters 52 and 53 latency and cost. This
chapter runs all of them against one system and records a baseline. It also does not compute a
groundedness figure: that is Chapter 32's claim-level check, and the citation checks in step 6
are the cheaper thing this pipeline has instead.

**What you need.** Python 3 and one package, in a virtual environment in a new empty folder:

```text
  python3 -m venv .venv
  .venv/bin/pip install pypdf==6.1.3
```

Then copy the book's `labs/corpus` directory into that folder, and `key.py` from Chapter 44
unchanged — it reads the eight queries and the graded key and nothing in this chapter needs it
any different. Set `OPENAI_API_KEY` in your environment. Eight programs, run in order, and each
one imports only from the ones before it:

| Save as | What it does | Imports |
|---|---|---|
| `parse.py` | turns the awkward PDF into text | nothing |
| `index.py` | strips, chunks, and stores a locator per chunk | `parse` |
| `search.py` | BM25, dense and fused retrieval, and the measures | `index`, `key` |
| `rerank.py` | one model scoring a query and a chunk together | `search`, `key` |
| `answer.py` | assembles a context, asks, writes a trace | `index`, `search`, `key` |
| `check.py` | the three citation checks | `answer`, `index`, `search` |
| `score.py` | two verdicts per case, and the four cells | `answer`, `index`, `search` |
| `trace.py` | cost and time off the traces | `answer` |

A cold run makes 153 requests — 113 to the chat model, of which 105 are step 4's reranking, and
40 to the embeddings model, two of them batches holding all 176 chunks and all 41 documents.
Well under a dollar at a small model's price. Both sets of vectors and all the reranking scores
are cached to files, so a second run of anything is free and the figures do not move under you.

> **Note:** Every figure below is one run on one day, against a hosted model pinned to a dated
> snapshot. **The counts that do not depend on a reply will match** — 176 chunks, nine stubs, a
> 258-character instruction and the locator arithmetic. The ranks and the room left are not on
> that list: a rank comes from a query embedding, which is a model call, and the room left is
> downstream of which passages the ranks let in. The counts
> derived from replies will not, and neither will the timings or the model's own words. Chapter 40 established that twenty identical calls at temperature zero can return two
> different answers, and this chapter met that again — step 4's reranker gave one query a
> different set of scores on a second run, which moved that query's figure by 0.14 and the mean
> by 0.02. The cache is there so that a figure quoted in prose stays attached to the run that
> produced it.

## Step 1: Parse the PDF, and Read What Came Out

Chapter 27's method has a step before every other one: parse, then read the output, for documents
you know, against the pages. Here it is on the file the book ships. Chapter 27 wrote its own
extractor out of a regular expression to show how little a page records, and its own lab step 9
is where that extractor met a second way of spelling the same instruction and found nothing at
all. This step uses a real library instead, which is what that step said to do.

**The corpus declares what was planted in this file**, and `labs/corpus/README.md` names this
chapter by number: a surcharge table drawn as three side-by-side blocks, and a second page that
is an image of text. Both are demonstrations, not discoveries. What was not planted is what this
particular parser does with them.

```python
"""The awkward PDF, parsed, and the output read before anything else.

Chapter 27's method has one step before every other: parse, then read
the output. This is that step on the file the book ships, with a real
library rather than the regex chapter 27 wrote to show how little a
page records.

    python3 -m venv .venv
    .venv/bin/pip install pypdf==6.1.3

The corpus README declares what was planted in this file: a table
drawn as three side-by-side blocks, and a second page with no text
layer. Both are demonstrations. What is NOT planted is what this
particular parser does with them, which is the reason for looking.
"""
import pathlib
import re

from pypdf import PdfReader

PDF = pathlib.Path("corpus/awkward.pdf")
DOCS = pathlib.Path("corpus/docs")
WIDTH = 58

# The table as a reader of the page sees it, typed off the page.
TRUE_ROWS = [
    ("Scottish Highlands", "AB36-38, IV, KW, PA20-80", "9.50"),
    ("Northern Ireland", "BT", "6.50"),
    ("Isle of Man, Channel Is.", "IM, GY, JE", "11.00"),
    ("Isles of Scilly", "TR21-25", "14.00"),
    ("Rest of the UK", "all others", "none"),
]


def pages():
    return [p.extract_text() for p in PdfReader(str(PDF)).pages]


def shown(line, width=WIDTH):
    """One extracted line, folded to fit a printed page. A folded line
    is marked, so a fold here is never read as a line break there."""
    out = []
    while len(line) > width:
        cut = line.rfind(" ", 0, width)
        cut = width if cut <= 0 else cut
        out.append("    " + line[:cut])
        line = "  >" + line[cut:].lstrip()
    out.append("    " + line)
    return out


def split_words(text):
    """A capital letter standing alone before a word is a kern pair
    the parser broke apart. Every place it happened."""
    return re.findall(r"\b([A-Z]) ([A-Za-z][A-Za-z0-9-]*)", text)


if __name__ == "__main__":
    ps = pages()
    print(f"  {PDF}: {len(ps)} pages")
    for n, text in enumerate(ps, 1):
        print(f"    page {n}: {len(text):4d} characters,"
              f" {len(text.split()):3d} words")

    print("\n  page 1, every line. A line starting > is this")
    print("  program folding a long one, not the parser:\n")
    for line in ps[0].split("\n"):
        for out in shown(line):
            print(out)

    print("\n  the same table, typed off the page by hand:\n")
    for area, codes, charge in TRUE_ROWS:
        print(f"    {area:24s} {codes:24s} {charge}")

    lines = [l for l in ps[0].split("\n") if l.strip()]
    first_area = next(i for i, l in enumerate(lines)
                      if l.startswith(TRUE_ROWS[0][0]))
    first_charge = lines.index(TRUE_ROWS[0][2])
    print(f"\n    'Area' is line {lines.index('Area') + 1},"
          f" the areas {first_area + 1} to {first_area + 5}")
    print(f"    'Surcharge' is line {lines.index('Surcharge') + 1},"
          f" the charges")
    print(f"    {first_charge + 1} to {first_charge + 5}:"
          f" {first_charge - first_area} lines from the first area")
    print("    to its own charge, and nothing joining them\n")

    broken = split_words(ps[0])
    for cap, rest in broken:
        print(f"    {cap!r} + {rest!r}   ->   {cap + rest!r}")
    print(f"    {len(broken)} places where a space is inside a word\n")

    doc = (DOCS / "delivery-exceptions.md").read_text()
    for name, text in (("the PDF text", ps[0]),
                       ("delivery-exceptions.md", doc)):
        print(f"    'PA20' in {name:24s} {'PA20' in text}")

    print(f"\n  page 2 returned {len(ps[1])} characters. Two facts")
    print("  are on it, and the PDF is the only place in the")
    print("  corpus that holds them:\n")
    for probe in ("5.50", "Dunmore"):
        where = [q.stem for q in sorted(DOCS.glob("*.md"))
                 if probe in q.read_text()]
        print(f"    {probe:8s} in {len(where)} of 40 documents"
              f"   {where}")
```

```text
  corpus/awkward.pdf: 2 pages
    page 1:  852 characters, 148 words
    page 2:    0 characters,   0 words

  page 1, every line. A line starting > is this
  program folding a long one, not the parser:

    Harbour Lane Retail Ltd
    Delivery surcharges — 2026 schedule
    The charges below are added to the standard, named-day or
      >next-day delivery charge for
    the areas listed. They are what our carriers charge us
      >for those routes and are passed on
    without a mark-up. Named-day and next-day services are
      >not available to any area in this
    table.
    Area
    Scottish Highlands and islands
    Northern Ireland
    Isle of Man and Channel Islands
    Isles of Scilly
    Rest of the United Kingdom
    Postcodes
    AB36–38, IV, KW, P A20–
    80
    BT
    IM, GY, JE
    TR21–25
    all others
    Surcharge
    9.50
    6.50
    11.00
    14.00
    none
    T wo-person delivery is not available to the Isles of
      >Scilly or the Channel Islands. F or the
    other areas it is available with the surcharge added to
      >the 19.99 pound two-person charge.
    Queries about this schedule go to the Operations team and
      >not to customer help, who cannot
    vary it.

  the same table, typed off the page by hand:

    Scottish Highlands       AB36-38, IV, KW, PA20-80 9.50
    Northern Ireland         BT                       6.50
    Isle of Man, Channel Is. IM, GY, JE               11.00
    Isles of Scilly          TR21-25                  14.00
    Rest of the UK           all others               none

    'Area' is line 7, the areas 8 to 12
    'Surcharge' is line 20, the charges
    21 to 25: 13 lines from the first area
    to its own charge, and nothing joining them

    'P' + 'A20'   ->   'PA20'
    'T' + 'wo-person'   ->   'Two-person'
    'F' + 'or'   ->   'For'
    3 places where a space is inside a word

    'PA20' in the PDF text             False
    'PA20' in delivery-exceptions.md   True

  page 2 returned 0 characters. Two facts
  are on it, and the PDF is the only place in the
  corpus that holds them:

    5.50     in 0 of 40 documents   []
    Dunmore  in 1 of 40 documents   ['shipping-partners']
```

**Start with the table, because the failure is not the one the README predicted.** The corpus
README records a real extraction from a different parser, poppler's `pdftotext`, in which `9.50`
is spliced into the middle of a wrapped postcode range and the column below it shifts up by one.
That is a misalignment: it produces a wrong surcharge against a right area, with no error.

This parser does something else. It emits the five areas, then the five postcode ranges, then the
five surcharges, in three runs — thirteen lines from the first area to its own charge. **Every
figure survived and every row is gone.** Ask the text which charge belongs to the Scottish
Highlands and nothing in it says; ask the page and it is 9.50. The cell that joined them was
never text in the first place — it was a position on a page, and Chapter 27 is why a position is
not something a parser can be relied on to reconstruct.

**So the defect you get is a property of the parser as much as of the file**, and that is worth
more than either defect. Two parsers, one page, two different wrong answers: one welds a figure
into a postcode, the other keeps every figure and drops every row. And it is worth being exact
about which parser is adding something. The corpus README says the page's three side-by-side
blocks make the content stream emit every cell of the first column before any cell of the second,
so these three runs *are* the file's recorded order, faithfully reported. The other parser tries
to reconstruct columns from positions — Chapter 27's layout analysis — and it is that attempt,
not the file, that splices 9.50 into a postcode. A team that had read about the first failure
would be looking for the wrong thing.

**Then the one the README did not promise.** Three places in this page have a space inside a
word: `P A20`, `T wo-person`, `F or`. Those are kern pairs — two glyphs the typesetter moved
closer together than the font asks — and the parser emitted the gap as a space. The prose reads
fine either way. `PA20` does not: it is a postcode, which is Chapter 43's identifier query, and
the string is on the page and not in the text the parser produced. **No exact match can find it,
and nothing downstream knows the difference.**

**And page 2 returned zero characters.** It is an image of text, so there is no text layer to
read and no error to catch. Two facts live on that page and nowhere else in the corpus, and the
two fail differently. `5.50` appears in none of the forty documents, so the Northern Ireland
surcharge having risen from it is unrecoverable: skip the page and that fact is gone. `Dunmore`
appears in one document, `shipping-partners`, which says Dunmore Freight handles two-person and
pallet deliveries and says nothing about the Isles of Scilly. So skipping page 2 does not merely
lose a page. It loses one fact outright, and leaves a second looking settled by a document that
does not settle it.

> **Warning:** The second of those is the dangerous kind. A missing fact produces a system that
> cannot answer; a fact the corpus half-contradicts produces a system that answers confidently
> from the wrong document. Chapter 32's planted disagreement is the same shape, and step 7 is
> where it costs something.

## Step 2: Chunk, Index, and Check the Size Against the Questions

Chapter 27 gives the order: strip the page furniture, cut on the document's own structure where
parsing preserved it, and then check the size against your questions before anything else is
built. This step does all three and the third is the one that decides whether the rest can work.

```python
"""Chunking and indexing the corpus, and the check chapter 27 asks for.

Forty markdown documents and page 1 of the PDF. Three decisions are
made here and each one is printed: what to strip, where to cut, and
how big a chunk may be. Chapter 27's step 5 is the check at the end -
write the questions down, find the shortest passage that answers
each, and make sure a chunk holds it.

Every row carries a locator. Chapters 27 and 28 both say what that
buys and both qualify it: an offset is recoverable later IF the
documents are kept and the chunk text is verbatim, and what cannot be
recovered is a position a store never recorded in any form. The
offset here is into the text this program produced rather than into
the file, so the stripping rules below are part of it.
"""
import pathlib
import re

import parse

DOCS = pathlib.Path("corpus/docs")
FURNITURE = ("Harbour Lane Retail Ltd · Policy document ·"
             " Review cycle: annual · Page 1 of 1")
MAX = 700
PDF_ID = "awkward-pdf-p1"
STRIP_HEADER = True
STRIP_FOOTER = True

# The shortest passage that answers each query, found by reading the
# documents. These are judgements, written down before any chunk size
# was chosen, which is the order chapter 27's step 5 asks for.
ANSWERS = {
    "q1": "return a standard item within 30 days of delivery",
    "q2": "Refunds are issued within 14 days of your return arriving"
          " at our warehouse, and your bank may\ntake a further three"
          " working days to show the money.",
    "q3": None,   # no single passage: the charge and the surcharge
    "q4": "A 1.7 litre jug kettle with a 3000 W element",
    "q5": None,   # no single passage: two documents disagree
    "q6": "Tell us within 48 hours of delivery.",
    "q7": "Free standard delivery on every order",
    "q8": "return a clearance item within 14 days of delivery",
}


def body(doc_id):
    """One document as the index holds it: the YAML header dropped and
    the repeated footer stripped. Chapter 27's method, step 3."""
    if doc_id == PDF_ID:
        return parse.pages()[0]
    text = (DOCS / f"{doc_id}.md").read_text()
    if STRIP_HEADER:
        text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    if STRIP_FOOTER:
        text = text.replace(FURNITURE, "").replace("\n---\n", "\n")
    return text.strip("\n")


def ids():
    return sorted(p.stem for p in DOCS.glob("*.md")) + [PDF_ID]


def pieces(text, maxlen=MAX):
    """Cut on the document's own structure: sections at a `## ` line
    first, then blank lines inside a section too long to keep whole,
    then a hard cut on length. Returns (offset, text) pairs, so the
    offsets are into `text` exactly as given."""
    out = []
    for block in split_keeping_offsets(text, r"\n(?=## )"):
        if len(block[1]) <= maxlen:
            out.append(block)
            continue
        for para in split_keeping_offsets(block[1], r"\n\n+"):
            at, piece = block[0] + para[0], para[1]
            while len(piece) > maxlen:
                out.append((at, piece[:maxlen]))
                at, piece = at + maxlen, piece[maxlen:]
            out.append((at, piece))
    return [(at, p.strip()) for at, p in out if p.strip()]


def split_keeping_offsets(text, pattern):
    out, at = [], 0
    for m in re.finditer(pattern, text):
        out.append((at, text[at:m.start()]))
        at = m.end()
    out.append((at, text[at:]))
    return out


def rows():
    out = []
    for doc in ids():
        text = body(doc)
        for n, (at, piece) in enumerate(pieces(text)):
            out.append({"id": f"{doc}#{n}", "doc": doc,
                        "start": at, "text": piece})
    return out


if __name__ == "__main__":
    import math

    docs = ids()
    raw = {d: (parse.pages()[0] if d == PDF_ID
               else (DOCS / f"{d}.md").read_text()) for d in docs}
    kept = {d: body(d) for d in docs}
    dropped = sum(len(raw[d]) - len(kept[d]) for d in docs)
    hit = sum(1 for d in docs if FURNITURE in raw[d])
    print(f"  {len(docs)} documents, 40 markdown and 1 PDF page")
    print(f"  stripping removed {dropped} characters,"
          f" {dropped / len(docs):.0f} a document;")
    print(f"  the footer was on {hit} of them, word for word\n")

    word = re.compile(r"[a-z0-9][a-z0-9.\-]*")
    before = {}
    for t in raw.values():
        for w in set(word.findall(t.lower())):
            before[w] = before.get(w, 0) + 1
    after = {}
    for t in kept.values():
        for w in set(word.findall(t.lower())):
            after[w] = after.get(w, 0) + 1
    n = len(docs)
    print("  the footer's own terms, before and after:\n")
    print("    term        DF with  without     IDF with  without")
    for t in ("policy", "annual", "cycle", "page"):
        b, a = before.get(t, 0), after.get(t, 0)
        fb = math.log((n - b + 0.5) / (b + 0.5) + 1)
        fa = math.log((n - a + 0.5) / (a + 0.5) + 1)
        print(f"    {t:10s} {b:7d} {b and a or a:8d}"
              f" {fb:12.4f} {fa:8.4f}")

    rs = rows()
    sizes = sorted(len(r["text"]) for r in rs)
    hard = sum(1 for r in rs if len(r["text"]) == MAX)
    print(f"\n  {len(rs)} chunks, cap {MAX} characters:"
          f" shortest {sizes[0]},")
    print(f"  median {sizes[len(sizes) // 2]}, longest {sizes[-1]},"
          f" and {hard} cut on the cap")
    print("  rather than on the structure\n")

    for r in (rs[0], [x for x in rs if x["doc"] == "refunds-policy"][3],
              [x for x in rs if x["doc"] == PDF_ID][0]):
        print(f"    {r['id']}")
        print(f"      start {r['start']:4d}  {r['text'][:30]!r}")

    stub = [r for r in rs if len(r["text"]) < 20]
    head = [r for r in stub if r["text"].startswith("#")]
    lead = [r for r in stub if r["text"].endswith(":")]
    print(f"\n  {len(stub)} chunks are under 20 characters:"
          f" {len(head)} a heading")
    print(f"  alone, {len(lead)} a line introducing a list,"
          f" {len(stub) - len(head) - len(lead)} other:\n")
    for r in sorted(stub, key=lambda r: len(r["text"]))[:3]:
        print(f"    {r['id']:26s} {len(r['text']):3d} chars"
              f"  {r['text'][:18]!r}")

    print("\n  then the check that decides whether any of this can")
    print("  work: the shortest passage answering each query, and")
    print("  whether one chunk holds it whole.\n")
    for qid in sorted(ANSWERS):
        want = ANSWERS[qid]
        if want is None:
            print(f"    {qid}  no single passage answers it")
            continue
        holding = [r["id"] for r in rs if want in r["text"]]
        print(f"    {qid}  {len(want):3d} chars"
              f"   {holding[0] if holding else 'NONE'}")
```

```text
  41 documents, 40 markdown and 1 PDF page
  stripping removed 3946 characters, 96 a document;
  the footer was on 10 of them, word for word

  the footer's own terms, before and after:

    term        DF with  without     IDF with  without
    policy          10        6       1.3863   1.8659
    annual          12        2       1.2119   2.8214
    cycle           10        0       1.3863   4.4308
    page            18        9       0.8199   1.4864

  176 chunks, cap 700 characters: shortest 1,
  median 178, longest 700, and 2 cut on the cap
  rather than on the structure

    about-us#0
      start    0  '# About Harbour Lane'
    refunds-policy#3
      start  396  '## 3. How long a refund takes\n'
    awkward-pdf-p1#0
      start    0  'Harbour Lane Retail Ltd\nDelive'

  9 chunks are under 20 characters: 6 a heading
  alone, 2 a line introducing a list, 1 other:

    warranty-full#4              1 chars  '.'
    damaged-on-arrival#2         8 chars  'Send us:'
    warranty-full#0             10 chars  '# Warranty'

  then the check that decides whether any of this can
  work: the shortest passage answering each query, and
  whether one chunk holds it whole.

    q1   49 chars   returns-standard#1
    q2  146 chars   where-is-my-refund#1
    q3  no single passage answers it
    q4   44 chars   product-kettle-hl-2208#0
    q5  no single passage answers it
    q6   36 chars   damaged-on-arrival#1
    q7   37 chars   plan-harbour-plus#2
    q8   50 chars   returns-clearance#1
```

**The footer is Chapter 27's page furniture and it is on ten documents word for word.** Stripping
it and the YAML header removes 3,946 characters, about 96 a document. What that does to Chapter
26's term statistics is in the table, and it is worth reading as a correction to the obvious
guess: `cycle` goes from ten documents to none, so its inverse document frequency rises from
1.3863 to 4.4308 — but the term is gone, so that figure now describes a term no query will ever
match. `annual` is the useful row: twelve documents down to two, and its IDF more than doubles,
because the two that keep it are the two that were talking about an annual review rather than
printing a footer. **Stripping the furniture did not make the index smaller so much as it made
ten documents stop sharing four terms they had nothing to do with.**

> **Note:** Chapter 27 derives a second effect that this corpus is too small and too uniform to
> show: adding the same text to every chunk moves each chunk's length ratio towards one, which
> costs a short chunk the advantage its shortness gave it. The footer here is on ten of
> forty-one documents rather than all of them, so the average moves and the discrimination
> survives. The chapter's claim is about a header on every page.

[**176 chunks**]{.noindex}, cut on `## ` sections, then on blank lines inside a section too long to keep
whole, then on a hard cap of 700 characters. Two chunks hit the cap, so the structure carried
almost all of the cutting.

**Nine chunks are under twenty characters, and they are rows**, which is the part of this step
worth stopping on. Six are a heading standing alone. Two are a line that introduces a list below
it — `Send us:` — and the list is in the next chunk. One holds a single full stop, the tail the
hard cap left in the longest document. Every one of them can be retrieved, scored, ranked and put
into a context, and none of them can answer anything. Step 5 sends two of them to the model, and
step 3 is where one of them *wins* a rank rather than merely occupying one.

**And note where the two lead-ins put their lists: in the next chunk.** That is Chapter 28's
split answer with the halves one row apart, and Chapter 28 built a mechanism for exactly it —
neighbour expansion, which fetches the rows adjacent in the original document and needs only the
locator each row above is carrying. Step 7 is where that comes back, because one of this
pipeline's failures has exactly this shape — a reply that quoted a lead-in whose list was in the
next chunk and was never sent. It is not one of these two stubs; `q7`'s lead-in is 49 characters
and not among the nine. The shape is what recurs, not the row.

**Then the check, which is Chapter 27's step 5 and costs ten minutes.** The shortest passage that
answers each of the eight queries is written into the program, and the program asks whether one
chunk holds it whole. Six of eight do. Note the order the chapter did this in: the answer
passages were read out of the documents and written down *before* any chunk size was chosen,
because a size chosen first and a question found afterwards is not a check.

**Two queries have no single passage that answers them, and neither is a chunking defect.** `q3`
asks what delivery costs to the Scottish Highlands, and the standard charge is in one document
while the surcharge added on top is in another. `q5` asks whether a refund is fourteen days or
thirty, and two documents in this corpus give different figures. Both are planted and the corpus
README names them. So Chapter 27's ceiling applies to both — no retrieval method can return a
single passage that answers either — and Chapter 28 is why that is not the same as the
information being out of reach: both answers are in the index, across two rows, and putting them
together is the model's job once the assembly sends both.

[**An answer passage**]{idx="answer passage"} is that written-down shortest passage: the text a reader would need in
front of them to be done with the question. It is worth having as a thing with a name, because it
is the only input in this lab that makes step 7's retrieval column mechanical rather than a
matter of opinion.

## Step 3: Retrieve Over Chunks, and Roll Up to Documents

Chapter 44 ran BM25, dense retrieval and reciprocal rank fusion over the forty documents of this
same corpus against this same key. This step runs the same formulas over the 176 chunks, because
the assembly in step 5 needs passages rather than documents. One thing has to be decided before
any measure means anything, and the program prints it first.

```python
"""Retrieval over chunks: BM25, dense, fusion, and the roll-up.

Chapter 44 ranked whole documents with the same formulas and the same
key. This ranks the 176 chunks, because the assembly in step 5 needs
passages and not documents, and then rolls them up to documents,
because the key judges documents and nothing in it judges a chunk. It
then runs the same eight queries over the whole documents as well, so
that "did chunking help?" is a measurement rather than an assumption.

The conventions are chapter 26's and chapter 44's, printed by the
program rather than assumed: BM25 with the +1 inside the logarithm,
k1 1.5 and b 0.75; reciprocal rank fusion at k = 60 on the top ten of
each list; recall@5 and nDCG@5 with the grade itself as the gain and
log2(i+1) as the discount.
"""
import json
import math
import os
import pathlib
import random
import re
import urllib.request

import index
from key import key, queries

WORD = re.compile(r"[a-z0-9][a-z0-9.\-]*")
K1, B = 1.5, 0.75
RRF_K, DEPTH, AT = 60, 10, 5
MODEL = "text-embedding-3-small"
URL = "https://api.openai.com/v1/embeddings"
TIMEOUT = 120

ROWS = index.rows()
BY_ID = {r["id"]: r for r in ROWS}


class Units:
    """One set of things to rank, with its own term statistics. Build
    it from chunks or from whole documents; nothing below knows which,
    so the two columns in the output differ only in the unit."""

    def __init__(self, texts, cache_path):
        self.texts = texts
        self.cache = pathlib.Path(cache_path)
        self.tokens = {i: WORD.findall(t.lower())
                       for i, t in texts.items()}
        self.n = len(texts)
        self.avgdl = sum(len(t) for t in self.tokens.values()) / self.n
        self.df = {}
        for toks in self.tokens.values():
            for w in set(toks):
                self.df[w] = self.df.get(w, 0) + 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log((self.n - n + 0.5) / (n + 0.5) + 1)

    def bm25(self, query, uid):
        toks = self.tokens[uid]
        dl, total = len(toks), 0.0
        for term in WORD.findall(query.lower()):
            tf = toks.count(term)
            if tf:
                total += (self.idf(term) * tf * (K1 + 1)
                          / (tf + K1 * (1 - B + B * dl / self.avgdl)))
        return total

    def lexical(self, query):
        """Only units that matched a term: chapter 26's warning is
        that a tail of zeros hands arbitrary positions a vote."""
        hit = {u: self.bm25(query, u) for u in self.texts}
        hit = {u: v for u, v in hit.items() if v > 0}
        return sorted(hit, key=lambda u: -hit[u]), hit

    def vectors(self):
        if self.cache.exists():
            return json.loads(self.cache.read_text())
        ids = list(self.texts)
        vecs, served = embed([self.texts[i] for i in ids])
        out = {"ids": ids, "model": served, "vecs": vecs}
        self.cache.write_text(json.dumps(out))
        return out

    def dense(self, query, cache=None):
        cache = cache or self.vectors()
        qv = embed([query])[0][0]
        s = {u: cosine(qv, v)
             for u, v in zip(cache["ids"], cache["vecs"])}
        return sorted(s, key=lambda u: -s[u]), s


def embed(texts):
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    body = json.dumps({"model": MODEL, "input": texts}).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {k}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    rows = sorted(d["data"], key=lambda x: x["index"])
    return [x["embedding"] for x in rows], d["model"]


def cosine(a, b):
    return (sum(x * y for x, y in zip(a, b))
            / (math.sqrt(sum(x * x for x in a))
               * math.sqrt(sum(y * y for y in b))))


def fuse(a, b, depth=DEPTH, k=RRF_K):
    f = {}
    for order in (a, b):
        for place, uid in enumerate(order[:depth], 1):
            f[uid] = f.get(uid, 0.0) + 1 / (k + place)
    return sorted(f, key=lambda u: -f[u]), f


def to_docs(order, judged=None):
    """Chunks to documents: best rank wins, duplicates dropped. A
    document the key never judged is dropped when `judged` is given,
    because a measure cannot score what the key does not cover."""
    out = []
    for uid in order:
        doc = BY_ID[uid]["doc"] if uid in BY_ID else uid
        if doc in out or (judged is not None and doc not in judged):
            continue
        out.append(doc)
    return out


def recall_at(order, grades, at=AT):
    total = sum(1 for g in grades.values() if g > 0)
    found = sum(1 for d in order[:at] if grades.get(d, 0) > 0)
    return found / total if total else 0.0


def dcg(order, grades, at=AT):
    return sum(grades.get(d, 0) / math.log(i + 1, 2)
               for i, d in enumerate(order[:at], 1))


def ndcg(order, grades, at=AT):
    best = dcg(sorted(grades, key=lambda d: -grades[d]), grades, at)
    return dcg(order, grades, at) / best if best else 0.0


def paired(a, b, trials=10_000, seed=45):
    """Chapter 20's paired bootstrap, resampling queries and keeping
    each query's pair of marks together. Also returns how many
    resamples came out at or below zero and how many queries the two
    methods scored differently, which is what the interval rests on."""
    rng = random.Random(seed)
    n = len(a)
    diffs = sorted(
        sum(b[i] - a[i] for i in (rng.randrange(n) for _ in range(n))) / n
        for _ in range(trials))
    return (diffs[int(0.025 * trials)], diffs[int(0.975 * trials)],
            sum(1 for d in diffs if d <= 0),
            sum(1 for x, y in zip(a, b) if x != y))


def tie_range(fused_scores, grades, judged):
    """A fused score shared by two units has no ordering, so report
    the range the tie spans rather than whichever one sort() emitted."""
    def g(uid):
        return grades.get(
            BY_ID[uid]["doc"] if uid in BY_ID else uid, 0)
    hi = sorted(fused_scores, key=lambda u: (fused_scores[u], g(u)),
                reverse=True)
    lo = sorted(fused_scores, key=lambda u: (fused_scores[u], -g(u)),
                reverse=True)
    return (ndcg(to_docs(lo, judged), grades),
            ndcg(to_docs(hi, judged), grades))


chunks = Units({r["id"]: r["text"] for r in ROWS},
               "chunk-vectors.json")
documents = Units({d: index.body(d) for d in index.ids()},
                  "doc-vectors.json")

# The pipeline from step 5 onwards runs on chunks, so these are the
# names the later programs import.
TEXTS = chunks.texts
TOKENS = chunks.tokens
N, AVGDL, DF = chunks.n, chunks.avgdl, chunks.df
idf, bm25 = chunks.idf, chunks.bm25
lexical, dense, vectors = chunks.lexical, chunks.dense, chunks.vectors


def rankings(units=chunks, cache=None):
    cache = cache or units.vectors()
    out = {}
    for qid, q in sorted(queries().items()):
        lex, _ = units.lexical(q)
        den, _ = units.dense(q, cache)
        fus, fsc = fuse(lex, den)
        out[qid] = {"lexical": lex, "dense": den, "fused": fus,
                    "fused_scores": fsc}
    return out


if __name__ == "__main__":
    k = key()
    judged = set(k["q1"])
    res = rankings(chunks)
    doc_res = rankings(documents)
    print(f"  {chunks.n} chunks, {documents.n} documents, model"
          f" {chunks.vectors()['model']}")
    print(f"  {chunks.avgdl:.1f} terms a chunk,"
          f" {documents.avgdl:.1f} a whole document")
    print(f"  BM25 k1 {K1} b {B}; RRF k {RRF_K} on the top"
          f" {DEPTH}; measures at {AT}\n")

    print("  the top fused chunk, and where the PDF rolls up to:\n")
    for qid in sorted(res):
        all_docs = to_docs(res[qid]["fused"])
        at = (all_docs.index(index.PDF_ID) + 1
              if index.PDF_ID in all_docs else None)
        print(f"    {qid}  {res[qid]['fused'][0]:26s} PDF at"
              f" {at if at else '-':>3} of {len(all_docs)}")

    marks = {}
    for name, fn in (("recall@5", recall_at), ("nDCG@5", ndcg)):
        for unit, rs in (("chunks", res), ("documents", doc_res)):
            for m in ("lexical", "dense", "fused"):
                marks[(name, unit, m)] = [
                    fn(to_docs(rs[q][m], judged), k[q])
                    for q in sorted(rs)]

    print("\n  rolled up to documents, beside the same queries over")
    print("  the whole documents - same formulas, same key, same")
    print("  stripped text, so the only difference is the unit:\n")
    for name in ("recall@5", "nDCG@5"):
        print(f"    {name}        chunks               documents")
        print("    query   lex  dense  fused    lex  dense  fused")
        for i, qid in enumerate(sorted(res)):
            row = [marks[(name, u, m)][i]
                   for u in ("chunks", "documents")
                   for m in ("lexical", "dense", "fused")]
            print(f"    {qid}   " + "  ".join(f"{v:.3f}" for v in row[:3])
                  + "  " + "  ".join(f"{v:.3f}" for v in row[3:]))
        print("    mean  " + "  ".join(
            f"{sum(marks[(name, 'chunks', m)]) / 8:.3f}"
            for m in ("lexical", "dense", "fused")) + "  " + "  ".join(
            f"{sum(marks[(name, 'documents', m)]) / 8:.3f}"
            for m in ("lexical", "dense", "fused")) + "\n")

    def report(label, a, b):
        lo, hi, below, differ = paired(a, b)
        print(f"      {label:24s} {sum(b) / 8 - sum(a) / 8:+.3f}"
              f"  {lo:+.3f} to {hi:+.3f}")
        print("               " + ("clears zero" if lo > 0 or hi < 0
              else "contains zero: cannot tell")
              + f", {differ} of 8 differ")
        return lo, hi, below, differ

    print("  Is any of that real? Chapter 20, paired on the eight,")
    print("  on the difference and never on a mean. First the three")
    print("  methods against each other, over chunks:\n")
    for name in ("recall@5", "nDCG@5"):
        print(f"    {name}")
        for a, b in (("lexical", "dense"), ("lexical", "fused"),
                     ("dense", "fused")):
            report(f"{b} - {a}", marks[(name, "chunks", a)],
                   marks[(name, "chunks", b)])
        print()

    print("  then the same method at the two granularities, which is")
    print("  what chunking cost or bought:\n")
    pinned = None
    for name in ("recall@5", "nDCG@5"):
        print(f"    {name}")
        for m in ("lexical", "dense", "fused"):
            got = report(f"{m}: chunks - docs",
                         marks[(name, "documents", m)],
                         marks[(name, "chunks", m)])
            if name == "recall@5" and m == "dense":
                pinned = got
        print()

    print("  Now the arithmetic behind those verdicts, because one")
    print("  of them could not have cleared zero whatever the")
    print("  differences were. It applies only where every")
    print("  per-query difference has the same sign:\n")
    print("    measure    comparison              ties  one-sided"
          "  clears")
    onesided = []
    for name in ("recall@5", "nDCG@5"):
        for a, b, lab in (("lexical", "dense", "dense - lexical"),
                          ("lexical", "fused", "fused - lexical"),
                          ("dense", "fused", "fused - dense"),
                          ("lexical", "lexical", "lexical: chunks - docs"),
                          ("dense", "dense", "dense: chunks - docs"),
                          ("fused", "fused", "fused: chunks - docs")):
            if a == b:
                x = marks[(name, "documents", a)]
                y = marks[(name, "chunks", b)]
            else:
                x = marks[(name, "chunks", a)]
                y = marks[(name, "chunks", b)]
            lo, hi, below, differ = paired(x, y)
            d = [q - p for p, q in zip(x, y)]
            one = not (any(v > 1e-9 for v in d) and any(v < -1e-9 for v in d))
            clears = lo > 0 or hi < 0
            print(f"    {name:10s} {lab:22s} {8 - differ:4d}"
                  f"  {str(one):>9s}  {str(clears):>6s}")
            if one:
                onesided.append((name, lab, 8 - differ, clears,
                                 [round(v, 3) for v in d]))
    print()
    for name, lab, ties, clears, d in onesided:
        print(f"    {name} {lab}: {ties} tied,")
        print(f"      differences {[v for v in d if v]}"
              f" and {ties} zeros,")
        print(f"      ({ties}/8) ** 8 = {(ties / 8) ** 8:.4f},"
              f" {'clears' if clears else 'pinned at zero'}")
    print()
    print("    tied of 8   chance a resample draws no difference")
    for t in range(8, 2, -1):
        pr = (t / 8) ** 8
        print(f"    {t:5d}       {pr:.4f}"
              + ("   pinned at zero" if pr >= 0.025 else ""))

    print("\n  and the fused figure is a range, not a number,")
    print("  because RRF ties and chapter 26 shows it cannot break")
    print("  them:\n")
    tlo = thi = 0.0
    for qid in sorted(res):
        a2, b2 = tie_range(res[qid]["fused_scores"], k[qid], judged)
        tlo += a2 / len(res)
        thi += b2 / len(res)
        flag = "  <- the tie decides it" if b2 - a2 > 1e-9 else ""
        print(f"    {qid}   {a2:.3f} to {b2:.3f}{flag}")
    dn = sum(marks[("nDCG@5", "chunks", "dense")]) / 8
    print(f"    mean  {tlo:.3f} to {thi:.3f}, and dense's"
          f" {dn:.3f} is outside it")
```

```text
  176 chunks, 41 documents, model text-embedding-3-small
  37.7 terms a chunk, 161.8 a whole document
  BM25 k1 1.5 b 0.75; RRF k 60 on the top 10; measures at 5

  the top fused chunk, and where the PDF rolls up to:

    q1  refunds-faq#1              PDF at   - of 13
    q2  where-is-my-refund#0       PDF at   - of 10
    q3  delivery-exceptions#2      PDF at   2 of 12
    q4  product-toaster-hl-2209#0  PDF at   - of 13
    q5  refunds-policy#3           PDF at   - of 9
    q6  damaged-on-arrival#0       PDF at   - of 11
    q7  plan-harbour-plus#0        PDF at   8 of 8
    q8  returns-clearance#1        PDF at   - of 6

  rolled up to documents, beside the same queries over
  the whole documents - same formulas, same key, same
  stripped text, so the only difference is the unit:

    recall@5        chunks               documents
    query   lex  dense  fused    lex  dense  fused
    q1   0.250  0.625  0.250  0.375  0.500  0.500
    q2   0.750  1.000  1.000  0.750  1.000  1.000
    q3   0.667  1.000  1.000  0.333  1.000  1.000
    q4   0.333  1.000  1.000  0.667  1.000  1.000
    q5   0.333  1.000  0.667  1.000  1.000  1.000
    q6   0.500  0.750  0.500  0.500  0.500  0.750
    q7   0.750  0.500  0.500  0.500  0.500  0.500
    q8   0.600  0.800  0.800  0.800  0.800  0.800
    mean  0.523  0.834  0.715  0.616  0.787  0.819

    nDCG@5        chunks               documents
    query   lex  dense  fused    lex  dense  fused
    q1   0.273  1.000  0.294  0.516  0.924  0.893
    q2   0.879  1.000  1.000  0.670  1.000  0.896
    q3   0.651  0.967  0.885  0.469  0.733  0.712
    q4   0.138  0.840  0.860  0.722  0.882  0.860
    q5   0.296  1.000  0.651  0.733  1.000  1.000
    q6   0.702  0.860  0.739  0.562  0.739  0.744
    q7   0.860  0.739  0.739  0.739  0.739  0.739
    q8   0.573  0.916  0.906  0.629  0.887  0.887
    mean  0.546  0.915  0.759  0.630  0.863  0.841

  Is any of that real? Chapter 20, paired on the eight,
  on the difference and never on a mean. First the three
  methods against each other, over chunks:

    recall@5
      dense - lexical          +0.311  +0.118 to +0.489
               clears zero, 8 of 8 differ
      fused - lexical          +0.192  +0.015 to +0.375
               clears zero, 6 of 8 differ
      fused - dense            -0.120  -0.234 to -0.031
               clears zero, 3 of 8 differ

    nDCG@5
      dense - lexical          +0.369  +0.167 to +0.571
               clears zero, 8 of 8 differ
      fused - lexical          +0.213  +0.055 to +0.397
               clears zero, 8 of 8 differ
      fused - dense            -0.156  -0.336 to -0.019
               clears zero, 6 of 8 differ

  then the same method at the two granularities, which is
  what chunking cost or bought:

    recall@5
      lexical: chunks - docs   -0.093  -0.307 to +0.105
               contains zero: cannot tell, 6 of 8 differ
      dense: chunks - docs     +0.047  +0.000 to +0.109
               contains zero: cannot tell, 2 of 8 differ
      fused: chunks - docs     -0.104  -0.208 to -0.031
               clears zero, 3 of 8 differ

    nDCG@5
      lexical: chunks - docs   -0.084  -0.292 to +0.101
               contains zero: cannot tell, 8 of 8 differ
      dense: chunks - docs     +0.052  +0.001 to +0.117
               clears zero, 5 of 8 differ
      fused: chunks - docs     -0.082  -0.266 to +0.063
               contains zero: cannot tell, 6 of 8 differ

  Now the arithmetic behind those verdicts, because one
  of them could not have cleared zero whatever the
  differences were. It applies only where every
  per-query difference has the same sign:

    measure    comparison              ties  one-sided  clears
    recall@5   dense - lexical           0      False    True
    recall@5   fused - lexical           2      False    True
    recall@5   fused - dense             5       True    True
    recall@5   lexical: chunks - docs    2      False   False
    recall@5   dense: chunks - docs      6       True   False
    recall@5   fused: chunks - docs      5       True    True
    nDCG@5     dense - lexical           0      False    True
    nDCG@5     fused - lexical           0      False    True
    nDCG@5     fused - dense             2      False    True
    nDCG@5     lexical: chunks - docs    0      False   False
    nDCG@5     dense: chunks - docs      3      False    True
    nDCG@5     fused: chunks - docs      2      False   False

    recall@5 fused - dense: 5 tied,
      differences [-0.375, -0.333, -0.25] and 5 zeros,
      (5/8) ** 8 = 0.0233, clears
    recall@5 dense: chunks - docs: 6 tied,
      differences [0.125, 0.25] and 6 zeros,
      (6/8) ** 8 = 0.1001, pinned at zero
    recall@5 fused: chunks - docs: 5 tied,
      differences [-0.25, -0.333, -0.25] and 5 zeros,
      (5/8) ** 8 = 0.0233, clears

    tied of 8   chance a resample draws no difference
        8       1.0000   pinned at zero
        7       0.3436   pinned at zero
        6       0.1001   pinned at zero
        5       0.0233
        4       0.0039
        3       0.0004

  and the fused figure is a range, not a number,
  because RRF ties and chapter 26 shows it cannot break
  them:

    q1   0.294 to 0.446  <- the tie decides it
    q2   1.000 to 1.000
    q3   0.885 to 0.906  <- the tie decides it
    q4   0.860 to 0.882  <- the tie decides it
    q5   0.651 to 0.651
    q6   0.739 to 0.739
    q7   0.739 to 0.739
    q8   0.906 to 0.906
    mean  0.759 to 0.784, and dense's 0.915 is outside it
```

**The key judges documents and the index holds chunks, so something has to give.** Three
possibilities, and only one of them is honest here. You could lift each document's grade onto
every chunk it was cut into — but then a relevant document cut into eight chunks contributes eight
relevant chunks, only five of which can fit in a top five, so recall@5 would be capped below one
by the chunking rather than by the retrieval. You could judge the chunks, which is 1,408 new
judgements and a different key. Or you can [**roll up**]{idx="roll-up"}: map each retrieved chunk back to its
document, let the best-ranked chunk stand for it, and drop duplicates. That is what a user is
shown anyway, and it is what the program does.

**The roll-up has a hole in it, and the program prints that before the table.** The index holds
forty-one documents, because page 1 of the PDF is in it, and the key judges forty. The PDF rolls
up to rank 2 for `q3` and rank 8 for `q7`. So every figure below drops it and scores the forty the
key covers. [**That is not free**]{.noindex}: the system a reader actually runs has forty-one documents in it
and the measures cannot see one of them — which is Chapter 26's point that a recall figure is
recall against your key, arriving as a missing row rather than as a caution.

**The two tables are the same eight queries at two granularities**, so "did chunking help?" is a
measurement here rather than an assumption. Read the method comparisons first and the granularity
comparisons second, because the first set is much the stronger.

**Two of the three method comparisons reproduce Chapter 44's and one does not.**

[**Dense beats lexical**]{.noindex}, +0.311 recall@5 and +0.369 nDCG@5, both intervals clearing zero with all
eight queries differing. Chapter 44 got +0.194 and +0.223 over whole documents, so the point
estimates grew — a document is one vector however long it is, which is Chapter 24's fixed width,
and at the 161.8 terms a document averages here everything in it shares that width, where at 37.7
a chunk it does not. (Chapter 44 prints 174.3 for the same forty documents, because it tokenises
each file whole and this one strips the header and footer first.)
[**Fusion beats lexical**]{.noindex}, +0.192 and +0.213 against Chapter 44's +0.177 and +0.195, which is the
established result about hybrid retrieval that Chapter 44 warns against dropping for being
unsurprising.

**And fusion loses to dense, which is the row Chapter 44 could not call.** −0.120 recall and
−0.156 nDCG, both intervals clearing zero. Chapter 26 refused a verdict on hybrid against dense
and said whether it helps you is a measurement; Chapter 44 made that measurement over documents
and reported *cannot tell*, at −0.017 and −0.028 with both intervals containing zero. **Over
chunks the same measurement comes out against fusion and clears zero.** Be exact about what that
is a verdict on: this corpus, these eight queries, this lexical half, at this granularity. It is
not a verdict on hybrid retrieval, and the mechanism says why it would not transfer — reciprocal
rank fusion gives each list an equal vote, and a vote cast by a weaker list costs more the better
the other one is.

**The lexical half is where the weakness is, and `q4` shows it.** The query asks what `HL-2208`
is; lexical nDCG@5 is 0.138 and the top fused chunk is a page about the toaster `HL-2209`. BM25
over 176 short chunks is a different scoring problem from BM25 over 40 long ones, and **the
obvious explanation is the wrong one**, so it is worth working out rather than guessing at.

The rare term did not get commoner. Chapter 44 found `hl-2208` in two of forty documents at an
inverse document frequency of 2.7973; over 176 chunks it is in two of them at *4.2599*, so it
became *more* discriminating. What changed is the other half of the formula. The average length
fell from 161.8 terms to 37.7, so the normalisation now divides by a quarter of what it did, and
a chunk of five terms that matches a common word is rewarded enormously for its shortness.
`q4`'s lexical ranking opens with `## 2. What is not covered` at 4.3256 and
`# What the stock statuses mean` at 3.2434 — five terms each, the first matching `what` and `is`
and the second only `what` — with a 23-term chunk between them at 3.4758. The kettle's page is
*eighth* at 3.0845 with 107 terms, and it is one of the two chunks whose terms include
`hl-2208`, which is where the 4.2599 comes from.

**So a short chunk can win a rank on a common word alone**, and this is the one place in the
chapter where a chunking decision and a retrieval formula can be seen meeting. Chapter 27 derived
that a header on every chunk destroys length normalisation's discrimination; this is the same
quantity broken from the other side, by cutting the collection into pieces short enough that
shortness itself becomes the signal.

**And the clearest case is not this one, which is worth saying rather than letting the stub count
do work it cannot.** `q4`'s winners are 25 and 30 characters — short, and not among step 2's nine
chunks under twenty. Go to `q7` and one of the nine wins outright: `plan-harbour-plus#0` is the
fourteen-character heading `# Harbour Plus`, and it is rank one lexically and the top fused chunk
the program prints. A stub is not merely occupying a rank there; it is holding the first one.

**Then what chunking itself was worth, which is the second block and the weaker evidence.**
Chunking helped dense retrieval: +0.052 nDCG@5, from +0.001 to +0.117, which clears zero on five
queries that differ. It hurt fusion on recall: −0.104, from −0.208 to −0.031. And its effect on
lexical retrieval cannot be told from zero on either measure, even though lexical is where the
`q4` damage above happened — a reminder that a mechanism you can see in one query is not the same
thing as a difference you can measure over eight.

**One of those intervals has a near end of exactly zero, and it is worth not rounding past.**
Dense over chunks beat dense over documents on two of the eight queries and tied on six, and no
per-query difference is negative. A bootstrap resample that happens to draw only tied queries
therefore has a mean of exactly zero — and if that happens often enough to reach the 2.5th
percentile, the near end of the interval is pinned there no matter how large the real differences
are. With `\(n\)`{=latex} queries of which `\(t\)`{=latex} are tied, that chance is:

```{=latex}
\[ \left(\frac{t}{n}\right)^{n} \]
```

At eight queries the program's table puts the boundary between five ties and six: at six,
`\((6/8)^8 = 0.1001\)`{=latex} and the bound is pinned; at five, 0.0233 and it is not.

**Three of this chapter's twelve comparisons are one-sided, and they land either side of that
boundary.** Dense chunks against documents has six ties and cannot clear zero whatever its other
two differences are — +0.125 and +0.250, which are large. Fusion against dense, and fusion at the
two granularities, each have five and each clears. So on eight queries a one-sided difference
needs at least three queries to move before it can be established at all, and that is arithmetic
about the bootstrap rather than anything about retrieval.

**Read the condition before reaching for the formula, though, because it is narrow.** It holds
only where every per-query difference has the same sign, and nine of the twelve comparisons here
have both signs — including the narrowest two-signed interval of the twelve, dense at the two
granularities on nDCG@5, which clears zero at 0.116 wide with three ties. A resample of a two-signed set can
come out negative as well as zero, so nothing is pinned and the formula says nothing about it.

**And the fused figure is a range rather than a number**, which Chapter 44 established and which
holds here: reciprocal rank fusion throws the scores away, so it cannot tell `(1, 2)` from
`(2, 1)`, and three of the eight queries have a tie that straddles a grade inside the top five.
The range is 0.759 to 0.784. Chapter 44's fused figure had dense's mean inside its range and could
conclude nothing from it; dense's 0.915 is outside this one and above it, so **the comparison does
not depend on which way a tie falls.**

## Step 4: Rerank a Candidate Set, and Measure Its Ceiling

Chapter 26 names three encoder arrangements and this is the third: one model given the query and
one chunk together, emitting one score for the pair, with nothing precomputed. Chapter 44 ran it
over whole documents and left this step two findings to take as given. It ran two scales: a
nought-to-ten scale could not express an order over ten candidates at all, and a nought-to-a-
hundred scale returned three to eight distinct scores, which is better and not enough. The scale
here is the second of those, so what follows confirms Chapter 44's result rather than testing it.
And the candidate set is a ceiling a reranker cannot raise, so the ceiling is computed before the
gain is believed.

Two candidate sets are reranked rather than one, because step 3 left a real question about which
first stage the pipeline should use. The two sets overlap, so the eight queries cost 105 scoring
calls rather than the 160 a pair of ten-candidate sets would suggest — the program counts them.

```python
"""Reranking the candidate set, and the ceiling it cannot pass.

Chapter 26 names the arrangement: a cross-encoder puts the query and
one chunk through a model together and emits one score for the pair,
so nothing is precomputed. This is that arrangement with a chat model
doing the joint scoring, which is not a purpose-built cross-encoder.

Chapter 44 ran the same thing over whole documents and found two
things this program takes as given. It tried two scales: 0 to 10,
which could not express an order over ten candidates at all, and
0 to 100, which gave three to eight distinct scores - better, and not
enough. The scale here is the second. And the candidate set is a
ceiling, so the ceiling is computed before the gain is believed.

Two candidate sets of ten for each of eight queries, and the two
overlap, so the run scores far fewer than 160 pairs - the program
prints how many. Cached to rerank-scores.json, so a second run is
free and the figures below do not move.
"""
import json
import os
import pathlib
import re
import urllib.request

import search
from key import key, queries

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
CACHE = pathlib.Path("rerank-scores.json")
TIMEOUT = 120
DEPTH = 10

PROMPT = (
    "Score how well the passage answers the question, 0 to 100.\n"
    "Use the whole range: two passages should get the same score\n"
    "only if they are equally good. Reply with the number only.\n\n"
    "Question: {q}\n\nPassage:\n{doc}"
)


def score(q, cid):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT.format(
            q=q, doc=search.BY_ID[cid]["text"][:4000])}],
        "max_tokens": 6, "temperature": 0,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    text = d["choices"][0]["message"]["content"]
    m = re.search(r"-?\d+(\.\d+)?", text)
    return (float(m.group()) if m else 0.0), d["model"]


def scores(res):
    """One score per (query, chunk) pair over both candidate sets.
    The two sets overlap, so a pair scored once is not scored again."""
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    out, served = {}, None
    for qid, q in sorted(queries().items()):
        out[qid] = {}
        for stage in ("fused", "dense"):
            for cid in res[qid][stage][:DEPTH]:
                if cid not in out[qid]:
                    out[qid][cid], served = score(q, cid)
    CACHE.write_text(json.dumps({"model": served, "scores": out}))
    return json.loads(CACHE.read_text())


def ceiling(candidates, grades, judged):
    """The best nDCG@5 any permutation of this candidate set can
    reach: sort it by the grade the key gives. Chapter 44's point -
    a reranker permutes, so this is the most one can be worth."""
    def g(cid):
        return grades.get(search.BY_ID[cid]["doc"], 0)
    best = sorted(candidates, key=g, reverse=True)
    return search.ndcg(search.to_docs(best, judged), grades)


if __name__ == "__main__":
    k = key()
    judged = set(k["q1"])
    res = search.rankings()
    got = scores(res)
    pairs = sum(len(v) for v in got["scores"].values())
    print(f"  two candidate sets of {DEPTH} per query, reranked")
    print(f"  by {got['model']}. The sets overlap, so the eight")
    print(f"  queries took {pairs} scoring calls and not"
          f" {2 * DEPTH * len(got['scores'])}.\n")

    print("  how many distinct scores the fused ten got. The")
    print("  instruction asked for the whole range:\n")
    shared = 0
    for qid in sorted(got["scores"]):
        cands = res[qid]["fused"][:DEPTH]
        vals = [got["scores"][qid][c] for c in cands]
        shared += sum(1 for v in vals if vals.count(v) > 1)
        shown = sorted(set(vals), reverse=True)
        print(f"    {qid}  {len(set(vals))} of {len(vals)} distinct"
              f"  {[int(v) for v in shown]}")
    seen = DEPTH * len(got["scores"])
    print(f"    {shared} of {seen} candidates sit in a block with")
    print("    another candidate on the same score, and every score")
    print("    the model returned is a multiple of five\n")

    cols = ("fused", "f+rr", "f-ceil", "dense", "d+rr", "d-ceil")
    print("  nDCG@5 after the roll-up. f+rr is the fused ten")
    print("  reranked, f-ceil the best any reordering of those ten")
    print("  could reach; d+rr and d-ceil the same over dense's:\n")
    print("    query " + " ".join(f"{c:>6s}" for c in cols))
    means = {n: 0.0 for n in cols}
    per = {n: [] for n in cols}
    for qid in sorted(got["scores"]):
        sc = got["scores"][qid]
        row = {}
        for stage, b in (("fused", "f"), ("dense", "d")):
            cands = res[qid][stage][:DEPTH]
            order = sorted(cands, key=lambda c: -sc[c])
            row[stage] = search.ndcg(
                search.to_docs(res[qid][stage], judged), k[qid])
            row[f"{b}+rr"] = search.ndcg(
                search.to_docs(order, judged), k[qid])
            row[f"{b}-ceil"] = ceiling(cands, k[qid], judged)
        for n, v in row.items():
            means[n] += v / len(got["scores"])
            per[n].append(v)
        print(f"    {qid}   " + " ".join(f"{row[n]:6.3f}"
                                         for n in cols))
    print("    mean  " + " ".join(f"{means[n]:6.3f}" for n in cols))

    print("\n  paired, chapter 20, on what the next step is"
          " handed:\n")
    for a, b in (("fused", "f+rr"), ("dense", "d+rr"),
                 ("f+rr", "d+rr"), ("f+rr", "f-ceil"),
                 ("d+rr", "d-ceil")):
        lo, hi, below, differ = search.paired(per[a], per[b])
        print(f"    {b:7s} - {a:7s}  {means[b] - means[a]:+.3f}"
              f"   {lo:+.3f} to {hi:+.3f}   "
              + ("clears" if lo > 0 or hi < 0 else "cannot tell"))

    print("\n  the headroom, which is the ceiling less the stage")
    print("  feeding it - what a better reranker could still be")
    print("  worth on that candidate set:\n")
    for stage, b in (("fused", "f"), ("dense", "d")):
        print(f"    from {stage}:  ceiling {means[f'{b}-ceil']:.3f},"
              f" first stage {means[stage]:.3f},")
        print(f"               headroom"
              f" {means[f'{b}-ceil'] - means[stage]:+.3f}, of which"
              f" this")
        print(f"               reranker took"
              f" {means[f'{b}+rr'] - means[stage]:+.3f}")

    for qid in sorted(got["scores"]):
        c = ceiling(res[qid]["fused"][:DEPTH], k[qid], judged)
        d = search.ndcg(search.to_docs(res[qid]["dense"], judged),
                        k[qid])
        if c < d - 1e-9:
            print(f"\n    {qid}: the fused ten cap any reranking at"
                  f" {c:.3f},")
            print(f"        and dense alone scores {d:.3f}")
```

```text
  two candidate sets of 10 per query, reranked
  by gpt-4o-mini-2024-07-18. The sets overlap, so the eight
  queries took 105 scoring calls and not 160.

  how many distinct scores the fused ten got. The
  instruction asked for the whole range:

    q1  7 of 10 distinct  [100, 90, 80, 30, 20, 10, 0]
    q2  5 of 10 distinct  [90, 85, 60, 10, 0]
    q3  5 of 10 distinct  [100, 90, 20, 10, 0]
    q4  4 of 10 distinct  [90, 30, 20, 0]
    q5  6 of 10 distinct  [100, 90, 80, 70, 30, 0]
    q6  7 of 10 distinct  [90, 70, 60, 30, 20, 10, 0]
    q7  4 of 10 distinct  [85, 20, 10, 0]
    q8  6 of 10 distinct  [100, 90, 60, 50, 20, 10]
    56 of 80 candidates sit in a block with
    another candidate on the same score, and every score
    the model returned is a multiple of five

  nDCG@5 after the roll-up. f+rr is the fused ten
  reranked, f-ceil the best any reordering of those ten
  could reach; d+rr and d-ceil the same over dense's:

    query  fused   f+rr f-ceil  dense   d+rr d-ceil
    q1    0.294  0.986  1.000  1.000  1.000  1.000
    q2    1.000  1.000  1.000  1.000  1.000  1.000
    q3    0.885  0.906  1.000  0.967  0.967  1.000
    q4    0.860  1.000  1.000  0.840  1.000  1.000
    q5    0.651  0.651  1.000  1.000  0.671  1.000
    q6    0.739  0.739  0.739  0.860  0.823  1.000
    q7    0.739  0.635  0.879  0.739  0.635  0.739
    q8    0.906  0.916  0.916  0.916  0.916  0.916
    mean   0.759  0.854  0.942  0.915  0.877  0.957

  paired, chapter 20, on what the next step is handed:

    f+rr    - fused    +0.095   -0.022 to +0.281   cannot tell
    d+rr    - dense    -0.039   -0.136 to +0.040   cannot tell
    d+rr    - f+rr     +0.022   +0.003 to +0.046   clears
    f-ceil  - f+rr     +0.088   +0.012 to +0.181   clears
    d-ceil  - d+rr     +0.080   +0.013 to +0.165   clears

  the headroom, which is the ceiling less the stage
  feeding it - what a better reranker could still be
  worth on that candidate set:

    from fused:  ceiling 0.942, first stage 0.759,
               headroom +0.182, of which this
               reranker took +0.095
    from dense:  ceiling 0.957, first stage 0.915,
               headroom +0.042, of which this
               reranker took -0.039

    q6: the fused ten cap any reranking at 0.739,
        and dense alone scores 0.860
```

**The scorer still cannot express an order, on a scale a hundred wide.** Four to seven distinct
scores for ten candidates, and 56 of the 80 candidates sit in a block with another candidate on
the same score. Inside such a block a stable sort keeps the order it was given, so part of every
reranked figure here is the first stage showing through. Chapter 44 ran both scales and found the
same thing on this one — three to eight distinct scores, with its tie range narrowing from 0.171
to 0.085 — so this confirms its result rather than testing it for the first time. And every score the model returned is a multiple of five, after an
instruction that asked for the whole range in so many words. **The instruction was followed in
part and not in the part that mattered** — the model used four to seven of a hundred available
values and every one of them a multiple of five. Chapter 42's rule is that a grammar can only
redirect where code can refuse; this is a rung below it, because prose is not even a grammar, and
a scale an instruction asks for is a scale you have to check rather than one you have.

**Reranking the fused ten is worth +0.095 and the interval contains zero**, from −0.022 to
+0.281. Reranking dense's ten is worth −0.039, also containing zero. So on this corpus the
reranker, at 105 model calls, buys nothing that can be told apart from nothing — and that is
Chapter 44's result again, from a different first stage and a different granularity.

**The ceiling is the row that says where the work is.** From the fused ten, the best any
reordering could reach is 0.942 against a first stage of 0.759: a headroom of +0.182, of which
this reranker took +0.095. From dense's ten the ceiling is 0.957 against 0.915, so the headroom
is +0.042 and there is almost nothing left to win. Both ceilings beat the reranked order by more
than zero with the interval clearing it, so **the candidate set still holds more than the
reranker extracted** in both cases.

**And one query settles which first stage to use.** For `q6`, the fused ten cap any reranking at
0.739 while dense on its own scores 0.860. No reranker at any price can reach, from that candidate
set, what the other first stage already had. That is Chapter 26's ceiling as a concrete
instruction rather than a caution: **the choice of first stage is a choice of ceiling**, and a
second stage cannot argue with it.

So the pipeline from here uses dense retrieval and no reranker. Nothing measured says the
reranker helps, one thing measured says the candidate set it was given is worse, and a stage you
cannot show to help is a stage to take out. **That is what measuring a stage is for** — it is
permission to delete one, and it is the cheapest result in this chapter.

## Step 5: Assemble One Request, and Write Its Trace

Chapter 28 owns the arithmetic of what fits and the three decisions inside it: how many passages,
in what order, and what the instruction asks for. Two of the three are made here the way Chapter
28's lab says. **The third is defaulted, and the chapter should say so rather than let it pass:**
the passages go in retrieval order, which Chapter 28 is explicit is one option and not an
instruction — *the order of the passages is a decision you are making whether or not you know
it*. Step 7 is where that costs something.

```python
"""The request: a context assembled under a budget, and one trace.

Chapter 28 owns the arithmetic and the THREE decisions inside it: how
many passages, in what order, and what the instruction asks for. Two
are made here rather than defaulted. The fill is by rank and it STOPS
at the first passage that does not fit, which is chapter 28's lab
step 3 - a greedy fill would silently promote short passages over the
ones ranked above them. The instruction goes in first and the
assembly refuses a budget too small to hold it. The third is
DEFAULTED: the passages go in retrieval order, which chapter 28 says
is one option and not an instruction.

Which ranking feeds this is a decision too, and step 4 made it:
dense retrieval on its own scored higher than the fused ranking and
higher than either reranked, so the reranker is not in the pipeline.
A stage you cannot show to help is a stage to take out, and that is
what measuring one is for.

One trace per request, chapter 33's fields, written to traces.json.
"""
import json
import os
import pathlib
import time
import urllib.request
import uuid

import index
import search
from key import queries

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
OUT = pathlib.Path("traces.json")
TIMEOUT = 120
BUDGET = 2500
STAGE = "dense"

INSTRUCTION = (
    "Answer the question using only the passages below. Quote the "
    "exact words you used from a passage, and give that passage's "
    "id. If none of the passages answers the question, say so. "
    "Reply as JSON: {\"answer\": \"...\", \"citations\": "
    "[{\"id\": \"...\", \"quote\": \"...\"}]}"
)


def build(question, order, budget=BUDGET):
    """Fill by rank and stop. Returns the passages kept, the ones not
    reached, and the room left over - which is the cost of stopping."""
    fixed = len(INSTRUCTION) + len(question)
    if fixed > budget:
        raise ValueError("no room for the instruction and the question")
    left = budget - fixed
    kept = []
    for i, cid in enumerate(order):
        block = f"[{cid}] {search.BY_ID[cid]['text']}\n"
        if len(block) > left:
            return kept, list(order[i:]), left
        kept.append(cid)
        left -= len(block)
    return kept, [], left


def context(question, kept):
    body = "\n".join(f"[{c}] {search.BY_ID[c]['text']}" for c in kept)
    return f"{INSTRUCTION}\n\n{body}\n\nQuestion: {question}"


def ask(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "max_tokens": 500, "temperature": 0,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def run():
    cache = search.vectors()
    out = []
    for qid, q in sorted(queries().items()):
        t0 = time.monotonic()
        order, scores = search.dense(q, cache)
        if STAGE == "fused":
            lex, _ = search.lexical(q)
            order, scores = search.fuse(lex, order)
        t1 = time.monotonic()
        kept, unreached, left = build(q, order)
        prompt = context(q, kept)
        d = ask(prompt)
        t2 = time.monotonic()
        try:
            reply = json.loads(d["choices"][0]["message"]["content"])
        except json.JSONDecodeError:
            reply = {"answer": d["choices"][0]["message"]["content"],
                     "citations": []}
        out.append({
            "request_id": uuid.uuid4().hex[:6],
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "query_id": qid,
            "question": q,
            "retrieval_query": q,
            "stage": STAGE,
            "candidates": [[c, round(scores[c], 4)]
                           for c in order[:10]],
            "passages_sent": kept,
            "room_left": left,
            "model": d["model"],
            "prompt_tokens": d["usage"]["prompt_tokens"],
            "output_tokens": d["usage"]["completion_tokens"],
            "finish_reason": d["choices"][0]["finish_reason"],
            "answer": reply.get("answer", ""),
            "citations": reply.get("citations", []),
            "retrieval_ms": round((t1 - t0) * 1000, 1),
            "model_ms": round((t2 - t1) * 1000, 1),
            "total_ms": round((t2 - t0) * 1000, 1),
            "verdict": None,
        })
    OUT.write_text(json.dumps(out, indent=1))
    return out


def traces():
    return json.loads(OUT.read_text()) if OUT.exists() else run()


def wrap(text, indent, hang=None, width=62):
    hang = indent if hang is None else hang
    out, line = [], indent
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line.rstrip())
            line = hang
        line += word + " "
    out.append(line.rstrip())
    return "\n".join(out)


if __name__ == "__main__":
    ts = traces()
    print(f"  budget {BUDGET} characters, of which the instruction")
    print(f"  is a fixed {len(INSTRUCTION)} and the question its"
          f" own length.")
    print(f"  Ranking: {STAGE}.\n")
    print("    query  sent  room left   in   out")
    for t in ts:
        print(f"    {t['query_id']}     {len(t['passages_sent']):3d}"
              f"     {t['room_left']:6d}  {t['prompt_tokens']:5d}"
              f" {t['output_tokens']:5d}")
    waste = [t["room_left"] for t in ts]
    print(f"\n  room left over: {min(waste)} to {max(waste)}"
          f" characters, mean")
    print(f"  {sum(waste) / len(waste):.0f} against a budget of"
          f" {BUDGET}. That is the cost of")
    print("  stopping rather than skipping.\n")

    print("  one whole request, which the next three steps read:\n")
    t = next(x for x in ts if x["query_id"] == "q3")
    for f in ("request_id", "query_id", "stage", "model",
              "prompt_tokens", "output_tokens", "finish_reason",
              "retrieval_ms", "model_ms", "total_ms"):
        print(f"    {f:15s} {t[f]}")
    print(wrap(t["question"], "    question       ",
               "                    "))
    print(f"    passages_sent   {len(t['passages_sent'])}:")
    for c in t["passages_sent"]:
        print(f"      {c}")
    print(wrap(t["answer"], "    answer         ",
               "                    "))
    for c in t["citations"]:
        print(f"    citation        {c.get('id')}")
        print(wrap(f"\"{c.get('quote', '')}\"", "                    "))
```

```text
  budget 2500 characters, of which the instruction
  is a fixed 258 and the question its own length.
  Ranking: dense.

    query  sent  room left   in   out
    q1       6        330    531   116
    q2      10          8    628    92
    q3       5         36    632    33
    q4       5        326    675    70
    q5       7         18    621    58
    q6       7         85    578   104
    q7      10         88    631    50
    q8      10         24    603    76

  room left over: 8 to 330 characters, mean
  114 against a budget of 2500. That is the cost of
  stopping rather than skipping.

  one whole request, which the next three steps read:

    request_id      2443cf
    query_id        q3
    stage           dense
    model           gpt-4o-mini-2024-07-18
    prompt_tokens   632
    output_tokens   33
    finish_reason   stop
    retrieval_ms    687.8
    model_ms        1207.6
    total_ms        1895.4
    question       How much does delivery cost to the
                    Scottish Highlands?
    passages_sent   5:
      delivery-exceptions#2
      awkward-pdf-p1#0
      delivery-fees#0
      international-delivery#0
      delivery-exceptions#4
    answer         9.50 pounds
    citation        delivery-exceptions#2
                    "9.50 pounds"
```

**The fill is by rank and it stops.** Chapter 28's greedy fill keeps any passage that fits in the
room left, which silently promotes a short passage over a longer one ranked above it; its lab
step 3 changes that to stopping at the first passage that does not fit, and says the honest cost
is the room left unused. Here that room is 8 to 330 characters, a mean of 114 against a budget of
2,500 — under five per cent, because 176 chunks with a median of 178 characters give the fill
small units to work with. **The cost of the safe behaviour is small when the passages are
small**, which is a fact about this chunking rather than about the rule.

**The instruction is a fixed 258 characters and goes in first**, and the assembly raises rather
than truncating if the budget cannot hold it. It asks for three things: answer only from the
passages, quote the exact words used and give the passage's id, and say so if none of them
answers. The third clause is the one Chapter 28 says changes which failure you get. The second is
what step 6 is built on.

**Then read the request the program prints, because it is the chapter in miniature.** `q3` asks
what delivery costs to the Scottish Highlands. Five passages were sent. The first is the
surcharge section of `delivery-exceptions`, the second is page 1 of the awkward PDF, and the
third is `delivery-fees#0` — which is the chunk holding `# Delivery charges` and nothing else.
**One of step 2's nine stub chunks is in the context**, occupying a rank, and the section that
gives the standard charge is not. The answer is `9.50 pounds`, with a sound citation.

9.50 is the surcharge. The question asked what delivery costs. **The reply is grounded, cited,
and wrong**, and the trace holds every field needed to say why.

**The trace is Chapter 33's**, with five fields this pipeline adds and two of Chapter 33's left
out. Added: the query id, which first stage was used, how much room the fill left, the finish
reason, and the citations as the model gave them. Left out: the user, because this lab has none,
and the tool calls, because it makes none — and dropping the user costs Chapter 33's *how many
users hit this?*, the one question on its list that no other field answers. Sixteen plus five
less two is nineteen. Chapter 33 says the decision about what a trace holds is a decision about what you can
measure later, and the three steps that follow are the proof: step 6 needs the citations, step 7
needs `passages_sent` and the answer, and step 8 needs the counts and the timings. Not one of them
re-runs the pipeline.

## Step 6: Check the Citations, and the Rule That Makes Them Checkable

Chapter 28's three mechanical checks are: does the cited document exist, is the quoted text in it,
and is it at the offset claimed. Chapter 28 ran them on five citations it wrote — one sound, three
failing a different check each, and one that passes every check and is still wrong, which is the
case its whole section is about. These are the ones a model produced.

```python
"""Chapter 28's three mechanical citation checks, on real replies.

Chapter 28 ran them on five citations it wrote: one sound, three
failing a different check each, and one that passes every check and
is still wrong. These are the ones a model produced, and the checks
are the same three in shape: does the cited thing exist, is the quoted text in it,
and is it where the citation says.

Two things make this harder than chapter 28's version and both are
the point. A quote is only "in" a passage under some rule about what
counts as the same text, which is chapter 41's answer normalisation
turning up where you would not expect it. And a chunk id is a place
in the index rather than in a document, so "where the citation says"
is a question about the stored locator: does it still find the text
it was recorded against.
"""
import re

import answer
import index
import search

ROWS = search.BY_ID


def loose(text):
    """What counts as the same text: markdown emphasis dropped and
    every run of whitespace made one space. A rule, written down,
    because the check cannot run without one."""
    return re.sub(r"\s+", " ", text.replace("**", "").replace("`", ""))


def locator_holds(cid):
    """Check three. The row recorded a document and an offset; this
    asks whether that offset still finds the text the row stored.
    It fails the moment the document, or the rule that stripped it,
    changes under you - which is chapter 33's warning."""
    row = ROWS[cid]
    body = index.body(row["doc"])
    at = row["start"]
    return body[at:at + len(row["text"])] == row["text"]


def where_in_doc(cid, quote, norm):
    """The quote's offset in the document, for a reader who wants to
    go and look. Measured in the normalised text, because that is the
    text the comparison was made in."""
    row = ROWS[cid]
    body = norm(index.body(row["doc"]))
    at = body.find(norm(quote))
    return None if at < 0 else at


def verdicts(trace, norm):
    out = []
    for c in trace["citations"]:
        cid, quote = c.get("id", ""), c.get("quote", "")
        if cid not in ROWS:
            out.append((cid, quote, "NO SUCH PASSAGE", None))
        elif norm(quote) not in norm(ROWS[cid]["text"]):
            other = [k for k, r in ROWS.items()
                     if norm(quote) in norm(r["text"])]
            out.append((cid, quote, "NOT IN IT"
                        + (f", IN {other[0]}" if other else ""), None))
        elif not locator_holds(cid):
            out.append((cid, quote, "LOCATOR STALE", None))
        else:
            out.append((cid, quote, "SOUND",
                        (ROWS[cid]["doc"],
                         where_in_doc(cid, quote, norm))))
    return out


def tally(ts, norm):
    return [(t["query_id"], cid, verdict, quote,
             cid in t["passages_sent"])
            for t in ts for cid, quote, verdict, _ in verdicts(t, norm)]


if __name__ == "__main__":
    ts = answer.traces()
    print(f"  {sum(len(x['citations']) for x in ts)} citations from"
          f" {len(ts)} replies, compared two ways:\n")
    strict = tally(ts, lambda s: s)
    rel = tally(ts, loose)
    print("    query  passage                    as given  by rule")
    for a, b in zip(strict, rel):
        print(f"    {a[0]}  {a[1]:26s} {a[2][:9]:9s} {b[2][:9]}")
    print(f"\n    sound: {sum(1 for r in strict if r[2] == 'SOUND')}"
          f" of {len(strict)} as given,"
          f" {sum(1 for r in rel if r[2] == 'SOUND')} by rule,"
          f" and {sum(1 for r in rel if not r[4])}")
    print("    citing a passage that was never sent\n")

    bad = next(r for r in strict if r[2] != "SOUND")
    print("  one that the first pass failed, against the passage")
    print("  it cites:\n")
    print(answer.wrap(f'quote:   "{bad[3][:70]}"', "    ",
                      "               "))
    print(answer.wrap(f'passage: "{ROWS[bad[1]]["text"][:70]}"',
                      "    ", "               "))

    left = [r for r in rel if r[2] != "SOUND"]
    print(f"\n  and the {len(left)} the rule does not rescue:\n")
    for r in left:
        print(answer.wrap(f'quote:   "{r[3][:66]}"', "    ",
                          "               "))
        print(answer.wrap(f'passage: "{ROWS[r[1]]["text"][:66]}"',
                          "    ", "               "))

    ok = [r for r in rel if r[2] == "SOUND"]
    base = ok[0]
    good, cid = base[3], base[1]
    print("\n  what the rule forgives. Four versions of one sound")
    print("  quote, under both comparisons:\n")
    edits = [("as the reply gave it", good),
             ("one digit changed", re.sub(r"\d", "7", good, count=1)),
             ("one word removed",
              good.replace(good.split()[3] + " ", "", 1)),
             ("the last three words cut",
              " ".join(good.split()[:-3]))]
    for name, text in edits:
        if name != "as the reply gave it":
            assert text != good, name
        print(f"    {name:24s} as given"
              f" {str(text in ROWS[cid]['text']):5s} by rule"
              f" {loose(text) in loose(ROWS[cid]['text'])}")

    print("\n  then check three. The offsets were recorded against")
    print("  text index.py produced under two stripping rules.")
    print("  Undo each in turn, change no document, ask again:\n")
    cited = {r[1] for r in rel}
    for label, header, footer in (("as indexed", True, True),
                                  ("footer kept", True, False),
                                  ("header kept", False, True)):
        index.STRIP_HEADER, index.STRIP_FOOTER = header, footer
        held = sum(1 for c in cited if locator_holds(c))
        stale = sum(1 for c in ROWS if not locator_holds(c))
        print(f"    {label:13s} cited locators holding"
              f" {held} of {len(cited)},")
        print(f"                  rows stale {stale} of {len(ROWS)}")
    index.STRIP_HEADER = False
    survived = [c for c in ROWS if locator_holds(c)]
    index.STRIP_HEADER = index.STRIP_FOOTER = True
    print(f"\n    the {len(survived)} that survive the header being"
          f" kept are")
    print(f"    {', '.join(survived)}: the PDF page, which")
    print("    never had a header")
```

```text
  9 citations from 8 replies, compared two ways:

    query  passage                    as given  by rule
    q1  returns-standard#1         NOT IN IT SOUND
    q1  returns-clearance#1        NOT IN IT SOUND
    q2  where-is-my-refund#1       NOT IN IT NOT IN IT
    q3  delivery-exceptions#2      SOUND     SOUND
    q4  product-kettle-hl-2208#0   NOT IN IT SOUND
    q5  refunds-policy#3           SOUND     SOUND
    q6  damaged-on-arrival#4       NOT IN IT SOUND
    q7  plan-harbour-plus#1        SOUND     SOUND
    q8  returns-clearance#1        NOT IN IT SOUND

    sound: 3 of 9 as given, 8 by rule, and 0
    citing a passage that was never sent

  one that the first pass failed, against the passage
  it cites:

    quote: "You may return a standard item within 30 days of
               delivery for any reas"
    passage: "## 1. The return window **You may return a
               standard item within 30 da"

  and the 1 the rule does not rescue:

    quote: "The longest an ordinary refund should take is
               about two and a half"
    passage: "Refunds are issued within 14 days of your
               return arriving at our w"

  what the rule forgives. Four versions of one sound
  quote, under both comparisons:

    as the reply gave it     as given False by rule True
    one digit changed        as given False by rule False
    one word removed         as given False by rule False
    the last three words cut as given False by rule True

  then check three. The offsets were recorded against
  text index.py produced under two stripping rules.
  Undo each in turn, change no document, ask again:

    as indexed    cited locators holding 8 of 8,
                  rows stale 0 of 176
    footer kept   cited locators holding 8 of 8,
                  rows stale 0 of 176
    header kept   cited locators holding 0 of 8,
                  rows stale 174 of 176

    the 2 that survive the header being kept are
    awkward-pdf-p1#0, awkward-pdf-p1#1: the PDF page, which
    never had a header
```

**The first pass says three of nine citations are sound — and five of the six failures are the
checker's fault.** Read one against the passage it cites and the reason is immediate: the passage
holds `**` around the sentence the document emphasises, and a line break where the markdown
wraps, and the reply dropped the first and turned the second into a space. The quote is faithful
in every way a person would judge faithful. The substring test is correct and useless.

**So the check needs a rule about what counts as the same text**, and that rule is Chapter 41's
answer normalisation turning up somewhere it was not expected. Written down — emphasis markers
dropped, runs of whitespace made one space, applied to both sides — eight of the nine pass.

**One still fails and it is a real one.** `q2`'s reply begins *The longest an ordinary refund
should take*; the document says *So the longest an ordinary refund should take*. One word dropped
and the next capitalised. That is a plausible edit rather than a quotation, which is
Chapter 28's second case produced by a model rather than written to fail.

**Then measure what the looser rule forgives, rather than trusting it.** Four versions of one
sound quote: as the reply gave it, passing under the rule and not as given; with one digit
changed, failing both; with one word removed, failing both; and with the last three words cut,
passing under the rule and still failing as given, because the emphasis markers are there either
way. **The rule forgives formatting and nothing else**, and the truncation passes it because a
substring test is what it is. Write the rule down and the verdicts mean something. Leave it
implicit and they are an accident of how the two texts happened to be stored.

**And the third check is not the one Chapter 28 ran, because a chunk id is not a place in a
document.** It is a place in the index. So the check asks whether the row's stored locator still
finds the text the row was recorded against — which is the failure Chapter 33 warns about, where
an id stops finding what was sent. It passes on everything so far, so the program breaks it on
purpose: undo each of the two stripping rules in turn, change no document, and ask again.

**Keeping the footer breaks nothing. Keeping the header leaves 2 of 176 locators standing**, and
the two are the PDF page, which never had a header. The difference is where the text sits. The
footer is at the end of a document, so putting it back shifts nothing before it. The header is at
the start, so putting it back shifts everything. **An offset survives a change downstream of it,
and a change upstream of it only while the length holds** — so replacing a header with another of
exactly the same length would break nothing, and that is the narrow case rather than the rule. It
is Chapter 27's claim about a parser, in the one place in this pipeline where it can be checked
with arithmetic.

> **Warning:** The practical form of that is unglamorous and expensive to learn late. The rules
> that produced the text you indexed are part of every locator you stored. Change how you strip,
> re-cut, or re-parse by anything that moves a character, and the offsets after the change are
> wrong — 174 of 176 here — with nothing to announce it: the
> citations still point at real documents, and they point at the wrong characters. Re-index when
> you change the rule, or store the quoted span as well as the offset so the two can be checked
> against each other.

**So the checks buy what Chapter 28 says they buy**: a reply that points at real text in a real
place. Three things got past them in this run, one of each kind. `q1` gave two sound citations for
one claim, the second quoting the fourteen-day clearance window the answer never mentions — a
sound citation attached to no statement at all. `q5`'s sound quote stands in for a question about
two documents disagreeing, and never mentions that they do. And `q7`'s citation is sound and its
quote ends in a colon: *Harbour Plus costs 29 pounds a year and includes:* — the list it
introduces is the next chunk, which was never sent. **Every check passes on a reply that answers
nothing.**

## Step 7: Measure the Two Halves, Then Change One Number

Chapter 32 scores every case twice — did the retrieved passages hold an answer at all, and was
the answer right — and turns one figure into four cells. Its forty cases were written out as
shapes. These are eight real ones.

```python
"""Chapter 32's two verdicts per case, on the eight replies.

Chapter 32's forty cases were written out as shapes. These are eight
real ones, and each carries two verdicts:

  R  did the passages that were SENT hold an answer at all
  A  was the answer the system gave right

R is mechanical for six of the eight, and only because index.py
wrote down the shortest passage that answers each query before any
chunk size was chosen: ask whether that passage is inside something
the context held. For q3 and q5 no single passage answers the
question, so R there is a judgement, and the chapter states its rule
beside the reason for every A. A is a judgement on every case. The
verdicts are data, as chapter 31 requires: no program here decides
one.

Relevance is a third column and it needs the QUESTION decomposed,
which chapter 32 is explicit is a judgement too. A part below is
something a reader asking the question needs and the corpus can
supply. They are listed so a reader can disagree with a part rather
than with a number.
"""
import json
import pathlib

import answer
import index
import search

TRACES = pathlib.Path("traces.json")

PARTS = {
    "q1": ("the standard window", "the clearance window"),
    "q2": ("how long it should take", "what to check"),
    "q3": ("the standard charge", "the surcharge"),
    "q4": ("what the product is",),
    "q5": ("which figure applies", "that two documents disagree"),
    "q6": ("tell us within 48 hours", "what to send",
           "do not return it yet"),
    "q7": ("what is included",),
    "q8": ("yes, and the window", "who pays the postage"),
}

# query: (R where judged rather than mechanical, A, parts answered)
VERDICTS = {
    "q1": (None, "Y", ("the standard window",)),
    "q2": (None, "Y", ("how long it should take",)),
    "q3": ("N", "N", ("the surcharge",)),
    "q4": (None, "Y", ("what the product is",)),
    "q5": ("Y", "N", ("which figure applies",)),
    "q6": (None, "N", ("do not return it yet",)),
    "q7": (None, "N", ()),
    "q8": (None, "Y", ("yes, and the window",)),
}


def mechanical_r(trace):
    """R where index.py's answer passage settles it."""
    want = index.ANSWERS[trace["query_id"]]
    if want is None:
        return None
    return "Y" if any(want in search.BY_ID[c]["text"]
                      for c in trace["passages_sent"]) else "N"


def scored(traces):
    out = []
    for t in traces:
        said, a, parts = VERDICTS[t["query_id"]]
        auto = mechanical_r(t)
        if auto and said and auto != said:
            raise SystemExit(f"  {t['query_id']}: the two Rs disagree")
        out.append({"qid": t["query_id"], "r": auto or said, "a": a,
                    "parts": parts,
                    "how": "the answer passage" if auto else "judged"})
    return out


def write_back(traces, rows):
    """Put each verdict into the trace that earned it. A trace with a
    verdict is an input, an output and a mark, which is chapter 20's
    case and chapter 33's reason for keeping the content fields."""
    for t, x in zip(traces, rows):
        t["verdict"] = f"R={x['r']} A={x['a']}"
    TRACES.write_text(json.dumps(traces, indent=1))


def cells(rows):
    return {(r, a): [x["qid"] for x in rows
                     if (x["r"], x["a"]) == (r, a)]
            for r in "YN" for a in "YN"}


if __name__ == "__main__":
    ts = answer.traces()
    rows = scored(ts)
    write_back(ts, rows)
    n = len(rows)
    c = cells(rows)

    print(f"  budget {answer.BUDGET}, ranking {answer.STAGE}.\n")
    print("    query   R   how R was decided    A")
    for x in rows:
        print(f"    {x['qid']}     {x['r']}   {x['how']:19s}  {x['a']}")

    right = len(c[("Y", "Y")]) + len(c[("N", "Y")])
    found = len(c[("Y", "Y")]) + len(c[("Y", "N")])
    print(f"\n  end to end: right on {right} of {n}"
          f"   {right / n:.1%}")
    print(f"  an answer was sent on {found} of {n}   {found / n:.0%}")
    print(f"  given that it was, right on {len(c[('Y', 'Y')])}"
          f" of {found}   {len(c[('Y', 'Y')]) / found:.0%}\n")

    labels = {("Y", "Y"): "fine",
              ("Y", "N"): "answer there, got it wrong",
              ("N", "N"): "answer not there, wrong",
              ("N", "Y"): "answer not there, right"}
    print("    cell                         count  which")
    for cell, label in labels.items():
        got = c[cell]
        print(f"    {label:28s} {len(got):4d}  "
              f"{', '.join(got) if got else '-'}")

    cache = search.vectors()
    print("\n  where the answer passage actually ranked:\n")
    print("    query  answer chunk ranked  passages sent")
    needed = {}
    for t in ts:
        qid = t["query_id"]
        want = index.ANSWERS[qid]
        if want is None:
            print(f"    {qid}    no single passage")
            continue
        order, _ = search.dense(t["question"], cache)
        held = next(c2 for c2 in order
                    if want in search.BY_ID[c2]["text"])
        rank = order.index(held) + 1
        needed[qid] = (rank, len(answer.INSTRUCTION)
                       + len(t["question"])
                       + sum(len(f"[{c2}] {search.BY_ID[c2]['text']}\n")
                             for c2 in order[:rank]))
        print(f"    {qid}    {rank:9d}            "
              f"{len(t['passages_sent']):9d}")

    print("\n  what reaching the two that were missed would cost:\n")
    for qid in ("q6", "q7"):
        rank, need = needed[qid]
        print(f"    {qid}  rank {rank}, so the budget must hold"
              f" {need} characters")
    worst = max(needed[q][1] - answer.BUDGET for q in ("q6", "q7"))
    print(f"    against the {answer.BUDGET} it had:"
          f" {worst} more at the most\n")

    print("  and what reaching them by chapter 28's neighbour")
    print("  expansion would cost instead. For each, whether the")
    print("  answer chunk sits next to one already sent:\n")
    extra = []
    for t in ts:
        qid = t["query_id"]
        want = index.ANSWERS[qid]
        if want is None or qid not in ("q6", "q7"):
            continue
        held = next(c2 for c2 in search.TEXTS
                    if want in search.TEXTS[c2])
        doc, n = held.split("#")
        sent = sorted(int(c2.split("#")[1]) for c2 in
                      t["passages_sent"] if c2.startswith(doc + "#"))
        near = [m for m in sent if abs(int(n) - m) == 1]
        block = len(f"[{held}] {search.TEXTS[held]}\n")
        need = max(0, block - t["room_left"])
        extra.append(need)
        print(f"    {qid}  {held} is next to"
              f" #{near[0] if near else '-'}, which was sent")
        print(f"        its block is {block} characters and"
              f" {t['room_left']} were left,")
        print(f"        so the budget needs {need} more")
    print(f"\n    one budget covers both at"
          f" {answer.BUDGET + max(extra)}, which is"
          f" {max(extra)} more,")
    print(f"    against the {worst} a deeper fill needs:"
          f" {worst / max(extra):.1f} times less\n")

    print("  parts of each question answered:\n")
    print("    query  parts  answered")
    t1 = tp = 0
    for x in rows:
        tp += len(PARTS[x["qid"]])
        t1 += len(x["parts"])
        print(f"    {x['qid']}     {len(PARTS[x['qid']]):d}"
              f"      {len(x['parts']):d}"
              f"   {', '.join(x['parts']) if x['parts'] else 'none'}")
    print(f"    all     {tp:2d}     {t1:2d}   {t1 / tp:.0%} of the"
          f" parts asked")
```

```text
  budget 2500, ranking dense.

    query   R   how R was decided    A
    q1     Y   the answer passage   Y
    q2     Y   the answer passage   Y
    q3     N   judged               N
    q4     Y   the answer passage   Y
    q5     Y   judged               N
    q6     N   the answer passage   N
    q7     N   the answer passage   N
    q8     Y   the answer passage   Y

  end to end: right on 4 of 8   50.0%
  an answer was sent on 5 of 8   62%
  given that it was, right on 4 of 5   80%

    cell                         count  which
    fine                            4  q1, q2, q4, q8
    answer there, got it wrong      1  q5
    answer not there, wrong         3  q3, q6, q7
    answer not there, right         0  -

  where the answer passage actually ranked:

    query  answer chunk ranked  passages sent
    q1            1                    6
    q2            3                   10
    q3    no single passage
    q4            3                    5
    q5    no single passage
    q6           11                    7
    q7           14                   10
    q8            2                   10

  what reaching the two that were missed would cost:

    q6  rank 11, so the budget must hold 3474 characters
    q7  rank 14, so the budget must hold 4616 characters
    against the 2500 it had: 2116 more at the most

  and what reaching them by chapter 28's neighbour
  expansion would cost instead. For each, whether the
  answer chunk sits next to one already sent:

    q6  damaged-on-arrival#1 is next to #0, which was sent
        its block is 162 characters and 85 were left,
        so the budget needs 77 more
    q7  plan-harbour-plus#2 is next to #1, which was sent
        its block is 500 characters and 88 were left,
        so the budget needs 412 more

    one budget covers both at 2912, which is 412 more,
    against the 2116 a deeper fill needs: 5.1 times less

  parts of each question answered:

    query  parts  answered
    q1     2      1   the standard window
    q2     2      1   how long it should take
    q3     2      1   the surcharge
    q4     1      1   what the product is
    q5     2      1   which figure applies
    q6     3      1   do not return it yet
    q7     1      0   none
    q8     2      1   yes, and the window
    all     15      7   47% of the parts asked
```

**The retrieval column is mechanical for six of the eight, and only because of step 2.** The
answer passages were written down before any chunk size was chosen, so the question *did the
passages sent hold an answer* becomes *is that passage inside something the context held*, which
is a substring test. For `q3` and `q5` no single passage answers the question, so those two are
judgements, and the rule for each is below. Every verdict in the answer column is a judgement.
The verdicts are data, as Chapter 31 requires: no program here decides one.

**Here are the reasons, because they are the part worth keeping.** Chapter 32 makes this point
about its own claim-level check — the share tells you how bad and the per-claim verdicts tell you
which sentence to fix — and it holds one level up, where the verdicts are per case and tell you
which case to fix.

| Case | A | Why |
|---|---|---|
| `q1` | right | 30 days, right for a standard item; silent on clearance, which it cited and did not use |
| `q2` | right | two and a half weeks, right; none of the four checks the document gives |
| `q3` | wrong | 9.50 is the surcharge, not the delivery cost. The standard charge never reached the context, so no passage sent holds a whole answer and R is N |
| `q4` | right | right |
| `q5` | wrong | both figures were in the context, so an answer is derivable from what was sent and R is Y. The reply asserts 14 days and never says the two disagree |
| `q6` | wrong | true and not the answer: the 48-hour window is the first thing to do and never reached the context |
| `q7` | wrong | a lead-in sentence and a colon. It names the price, which no part of the question asked for, and lists nothing |
| `q8` | right | 14 days, right; silent on who pays the postage |

**50 per cent end to end, and the four cells say what it cannot.** An answer was sent on five of
eight; given that it was, the reply was right on four of five. Three failures are retrieval's and
one is generation's. Chapter 20's caution applies to that ratio — one case in the generation cell
decides nothing, because a case is a row and the statistics count rows — so what makes this
actionable is not three against one. It is that the three retrieval failures have one shape.

**The diagnosis is the rank beside the fill.** For `q6` the passage holding the answer ranked
eleventh and the context reached seven. For `q7` it ranked fourteenth and the context reached ten.
**The first stage did rank it**, above a hundred and sixty others, and the assembly stopped short
of it.

That rules out the fix most people reach for. A reranker permutes a candidate set; step 4's was
the top ten, and both passages are outside it. **No reranker at any price could have put either
one in the context.** Chapter 26's ceiling, arriving as a diagnosis rather than as a caution — and
step 4 had already measured this reranker as worth nothing here, so this is the second independent
reason not to buy one.

**Two things can work, and the chapter's own figures say the cheaper one is the one step 2 pointed
at.**

**A deeper fill is the obvious one, and it is arithmetic.** Reaching rank eleven needs a budget of
3,474 characters and reaching rank fourteen needs 4,616, against the 2,500 the fill had: 2,116
more at the most. Chapter 28 says the candidate set is not sized by what fits in a window. This is
the other half of that — **what fits in the window is not sized by habit either**, and here the
number came out of a failure rather than out of a default.

**And the other is Chapter 28's neighbour expansion, which costs a fifth as much.** Look at which
chunks the two failing contexts already held. `q6`'s answer is `damaged-on-arrival#1`, and
`damaged-on-arrival#0` was sent — the row immediately before it. `q7`'s answer is
`plan-harbour-plus#2`, and `plan-harbour-plus#1` was sent, which is the row immediately before it
and also the one the reply quoted. So in both failures the passage that was missing sat next to a
passage that was already in the context, and the locator that finds it is the one every row has
carried since step 2.

The arithmetic is not close, and the program prints it. Expanding by one neighbour costs 162
characters for `q6` and 500 for `q7`, against room left of 85 and 88, so the budget needs 77 more
and 412 more — and one budget covers both at 2,912, which is **412 more against the 2,116 a deeper
fill needs: five times less, for the same two answers.** Compare the right things here: both
figures are a raise to the same single constant, which is why they can be compared at all. And
step 2 printed the reason the expansion works: two of the nine stub chunks are a line that introduces a list, with the list
in the next chunk, and `q7` is that exact shape in production — a reply that cited a lead-in and
had no list to read.

> **Note:** Expansion is not free and Chapter 28 says what it costs: it is blind, so it fetches
> what was adjacent rather than what is relevant, and Chapter 28 puts the cost exactly: expanding
> every hit by one neighbour halves how many separate hits the budget can hold. Chapter 28's own worked case expands the wrong way and gets the tail of one rule
> welded to the head of another. What makes it cheap *here* is a property of this corpus — short
> structural chunks with their continuation next door — and not a general discount.

**The chapter measures the deeper fill rather than the expansion**, for one reason worth stating
plainly: the budget is one number and the expansion is a change to `answer.py`, and a lab that
changes one number can show you the whole consequence in one run. That is a reason about this
chapter and not a recommendation. On this evidence the expansion is the better fix, and it is the
one to reach for first on your own data.

**Step 7a.** In `answer.py`, set `BUDGET = 5000`. Delete `traces.json`, run `answer.py`, and then
run `score.py` again.

*Expected result:* **the retrieval cell empties, three to zero**, and the end-to-end column goes
from four right to five. All three failures were where the measurement said they were, and the fix
closed all three *as retrieval failures* — which is not the same as getting three more answers
right, so do the arithmetic before reading on. `q6` now gives the 48-hour window and `q7` the five
inclusions in full, so those two are right. `q3`'s standard charge reached the context at last,
sixteen passages instead of five, and the reply is *still* `9.50 pounds`: it moved from the
retrieval cell to the generation cell without becoming right. Two answers gained, then.

*And one answer that was right is now wrong.* `q2` had the right figure on the smaller budget and
comes back with the other document's contradicting one on the larger — *most refunds are processed
within 30 days*, from the FAQ the rest of the corpus disagrees with. The corpus's planted disagreement now accounts for two
of the three remaining failures.

**Now look at what did and did not change, because the fill makes it unusually clean.** Fill by
rank and stop means a bigger budget can only append, and it does: at every one of the eight
queries the smaller run's passages are a prefix of the larger run's. For `q2` that is ten
passages becoming twenty-one. So the passage the reply switched
to was not newly arrived and was not promoted. `refunds-faq#1`, which says thirty days, sat at
rank 2 in *both* contexts — above `where-is-my-refund#1` at rank 3, which is the passage the
smaller run quoted. Eleven passages were appended and not one of them mentions thirty days.

**So nothing was displaced, nothing was reordered, and the two candidates held the same two
ranks.** The only thing that changed is how much other material sat around them. **That is
Chapter 16's finding in the cleanest form this pipeline could have produced by accident**: same
passages, same order, more of them, different answer. More in the window was not more of it used.

**And it is where step 5's defaulted decision comes due, though not in the way that promise
implied.** The order never varied, so it cannot be what moved the answer. What the default costs
is the follow-up: having never chosen an ordering, the pipeline has none to vary, so it cannot
ask whether putting `where-is-my-refund#1` first would have held the answer at twenty-one
passages. Defaulting a decision produced no wrong result here. It produced a question this lab
is unable to ask.

*So the cells move like this*, and the second column is a different system from the first:

| Cell | 2500 | 5000 |
|---|---|---|
| fine | 4 | 5 |
| answer there, got it wrong | 1 | 3 |
| answer not there, wrong | 3 | 0 |
| answer not there, right | 0 | 0 |
| an answer was sent | 5 | 8 |

**Every remaining failure is in the generation cell.** One to three. The problem did not shrink so
much as move halves, and the half it moved to is the one Chapter 28 is blunt about: order,
trimming and the instruction change what you can check rather than what the model does.

**Step 7b.** Put Chapter 20's paired bootstrap on the headline, because this is exactly the change
that feels like an improvement. Take the eight answer verdicts from each run as ones and zeros and
pass them to `search.paired`.

*Expected result:* four right becomes five, a paired difference of **+0.125 with 95 per cent from
−0.250 to +0.500**. Three of the eight cases changed verdict, two up and one down, and the
interval is three quarters of a point wide. **Contains zero: cannot tell.**

**So read the two results apart, because they are not equally strong.** The diagnosis held up and
it was close to mechanical — the retrieval column is a substring test on six of eight cases, and
that column went to zero. The verdict on whether the system got *better* does not survive eight
queries, and nothing about doubling the context changes that. Chapter 41 builds thirty labelled
cases from scratch, and this is what thirty are for.

> **Tip:** The sentence worth having ready is that the cell counts and the headline carry
> different weights of evidence. Which half is failing is a question about where a passage was,
> and a handful of cases can answer it. Whether a change helped is a question about a mean, and a
> handful of cases cannot. An interview answer that reports the second without the interval has
> given away the thing that makes the first one credible.

**And relevance is a third question that neither column asks.** Chapter 32 decomposes the question
as well as the answer, so the program lists the parts of each of the eight — something a reader
asking that question needs and the corpus can supply — and counts how many each reply addressed.
Seven of fifteen, 47 per cent, against four of eight answers counted right. Three of those four
leave a part of the question untouched: `q1` never mentions the clearance window, `q2` gives none
of the four checks its document offers, and `q8` is silent on who pays the postage. **A reply can
be right and partial**, which is why Chapter 32 keeps the two numbers apart.

**And one of the fifteen is where decomposing a question turned out to be harder than it looks.**
`q7` asks what Harbour Plus includes. The reply named the price and nothing else, and the price is
not what was asked — so *what it costs* is not a part of this question, and `q7` has one part
rather than two. That decision is why the denominator is fifteen and not sixteen, and getting it
wrong the other way would have credited the reply with half the question for answering none of it.
The parts are listed in the program rather than summarised for exactly this reason: a reader can
disagree with a part instead of with a percentage.

Run step 7a and the figure goes to eight of fifteen, 53 per cent — **six points while the
end-to-end column moves twelve and a half.**

## Step 8: Read Cost and Time Off the Trace

Everything above came out of files the pipeline wrote. So does this.

```python
"""What the traces say, which is the only place cost and time live.

Chapter 33 owns the trace and says what the decision inside it is.
This reads the eight the pipeline wrote and takes two things off
them: what a request cost and where the time went. Chapter 52 owns
latency in production, chapter 53 cost, and chapter 49 is the lab
that reduces either; this one only records the baseline they point
back to.

The baseline is in TOKENS. A token count is a property of the
request and does not move when a price list does, so money here is
a count multiplied by a price the reader supplies - the arithmetic
is the durable part and the price is not.
"""
import answer

# Units per million tokens. Chapter 6's convention: a placeholder, so
# that nothing in this book has to be right about a price list. Put
# your own contract's numbers here and the column below is money.
PER_M_IN, PER_M_OUT = 1.0, 4.0

def cost(t):
    return (t["prompt_tokens"] * PER_M_IN / 1e6
            + t["output_tokens"] * PER_M_OUT / 1e6)


if __name__ == "__main__":
    ts = answer.traces()
    print(f"  {len(ts)} traces, {len(ts[0])} fields each.\n")
    print("    query    in   out   retrieval   model   total")
    for t in ts:
        print(f"    {t['query_id']}    {t['prompt_tokens']:5d}"
              f" {t['output_tokens']:5d}"
              f"   {t['retrieval_ms']:8.0f}{t['model_ms']:8.0f}"
              f"{t['total_ms']:8.0f}")
    tin = sum(t["prompt_tokens"] for t in ts)
    tout = sum(t["output_tokens"] for t in ts)
    rms = sum(t["retrieval_ms"] for t in ts)
    mms = sum(t["model_ms"] for t in ts)
    print(f"    mean   {tin / len(ts):5.0f} {tout / len(ts):5.0f}"
          f"   {rms / len(ts):8.0f}{mms / len(ts):8.0f}"
          f"{sum(t['total_ms'] for t in ts) / len(ts):8.0f}")

    print(f"\n  the baseline, as counts rather than as money:\n")
    print(f"    {tin / len(ts):.0f} input and {tout / len(ts):.0f}"
          f" output tokens a request")
    print(f"    {tin / tout:.1f} input tokens for every output one")
    print(f"    at {PER_M_IN} and {PER_M_OUT} units per million,"
          f" {sum(cost(t) for t in ts) / len(ts) * 1000:.3f} units")
    print("    a thousand requests - and that last line is the only")
    print("    one here a price list can falsify")
    ci = tin * PER_M_IN
    co = tout * PER_M_OUT
    print(f"    of which the input is {ci / (ci + co):.0%} and the"
          f" output {co / (ci + co):.0%}\n")

    print(f"  time: retrieval {rms / (rms + mms):.1%},"
          f" the model {mms / (rms + mms):.1%}. Retrieval is")
    print("  a network call too, because the dense search embeds the")
    print("  query; the cosine over 176 vectors is arithmetic in")
    print("  Python and the round trip is not.\n")

    content = {"question", "retrieval_query", "answer", "citations",
               "passages_sent"}
    print(f"  chapter 33's decision on this trace."
          f" {len(content)} of {len(ts[0])}")
    print("  fields hold text somebody typed or that came out of")
    print("  the documents:\n")
    print("    " + ", ".join(sorted(content)))
```

```text
  8 traces, 19 fields each.

    query    in   out   retrieval   model   total
    q1      531   116        676    2240    2916
    q2      628    92        364    1855    2219
    q3      632    33        688    1208    1895
    q4      675    70        758    1542    2300
    q5      621    58        527    1448    1974
    q6      578   104        371    1905    2276
    q7      631    50        658    1494    2152
    q8      603    76        603    1751    2354
    mean     612    75        581    1680    2261

  the baseline, as counts rather than as money:

    612 input and 75 output tokens a request
    8.2 input tokens for every output one
    at 1.0 and 4.0 units per million, 0.912 units
    a thousand requests - and that last line is the only
    one here a price list can falsify
    of which the input is 67% and the output 33%

  time: retrieval 25.7%, the model 74.3%. Retrieval is
  a network call too, because the dense search embeds the
  query; the cosine over 176 vectors is arithmetic in
  Python and the round trip is not.

  chapter 33's decision on this trace. 5 of 19
  fields hold text somebody typed or that came out of
  the documents:

    answer, citations, passages_sent, question, retrieval_query
```

**The baseline is 612 input and 75 output tokens a request**, 8.2 in for every one out. That ratio
is the shape of a retrieval system: the question is short, the answer is short, and the passages
are neither. Chapter 1's rule still holds — a reply costs more per token, four against one in both
its arithmetic and this program's — and the ratio is what decides which half of the bill is
bigger. At 8.2 to 1 the input is 67 per cent of the cost here, against 56 per cent in Chapter 1's
example, where the ratio was 5 to 1 — and Chapter 1 counts in words rather than tokens on purpose,
because it comes before the tokeniser. **So retrieval pushes the bill towards the half you did not
write**, and a page of standing instructions is a smaller share of a context full of passages than
of one that holds only a question.

**The baseline is in tokens and not in money, and that is deliberate.** A token count is a
property of the request and does not move when a price list does. Money is that count times a
price, so the program takes the price as a parameter with Chapter 6's convention — a placeholder,
so that nothing in this book has to be right about a price list — and the output marks the one
line a price list can falsify. [**Chapter 53 owns cost**]{.noindex}, Chapter 52 latency, and Chapter 49 is the
lab that reduces either. This chapter records what they point back at.

**Time: a quarter in retrieval and three quarters in the model.** The quarter is worth
understanding before anyone optimises it, because the name is misleading. The cosine over 176
vectors is arithmetic in Python and takes no measurable time; what takes 581 milliseconds on
average is embedding the query, which is a network round trip to the same provider. **So this
pipeline makes two calls per request and the trace was recording them as one stage.** Chapter 52
is where that distinction decides what to cache — and a figure that attributes a network wait to
an index is the kind of figure that sends a team to the wrong library.

**And now price step 7's fix, which is what a baseline is for.** Run `trace.py` after step 7a and
the mean input goes from 612 tokens to 1,212, a factor of 1.98, while the mean total time moves
from 2,261 milliseconds to 2,366 — inside five per cent. **Double the bill, for a net one answer
and an interval that contains zero.** Both halves of that trade came off the same two files, so
nothing had to be estimated, and the decision it supports is a decision rather than a hunch.

> **Note:** Doubling the input and not the time is a result about this model, this length and this
> day, and it is the sort of thing Chapter 15 explains from the inside: reading the input is one
> pass and writing the reply is one pass per token, so a context that doubles while the reply
> stays short adds little to the wait. A context ten times longer would not be free, and what the
> trace gives you is the measurement rather than the expectation.

**Then Chapter 33's decision, on this trace.** Five of the nineteen fields hold text somebody
typed or that came out of the documents. Drop them and this step's figures all survive, because
every one of them is a count or a timing; so does step 7's retrieval column, because an id answers
*was the answer chunk retrieved* with no text at all. What stops being answerable is why the reply
said what it said, and whether a case can become a regression case — which is every verdict in
step 7 and every example in step 6.

**One field is worth looking at twice, and it is `passages_sent`.** Chapter 33 already counts it
as content, and this is the argument for why: it holds ids rather than text, so it reads like
metadata and looks as though it would survive a content-free trace. But step 6 left 2 of 176
locators standing by changing one rule in the indexing step, and an id resolves against whatever
the index currently says. **An id is a promise about a document you still have**, and about a rule you have
not changed. Chapter 33 names the whole document as the field to think twice about for the same
reason; this pipeline shows the smaller version of it.

**Finally, the loop closes where Chapter 33 says it does.** `score.py` wrote a verdict against
each request, so each trace is now an input, an output and a mark. Chapter 20 defines a case as an
input plus whatever marks the answer right or wrong, and Chapter 33 is what keeps the output
beside it. Eight of them are not a regression set. They are the first eight rows of
one, and Chapter 46 is where forty become a method.

## Summary, Key Terms, and Review Questions

### Summary

Eight programs, one corpus, one traced request per query, and the stages measured apart.

**Parsing loses what no later stage can restore, and the shape of the loss belongs to the
parser.** The corpus declares the PDF's planted defects and this parser produced different ones
from the parser the corpus README records. The surcharge table came out as five areas, then five
postcode ranges, then five charges — thirteen lines from the first area to its own charge, every
figure intact and every row gone — where the README's extraction splices `9.50` into a postcode
and shifts a column. Three kern pairs came out with a space inside the word, so `PA20` is on the
page and not in the text, which is Chapter 43's identifier failing a different way. And page 2
returned zero characters with no error: of its two facts, `5.50` is nowhere else in the forty
documents and `Dunmore` is in one that says something adjacent and not the same, so skipping the
page loses one fact and leaves a second looking settled.

**Then the check that decides whether the rest can work.** 176 chunks, cut on structure with a
700-character cap that caught only two of them, and nine chunks under twenty characters — six a
heading alone, two a line introducing a list, one a single full stop. Each is a row retrieval can
return and nobody can use; step 5 sent two of them and step 3 shows one WINNING a rank, because a
five-term chunk matching a common word is rewarded for its shortness. Chapter 27's step 5, run
with the **answer
passages** written down first, says six of eight queries have a chunk holding a whole answer.
The two that do not are planted: one needs a charge from one document and a surcharge from
another, and one asks which of two disagreeing documents to believe.

**Retrieval over chunks needs the key's unit decided before any measure.** The key judges
documents, so the chunks are [**rolled up**]{idx="roll-up"} — best-ranked chunk stands for its document,
duplicates dropped — and the PDF is dropped from every figure because nothing judged it, which is
a hole in the denominator rather than a caution about one. Dense beats lexical by +0.311 recall@5
and +0.369 nDCG@5 and fusion beats lexical by +0.192 and +0.213, all four intervals clearing zero
and all four larger than Chapter 44's over whole documents. **And fusion loses to dense**, −0.120
and −0.156, both clearing zero, where Chapter 26 refused the verdict and Chapter 44 reported
*cannot tell* at −0.017 and −0.028. That is a verdict about this corpus, these eight queries and
this granularity, and the mechanism — RRF gives each list an equal vote and a weak vote costs more
the better the other list is — says why it would not transfer. **Chunking itself helped dense**, +0.052 nDCG
over whole documents with 95 per cent from +0.001 to +0.117, and **hurt fusion** on recall, −0.104
from −0.208 to −0.031, while its effect on lexical cannot be told from zero on either measure.
The lexical half is where the weakness is, and `q4` is where the obvious explanation is wrong:
the rare term got *more* discriminating, 2.7973 over forty documents to *4.2599* over 176
chunks, and what broke is the other half of the formula — the average length fell from 161.8
terms to 37.7, so `## 2. What is not covered` at five terms outscores the kettle's 107-term page,
which lands eighth — and on `q7` one of step 2's nine stubs, the fourteen-character
`# Harbour Plus`, takes rank one outright. **A short chunk can win a rank on a common word
alone.**
**Two intervals sit either side of one tie**: dense chunks against documents has six ties and
cannot clear zero though its two differences are +0.125 and +0.250, while fusion against dense has
five and does. The near end is pinned at zero while `\((t/n)^n \ge 0.025\)`{=latex} and no
difference has the other sign — at eight queries that is six ties, so three queries must move
before a one-sided difference can be established at all. The fused figure is the range 0.759 to
0.784, and dense's 0.915 is outside it.

**Reranking bought nothing that can be told from nothing**, +0.095 from the fused ten with the
interval straddling zero and −0.039 from dense's. Four to seven distinct scores for ten
candidates on a scale a hundred wide, every score a multiple of five after an instruction asking
for the whole range: **the instruction was followed in part, and not in the part that
mattered.** The ceiling is the row that matters —
0.942 against a fused first stage of 0.759 and 0.957 against dense's 0.915 — and for `q6` the
fused ten cap any reranking at 0.739 while dense alone scores 0.860, so **the choice of first
stage is a choice of ceiling** and no second stage can argue with it. Nothing measured said the
reranker helped, so it is not in the pipeline: **measuring a stage is permission to delete one.**

**The request is Chapter 28's arithmetic with two of its three decisions made and the third
defaulted.** Fill by rank and stop, which
left 8 to 330 characters unused against a 2,500 budget — a small price here because the chunks
are small. The instruction is a fixed 258 characters, goes in first, and asks for a quote and an
id. And the printed request is the chapter in miniature: `q3` sent five passages, one of them a
stub chunk holding `# Delivery charges`, and answered `9.50 pounds` with a sound citation. 9.50 is
the surcharge. **The reply is grounded, cited and wrong.**

**The citation checks need a rule before they mean anything.** Three of nine sound as the strings
stand, and five of the six failures are the checker's: the passage carries markdown emphasis and a
line break the reply dropped. With the rule written down — emphasis dropped, whitespace
collapsed, both sides — eight of nine pass, and the one that does not is real, a reply that
dropped one word and capitalised the next. The rule forgives formatting and nothing else: a
changed digit and a removed word both still fail, and a truncated quote passes because a
substring test is what it is. **And the third check is about the locator**, because a chunk id is
a place in an index. Undo the footer stripping and nothing breaks; undo the header stripping and
2 of 176 locators survive, the two being the PDF page that never had one. **An offset survives a
change downstream of it, and a change upstream of it only while the length holds.** Three things
got past every check: a
sound citation attached to no statement, a sound quote standing in for a disagreement it never
mentions, and a sound quote ending in a colon whose list was never sent.

**Then the two halves, and the diagnosis is stronger than the headline.** Four of eight right end
to end; an answer was sent on five of eight; right on four of five given that it was. Three
failures retrieval's, one generation's — and what makes it actionable is that the three share a
shape: the answer passage ranked eleventh and fourteenth while the context reached seven and ten.
A reranker permutes a candidate set of ten, so **no reranker could have reached either**. Two
things could. A budget of 3,474 and 4,616 characters, which is 2,116 more at the most — and
**Chapter 28's neighbour expansion for 412**, because in both failures the missing passage sat in
the row immediately after one the context already held, and `q7`'s reply had quoted that very row.
Five times less, for the same two answers, and step 2 had printed the shape of it: two stub
chunks are a lead-in whose list is in the next chunk. The chapter measures the budget because it
is one number and shows its whole consequence in one run, which is a reason about a lab rather
than a recommendation. Set the budget to 5,000 and
**the retrieval cell empties, three to zero** — as retrieval failures, which is not three more
right answers: `q6` and `q7` become right and `q3` moves to the generation cell still answering
`9.50 pounds`. And `q2`, which had been right, returns the contradicting document's figure
instead, so the planted disagreement accounts for two of the three remaining failures, all of
them now in the generation cell. The headline moves from four to
five: +0.125, 95 per cent from −0.250 to +0.500, **contains zero: cannot tell.** The retrieval
column is a substring test on six of eight cases and went to zero; the verdict on whether the
system improved does not survive eight queries. Relevance, with each question decomposed into
parts, is 7 of 15 against four of eight answers counted right, and goes to 8 of 15 on the larger
budget — **six points while the headline moves twelve and a half.**

**And the trace is where cost and time live.** 612 input and 75 output tokens a request, 8.2 in
for every one out, which puts the input at 67 per cent of the bill against Chapter 1's 56 at a
ratio of 5 to 1. The baseline is in **tokens**, because a count does not move when a price list
does. A quarter of the time is in retrieval and the quarter is a network round trip to embed the
query rather than anything the index did — **two calls a request, recorded as one stage.** The
step-7 fix doubled the input, 612 tokens to 1,212, and left the latency within five per cent, for
a net one answer and an interval containing zero. Five of nineteen fields are content; drop
them and every count, timing and retrieval verdict survives while every reason disappears. And
`passages_sent` is the field to argue about: it holds ids, so it looks like metadata, and step 6
left 2 of 176 locators standing by changing one rule. **An id is a promise about a document you
still have.**

### Key Terms

| Term | Meaning |
|---|---|
| **Answer passage** | The shortest passage that answers one of your questions, read out of the documents and written down *before* a chunk size is chosen. It is what turns "did retrieval work" into a substring test instead of an opinion |
| **Roll-up** | Mapping retrieved chunks back to their documents, letting the best-ranked chunk stand for its document and dropping duplicates. What lets a document-level key score a chunk-level index, and what a user is shown anyway |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The first step of a pipeline | Parse, then read the output against the page. The defect you get belongs to the parser as much as to the file: two parsers gave this one page two different wrong answers |
| What a scanned page costs | Zero characters and no error. Check whether its facts are anywhere else: one of this page's two was in no other document, and one was in a document that says something adjacent and not the same |
| Running Chapter 27's chunk-size check | Write the answer passages down first, then ask whether one chunk holds each whole. Six of eight here; the two that failed were a split answer and a contradiction, neither a chunking defect |
| Scoring a chunk index against a document key | Roll up to documents, best rank wins, duplicates dropped — and drop anything the key never judged, which here was the whole PDF. Lifting a document's grade onto each of its chunks instead caps recall@k by the chunking |
| When a paired interval cannot clear zero | With `\(t\)`{=latex} of `\(n\)`{=latex} queries tied and no difference of the other sign, the near bound is pinned at zero while `\((t/n)^n \ge 0.025\)`{=latex}. At eight queries that is six ties, so three queries must move. Three of this chapter's comparisons are one-sided: two clear zero with five ties and one is pinned with six. It says nothing about a comparison whose differences have both signs |
| The two fixes for a passage that ranked below the fill | A deeper budget, or Chapter 28's neighbour expansion. Both are a raise to the same budget: 2,116 against 412 for the same two answers, because both missing passages sat in the row after one already sent |
| What a reranker cannot do | Reach outside its candidate set. The two failures here ranked 11th and 14th against a candidate set of 10, so no reranker at any price could have fixed either |
| The choice of first stage | A choice of ceiling. One query's fused candidate set capped any reranking at 0.739 while dense alone scored 0.860 |
| Why measure a stage | To be allowed to delete it. The reranker's gain here straddled zero at 105 model calls, so it is not in the pipeline |
| What a citation check needs first | A written-down rule for what counts as the same text. Without one, 5 of the 8 true citations failed on markdown emphasis and a line break; with one, 8 of 9 passed and the survivor was a real plausible edit |
| What a stored offset survives | A change downstream of it, and one upstream only if the length holds. Keeping the footer broke nothing; keeping the header left 2 of 176 locators valid |
| Diagnosis against verdict | Which half is failing is a question about where a passage was, and eight cases can answer it. Whether a change helped is a question about a mean, and eight cases gave −0.250 to +0.500 |
| The durable cost baseline | A token count, not money. 612 in and 75 out a request here, 8.2 to 1, which is 67 per cent of the bill on the input |
| Where a retrieval system's time goes | Three quarters in the model and a quarter embedding the query — a network call, not the index. Two calls a request |

### Review Questions

1. Walk me through something you built end to end, and tell me the numbers you got.
2. Your end-to-end accuracy is 50 per cent. What do you do next?
3. You add a reranker and nothing improves. What would you have measured first?
4. Your replies cite passages and every citation check passes. What is still broken?
5. You doubled the context and accuracy went up. What would you need before reporting that?

### Review Answers

1. Forty short documents, eight queries with a graded key, and one deliberately awkward PDF, run
through eight stages with a trace per request. **Start with the parsing, because nothing
downstream repairs it.** The PDF's surcharge table came out as five areas, then five postcode
ranges, then five charges, thirteen lines from the first area to its own charge — every figure
intact and every row gone — and a different parser on the same page splices a charge into a
postcode instead, so the defect belongs to the parser as much as to the file. Page 2 is a scan and
returned zero characters with no error, and one of its two facts is in no other document. Then
176 chunks, with the answer passages written down first: six of eight queries have a chunk holding
a whole answer, and the two that do not are a split answer and two documents disagreeing.
**Retrieval: dense beat lexical and beat fusion**, 0.915 nDCG@5 against 0.546 and 0.759, with
both differences clearing a paired interval — and fusion losing to dense is the row Chapter 44
could not call. **The reranker bought nothing**,
+0.095 with the interval straddling zero over 105 model calls, so it is not in the pipeline — and
the candidate set's ceiling was 0.942 against a first stage of 0.759, so the headroom was there
and the reranker did not take it. **End to end, four of eight right**: an answer was sent on five
of eight, and the reply was right on four of five given that it was. The three retrieval failures
had one shape — the answer passage ranked eleventh and fourteenth while the context reached seven
and ten — so a bigger fill could reach them and no reranker could. Raising the budget emptied the
retrieval cell and broke one answer that had been right, for a headline of five of eight with an
interval from −0.250 to +0.500. **612 input and 75 output tokens a request**, 8.2 to 1, a quarter
of the latency in a round trip to embed the query. The thing I would say last is the thing I would
want asked about: the diagnosis was near-mechanical and the verdict was not, and eight queries is
not an evaluation set.
2. Score the same cases twice and read the four cells, which takes an afternoon and decides where
a month goes. One verdict per case cannot say which half failed; two can. Did the passages that
were *sent* hold an answer at all, and was the answer right. In this pipeline 50 per cent end to
end was an answer sent on five of eight and right on four of five given that it was — three
retrieval failures and one generation failure, and the single figure said neither. **Then do the
thing that makes the retrieval column cheap**: write down, for each question, the shortest passage
that answers it, and the column becomes a substring test over what was sent rather than a
judgement. **And do not stop at the ratio.** Three against one is four cases and settles nothing
on its own; what was actionable here was that the three failures shared a shape. The answer
passage had ranked eleventh and fourteenth while the context reached seven and ten, which rules
out a reranker — it permutes a candidate set of ten and both were outside it — and prices the two
fixes that do work: 2,116 more characters of budget, or Chapter 28's neighbour expansion for 412,
since both missing passages sat in the row after one the context already held. Last, check the cell everybody skips:
right answer, no supporting passage. There were none here, and if there had been they would be
failures rather than successes, because nothing in the system could show where the answer came
from.
3. **The ceiling of the candidate set you are feeding it**, before buying anything. A reranker can
only permute what the first stage handed it, so the most it can be worth is the gap between what
that stage scores and what the best possible reordering of the same candidates scores. Here that
was +0.182 from the fused ten and +0.042 from dense's: on the second one there was nearly nothing
to win and no reranker could have changed that. **Then two things about the scorer itself.** Count
its distinct scores: asked for nought to a hundred it returned four to seven distinct values for
ten candidates, 56 of 80 candidates sitting in a block with another on the same score, and inside
such a block a stable
sort keeps the order it was given — so part of the reported gain is the stage the reranker was
meant to improve. And put Chapter 20's paired interval on the difference, because +0.095 with an
interval from −0.022 to +0.281 is not an improvement, it is a measurement that cannot tell.
**Finally, check the failures you actually have against the candidate set's depth.** Two of the
three here were at ranks eleven and fourteen, outside a candidate set of ten, so five more
candidates were worth more than any reranker — which is the same arithmetic the ceiling gives, read
the other way.
4. Three things, and this run had one of each. **A sound citation attached to no statement**: one
reply made one claim and gave two citations, the second quoting a fourteen-day window the answer
never mentions. **A sound quote standing in for a question it does not answer**: another reply was
asked whether a refund takes fourteen days or thirty, had both documents in its context, quoted
one correctly and never said they disagree. **And a sound quote that answers nothing**: a citation
whose quote ends in a colon, introducing a list that was in the next chunk and never sent. Every
mechanical check passed on all three, which is Chapter 28's point — the checks establish that a
reply points at real text in a real place, and not that the text entails the claim. Two more
things are broken before any of that, and both are about the checker. **It needs a written rule
for what counts as the same text**, because five of the eight true citations failed a plain
substring test over markdown emphasis and a line break, and the rule has to be measured for what it
forgives rather than trusted: this one forgives formatting, fails a changed digit and a removed
word, and passes a truncation. **And a stored offset only means something under the rules that
produced the text it was measured against**: changing one stripping rule in the indexing step left
2 of 176 locators valid, with no document changed and nothing to announce it.
5. **The interval, the cell counts and the cost, and the interval is the one that decides whether
to report it at all.** Doubling the context here took four of eight right to five of eight: a
paired difference of +0.125 with 95 per cent from −0.250 to +0.500, three cases changing verdict,
two up and one down. That contains zero, so the honest report is that the change cannot be told
from no change on this set, and eight queries is the reason — Chapter 41 builds thirty for exactly
this. **Then the cells, because they moved decisively where the headline did not**: the retrieval
cell went from three to zero, which is the diagnosis confirmed, and the generation cell went from
one to three, so the problem moved halves rather than shrinking. That is worth reporting and it is
a different claim from "accuracy improved". **Then look for what broke**, because a change that
helps on average usually costs something: one answer that had been right came back with a
contradicting document's figure, which is Chapter 16's finding that more in the window is not
reliably more of it used. **And then the cost**: input tokens went from 612 to 1,212 a request, a
factor of 1.98, with latency inside five per cent. So the full report is a doubled bill, a
diagnosis confirmed, one regression, and a headline that cannot be told from zero — which is a
useful thing to know and not an improvement to announce.

> **You understand this when** you can name, for a pipeline of yours, the one stage whose failures
> no later stage can repair — and say which of your own numbers is a diagnosis you would defend
> from eight cases and which is a verdict you would not.
