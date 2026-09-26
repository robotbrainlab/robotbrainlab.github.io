# Build the book from the Markdown (the only source of truth).
#   make           convert Markdown -> chapters/*.tex, then typeset book.pdf (MacTeX: latexmk + XeLaTeX)
#   make convert   only regenerate chapters/*.tex
#   make tectonic  OPTIONAL fallback: typeset with Tectonic into book-tectonic.pdf
#   make clean     remove everything generated
.PHONY: all convert pdf tectonic clean

# MacTeX installs here. Exported so latexmk finds xelatex even in terminals opened before the
# install; latexmk itself is called by full path (macOS make ignores PATH set here for lookup).
export PATH := /Library/TeX/texbin:$(PATH)
LATEXMK := $(shell command -v latexmk 2>/dev/null || echo /Library/TeX/texbin/latexmk)

all: convert pdf

convert:
	bash tools/convert.sh

pdf:
	$(LATEXMK) -xelatex -interaction=nonstopmode -halt-on-error book.tex

tectonic: convert
	mkdir -p .tectonic && tectonic --keep-logs --outdir .tectonic book.tex && mv .tectonic/book.pdf book-tectonic.pdf

clean:
	$(LATEXMK) -C book.tex >/dev/null 2>&1 || true
	rm -rf chapters generated .tectonic book.pdf book-tectonic.pdf
	rm -f book.aux book.log book.toc book.out book.fls book.fdb_latexmk book.xdv
