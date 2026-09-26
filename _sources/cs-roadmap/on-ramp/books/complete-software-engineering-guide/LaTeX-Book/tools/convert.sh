#!/usr/bin/env bash
# ================================================================
# convert.sh — Markdown (the only source of truth) -> chapters/*.tex
#
# Each entry:  <stem>|<numbered>|<mode>|<path relative to the library root>
#   numbered=true  -> a chapter of The Book (keeps "Chapter N" / "N.M")
#   mode           -> chapter | split | appendix | intro   (see tools/filter.lua)
# Requirements: pandoc 3+, perl
# ================================================================
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"          # LaTeX-Book/
LIB="$(cd "$HERE/.." && pwd)"                      # library root
BOOK_MD="4-Building-Real-Applications/from-writing-code-to-production-system/markdown"

SOURCES=(
  "how-software-gets-built|false|chapter|LaTeX-Book/content/how-software-gets-built.md"
  "product-discovery|false|chapter|1-Product-Discovery/product-discovery.md"
  "project-planning-guide|false|chapter|2-Project-Planning/project-planning-guide.md"
  "writing-good-code|false|split|3-Writing-the-Code/writing-good-code.md"
  "part4-introduction|false|intro|$BOOK_MD/00-front-matter.md"
)
for f in "$LIB/$BOOK_MD"/[0-4][0-9]-*.md; do
  stem="$(basename "$f" .md)"
  case "$stem" in
    00-*) ;;                                               # book index / front matter
    44-appendices) SOURCES+=("$stem|false|appendix|$BOOK_MD/$stem.md") ;;
    *)             SOURCES+=("$stem|true|chapter|$BOOK_MD/$stem.md") ;;
  esac
done
# Book-only chapters (the process map around the four parts), kept in LaTeX-Book/content/
SOURCES+=("the-same-process-in-a-team|false|chapter|LaTeX-Book/content/the-same-process-in-a-team.md")

mkdir -p "$HERE/chapters" "$HERE/generated"

buildset=""
for s in "${SOURCES[@]}"; do buildset="$buildset,${s%%|*}"; done
buildset="${buildset#,}"

# Syntax-highlighting colour macros (pandoc's "tango" style)
printf '```python\nx = 1\n```\n' |
  pandoc -f gfm -t latex -s --syntax-highlighting=tango |
  grep -E '^\\(DefineVerbatimEnvironment\{Highlighting\}|newcommand\{\\[A-Za-z]+Tok\})' \
  > "$HERE/generated/highlighting.tex"

for s in "${SOURCES[@]}"; do
  IFS='|' read -r stem numbered mode path <<< "$s"
  extra=()
  if [[ "$mode" == intro ]]; then
    extra=(-M chaptertitle="Introduction to Part IV")
  fi
  perl "$HERE/tools/standalone.pl" "$stem" < "$LIB/$path" |
  pandoc -f gfm+smart -t latex --wrap=preserve \
         --syntax-highlighting=tango \
         --lua-filter "$HERE/tools/filter.lua" \
         -M stem="$stem" -M numbered="$numbered" -M mode="$mode" -M buildset="$buildset" \
         ${extra[@]+"${extra[@]}"} \
         -o "$HERE/chapters/$stem.tex"
done
echo "converted ${#SOURCES[@]} files -> chapters/"
