#!/usr/bin/env python3
"""swap-cover.py — put a one-page cover PDF in place of page 1 of a book's PDF.

For the books that can't be rebuilt from this repository (APIs to FastAPI and
The Complete Software Engineering Guide); see their cover/ folders. The new cover is
appended to the file as a PDF incremental update: the original bytes stay as they are,
and the update holds only the new page 1, the unchanged document info (title, subject,
…; repeated so viewers still find it) and the cover's fonts. Every other page, the
bookmarks and the links are not touched. Running it again just swaps the cover again.

Usage: swap-cover.py <book.pdf> <cover.pdf>      (needs pypdf 5 or later)
"""
import os
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject

if len(sys.argv) != 3:
    sys.exit(__doc__.strip().splitlines()[-1])
book, cover_path = sys.argv[1:]

original = PdfReader(book)            # read before .pages, which copies inherited values in
cover = PdfReader(cover_path).pages[0]
writer = PdfWriter(book, incremental=True)
page = writer.pages[0]
if [round(float(v), 2) for v in cover.mediabox] != [round(float(v), 2) for v in page.mediabox]:
    sys.exit(f"{cover_path}: page size {list(cover.mediabox)} is not the book's {list(page.mediabox)}")

# Empty the old cover but keep its page object, so bookmarks and links to page 1 still work.
page[NameObject("/Contents")] = ArrayObject()
page[NameObject("/Resources")] = DictionaryObject()
page.pop("/Annots", None)
page.merge_page(cover)

# pypdf copies inherited values (/MediaBox, …) into every page it reads; take them out again,
# so no page other than the cover is rewritten.
for p in writer.pages:
    raw = original.get_object(p.indirect_reference.idnum)
    for key in list(p.keys()):
        if key not in raw and key not in ("/Contents", "/Resources"):
            del p[key]

# pypdf leaves /Info out of an update unless it changed, and then viewers lose the title:
# mark it changed so it is written again, unchanged, and named in the update.
info = writer._info
if info is not None:
    writer._original_hash[info.indirect_reference.idnum - 1] = None

tmp = book + ".tmp"
with open(tmp, "wb") as f:
    writer.write(f)
os.replace(tmp, book)
print(f"new cover in {book}")
