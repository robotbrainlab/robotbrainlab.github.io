#!/usr/bin/env bash
# The suite. It must end ALL GATES PASS.
#
# A gate nobody reads the output of is worse than no gate. When this says FAILED, find
# out which gate and why, every time.
#
# [STATED 2026-11-13] A GATE MUST PROVE IT READ SOMETHING. Every gate prints how many
# files it read, and a gate that read zero files exits 2 and never prints a pass. Before
# chapter 1 exists that is the true state and not a failure, so this script says so
# plainly instead of claiming a pass it has not earned.
set -uo pipefail
cd "$(dirname "$0")/.."
BOOK_SLUG="$(basename "$PWD")"
fail=0
run () { printf '\n=== %s ===\n' "$1"; shift; "$@" || fail=1; }

CHAPTERS=$(ls markdown/[0-9][0-9]-*.md 2>/dev/null | grep -v '/00-' | wc -l | tr -d ' ')

if [ "$CHAPTERS" = "0" ]; then
  printf '\n=== NO CHAPTERS YET ===\n'
  echo "markdown/ holds no numbered chapter, so every chapter gate would read nothing."
  echo "They are NOT run, and nothing below claims to have checked a chapter."
  echo "What is checked: that the book builds, and that its contents tree is sound."
else
  run "VOICE    the book never refers to its own origins" python3 tools/verify-voice.py
  run "BOUNDARY nothing above the Fundamentals stage"     python3 tools/verify-boundary.py
  run "RENDER   markdown renders as written"              python3 tools/verify-render.py
  run "CODE     every sample runs and prints what is printed" python3 tools/verify-code.py
  run "RECORD   every chapter evidenced and fresh"        python3 tools/verify-record.py
  # Per-chapter, but the bare-jargon half of verify-inputs.py is a verdict rather than a
  # hint list, so it belongs in the suite.
  for ch in markdown/[0-9][0-9]-*.md; do
    case "$ch" in markdown/00-*) continue ;; esac
    [ -e "$ch" ] || continue
    out=$(python3 tools/verify-inputs.py "$ch" 2>&1) || {
      printf '\n=== INPUTS   no jargon used before the book gives it ===\n'
      printf '%s\n' "$out" | grep -E 'BARE|bare-terms'
      echo "  in $ch"
      fail=1
    }
  done
  run "GLOSSARY Appendix C matches every Key Terms table"  python3 tools/glossary.py --check
  run "CHEATSHT Appendix A matches every Worth Memorising" python3 tools/cheatsheet.py --check
fi

printf '\n=== BUILD  0 overfull / 0 glyphs / 0 undefined ===\n'
if [ -f book.tex ] && [ -d ../latex ]; then
  make -C ../latex BOOK="$BOOK_SLUG" >/dev/null 2>&1 || { echo "build FAILED"; fail=1; }
  if [ -f book.log ]; then
    for pat in 'Overfull' 'Missing character' 'undefined' 'Undefined'; do
      n=$(grep -c "$pat" book.log || true)
      printf '%-22s %s\n' "$pat" "$n"
      [ "$n" = "0" ] || fail=1
    done
  else
    echo "no book.log after the build - this gate checked NOTHING"; fail=1
  fi
else
  echo "no book.tex here, or no ../latex - this gate checked NOTHING"; fail=1
fi

# After the build: both read what the build wrote.
if [ "$CHAPTERS" != "0" ]; then
  printf '\n=== INDEX  every automatic index entry is shaped like a term ===\n'
  python3 tools/verify-index.py || fail=1
fi

printf '\n=== CONTENTS the contents tree nests correctly ===\n'
python3 tools/verify-contents.py || fail=1

printf '\n'
if [ "$fail" != "0" ]; then
  echo "GATES FAILED"
elif [ "$CHAPTERS" = "0" ]; then
  echo "NO CHAPTERS YET - the build is proven; the chapter gates are waiting for chapter 1"
else
  echo "ALL GATES PASS"
fi
exit "$fail"
