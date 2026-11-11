# Build the series cover and put it in place of page 1 of the book's PDF (the rest of the
# PDF is left byte for byte as it was), then copy the PDF to the website (cse/books/).
#   make         cover.pdf -> page 1 of "../The Complete Software Engineering Guide.pdf" -> website copy
#   make cover   only build cover.pdf
export PATH := /Library/TeX/texbin:$(PATH)
LATEXMK := $(shell command -v latexmk 2>/dev/null || echo /Library/TeX/texbin/latexmk)
PDF  := ../The Complete Software Engineering Guide.pdf
SITE := ../../../../../../cse/books/complete-software-engineering-guide/
.PHONY: all cover

all: cover
	python3 ../../book-template/tools/swap-cover.py "$(PDF)" cover.pdf
	cp "$(PDF)" "$(SITE)"

cover:
	$(LATEXMK) -xelatex -interaction=nonstopmode -halt-on-error cover.tex
	$(LATEXMK) -c cover.tex
