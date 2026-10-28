# Parsing, Chunking and Indexing Your Documents

Chapter 25 listed the failures of dense retrieval and handed one of them here: documents too
long or badly split to match. That one is not a limit of retrieval at all. It is a limit of the
machinery that turns your files into things retrieval can see, and this chapter is about that
machinery — what a parser really gives you, what a chunk boundary decides, and why some
questions have no single passage that answers them, before any model is chosen.

*The problem.* I pointed the thing at my PDFs and the answers are nonsense, even though the
answer is definitely in there.

*The question.* What happens to a document between the file on disk and the thing a search
returns, and which of those steps can ruin it?

## A Page Is Not Text

**Parsing** is turning a file into the text a program can work on. The word sounds like a
solved problem, and for a plain text file it is. For the formats documents actually arrive in it
is not, and the reason is worth seeing rather than being told.

A PDF page does not contain a paragraph. It contains instructions for putting marks on paper.
The text ones say, in effect, *put this string at this position in this font* — and that is all.
There is no sentence, no paragraph, no column, no reading order. The program below writes two
PDFs to make the point concrete.

```python
"""Write two PDFs that LOOK identical and are drawn in different orders."""
import pathlib

# A two-column page. Each entry is (x, y, text). The left column is the
# refund policy; the right column is the cancellation policy. They are two
# different policies that happen to sit side by side.
LEFT = [
    (60, 700, "Refund policy"),
    (60, 680, "A refund is issued to the"),
    (60, 660, "original payment method"),
    (60, 640, "within 14 days, in full."),
]
RIGHT = [
    (320, 700, "Cancellation policy"),
    (320, 680, "A cancellation after"),
    (320, 660, "dispatch carries a fee"),
    (320, 640, "of 10 per cent."),
]

def content_stream(items):
    parts = ["BT", "/F1 11 Tf"]
    for x, y, text in items:
        parts.append(f"1 0 0 1 {x} {y} Tm ({text}) Tj")
    parts.append("ET")
    return "\n".join(parts).encode()

def write_pdf(path, items):
    stream = content_stream(items)
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
        + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    pathlib.Path(path).write_bytes(out)
    return len(out)

if __name__ == "__main__":
    # Drawn one column at a time.
    n1 = write_pdf("bycolumn.pdf", LEFT + RIGHT)
    # Drawn one ROW at a time, across both columns. Same page to look at.
    rows = []
    for left, right in zip(LEFT, RIGHT):
        rows.append(left)
        rows.append(right)
    n2 = write_pdf("byrow.pdf", rows)
    print(f"  bycolumn.pdf  {n1} bytes")
    print(f"  byrow.pdf     {n2} bytes")
    print("\n  Both place the same eight strings at the same eight")
    print("  positions. Printed, they are the same page. The only")
    print("  difference is the order the strings were written in.")
```

```text
  bycolumn.pdf  917 bytes
  byrow.pdf     917 bytes

  Both place the same eight strings at the same eight
  positions. Printed, they are the same page. The only
  difference is the order the strings were written in.
```

Both files are real PDFs — open them and you will see two columns of text. The `Tm` operator
sets a position and `Tj` draws a string there. The sequence of those instructions is the
**content stream**, and the order of the stream is the order the marks were made, which has
nothing to do with the order a person reads them in.

**That gap is the whole subject.** A **reading order** is a human fact about a page. The file
records positions. Recovering one from the other is a guess, and the next section shows three
different guesses giving three different documents.

> **Note:** This is PDF, chosen because it is the format that arrives most often and because
> its text can be reached in a few lines. The specific operators are a dated detail and other
> formats differ: a word processor's format does store a paragraph order, and HTML stores a
> document tree. What transfers is the shape of the problem — a file records *presentation*, and
> the text you want is something you reconstruct from it.

## Three Readings of One Page

```python
"""Three ways to read the same page, and three different texts."""
import pathlib
import re

def pieces(path):
    """Every string the page draws, with where it was drawn."""
    raw = pathlib.Path(path).read_bytes().decode("latin-1")
    found = []
    for m in re.finditer(r"1 0 0 1 (\d+) (\d+) Tm \((.*?)\) Tj", raw):
        x, y, text = int(m.group(1)), int(m.group(2)), m.group(3)
        found.append((x, y, text))
    return found

def in_stream_order(items):
    return [t for _, _, t in items]

def by_position(items):
    # Top to bottom, then left to right. The obvious fix, and on a
    # two-column page it reads straight across the gap.
    return [t for _, _, t in sorted(items, key=lambda p: (-p[1], p[0]))]

def by_column(items, gap=100):
    # Group by x first: a jump of more than `gap` starts a new column.
    xs = sorted({x for x, _, _ in items})
    columns, current = [], [xs[0]]
    for x in xs[1:]:
        if x - current[-1] > gap:
            columns.append(current)
            current = [x]
        else:
            current.append(x)
    columns.append(current)
    out = []
    for col in columns:
        block = [p for p in items if p[0] in col]
        out += [t for _, _, t in sorted(block, key=lambda p: -p[1])]
    return out

def wrapped(text, width=56, pad="      "):
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(pad + line)
            line = word
        else:
            line = f"{line} {word}".strip()
    out.append(pad + line)
    return "\n".join(out)

if __name__ == "__main__":
    for path in ("bycolumn.pdf", "byrow.pdf"):
        items = pieces(path)
        print(f"  === {path} ===")
        for name, fn in (("stream order", in_stream_order),
                         ("by position", by_position),
                         ("by column", by_column)):
            print(f"    {name}:")
            print(wrapped(" ".join(fn(items))))
        print()

    print("  Same page, three readings, and the by-position one welds")
    print("  the two policies together on BOTH files. Nothing printed")
    print("  on the page says which reading is the right one.\n")

    print("  and by_column only works because of a chosen number:")
    items = pieces("byrow.pdf")
    for gap in (100, 260):
        first = " ".join(by_column(items, gap=gap)).split()[:4]
        print(f"    gap={gap:3d} -> starts {' '.join(first)}")
    print("    the columns sit 260 apart, so any threshold at or")
    print("    above 260 merges them back. That number is fitted to")
    print("    this page, not derived from anything.")
```

```text
  === bycolumn.pdf ===
    stream order:
      Refund policy A refund is issued to the original payment
      method within 14 days, in full. Cancellation policy A
      cancellation after dispatch carries a fee of 10 per
      cent.
    by position:
      Refund policy Cancellation policy A refund is issued to
      the A cancellation after original payment method
      dispatch carries a fee within 14 days, in full. of 10
      per cent.
    by column:
      Refund policy A refund is issued to the original payment
      method within 14 days, in full. Cancellation policy A
      cancellation after dispatch carries a fee of 10 per
      cent.

  === byrow.pdf ===
    stream order:
      Refund policy Cancellation policy A refund is issued to
      the A cancellation after original payment method
      dispatch carries a fee within 14 days, in full. of 10
      per cent.
    by position:
      Refund policy Cancellation policy A refund is issued to
      the A cancellation after original payment method
      dispatch carries a fee within 14 days, in full. of 10
      per cent.
    by column:
      Refund policy A refund is issued to the original payment
      method within 14 days, in full. Cancellation policy A
      cancellation after dispatch carries a fee of 10 per
      cent.

  Same page, three readings, and the by-position one welds
  the two policies together on BOTH files. Nothing printed
  on the page says which reading is the right one.

  and by_column only works because of a chosen number:
    gap=100 -> starts Refund policy A refund
    gap=260 -> starts Refund policy Cancellation policy
    the columns sit 260 apart, so any threshold at or
    above 260 merges them back. That number is fitted to
    this page, not derived from anything.
```

**Read the by-position block, because it is the one that matters.** Taking the strings top to
bottom and then left to right is the obvious thing to do, and on a two-column page it reads
straight across the gap between the columns. The result is this:

> Refund policy Cancellation policy A refund is issued to the A cancellation after original
> payment method dispatch carries a fee within 14 days, in full. of 10 per cent.

Two separate policies are now one paragraph. And notice what that paragraph contains: the word
*refund* and the phrase *a fee of 10 per cent*, a few words apart. Be exact about what that
does and does not show. The paragraph does not *say* refunds carry a fee — the words merely
co-occur, and nothing here runs a retrieval over them. What it shows is that a passage built to
look relevant to a question about refund fees now exists, and that it was manufactured by the
reader rather than written by anybody. **The retrieval would be working perfectly. The text is
wrong.**

**Stream order is right for one file and wrong for the other**, and the two files are the same
page. So the obvious first strategy is not a strategy at all — it is a bet on how the file
happened to be generated, and nothing you can see tells you which way the bet went.

**Reconstructing columns is what actually works here**, and it is worth being exact about why
it works. The function groups the strings by horizontal position and treats a jump of more
than `gap` as a new column. The two columns in these files sit 260 apart, so any threshold
below 260 separates them and any threshold at or above 260 merges them back. **That number is
fitted to this page.** Narrower columns, an indented quotation, a figure caption beside a
paragraph — each of those needs a different number, and this one was read off this page. (A
procedure that looks for the *largest* gap instead of a fixed threshold handles both of this
chapter's layouts with no number at all, which is the point rather than a counter-example: the
choice of rule is doing the work, and every rule encodes some assumption about what a page looks
like.) This is what **layout analysis** is: inferring the structure of a page from the positions
of its marks, by rules that are always approximate.

> **Warning:** The extractor above works on the two PDFs this chapter writes and is *not a PDF
> parser*. It matches one exact spelling of one positioning operator. Real files compress their
> content streams, use a dozen operators to place text, encode glyphs through font tables that
> may not map back to characters at all, and reach you as scans with no text layer whatsoever —
> which is a different problem again, solved by recognising characters in an image, or **OCR**,
> and solved imperfectly. Use a real library. The point of these twenty lines is not to replace
> one; it is that you now know what the library is *doing*, and therefore what it can get wrong.
>
> **And the two PDFs are not real documents either.** They are 917 bytes each and this chapter
> wrote them to make one thing visible. They show that a page *can* be drawn in an order that
> defeats a reader, which is a fact about the format; they say nothing whatever about how often
> that happens to the files on your disk. That is a question for your own documents, by the
> method below.

## Why This Is the Upstream Bottleneck

Now the claim the chapter is named for, and it is worth separating into two halves because they
have different kinds of support.

**The derivable half.** Everything after parsing consumes the parser's output and nothing
reconsults the file. Chunking cuts that text. The embedding model in Chapter 24 is handed those
chunks. The BM25 index in Chapter 26 counts terms in those chunks. A reranker scores those
chunks. The model in Chapter 28 is shown those chunks. So a word the parser dropped is absent
from every one of those steps, and a sentence it welded together is welded in all of them.
**No later stage can correct an error upstream of it, because no later stage can see the
document.** That follows from the arrangement and needs no measurement. And the exact line is
worth having, because it is not quite "nothing can be done later". What no later stage can do is
restore information the parser's output does *not contain* — a dropped word is simply gone.
Removing text that *is* there stays available at any point, which is why stripping page
furniture, below, is allowed and un-welding two columns is not.

**The observed half.** That parsing is in practice the most common cause of a retrieval system
answering badly is an observation, and this chapter cannot show you a rate — nor where on
Chapter 6's ladder it sits, which would take the practitioner reports this chapter does not
have. What it can show
you is why the failure is hard to find, which is the next section.

> **Tip:** This is the answer to have ready, and the two halves are what make it a good one.
> The arrangement guarantees that a parsing error survives every later stage untouched, because
> nothing later reads the original file. Whether parsing is the *biggest* source of trouble on
> your data is a thing to look at, and looking takes ten minutes.

## Look At What The Parser Produced

Chapter 25 showed that a result list cannot tell you what is missing. Parsing has the same
shape and it is worse, because the damage is invisible twice over: the page looks right, and the
retrieved passage looks like prose.

**So print the text.** Not the answers, not the scores — the extracted text, for a handful of
documents you know well, read by eye against the original page. It is the cheapest diagnostic in
this part of the book and it is the one people skip, because it feels too simple to be worth
doing.

Four things to look for, all of them visible in a minute:

| What to look for | What it means |
|---|---|
| Columns reading across | Either your reader is sorting by position, or it is taking the content stream in order on a file written row by row. The two look identical in the output |
| A table as a run of words | Rows and columns are gone; the numbers no longer belong to anything |
| Headers and footers mid-sentence | Page furniture is being treated as body text |
| A page that came out empty | No text layer: it is a scan, and it needs OCR before anything else |

The third is worth more attention than it gets. Headers, footers, page numbers and watermarks
are **page furniture** — text that is on the page without being part of the document — and a
parser has no way to tell them from body text, because on the page they are just more strings at
more positions. A header repeated on ninety pages puts the same
sentence into ninety chunks, and in Chapter 26's terms that is ninety documents sharing a term,
so the header's *own* terms lose a good deal of their inverse document frequency — how much
depends on how many chunks there are in total.

**The second effect is worth working out rather than guessing at, because the obvious guess is
wrong.** Chapter 26's BM25 divides a chunk's length by the collection average. Adding the same
header to every chunk raises both, so every chunk's ratio moves *towards one* — and a term in a
chunk of exactly average length is unaffected, because its ratio was one already. What the
furniture actually destroys is the *discrimination*: a short focused chunk loses the advantage
its shortness gave it, and a long padded chunk loses the penalty, so length normalisation stops
telling them apart. Run it at `\(k_1 = 1.5\)`{=latex} and `\(b = 0.75\)`{=latex} on chunks of
40, 60, 100, 160 and 200 against an average of 112 and a 20-character header: the short ones
drop from 1.4070 to 1.3253, and the long ones *rise*, from 0.7388 to 0.7692. So the furniture is
not just noise — but it does not shrink every term, and saying so would be the kind of claim
that sounds mechanical and is not.

## Chunks, and What a Boundary Decides

A document can be too long to embed as one vector and too long to hand to a model whole, and
then it is cut into pieces. A **chunk** is one of those pieces: the unit that gets embedded, the unit the
index stores, and the unit retrieval returns. Three jobs, one piece of text, and the cuts decide
all three at once. How much text each piece holds is the **chunk size**, and it is the first
number anybody reaches for — so it is worth seeing what it settles before you pick one.

```python
"""What a chunk boundary decides, and what it makes unretrievable."""

DOC = (
    "Returns are handled by the support team. "
    "A refund is issued to the original payment method within 14 days. "
    "A cancellation after dispatch carries a fee of 10 per cent."
)

# The question is "how long does a refund take". Answering it needs the
# subject and the period in the SAME chunk: a passage saying "within 14
# days" without saying what takes 14 days answers nothing.
ANSWER = "A refund is issued to the original payment method within 14 days."

def fixed(text, size, overlap=0):
    """Cut every `size` characters, stepping back `overlap` each time."""
    step = size - overlap
    if step <= 0:
        raise ValueError("overlap must be smaller than size")
    out, start = [], 0
    while start < len(text):
        out.append(text[start:start + size])
        start += step
    return out

def holds_answer(chunk):
    # The whole sentence, not two substrings of it. Testing for the
    # pieces separately would accept a chunk that holds "refund" and
    # "14 days" with the sentence broken between them.
    return ANSWER in chunk

def report(size, overlap=0):
    cs = fixed(DOC, size, overlap)
    hit = [i for i, c in enumerate(cs, 1) if holds_answer(c)]
    stored = sum(len(c) for c in cs)
    print(f"  size {size:3d} overlap {overlap:2d}  ->  {len(cs)} chunks, "
          f"{stored} chars stored,")
    print(f"                        answer in {hit or 'NONE'}")
    return cs, hit

if __name__ == "__main__":
    print(f"  document {len(DOC)} chars; the answer is {len(ANSWER)}"
          f" chars long\n")

    print("  (a) the chunk is smaller than the answer:")
    report(60)
    report(60, 20)
    report(60, 40)
    print("      no overlap rescues this. A chunk of 60 cannot hold")
    print("      65 characters, so the size alone decides it.\n")

    print("  (b) the chunk is big enough, and the boundary is wrong:")
    cs, _ = report(80)
    print(f"      chunk 1 ends: ...{cs[0][-24:]!r}")
    print(f"      chunk 2 starts: {cs[1][:24]!r}...")
    print("      one says who gets a refund and never when; the")
    print("      other says 'within 14 days' and never what does.\n")

    print("  (c) same size, with overlap:")
    cs, hit = report(80, 40)
    print(f"      chunk {hit[0]}: {cs[hit[0]-1][:46]!r}")
    print(f"      overlap cost: {sum(len(c) for c in cs) - len(DOC)}"
          f" characters stored twice\n")

    print("  (d) cutting on sentences instead:")
    for i, c in enumerate([s.strip() + "." for s in DOC.split(". ")
                           if s.strip()], 1):
        c = c.rstrip(".") + "."
        mark = "  <- the answer" if holds_answer(c) else ""
        print(f"      {i}: {c[:40]}{mark}")
    print("      the answer is whole, and no size was chosen at all.")
```

```text
  document 166 chars; the answer is 65 chars long

  (a) the chunk is smaller than the answer:
  size  60 overlap  0  ->  3 chunks, 166 chars stored,
                        answer in NONE
  size  60 overlap 20  ->  5 chunks, 232 chars stored,
                        answer in NONE
  size  60 overlap 40  ->  9 chunks, 438 chars stored,
                        answer in NONE
      no overlap rescues this. A chunk of 60 cannot hold
      65 characters, so the size alone decides it.

  (b) the chunk is big enough, and the boundary is wrong:
  size  80 overlap  0  ->  3 chunks, 166 chars stored,
                        answer in NONE
      chunk 1 ends: ...'ued to the original paym'
      chunk 2 starts: 'ent method within 14 day'...
      one says who gets a refund and never when; the
      other says 'within 14 days' and never what does.

  (c) same size, with overlap:
  size  80 overlap 40  ->  5 chunks, 292 chars stored,
                        answer in [2]
      chunk 2: ' A refund is issued to the original payment me'
      overlap cost: 126 characters stored twice

  (d) cutting on sentences instead:
      1: Returns are handled by the support team.
      2: A refund is issued to the original payme  <- the answer
      3: A cancellation after dispatch carries a 
      the answer is whole, and no size was chosen at all.
```

**So here is the answer to what a boundary decides, in three parts.**

**It decides what is in one vector.** A chunk is embedded as a whole, so everything inside it
contributes to one point — which is Chapter 24's fixed width again, now with you choosing how
much text has to share it. A chunk holding one topic has that topic to itself. A chunk holding
the end of one section and the start of the next makes them share — and Chapter 25's denial
applies here too, so say what the arrangement forces rather than what the vector means: neither
section gets the width to itself.

**It decides what can be returned together.** Retrieval returns chunks, so a fact and the
sentence that qualifies it either travel together or they do not travel at all.

**And it decides which questions are answerable, which is the part that surprises people.**
Block (a) is the clean case: the answer runs to 65 characters, the chunks are 60, and no chunk
of 60 can contain 65 characters. Adding overlap makes more chunks — nine of them, storing 438
characters for a 166-character document — and not one of them holds the answer. **The size
alone settled it**, before any boundary was placed and before any model was chosen.

Block (b) is the other failure and it is the one overlap is for. At size 80 the answer fits,
but the cut falls inside it: one chunk says who gets a refund and never when, the next says
*within 14 days* and never what does. Neither is wrong. Neither is useful. **Overlap** — cutting
the next chunk a little before the last one ended — fixes exactly this, and block (c) shows it
working at the cost of storing 126 characters twice.

> **Note:** Chunk sizes in practice are counted in Chapter 10's tokens rather than characters,
> and the figures you will see quoted — a few hundred tokens with a tenth of that as overlap —
> are a current convention in Chapter 6's sense — which is not the opposite of a derivation,
> since a convention can have a reason you can work out; these particular figures do not. These programs count
> characters because that is checkable by hand. The relation is Chapter 10's four characters to
> the token, so a
> 512-token chunk is roughly two thousand characters. Chapter 10's direction warning is about
> words against tokens rather than this conversion, so it does not apply here — but check which
> way round you are multiplying all the same.

**Cutting on the document's own structure is usually better than cutting on a count**, and block
(d) shows why: split on sentences and the answer is whole, with no size chosen at all. Say that
as a property rather than a rule, though, because it has its own failure. A sentence can be
longer than the model's input limit. A table row is not a sentence. A heading is a line with no
full stop. Structural splitting works where the document has structure the parser managed to
preserve — which puts you back at the first half of this chapter.

## The Index, and What It Puts Out of Reach

The last step is storing the chunks so retrieval can score them. Chapter 29 is about making that
fast at a million chunks; what matters here is what a row holds.

```python
"""An index of chunks, and what it puts out of reach."""
from chunks import ANSWER, DOC, fixed, holds_answer

def build(doc_name, text, size, overlap=0):
    """One row per chunk. The text is what gets embedded and returned;
    the rest is what lets you say where it came from."""
    rows = []
    step = size - overlap
    for n, chunk in enumerate(fixed(text, size, overlap)):
        rows.append({"id": f"{doc_name}#{n}", "doc": doc_name,
                     "start": n * step, "text": chunk})
    return rows

def whole_in_one(rows):
    return [r["id"] for r in rows if holds_answer(r["text"])]

if __name__ == "__main__":
    print("  an index of three chunks, cut at 60:\n")
    rows = build("policy.pdf", DOC, 60)
    for r in rows:
        print(f"    {r['id']}  start {r['start']:3d}  "
              f"{r['text'][:28]!r}")

    print("\n  every retrieval method in chapters 24 to 26 scores")
    print("  these rows and sorts them. Lexical, dense, hybrid,")
    print("  a reranker on top: all of them return rows.\n")

    print(f"  rows holding the answer WHOLE: {whole_in_one(rows) or 'NONE'}")
    print("  So no single passage this index can return answers the")
    print("  question. That is a fact about the chunking, settled")
    print("  before any model was chosen.\n")

    print("  but be careful how far that goes. These rows tile the")
    print("  document with nothing dropped:")
    print(f"    rejoined == original ?  {''.join(r['text'] for r in rows) == DOC}")
    print("  so rows 0 and 1 TOGETHER do contain the sentence:")
    print(f"    {holds_answer(rows[0]['text'] + rows[1]['text'])}")
    print("  Return both and a reader has the answer. What the")
    print("  chunking removed is the single passage, not the")
    print("  information - and joining two passages is chapter 28's")
    print("  job, not retrieval's.\n")

    print("  and retrieval has to pick them first. Row 1 holds the")
    print("  period but never says 'refund':")
    print(f"    {'refund' in rows[1]['text'].lower()}")
    print("  so a query about refunds has little to match it on,")
    print("  which is a claim about how likely the pair is to be")
    print("  retrieved, not a derivation.\n")

    print("  the same document cut at 80 with overlap 40:\n")
    rows2 = build("policy.pdf", DOC, 80, 40)
    for r in rows2:
        mark = "  <- whole" if holds_answer(r["text"]) else ""
        print(f"    {r['id']}  start {r['start']:3d}  "
              f"{r['text'][:20]!r}{mark}")
    print(f"\n  rows holding it whole: {whole_in_one(rows2)}")
    print("  Same document, same words, same retrieval. The only")
    print("  thing that changed is where the cuts fell.\n")

    print("  what each row carries beyond its text:")
    r = rows2[1]
    print(f"    id    {r['id']}")
    print(f"    doc   {r['doc']}")
    print(f"    start {r['start']}")
    print("  Without those the chunk is an orphan: you can return")
    print("  it and you cannot say where it came from. The offset")
    print("  is also how you would fetch a neighbour, which is how")
    print("  a system reaches a sentence no one row holds.")
```

```text
  an index of three chunks, cut at 60:

    policy.pdf#0  start   0  'Returns are handled by the s'
    policy.pdf#1  start  60  'to the original payment meth'
    policy.pdf#2  start 120  'n after dispatch carries a f'

  every retrieval method in chapters 24 to 26 scores
  these rows and sorts them. Lexical, dense, hybrid,
  a reranker on top: all of them return rows.

  rows holding the answer WHOLE: NONE
  So no single passage this index can return answers the
  question. That is a fact about the chunking, settled
  before any model was chosen.

  but be careful how far that goes. These rows tile the
  document with nothing dropped:
    rejoined == original ?  True
  so rows 0 and 1 TOGETHER do contain the sentence:
    True
  Return both and a reader has the answer. What the
  chunking removed is the single passage, not the
  information - and joining two passages is chapter 28's
  job, not retrieval's.

  and retrieval has to pick them first. Row 1 holds the
  period but never says 'refund':
    False
  so a query about refunds has little to match it on,
  which is a claim about how likely the pair is to be
  retrieved, not a derivation.

  the same document cut at 80 with overlap 40:

    policy.pdf#0  start   0  'Returns are handled '
    policy.pdf#1  start  40  ' A refund is issued '  <- whole
    policy.pdf#2  start  80  'ent method within 14'
    policy.pdf#3  start 120  'n after dispatch car'
    policy.pdf#4  start 160  ' cent.'

  rows holding it whole: ['policy.pdf#1']
  Same document, same words, same retrieval. The only
  thing that changed is where the cuts fell.

  what each row carries beyond its text:
    id    policy.pdf#1
    doc   policy.pdf
    start 40
  Without those the chunk is an orphan: you can return
  it and you cannot say where it came from. The offset
  is also how you would fetch a neighbour, which is how
  a system reaches a sentence no one row holds.
```

**Here is the derivation, and it is worth stating no wider than it holds.** Retrieval scores the
rows of an index and returns some of them. That is all any of Chapters 24 to 26 does: BM25
counts terms in a row, a cosine compares a row's vector, a reranker rescores a row. So **if no
row holds a whole answer, no retrieval method can return a single passage that answers the
question** — and that was fixed when you chose the parser and the cuts, before any model
existed. It holds for every retrieval method, every embedding model and every reranker, because
none of them can return a passage that is not a row.

**Now the limit of that limit, because the program shows it.** The three rows at size 60 tile
the document with nothing dropped, so rows 0 and 1 *together* contain the sentence. Return both
and a reader has the answer. What the chunking destroyed is the single passage, not the
information — and assembling an answer out of two passages is Chapter 28's job rather than
retrieval's, which is why the row keeps an offset: an offset is how a system fetches a
neighbour. So the honest statement is narrower than it first looks, and more useful: bad cuts do
of *this* kind — cuts that tile the document, dropping nothing — do not put the information
beyond reach; they move the work of reassembling it downstream and make it somebody's problem. A
chunker that *discards* text is a different matter, and the method below has you discard page
furniture on purpose.

**And there is a practical catch that is a likelihood rather than a derivation.** Row 1 holds
*within 14 days* and never says *refund*, so a query about refunds has little to match it on.
The pair exists in the index and retrieval has to choose to return it, which is a claim about
what is likely to be ranked, not about what is possible.

This is Chapter 26's reranking ceiling one step further upstream. There, a reranker could only
permute the candidate set. Here, the candidate set can only be drawn from the index, and the
index holds what the chunking made.

**The other fields are what stop a chunk being an orphan.** A row that carries only text can be
returned and cannot be placed: you cannot tell the reader which document it came from or where.
Keeping the document name and the offset costs nothing at index time and is impossible to
reconstruct afterwards. Chapter 28 is where they get used.

## What To Actually Do

In order, because the order is the point: each step can only be checked after the one above it
is right.

1. **Parse, then read the output.** Print the extracted text for five documents you know and
   compare it against the pages. Do this before anything else exists.
2. **Fix the parser before touching anything downstream.** A better embedding model cannot
   recover a word that is not in the text.
3. **Strip the page furniture.** Repeated headers and footers change term statistics as well as
   adding noise.
4. **Cut on the document's structure where it survived parsing**, and on a size where it did
   not.
5. **Check the size against your questions.** Write down five real questions, find the shortest
   passage that answers each, and make sure your chunk is bigger than the longest of them. This
   is block (a), and it is a ten-minute check that no amount of later tuning substitutes for.
6. **Add overlap for the boundary cases**, knowing it costs storage and returns near-duplicate
   passages.
7. **Then measure.** Chapter 24's answer key with Chapter 26's measures, and Chapter 20 for whether a
   difference between two chunkings is real rather than luck on a few queries.

> **Warning:** Steps 1 to 3 are not glamorous and they are where the wins are. A team that
> tunes chunk sizes for a week on text whose columns are interleaved is optimising a parameter
> of a broken pipeline, and every measurement it takes will be real, repeatable and about the
> wrong thing.

## Lab: Break a Page and Find Out

Four programs, pure Python, nothing to install. About forty minutes, and there is a key for
every step. Work in a new empty folder.

**Step 1.** Save the first program as `makepdf.py` and run it.

*Expected result:* two files of 917 bytes each. Open them both in whatever opens a PDF. They
are the same page.

**Step 2.** Save the second as `extract.py` and run it.

*Expected result:* the six readings in the output above. Confirm for yourself that
`bycolumn.pdf` reads correctly in stream order and `byrow.pdf` does not, and that the
by-position reading is wrong for both.

**Step 3.** Before reading on: which of the three functions would you ship, and what would you
need to know about your documents to decide?

*Expected result:* none of them, on this evidence. `by_column` is right on both files here, and
it is right because its threshold is smaller than the gap between these two columns — step 5
breaks it. What you would need to know is what the layouts actually are, which means looking at
the extracted text for real documents, which is step 1 of the method above.

**Step 4.** In `extract.py`, change `by_column`'s `gap` to `260` and run it again.

*Expected result:* the columns merge and the output matches the by-position reading. The
threshold is the whole of the function's correctness, and nothing in the file tells you what to
set it to.

**Step 5.** In `makepdf.py`, move the right column from `x = 320` to `x = 150`, so the columns
are 90 apart. Run both programs again with `gap` back at `100`.

*Expected result:* `by_column` now merges the columns, because 90 is less than the 100
threshold, and its output is the welded text. The function did not change. The page did.

Two things to notice while you are here. The program's own closing lines still say *the columns
sit 260 apart*, which is now false — a hard-coded explanation of a number that moved, which is
its own small lesson. And at `x = 150` the two columns overlap on the page, so the PDF you open
is a garbled mess rather than a tidy two-column layout; the extractor neither knows nor cares,
which is the point.

**Step 6.** Save the third program as `chunks.py` and run it. Then work out, from block (a)
alone, what the smallest chunk size is that could possibly answer the question.

*Expected result:* 65 characters, the length of the answer — and that is a floor rather than a
good choice, because at exactly 65 the answer fits only if the boundary falls exactly right.
Block (b) is what happens when it does not.

**Step 7.** In `chunks.py`, change the question. Point `holds_answer` at the other sentence —
`return "A cancellation after dispatch carries a fee of 10 per cent." in chunk` — and run it
again. Keep it testing a whole sentence, as `holds_answer` already does, so the two questions
are being asked the same way.

*Expected result:* **`NONE` at every size the program prints** — including size 80 with overlap
40, which answered the refund question. The cancellation passage is 59 characters, shorter than
the refund one, and it still fails: it starts at character 107 and every boundary the program
tries falls inside it.

Then go looking, because the pattern is the point and it runs both ways. Size 100 with no
overlap answers the cancellation question and *not* the refund one — the reverse of block (c).
Size 120 with no overlap answers the refund question and not the cancellation one. Plenty of
configurations answer both, so this is not a hunt for the single right setting; what matters is
that **a chunking is not good or bad, it is good or bad for a set of questions**, and a size
chosen by checking one question will fail the next one. That is why step 5 of the method asks
for the questions, plural, first.

You will also see `chunks.py` stop with `IndexError` part way through block (c): that block
prints the chunk holding the answer, and with this question there isn't one at size 80. The five
`NONE` lines print first, which is what the step is about, and blocks (c) and (d) do not appear.
Same defect as `by_column`'s in step 9 — a line written when the answer was always found.

**Then put `holds_answer` back as it was**, because `index.py` imports it from `chunks.py` and
step 8's expected result depends on it.

**And one number here is worth having.** Scan the sizes and overlaps and the smallest size that
can answer both questions is 65 — the length of the *longer* of the two answers, which is
exactly the floor step 6 made you work out, now taken across a set of questions rather than one.
At 65 it only works with heavy overlap, because at the floor the boundaries have to fall almost
perfectly. That is what makes the floor a floor and not a choice.

**Step 8.** Save the fourth program as `index.py` and run it.

*Expected result:* `NONE` at size 60 and `policy.pdf#1` at size 80 with overlap 40. Then say in
one sentence why no reranker from Chapter 26 could fix the first case.

**Step 9.** In `makepdf.py`, change `content_stream` to place text with `Td` instead of `Tm`:
replace the line building each piece with
`parts.append(f"1 0 0 1 0 0 Tm {x} {y} Td ({text}) Tj")`. Run `makepdf.py`, then `extract.py`.

*Expected result:* `pieces()` finds *nothing* — zero strings — and then `extract.py` *crashes*
with `IndexError: list index out of range` in `by_column`, which indexes `xs[0]` on an empty
list. You get two blank readings for the first file and a traceback before the second. The files
also grow to 973 bytes, because `0 0 Tm` plus `x y Td` is longer than `x y Tm`.

Three lessons for the price of one. The page is unchanged and still opens correctly: `Td` sets a
position exactly as `Tm` does, and the regex matches only the one spelling it was written for —
that is the gap between a demonstration and a library, and it is why the Warning says to use a
real one. A real file may also compress its content stream, encode glyphs through a font table
that does not map back to characters, or have no text layer at all. And `by_column` has no empty
case, which is what a function written against one input looks like when it meets another.

## Summary, Key Terms, and Review Questions

### Summary

**Parsing** is turning a file into text, and it is hard because a page is not text. A PDF's
**content stream** is a list of instructions placing strings at positions, with no sentence, no
column and no **reading order** in it — so reading order is reconstructed, and the chapter's two
917-byte files prove how little that reconstruction rests on. They place the same eight strings
at the same eight positions and differ only in the order they were drawn: stream order reads one
correctly and welds the other's two policies into one paragraph, and sorting top-to-bottom then
left-to-right — the obvious fix — welds both. The welded paragraph puts *refund* a few words
from *a fee of 10 per cent* — words that merely co-occur in a paragraph nobody wrote, which is
the shape a plausible and wrong passage takes.
Grouping by column is right on both, and only because its threshold is below the 260 these
columns happen to sit apart; that is **layout analysis**, which is inference from positions by
always-approximate rules.

**Parsing is the upstream bottleneck, and the claim has two halves.** The derivable half: every
later stage consumes the parser's output and none reconsults the file, so a dropped word is
absent from the chunker, the embedding, the index and the reranker alike, and no stage can
correct an error upstream of it. The observed half — that it is in practice the commonest cause
of bad answers — is an observation this chapter cannot put a rate on. So **print the extracted
text** for documents you know: columns reading across, a table reduced to a run of words, page
furniture mid-sentence, and an empty page that needs **OCR** are all visible in a minute, and a
header repeated on ninety pages changes Chapter 26's term statistics as well as adding noise.

A **chunk** is the unit that gets embedded, stored and returned, so **a boundary decides three
things**: what shares one vector, what can be returned together, and which questions are
answerable at all. Two failures are distinct. When the chunk is smaller than the answer — 60
against 65 characters — **no overlap helps**: nine chunks storing 438 characters for a
166-character document contained the answer zero times, and the size alone settled it. When the
chunk is big enough but the cut falls inside the answer, **overlap** is exactly the fix, at the
cost of 126 characters stored twice. Cutting on sentences kept the answer whole with no size
chosen, which is a property and not a rule: a sentence can exceed the input limit, and a table
row is not a sentence.

**And the derivation worth carrying:** retrieval scores the rows of an index and returns some of
them, so **if no row holds a whole answer, no retrieval method can return a single passage that
answers the question** — fixed when the parser and the cuts were chosen, and true of every
method, embedding and reranker. State it no wider than that: the chapter's three rows tile the
document, so rows 0 and 1 together *do* hold the sentence, and cuts that tile like that move the
work of reassembling an answer downstream to Chapter 28 rather than putting the information
beyond reach — a chunker that *discards* text, as the method does with page furniture, is a
different matter. That retrieval is unlikely to return the pair, since row 1 never says *refund*, is a
likelihood and not a derivation. It is Chapter 26's reranking ceiling one step further upstream. Keep each row's
document name and offset, because a chunk without them can be returned and cannot be placed.

### Key Terms

| Term | Meaning |
|---|---|
| **Parsing** | Turning a file into text a program can work on. For a document format this means reconstructing something the file does not record |
| **Content stream** | A PDF page's list of drawing instructions, each placing a string at a position. Its order is the order the marks were made, not a reading order |
| **Reading order** | The order a person reads a page in. A human fact about a layout, and not something a page description like PDF records — some formats do store an order, which is why the problem is format-specific |
| **Layout analysis** | Inferring a page's structure — columns, tables, headings — from where its marks sit. Always approximate; the chapter's version turns on one threshold fitted to one page |
| **OCR** | Recognising characters in an image, for pages that have no text layer at all. Imperfect, and a separate step before parsing can begin |
| **Chunk** | One piece of a split document: the unit that is embedded, stored in the index and returned by retrieval |
| **Chunk size** | How much text a chunk holds. A floor on it is set by taking the *shortest* passage that answers each of your questions and keeping the longest of those |
| **Overlap** | Starting each chunk a little before the last one ended, so a passage cut by one boundary survives whole in a neighbour. Costs storage and returns near-duplicates |
| **Page furniture** | Headers, footers, page numbers and watermarks: text on the page that is not part of the document |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Why parsing is the bottleneck | A derivation: every later stage reads the parser's output and none reconsults the file, so no later stage can restore information that output does not contain. Removing text that is there stays available |
| What a page actually holds | Strings and positions. No sentence, no column, no reading order — those are reconstructed |
| The three readings | Stream order is a bet on how the file was generated; sorting by position reads across columns; grouping by column needs a threshold fitted to the page |
| What a chunk boundary decides | What shares one vector, what can be returned together, and which questions are answerable at all |
| When overlap cannot help | When the chunk is smaller than the answer. 60-character chunks never held a 65-character answer at any overlap |
| When overlap is the fix | When the chunk is big enough and the cut falls inside the answer |
| The retrieval ceiling | A derivation: retrieval returns rows, so if no row holds a whole answer, no method, model or reranker can return a single passage that answers it |
| What that ceiling does *not* say | Where the cuts tile the document, the information is still there across two rows, and the reassembly moves downstream to Chapter 28 rather than becoming impossible. A chunker that discards text is another matter |
| The ten-minute check | Write five real questions, find the shortest passage answering each, make the chunk bigger than the longest |
| The first diagnostic | Print the extracted text and read it against the page. Before anything downstream exists |

### Review Questions

1. Why is document parsing the upstream bottleneck for everything downstream?
2. What does a chunk boundary decide?
3. Your retrieval returns a passage saying refunds carry a 10 per cent fee. The PDF says no such thing. What happened?
4. How would you choose a chunk size?
5. Your answers are poor and somebody proposes a better embedding model. What would you do first?

### Review Answers

1. Because every stage after it consumes its output and none of them ever reads the file again.
Chunking cuts the parser's text; Chapter 24's embedding model is handed those chunks; Chapter
26's index counts terms in them; a reranker rescores them; the model is shown them. So a word
the parser dropped is missing from all of those, and a sentence it welded together is welded in
all of them — **no later stage can restore information the parser's output does not contain,
because no later stage
downstream can see the document.** That part is a derivation from the arrangement and needs no
measurement. Then be careful with the second half: that parsing is the *most common* cause of
bad answers in practice is an observation rather than something the arrangement gives you. What
makes it dangerous is that it hides twice — the page looks right, and the retrieved passage
reads like prose — so the diagnostic is to print the extracted text and read it against the
page, which takes ten minutes and is the step people skip.
2. Three things, and the third is the one worth leading with. It decides **what shares one
vector**, because a chunk is embedded whole, so a chunk spanning the end of one section and the
start of another makes two sections share one width, and neither gets it to itself. It decides
**what can be returned together**,
because retrieval returns chunks, so a fact and the sentence qualifying it either travel
together or not at all. And it decides **which questions are answerable at all**: if no chunk
contains a whole answer, no retrieval method can return a single passage that answers it — which
is not the same as the information being gone, since two rows may hold it between them. Add the distinction between the two
ways that goes wrong, because it changes what you do about it. If the chunk is *smaller* than
the answer, no overlap and no boundary placement can help — the chapter's 60-character chunks
never held a 65-character answer however much they overlapped, and the size alone settled it. If
the chunk is big enough and the cut merely falls in the wrong place, overlap is exactly the fix.
3. The parser welded two columns together. A two-column page records strings and positions, with
no reading order, so two different readers interleave them: one that sorts top-to-bottom and
then left-to-right runs straight across the gap, and one that takes the content stream in order
does the same if the file was written row by row. The output looks identical either way, so
finding out which it is means looking at the extractor, not the text. The chapter's own example comes out as
*"Refund policy Cancellation policy A refund is issued to the A cancellation after…"* — the
refund policy and the cancellation policy, now one paragraph, with *refund* a few words from *a
fee of 10 per cent*. **The retrieval is working correctly and the text is wrong**, which is why
no amount of looking at scores or swapping models finds it. Confirm it by printing the extracted
text for that document and reading it against the page, then fix the reader — here, by grouping
the strings into columns before sorting, remembering that the threshold doing that work is
fitted to the layout and will need checking on the others.
4. Not from a default, and the honest answer is a procedure rather than a number. Write down five
real questions, find the shortest passage in your documents that actually answers each, and take
the longest of those: that is a *floor* on the size, because a chunk smaller than an answer
cannot hold it whatever else you do. Then go up from there, because at exactly the floor the
answer survives only if the boundary falls perfectly, and add overlap for the boundary cases
knowing it costs storage and returns near-duplicate passages. Prefer the document's own
structure to a count where parsing preserved it — sentences, paragraphs, sections — since that
kept the chapter's answer whole with no size chosen at all, and say that as a property rather
than a rule, because a sentence can exceed the model's input limit and a table row is not a
sentence. The figures you will see quoted, a few hundred tokens with a tenth as overlap, are a
current convention and a reasonable starting point, not a result. Finally, note that one
chunking is not good or bad in itself but good or bad *for a set of questions*: change the
question and different sizes succeed, which is why the questions come first. Then measure two
candidates against Chapter 24's answer key with Chapter 26's measures, paired, with an interval
— Chapter 20.
5. Print the extracted text for five documents I know well and read it against the original
pages. It takes ten minutes, it needs nothing built, and it tests the one stage whose errors
nothing downstream can repair. Four things are visible immediately: columns reading across each
other, a table reduced to a run of words with the numbers no longer attached to anything, page
furniture appearing mid-sentence, and a page that came out empty because it is a scan and needs
OCR first. If any of those is happening, a better embedding model is being asked to recover
words that are not in the text, which it cannot do. The second check is nearly as cheap and is
the chapter's other derivation: take five real questions and confirm some chunk holds a whole
answer to each, because if none does then no single passage the index can return answers it —
the information may still be spread across two rows, but putting it back together stops being
retrieval's job and becomes Chapter 28's — and that is settled by the chunking, not by retrieval. Only when both of those
are clean does the model become the binding constraint, and at that point Chapter 24 is how to
compare two candidates on your own data.

> **You understand this when** you can say what a PDF page actually contains and why that makes
> reading order a guess — and name the one check that tells you whether your chunking has put a
> question beyond the reach of a single retrieved passage, before any model is involved.
