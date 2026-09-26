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

HERE="$(cd "$(dirname "$0")/.." && pwd)"                 # the latex folder
MD="${MARKDOWN_DIR:-$HERE/../markdown}"
if [[ ! -d "$MD" ]]; then
  echo "convert.sh: no Markdown folder at $MD" >&2
  echo "  (layout: books/<slug>/markdown/*.md next to books/<slug>/latex/)" >&2
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
  pandoc -f commonmark_x -t latex -s --syntax-highlighting="$HERE/tools/code.theme" |
  grep -E '^\\(DefineVerbatimEnvironment\{Highlighting\}|newcommand\{\\[A-Za-z]+Tok\})' \
  > "$HERE/generated/highlighting.tex"

# Markdown dialect: CommonMark + pipe tables, definition lists, attributes ([x]{.idx}),
# GitHub alerts, footnotes, smart quotes. No emoji shortcodes, no $…$ math (so "$5" stays text).
FROM="commonmark_x-emoji-tex_math_dollars+implicit_figures"

for f in "${files[@]}"; do
  stem="$(basename "$f" .md)"
  (cd "$MD" && pandoc -f "$FROM" -t latex --wrap=preserve \
         --syntax-highlighting="$HERE/tools/code.theme" \
         --lua-filter "$HERE/tools/filter.lua" \
         -M stem="$stem" -M buildset="$buildset" \
         -o "$HERE/chapters/$stem.tex" "$f")
done
echo "converted ${#files[@]} Markdown files -> chapters/"

# book.tex and the Markdown folder should agree
for f in "${files[@]}"; do
  stem="$(basename "$f" .md)"
  grep -q -s "chapters/$stem}" "$HERE/book.tex" "$HERE"/front/*.tex ||
    echo "  note: $stem.md is not \\input in book.tex"
done
grep -o 'chapters/[^}]*}' "$HERE/book.tex" | sed 's#chapters/##; s#}##' | while read -r s; do
  [[ -f "$HERE/chapters/$s.tex" ]] || echo "  note: book.tex inputs chapters/$s but there is no $s.md"
done
