# ================================================================
# The shared book build. One copy, used by every book.
#
#   make list                          every book that can be built
#   make BOOK=linux-and-git            convert markdown -> chapters, then typeset
#   make BOOK=linux-and-git pdf        typeset only
#   make BOOK=linux-and-git convert    regenerate chapters/*.tex only
#   make BOOK=linux-and-git check      pre-flight checks
#
# Layout:  books/latex/   this file, preamble.tex, latexmkrc, front/, tools/, styles/
#          books/<slug>/  book.tex, book-meta.tex, markdown/, chapters/, generated/, assets/
#
# [2026-11-11] Replaces six near-identical Makefiles, one per book. The split between shared
# machinery and book content is the one the template's own Makefile already declared:
#   TEMPLATE_FILES := Makefile latexmkrc preamble.tex tools front .gitignore
#
# Most books use preamble.tex. Two are too different to merge and keep their own in styles/:
# interview-prep and complete-software-engineering-guide. Their book.tex names the style file.
#
# NEVER run `make clean` for complete-software-engineering-guide. Its Markdown library is not
# in this repository, so chapters/*.tex is its only source and nothing can regenerate it.
# The clean target refuses that book for exactly this reason.
# ================================================================
.PHONY: all convert pdf check clean list

export PATH := /Library/TeX/texbin:/opt/homebrew/bin:$(PATH)
LATEXMK := $(shell command -v latexmk 2>/dev/null || echo /Library/TeX/texbin/latexmk)

SHARED  := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
BOOKS   := $(abspath $(SHARED)/..)
BOOKDIR  = $(BOOKS)/$(BOOK)

# preamble.tex, front/ and styles/ are found here; the book's own files in its own folder.
export TEXINPUTS   := $(SHARED)//:
export BOOK_SHARED := $(SHARED)
export BOOK_DIR     = $(BOOKDIR)

define need_book
@test -n "$(BOOK)" || { echo "Set BOOK=<slug>.  Try: make list"; exit 1; }
@test -f "$(BOOKDIR)/book.tex" || { echo "No book.tex in $(BOOKDIR)"; exit 1; }
endef

all: convert pdf

list:
	@for d in $(BOOKS)/*/; do test -f "$$d/book.tex" && basename "$$d"; done

convert:
	$(need_book)
	bash $(SHARED)/tools/convert.sh

pdf:
	$(need_book)
	cd $(BOOKDIR) && $(LATEXMK) -r $(SHARED)/latexmkrc -xelatex \
	    -interaction=nonstopmode -halt-on-error book.tex

check:
	$(need_book)
	cd $(BOOKDIR) && bash $(SHARED)/tools/check.sh

clean:
	$(need_book)
	@test "$(BOOK)" != "complete-software-engineering-guide" || \
	  { echo "REFUSED: that book's chapters/*.tex cannot be regenerated."; exit 1; }
	cd $(BOOKDIR) && $(LATEXMK) -C book.tex >/dev/null 2>&1 || true
	cd $(BOOKDIR) && rm -rf chapters generated book.pdf && \
	  rm -f book.aux book.log book.toc book.out book.fls book.fdb_latexmk book.xdv book.idx book.ilg book.ind
