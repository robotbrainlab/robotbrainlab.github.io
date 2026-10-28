#!/usr/bin/env bash
# The suite. It must end ALL GATES PASS.
#
# A gate nobody reads the output of is worse than no gate: in the French project three
# of nine gates were at some point lying to the suite - one failing on an empty folder,
# one crashing on a renamed column, one printing CLEAN over nothing for a whole build.
# When this says FAILED, find out which gate and why, every time.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
run () { printf '\n=== %s ===\n' "$1"; shift; "$@" || fail=1; }

run "VOICE    the book never refers to its own origins" python3 tools/verify-voice.py
run "BOUNDARY no theory outside BOOK-GUIDE section 6"   python3 tools/verify-boundary.py
run "RENDER   markdown renders as written"              python3 tools/verify-render.py
run "ARITH    the arithmetic it can read holds"         python3 tools/verify-arithmetic.py
run "RECORD   every chapter evidenced and fresh"        python3 tools/verify-record.py
# Per-chapter, but the bare-jargon half of verify-inputs.py is a verdict rather than a hint
# list, so it belongs in the suite. Chapter 6 used "reranker" and "context window", neither
# of which the book had given the reader; every gate passed it, because this one read only
# backticked spans and chapter 6 has no backticks. See LEDGER-DEFECTS.md entry 18.
for ch in markdown/[0-9][0-9]-*.md; do
  [ -e "$ch" ] || continue
  out=$(python3 tools/verify-inputs.py "$ch" 2>&1) || {
    printf '\n=== INPUTS   no field jargon used before the book gives it ===\n'
    printf '%s\n' "$out" | grep -E 'BARE|bare-terms'
    echo "  in $ch"
    fail=1
  }
done
run "OUTLINE  the PDF outline nests correctly"          python3 tools/verify-outline.py
run "GLOSSARY Appendix C matches every Key Terms table"  python3 tools/glossary.py --check
run "CHEATSHT Appendix A matches every Worth Memorising"  python3 tools/cheatsheet.py --check

printf '\n=== BUILD  0 overfull / 0 glyphs / 0 undefined ===\n'
if [ -d latex ]; then
  ( cd latex && make >/dev/null 2>&1 ) || { echo "build FAILED"; fail=1; }
  if [ -f latex/book.log ]; then
    # The header has promised "0 undefined" since this gate was written and never
    # checked for it: the loop below only ever had Overfull and Missing character in
    # it. Found 2026-10-28 by a reviewer reading the gate's own output, which is
    # LEDGER-DEFECTS.md entry 35's lesson arriving from the other direction.
    for pat in 'Overfull' 'Missing character' 'undefined' 'Undefined'; do
      n=$(grep -c "$pat" latex/book.log || true)
      printf '%-22s %s\n' "$pat" "$n"
      [ "$n" = "0" ] || fail=1
    done
  fi
fi

# After the build, because it reads the generated chapters/*.tex.
printf '\n=== INDEX  every automatic index entry is shaped like a term ===\n'
python3 tools/verify-index.py || fail=1

printf '\n'
if [ "$fail" = "0" ]; then echo "ALL GATES PASS"; else echo "GATES FAILED"; fi
exit "$fail"
