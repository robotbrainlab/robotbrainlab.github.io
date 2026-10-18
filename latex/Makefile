# Build the book from the Markdown (the only source of truth).
#   make           convert ../markdown/*.md -> chapters/*.tex, then typeset book.pdf
#   make convert   only regenerate chapters/*.tex
#   make pdf       only typeset (after a convert)
#   make check     pre-flight: overfull boxes, glyphs, references, page size/count, fonts
#   make clean     remove everything generated
#   make sample    (template folder only) build the sample mini book -> sample/sample.pdf
.PHONY: all convert pdf check clean sample

# MacTeX lives here; exported so latexmk finds xelatex/makeindex in any terminal.
export PATH := /Library/TeX/texbin:/opt/homebrew/bin:$(PATH)
LATEXMK := $(shell command -v latexmk 2>/dev/null || echo /Library/TeX/texbin/latexmk)

all: convert pdf

convert:
	bash tools/convert.sh

pdf:
	$(LATEXMK) -xelatex -interaction=nonstopmode -halt-on-error book.tex

check:
	bash tools/check.sh

clean:
	$(LATEXMK) -C book.tex >/dev/null 2>&1 || true
	rm -rf chapters generated book.pdf
	rm -f book.aux book.log book.toc book.out book.fls book.fdb_latexmk book.xdv book.idx book.ilg book.ind

# ---- The sample mini book (only in book-template/) -----------------------------
# sample/markdown/ + sample/latex/{book.tex,book-meta.tex} are its sources; the rest of
# sample/latex/ is copied from this template, exactly as a new book would copy it.
TEMPLATE_FILES := Makefile latexmkrc preamble.tex tools front .gitignore
sample:
	@test -d sample/markdown || { echo "no sample/ here (this is a book copy, not the template)"; exit 1; }
	cp -R $(TEMPLATE_FILES) sample/latex/
	$(MAKE) -C sample/latex all
	cp sample/latex/book.pdf sample/sample.pdf
	-$(MAKE) -C sample/latex check PAGES_MIN=10 PAGES_MAX=40
