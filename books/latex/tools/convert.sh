#!/usr/bin/env bash
# ================================================================
# convert.sh — Markdown (the only source of truth) -> chapters/*.tex
#
# Converts every ../markdown/*.md (relative to the latex folder) into
# chapters/<stem>.tex. Files whose name starts with "_" are drafts and skipped.
# The order of the book is set in book.tex (\input{chapters/<stem>}), not here.
#
#   MARKDOWN_DIR=/some/dir bash tools/convert.sh     # another source folder
#
# Requirements: pandoc 3+
# ================================================================
set -euo pipefail

# [2026-11-11] Shared by every book; lives in books/latex/tools/.
# SHARED is where this script lives. HERE is the book being built, passed in as BOOK_DIR
# by the shared Makefile; run by hand from inside a book folder it defaults to $PWD.
SHARED="$(cd "$(dirname "$0")/.." && pwd)"               # books/latex
HERE="${BOOK_DIR:-$PWD}"                                 # books/<slug>
MD="${MARKDOWN_DIR:-$HERE/markdown}"
if [[ ! -d "$MD" ]]; then
  echo "convert.sh: no Markdown folder at $MD" >&2
  echo "  (layout: books/<slug>/markdown/*.md, build machinery in books/latex/)" >&2
  exit 1
fi
MD="$(cd "$MD" && pwd)"

shopt -s nullglob
files=()
for f in "$MD"/*.md; do
  case "$(basename "$f")" in _*|README.md|TOC.md) continue ;; esac
  files+=("$f")
done
if [[ ${#files[@]} -eq 0 ]]; then echo "convert.sh: no .md files in $MD" >&2; exit 1; fi

mkdir -p "$HERE/chapters" "$HERE/generated"
rm -f "$HERE"/chapters/*.tex

buildset=""
for f in "${files[@]}"; do buildset="$buildset,$(basename "$f" .md)"; done
buildset="${buildset#,}"

# Syntax-highlighting macros from the series theme (tools/code.theme)
printf '```python\nx = 1\n```\n' |
  pandoc -f commonmark_x -t latex -s --syntax-highlighting="$SHARED/tools/code.theme" |
  grep -E '^\\(DefineVerbatimEnvironment\{Highlighting\}|newcommand\{\\[A-Za-z]+Tok\})' \
  > "$HERE/generated/highlighting.tex"

# Markdown dialect: CommonMark + pipe tables, definition lists, attributes ([x]{.idx}),
# GitHub alerts, footnotes, smart quotes. No emoji shortcodes, no $…$ math (so "$5" stays text).
FROM="commonmark_x-emoji-tex_math_dollars+implicit_figures"

for f in "${files[@]}"; do
  stem="$(basename "$f" .md)"
  (cd "$MD" && pandoc -f "$FROM" -t latex --wrap=preserve \
         --syntax-highlighting="$SHARED/tools/code.theme" \
         --lua-filter "$SHARED/tools/filter.lua" \
         -M stem="$stem" -M buildset="$buildset" \
         -o "$HERE/chapters/$stem.tex" "$f")
done
echo "converted ${#files[@]} Markdown files -> chapters/"

# book.tex and the Markdown folder should agree
for f in "${files[@]}"; do
  stem="$(basename "$f" .md)"
  # [2026-11-13] $SHARED/front is searched too. front/ moved to books/latex/ on
  # 2026-11-11, so a book without its own copy - which is every book but one - was told
  # on every build that its preface "is not \\input in book.tex". It is: through
  # front/preface.tex, which this check could no longer see.
  grep -q -s "chapters/$stem}" "$HERE/book.tex" "$HERE"/front/*.tex "$SHARED"/front/*.tex ||
    echo "  note: $stem.md is not \\input in book.tex"
done
# [2026-11-13] Commented-out lines are skipped. books/python/book.tex lists all 51
# chapters with their \input commented out, so a chapter joins the book by being written
# and having one line uncommented. Without this filter that book printed 54 notes about
# chapters nobody claimed to have written yet, on every single build - which is the
# cry-wolf failure: a warning you always see is a warning you stop reading.
# `|| true` on the match: with every \input commented out there is nothing to find, and
# grep exits 1. Under `set -e -o pipefail` that failed the whole convert step, which is
# how a book with no chapters yet could not be built at all.
{ grep -v '^[[:space:]]*%' "$HERE/book.tex" | grep -o 'chapters/[^}]*}' || true; } |
  sed 's#chapters/##; s#}##' | while read -r s; do
  [[ -f "$HERE/chapters/$s.tex" ]] || echo "  note: book.tex inputs chapters/$s but there is no $s.md"
done
